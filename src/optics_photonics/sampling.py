"""Run complete research episodes in native workers, with ordered training records."""
import json
import math
import os
from pathlib import Path
import time
from . import jobs, execution


def positive_int(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + ' must be a positive integer')
    return value


def versioned(value, name):
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) and value[k].strip() for k in ('id', 'version')):
        raise ValueError(name + ' needs an id and version')
    return value


class Writer:
    """JSON Lines metadata; numerical arrays remain typed, non-pickled NPY files."""
    def __init__(self, directory):
        self.root = Path(directory)
        self.root.mkdir(parents=True, exist_ok=True)
        self.stream = (self.root / 'trajectory.jsonl').open('x', encoding='utf-8')
        self.array_count = 0

    def value(self, value):
        # NumPy is optional, but installed scientific tools may return its types.
        if type(value).__module__.split('.')[0] == 'numpy':
            import numpy as np
            if isinstance(value, np.ndarray):
                if value.dtype.hasobject:
                    raise ValueError('Object arrays cannot be stored as numerical observations')
                self.array_count += 1
                folder = self.root / 'arrays'
                folder.mkdir(exist_ok=True)
                name = f'arrays/{self.array_count:09d}.npy'
                np.save(self.root / name, value, allow_pickle=False)
                return {'$array': name, 'dtype': str(value.dtype), 'shape': list(value.shape)}
            return self.value(value.item())
        if isinstance(value, dict):
            if any(not isinstance(k, str) for k in value):
                raise ValueError('Observation and info object keys must be strings')
            return {k: self.value(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self.value(v) for v in value]
        return value

    def write(self, record):
        self.stream.write(json.dumps(self.value(record), ensure_ascii=False, allow_nan=False) + '\n')
        self.stream.flush()

    def close(self):
        self.stream.close()


def collect(make_env, make_policy, *, output, task, policy, episodes=1, start=0, stride=1,
            seed=0, max_steps=1000, options=None):
    """Collect Gymnasium-style reset/step episodes without an MCP request per step.

    Each worker owns one environment; policy state is fresh for every episode.
    Episode i uses seed+i regardless of how workers partition the episode IDs.
    """
    versioned(task, 'task'); versioned(policy, 'policy')
    positive_int(episodes, 'episodes'); positive_int(stride, 'stride'); positive_int(max_steps, 'max_steps')
    if type(seed) is not int or seed < 0 or type(start) is not int or not 0 <= start < episodes:
        raise ValueError('seed must be nonnegative; start must be an episode index')
    if options is not None and not isinstance(options, dict):
        raise ValueError('options must be an object')
    # Validate metadata before opening a solver or starting an expensive job.
    jobs.encoded({'task': task, 'policy': policy, 'options': options})
    writer = Writer(output)
    env = None
    completed = transitions = 0
    started = time.monotonic()
    try:
        env = make_env()
        for eid in range(start, episodes, stride):
            episode_seed = seed + eid
            actor = make_policy(episode_seed)
            observation, info = env.reset(seed=episode_seed, options=dict(options or {}))
            if not isinstance(info, dict):
                raise ValueError('reset must return observation and an info object')
            writer.write({'type': 'episode', 'schema_version': 1, 'episode_id': eid,
                          'task': task, 'policy': policy, 'seed': episode_seed,
                          'observation': observation, 'info': info, 'time': time.time()})
            total = 0.0
            for sequence in range(max_steps):
                action = actor(observation)
                # Snapshot before step: an implementation may reuse its action buffer.
                saved_action = writer.value(action)
                next_observation, reward, terminated, truncated, info = env.step(action)
                if not isinstance(info, dict):
                    raise ValueError('step info must be an object')
                # Accept numpy.bool_ and numeric scalar rewards, not vector-env arrays.
                if type(terminated).__name__ not in ('bool', 'bool_') or type(truncated).__name__ not in ('bool', 'bool_'):
                    raise ValueError('step must return scalar terminated and truncated flags')
                reward = float(reward)
                if not math.isfinite(reward):
                    raise ValueError('step reward must be finite')
                terminated, truncated = bool(terminated), bool(truncated)
                if sequence + 1 == max_steps and not (terminated or truncated):
                    truncated = True
                    info = {**info, 'sampling_limit': max_steps}
                writer.write({'type': 'transition', 'schema_version': 1, 'episode_id': eid,
                              'sequence': sequence, 'action': saved_action, 'observation': next_observation,
                              'reward': reward, 'terminated': terminated, 'truncated': truncated,
                              'info': info, 'time': time.time()})
                total += reward; transitions += 1
                observation = next_observation
                if terminated or truncated:
                    break
            writer.write({'type': 'episode_end', 'episode_id': eid, 'steps': sequence + 1,
                          'return': total, 'terminated': terminated, 'truncated': truncated})
            # Preserve completed episodes even if a later episode is interrupted.
            os.fsync(writer.stream.fileno())
            completed += 1
        return {'episodes': completed, 'transitions': transitions, 'elapsed_s': time.monotonic() - started,
                'trajectory': 'trajectory.jsonl', 'arrays': writer.array_count}
    finally:
        try:
            if env is not None:
                env.close()
        finally:
            writer.close()


def restore(value, directory):
    """Load numerical references written by this collector; all paths stay in directory."""
    if isinstance(value, dict):
        if set(value) == {'$array', 'dtype', 'shape'}:
            import numpy as np
            root = Path(directory).resolve()
            file = (root / value['$array']).resolve()
            if not file.is_relative_to(root):
                raise ValueError('Array is outside its trajectory directory')
            result = np.load(file, allow_pickle=False)
            if str(result.dtype) != value['dtype'] or list(result.shape) != value['shape']:
                raise ValueError('Array metadata does not match its file')
            return result
        return {k: restore(v, directory) for k, v in value.items()}
    if isinstance(value, list):
        return [restore(v, directory) for v in value]
    return value


def records(directory, *, arrays=False):
    """Iterate records with constant metadata memory; ignore an interrupted final line."""
    root = Path(directory)
    with (root / 'trajectory.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            if not line.endswith('\n'):
                break
            value = json.loads(line)
            yield restore(value, root) if arrays else value


def submit(tool, source, *, task, policy, episodes, workers=1, max_steps=1000, seed=0,
           inputs=None, options=None, request_id=None, timeout=None, path=None):
    """Split whole episodes into bounded native jobs using the existing resource scheduler.

    source defines make_env() and make_policy(seed); all solver APIs remain available.
    """
    versioned(task, 'task'); versioned(policy, 'policy')
    positive_int(episodes, 'episodes'); positive_int(workers, 'workers'); positive_int(max_steps, 'max_steps')
    if type(seed) is not int or seed < 0:
        raise ValueError('seed must be a nonnegative integer')
    if not isinstance(source, str) or not source.strip():
        raise ValueError('source must define make_env() and make_policy(seed)')
    compile(source, '<sampling-program>', 'exec')
    if inputs is not None and not isinstance(inputs, dict) or options is not None and not isinstance(options, dict):
        raise ValueError('inputs and options must be objects')
    if execution.binding(tool, path)['kind'] not in ('python', 'native'):
        raise ValueError('Episode programs need a Python or native SDK binding; use bind with a Python interpreter')
    count = min(workers, episodes)
    wrapper = '''from optics_photonics.sampling import collect
_sampling = INPUTS['sampling']
INPUTS = INPUTS['program']
(OUTPUT_DIR / 'research.py').write_text(_sampling['source'], encoding='utf-8')
exec(compile(_sampling['source'], str(OUTPUT_DIR / 'research.py'), 'exec'), globals())
RESULT = collect(make_env, make_policy, output=OUTPUT_DIR / 'samples',
    **{k:v for k,v in _sampling.items() if k != 'source'})
RESULT['trajectory'] = 'samples/trajectory.jsonl'
'''
    steps = [{'id': f'sampler-{i}', 'tool': tool, 'source': wrapper, 'timeout': timeout,
              'inputs': {'program': inputs or {}, 'sampling': {'source': source, 'task': task, 'policy': policy,
                         'episodes': episodes, 'start': i, 'stride': count, 'seed': seed,
                         'max_steps': max_steps, 'options': options or {}}}}
             for i in range(count)]
    return jobs.submit(steps, name=task['id'], request_id=request_id, path=path)
