"""Read simulated and instrument episodes as one sequence of training episodes.

Two record sources share the same decision structure:

- ``samples/trajectory.jsonl`` written by :func:`optics_photonics.sampling.collect`;
- an IOP episode export (``Episode.export``) from a physical experiment.

Both describe an initial observation followed by transitions whose observation
is the state after the action. They differ in identifiers and provenance:
episode IDs are integers here and strings in IOP, IOP links each transition to
completed instrument operations, IOP rewards may be null for unscored records,
and only this collector writes an ``episode_end`` record. :func:`read` maps both
onto one dictionary layout without changing either file format, and
:func:`collected` assembles the episodes of sampling runs, each one once.
"""
import json
from pathlib import Path
from . import environments, jobs, sampling
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
    return {'source': source, 'run_id': run_id, 'step': header.get('step'), 'attempt': header.get('attempt'),
            'episode_id': str(episode_id), 'definition': header.get('definition'),
            'task': header['task'], 'policy': header.get('policy'), 'seed': header.get('seed'),
            'observation': header.get('observation'), 'info': header.get('info', {}),
            'transitions': [], 'complete': False, 'error': None}


def _transition(record):
    step = {key: record[key] for key in TRANSITION_FIELDS}
    step['operation_ids'] = list(record.get('operation_ids', []))
    return step


def _records(records, run_id, root, arrays):
    """Group collector records into episodes; an episode without its end record is incomplete."""
    current = None
    for record in records:
        if arrays:
            record = restore(record, root)
        kind = record.get('type')
        mine = current is not None and str(record.get('episode_id')) == current['episode_id']
        if kind == 'episode' or kind == 'episode_error' and not mine:
            if current is not None:
                yield current
            # A failure before the first observation carries the episode identity itself.
            current = _episode('simulation', record.get('run_id', run_id), record['episode_id'], record)
        elif not mine:
            raise ValueError('Record before its episode header')
        if kind == 'transition':
            current['transitions'].append(_transition(record))
        elif kind == 'episode_error':
            current['error'] = {'stage': record['stage'], 'message': record['error']}
            yield current
            current = None
        elif kind == 'episode_end':
            current['complete'] = True
            yield current
            current = None
    if current is not None:
        yield current


def _simulated(file, run_id, arrays):
    return _records(_lines(file), run_id, file.parent, arrays)


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

    Each episode is ``{source, run_id, step, attempt, episode_id, definition,
    task, policy, seed, observation, info, transitions, complete, error}``.
    ``source`` is ``simulation`` or ``instrument``; ``episode_id`` is always a
    string. Each transition holds sequence, action, observation, reward
    (``None`` when unscored), terminated, truncated, info and operation_ids
    (empty for simulation). ``complete=True`` omits episodes that did not
    finish: an interrupted collection leaves ``error`` empty, a failure of the
    environment or policy sets ``error`` to its stage and message.
    ``arrays=True`` loads NumPy arrays written by the collector; IOP artifact
    references stay unchanged. ``run_id`` labels simulated episodes collected
    outside a run; step, attempt and definition are empty for instruments.
    """
    for path in paths:
        file = _trajectory(path)
        source = _instrument(file) if _is_instrument(file) else _simulated(file, run_id, arrays)
        for episode in source:
            if episode['complete'] or not complete:
                yield episode


def collected(*runs, path=None, arrays=False, complete=True):
    """Yield each episode of the given sampling runs once, in episode order.

    An episode completed by several attempts or runs (a retried worker, a
    continued run) is taken from the first of them: runs as given, then steps
    and attempts in order. Completed episodes are located through index.jsonl
    and read by byte range. ``complete=False`` then also yields every record
    of an episode that completed nowhere, interrupted or failed.
    """
    home = environments.home(path)
    chosen, folders = {}, []
    for run in runs:
        root = home / 'runs' / jobs.identifier(run)
        if not root.is_dir():
            raise ValueError('Unknown run: ' + run)
        for folder in sorted(root.glob('*/attempt-*/samples'),
                             key=lambda f: (f.parents[1].name, int(f.parent.name.rpartition('-')[2]))):
            folders.append((run, folder))
            for entry in sampling.completed(folder):
                chosen.setdefault((entry.get('definition') or '', entry['episode_id']), (run, folder, entry))
    for key in sorted(chosen):
        run, folder, entry = chosen[key]
        with (folder / 'trajectory.jsonl').open('rb') as stream:
            stream.seek(entry['offset'])
            lines = stream.read(entry['end'] - entry['offset']).decode('utf-8').splitlines()
        episode = next(_records(map(json.loads, lines), run, folder, arrays))
        yield _located(episode, folder)
    if not complete:
        for run, folder in folders:
            for episode in _simulated(folder / 'trajectory.jsonl', run, arrays):
                if not episode['complete'] and (episode['definition'] or '', int(episode['episode_id'])) not in chosen:
                    yield _located(episode, folder)


def _located(episode, folder):
    # Records written before run, step and attempt were stored take them from their folder.
    episode['step'] = episode['step'] or folder.parents[1].name
    episode['attempt'] = episode['attempt'] or int(folder.parent.name.rpartition('-')[2])
    return episode


def scored(episodes):
    """Yield (episode, transition) pairs that carry a reward, for a training set."""
    for episode in episodes:
        for transition in episode['transitions']:
            if transition['reward'] is not None:
                yield episode, transition
