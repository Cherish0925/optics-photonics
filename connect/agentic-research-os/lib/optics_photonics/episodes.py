"""Read simulated and instrument episodes as one sequence of training episodes.

Two record sources share the same decision structure:

- ``samples/trajectory.jsonl`` written by :func:`optics_photonics.sampling.collect`;
- an IOP episode export (``Episode.export``) from a physical experiment.

Both describe an initial observation followed by transitions whose observation
is the state after the action. They differ in identifiers and provenance:
episode IDs are integers here and strings in IOP, IOP links each transition to
completed instrument operations, IOP rewards may be null for unscored records,
and only this collector writes an ``episode_end`` record. :func:`read` maps both
onto one dictionary layout without changing either file format.
"""
import json
from pathlib import Path
from .sampling import restore

TRANSITION_FIELDS = ('sequence', 'action', 'observation', 'reward', 'terminated', 'truncated', 'info')


def _lines(file):
    with Path(file).open(encoding='utf-8') as stream:
        for line in stream:
            # A writer interrupted mid-line leaves no newline; earlier records remain valid.
            if not line.endswith('\n'):
                return
            if line.strip():
                yield json.loads(line)


def _trajectory(path):
    path = Path(path)
    if path.is_dir():
        for candidate in (path / 'trajectory.jsonl', path / 'samples' / 'trajectory.jsonl'):
            if candidate.is_file():
                return candidate
        raise ValueError('No trajectory.jsonl in ' + str(path))
    return path


def _episode(source, run_id, episode_id, header):
    return {'source': source, 'run_id': run_id, 'episode_id': str(episode_id),
            'task': header['task'], 'policy': header.get('policy'), 'seed': header.get('seed'),
            'observation': header['observation'], 'info': header.get('info', {}),
            'transitions': [], 'complete': False}


def _transition(record):
    step = {key: record[key] for key in TRANSITION_FIELDS}
    step['operation_ids'] = list(record.get('operation_ids', []))
    return step


def _simulated(file, run_id, arrays):
    root = file.parent
    current = None
    for record in _lines(file):
        if arrays:
            record = restore(record, root)
        kind = record.get('type')
        if kind == 'episode':
            if current is not None:
                yield current
            current = _episode('simulation', run_id, record['episode_id'], record)
        elif current is None or str(record.get('episode_id')) != current['episode_id']:
            raise ValueError('Record before its episode header in ' + str(file))
        elif kind == 'transition':
            current['transitions'].append(_transition(record))
        elif kind == 'episode_end':
            current['complete'] = True
            yield current
            current = None
    if current is not None:
        yield current


def _instrument(file):
    lines = _lines(file)
    header = next(lines, None)
    if header is None:
        return
    episode = _episode('instrument', header['run_id'], header['id'], header)
    for record in lines:
        if record.get('type') != 'transition' or record.get('episode_id') != header['id']:
            raise ValueError('An IOP export contains one episode followed by its transitions: ' + str(file))
        episode['transitions'].append(_transition(record))
    last = episode['transitions'][-1] if episode['transitions'] else None
    episode['complete'] = bool(last and (last['terminated'] or last['truncated']))
    yield episode


def _is_instrument(file):
    first = next(_lines(file), None)
    # IOP headers carry the experiment run and the episode under ``id``.
    return bool(first and first.get('type') == 'episode' and 'id' in first and 'run_id' in first
                and 'episode_id' not in first)


def read(*paths, run_id=None, arrays=False, complete=True):
    """Yield episodes from trajectory files, sample directories or IOP exports.

    Each episode is ``{source, run_id, episode_id, task, policy, seed,
    observation, info, transitions, complete}``. ``source`` is ``simulation`` or
    ``instrument``; ``episode_id`` is always a string. Each transition holds
    sequence, action, observation, reward (``None`` when unscored), terminated,
    truncated, info and operation_ids (empty for simulation). ``complete=True``
    omits episodes cut off by an interruption. ``arrays=True`` loads NumPy
    arrays written by the collector; IOP artifact references stay unchanged.
    ``run_id`` labels simulated episodes, which do not record their run.
    """
    for path in paths:
        file = _trajectory(path)
        source = _instrument(file) if _is_instrument(file) else _simulated(file, run_id, arrays)
        for episode in source:
            if episode['complete'] or not complete:
                yield episode


def scored(episodes):
    """Yield (episode, transition) pairs that carry a reward, for a training set."""
    for episode in episodes:
        for transition in episode['transitions']:
            if transition['reward'] is not None:
                yield episode, transition
