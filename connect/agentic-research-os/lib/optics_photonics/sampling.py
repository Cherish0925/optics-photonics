"""Run complete research episodes in native workers, with ordered training records."""
import hashlib
import json
import math
import os
from pathlib import Path
import time
from . import environments, execution, jobs


def positive_int(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + ' must be a positive integer')
    return value


def versioned(value, name):
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) and value[k].strip() for k in ('id', 'version')):
        raise ValueError(name + ' needs an id and version')
    return value


def definition(task, policy, seed, max_steps, options=None, inputs=None):
    """Identify what makes two samplings produce the same episode for an episode ID.

    Environment or policy changes are declared through the task and policy versions.
    """
    content = jobs.encoded({'task': {k: task[k] for k in ('id', 'version')}, 'policy': {k: policy[k] for k in ('id', 'version')},
                            'seed': seed, 'max_steps': max_steps, 'options': options or {}, 'inputs': inputs or {}})
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]


class Writer:
    """JSON Lines metadata; numerical arrays remain typed, non-pickled NPY files.

    index.jsonl gains one line per completed episode with its byte range in
    trajectory.jsonl, so completed episodes are found and read without a scan.
    """
    def __init__(self, directory):
        self.root = Path(directory)
        self.root.mkdir(parents=True, exist_ok=True)
        self.stream = (self.root / 'trajectory.jsonl').open('xb')
        self.index = (self.root / 'index.jsonl').open('xb')
        self.array_count = self.offset = 0

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
        data = (json.dumps(self.value(record), ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')
        self.stream.write(data)
        self.stream.flush()
        self.offset += len(data)

    def completed(self, entry):
        """Keep a finished episode and its index line even if a later episode is interrupted."""
        os.fsync(self.stream.fileno())
        self.index.write((json.dumps(entry, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8'))
        self.index.flush()
        os.fsync(self.index.fileno())

    def close(self):
        self.stream.close()
        self.index.close()


def collect(make_env, make_policy, *, output, task, policy, episodes=1, start=0, stride=1,
            seed=0, max_steps=1000, options=None, skip=(), origin=None, identity=None, on_error='stop'):
    """Collect Gymnasium-style reset/step episodes without an MCP request per step.

    Each worker owns one environment; policy state is fresh for every episode.
    Episode i uses seed+i regardless of how workers partition the episode IDs.
    Episode IDs in skip are left out; they were completed by an earlier attempt
    or run. An exception from the environment or policy is recorded as an
    episode_error record; on_error='continue' then proceeds with the next
    episode instead of ending the collection.
    """
    versioned(task, 'task'); versioned(policy, 'policy')
    positive_int(episodes, 'episodes'); positive_int(stride, 'stride'); positive_int(max_steps, 'max_steps')
    if type(seed) is not int or seed < 0 or type(start) is not int or not 0 <= start < episodes:
        raise ValueError('seed must be nonnegative; start must be an episode index')
    if options is not None and not isinstance(options, dict):
        raise ValueError('options must be an object')
    if on_error not in ('stop', 'continue'):
        raise ValueError("on_error is 'stop' or 'continue'")
    # Validate metadata before opening a solver or starting an expensive job.
    jobs.encoded({'task': task, 'policy': policy, 'options': options, 'origin': origin})
    identity = identity or definition(task, policy, seed, max_steps, options)
    skip = frozenset(skip)
    writer = Writer(output)
    env = None
    completed = transitions = skipped = failed = 0
    started = time.monotonic()
    try:
        env = make_env()
        for eid in range(start, episodes, stride):
            if eid in skip:
                skipped += 1
                continue
            episode_seed = seed + eid
            begin, stage, sequence, opened = writer.offset, 'policy', 0, False
            try:
                actor = make_policy(episode_seed)
                stage = 'reset'
                observation, info = env.reset(seed=episode_seed, options=dict(options or {}))
                if not isinstance(info, dict):
                    raise ValueError('reset must return observation and an info object')
                writer.write({'type': 'episode', 'schema_version': 1, 'episode_id': eid,
                              'task': task, 'policy': policy, 'seed': episode_seed, 'definition': identity,
                              **(origin or {}), 'observation': observation, 'info': info, 'time': time.time()})
                opened = True
                total = 0.0
                for sequence in range(max_steps):
                    stage = 'policy'
                    action = actor(observation)
                    # Snapshot before step: an implementation may reuse its action buffer.
                    saved_action = writer.value(action)
                    stage = 'step'
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
            except Exception as error:
                # A solver or program failure, as distinct from an interrupted collection (no record)
                # and from a low reward (a completed episode).
                record = {'type': 'episode_error', 'episode_id': eid, 'stage': stage, 'sequence': sequence,
                          'error': type(error).__name__ + ': ' + str(error)}
                if not opened:
                    record.update(task=task, policy=policy, seed=episode_seed, definition=identity, **(origin or {}))
                writer.write(record)
                os.fsync(writer.stream.fileno())
                failed += 1
                if on_error == 'stop':
                    raise
                continue
            writer.write({'type': 'episode_end', 'episode_id': eid, 'steps': sequence + 1,
                          'return': total, 'terminated': terminated, 'truncated': truncated})
            writer.completed({'episode_id': eid, 'seed': episode_seed, 'definition': identity, 'steps': sequence + 1,
                              'return': total, 'terminated': terminated, 'truncated': truncated,
                              'offset': begin, 'end': writer.offset})
            completed += 1
        return {'episodes': completed, 'transitions': transitions, 'skipped': skipped, 'failed': failed,
                'elapsed_s': time.monotonic() - started, 'trajectory': 'trajectory.jsonl', 'arrays': writer.array_count}
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


def completed(samples):
    """Index entries of the episodes completed in one samples directory.

    Each entry has episode_id, seed, definition, steps, return, terminated,
    truncated and the byte range offset..end of the episode in trajectory.jsonl.
    Directories written before index.jsonl existed are scanned once instead;
    their entries have no definition.
    """
    root = Path(samples)
    entries = []
    if (root / 'index.jsonl').is_file():
        with (root / 'index.jsonl').open('rb') as stream:
            for line in stream:
                if line.endswith(b'\n'):  # an interrupted final line belongs to no completed episode
                    entries.append(json.loads(line))
        return entries
    if not (root / 'trajectory.jsonl').is_file():
        return entries
    offset, begin, header = 0, None, None
    with (root / 'trajectory.jsonl').open('rb') as stream:
        for line in stream:
            if not line.endswith(b'\n'):
                break
            record = json.loads(line)
            if record.get('type') == 'episode':
                begin, header = offset, record
            offset += len(line)
            if record.get('type') == 'episode_end' and header is not None and header['episode_id'] == record['episode_id']:
                entries.append({'episode_id': record['episode_id'], 'seed': header.get('seed'), 'definition': header.get('definition'),
                                'steps': record['steps'], 'return': record['return'], 'terminated': record['terminated'],
                                'truncated': record['truncated'], 'offset': begin, 'end': offset})
                header = None
    return entries


def finished(output, identity, runs=()):
    """Episode IDs already completed under this definition, for a worker writing to output.

    Looks at earlier attempts of the same step and at every step of the named
    earlier runs, all under the same runs directory.
    """
    output = Path(output)
    folders = [folder for folder in output.parent.glob('attempt-*/samples') if folder.parent != output]
    for run in runs:
        folders += (output.parents[2] / jobs.identifier(run)).glob('*/attempt-*/samples')
    return {entry['episode_id'] for folder in folders for entry in completed(folder) if entry.get('definition') == identity}


WRAPPER = '''from optics_photonics.sampling import collect, finished
_sampling = INPUTS['sampling']
INPUTS = INPUTS['program']
(OUTPUT_DIR / 'research.py').write_text(_sampling['source'], encoding='utf-8')
exec(compile(_sampling['source'], str(OUTPUT_DIR / 'research.py'), 'exec'), globals())
_previous = _sampling.pop('continue_from', [])
RESULT = collect(make_env, make_policy, output=OUTPUT_DIR / 'samples',
    skip=finished(OUTPUT_DIR, _sampling['identity'], _previous),
    origin={'run_id': OUTPUT_DIR.parents[1].name, 'step': OUTPUT_DIR.parent.name, 'attempt': int(OUTPUT_DIR.name.rpartition('-')[2])},
    **{k:v for k,v in _sampling.items() if k != 'source'})
RESULT['trajectory'] = 'samples/trajectory.jsonl'
'''


def submit(tool, source, *, task, policy, episodes, workers=1, max_steps=1000, seed=0,
           inputs=None, options=None, continue_from=None, on_error='stop', request_id=None, timeout=None, path=None):
    """Split whole episodes into bounded native jobs using the existing resource scheduler.

    source defines make_env() and make_policy(seed); all solver APIs remain available.
    continue_from names earlier sampling runs: episodes they completed under the
    same task and policy versions, seed, step limit, options and inputs are not
    collected again, whatever the worker count. A retried worker step likewise
    leaves out the episodes its earlier attempts completed.
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
    if on_error not in ('stop', 'continue'):
        raise ValueError("on_error is 'stop' or 'continue'")
    previous = list(continue_from or [])
    for run in previous:
        if not (environments.home(path) / 'runs' / jobs.identifier(run)).is_dir():
            raise ValueError('Unknown run: ' + run)
    if execution.binding(tool, path)['kind'] not in ('python', 'native'):
        raise ValueError('Episode programs need a Python or native SDK binding; use bind with a Python interpreter')
    count = min(workers, episodes)
    sampling = {'source': source, 'task': task, 'policy': policy, 'episodes': episodes, 'stride': count, 'seed': seed,
                'max_steps': max_steps, 'options': options or {}, 'on_error': on_error,
                'identity': definition(task, policy, seed, max_steps, options, inputs)}
    if previous:
        sampling['continue_from'] = previous
    steps = [{'id': f'sampler-{i}', 'tool': tool, 'source': WRAPPER, 'timeout': timeout,
              'inputs': {'program': inputs or {}, 'sampling': {**sampling, 'start': i}}}
             for i in range(count)]
    return jobs.submit(steps, name=task['id'], request_id=request_id, path=path)
