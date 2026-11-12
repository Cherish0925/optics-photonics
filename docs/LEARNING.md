# Research environments and episode sampling

A research environment defines an initial state, available actions, resulting observations, task feedback and an end condition. The solver supplies the scientific model. This package runs independent environment instances and retains their data; a learning framework supplies policy optimization.

Use a complete program for one episode or many successive episodes. MCP submits that program once; the numerical loop runs next to the solver.

## Run the coating example

[`examples/learning/thin_film.py`](../examples/learning/thin_film.py) defines a Gymnasium environment for a three-layer dielectric coating. It evaluates reflectance at 21 wavelengths from 450 to 700 nm using TMM. Actions specify layer thicknesses; observations contain thicknesses and the spectrum. Reward is negative mean reflectance. This example's constant, lossless refractive indices are an explicit model assumption.

Install the software into a selected Python environment, then bind that same interpreter:

```sh
python -m pip install "optics-photonics[rl] @ git+https://github.com/Cherish0925/Optics-Photonics-AI-Lab.git" numpy tmm
```

```python
from pathlib import Path
import sys
from optics_photonics import environments, sampling

environments.bind('tmm', python=sys.executable, threads=1, concurrency=4)
submission = sampling.submit(
    'tmm', Path('examples/learning/thin_film.py').read_text(),
    task={'id': 'broadband-coating', 'version': '1'},
    policy={'id': 'random-search', 'version': '1'},
    episodes=100, workers=4, max_steps=12, seed=41,
    request_id='coating-study-001')
print(submission)  # Save run_id and request_id.
```

Read progress with `optics-photonics status RUN_ID`, files with `optics-photonics files RUN_ID`, or use the corresponding MCP tools. The same operation is available as `optics-photonics sample TOOL PROGRAM --task JSON --policy JSON --episodes N --workers W`.

## Program interface

`make_env()` creates a worker-owned environment. It implements:

- `reset(seed=..., options=...) -> (observation, info)`.
- `step(action) -> (observation, reward, terminated, truncated, info)`.
- `close()` releases that worker's environment resources.

`make_policy(seed)` returns a callable `policy(observation) -> action`. It is called separately for every episode, so recurrent policy state can begin afresh. Use that seed for all stochastic policy decisions. A trained model can be loaded once at module scope and shared across successive episodes in the same process.

The interface follows [Gymnasium](https://gymnasium.farama.org/api/env/). A Gymnasium subclass can also be used directly by its compatible learners. The collector itself has no mandatory Gymnasium dependency. Native session adapters expose their existing session objects to the submitted program; the program defines the solver-specific model initialization and step behavior.

Each episode has a global integer ID. Its seed is `seed + episode_id`, independent of worker count. A worker receives disjoint episode IDs and uses its configured scientific interpreter. CPU and per-software concurrency limits continue to apply across all submitted calculations. This is local process parallelism; an MPI launcher, cluster scheduler or remote solver keeps its own resource configuration.

## Data

Each worker writes `samples/trajectory.jsonl`:

| Record | Meaning |
| --- | --- |
| `episode` | Task/policy identities and versions, seed, definition, run, step and attempt, initial observation and context. |
| `transition` | Episode ID, sequence, action, next observation, scalar reward, terminated/truncated and info. |
| `episode_end` | Completed step count, total return and termination information. |
| `episode_error` | The environment or policy raised an exception: stage (`policy`, `reset` or `step`), sequence and message. |

`samples/index.jsonl` has one line per completed episode: episode ID, seed, definition, step count, return, and the byte range of that episode in `trajectory.jsonl`. Completed episodes are found and read through it without scanning the trajectory.

NumPy arrays are stored as NPY files with dtype and shape references; object arrays are not used. The native job also retains the full program, inputs, software versions, execution output and attempt number. Files remain readable while other workers continue.

```python
from optics_photonics.sampling import records
for record in records('PATH/TO/samples', arrays=True):
    # Numerical references become NumPy arrays, one record at a time.
    consume(record)
```

`terminated` denotes the task's own terminal state; `truncated` denotes an external collection limit. The collector keeps the final observation. `records` ignores an unfinished final line after process interruption.

Three outcomes stay distinct. A low or negative reward is a completed episode. A solver or program exception writes `episode_error` and, by default, ends that worker with the job's error; `on_error="continue"` goes on with the next episode. An interrupted collection (cancellation, time limit, a stopped machine) leaves the episode without an end or error record. None of them synthesizes a terminal transition.

## Continue a collection

The definition of a sampling is its task and policy IDs and versions, seed, step limit, reset options and program inputs. Under one definition, episode `i` is the same episode wherever it is collected, so completed episodes are never collected twice:

- `resume_run` reruns a failed or interrupted worker step in a new attempt; the episodes its earlier attempts completed are left out.
- `continue_from=[RUN_ID, ...]` in a new submission leaves out the episodes those runs completed. The worker count and the number of episodes may differ, so a collection can be finished with other resources or extended.

Change the task or policy version when the environment or policy changes; earlier episodes then no longer count. The internal state of an interrupted solver is not restored: an unfinished episode starts again from its seed.

```python
from optics_photonics import episodes, sampling
more = sampling.submit('tmm', program, task=task, policy=policy, episodes=200, workers=8,
                       max_steps=12, seed=41, continue_from=['RUN_ID'])
for episode in episodes.collected('RUN_ID', more['run_id']):
    consume(episode['episode_id'], episode['run_id'], episode['step'], episode['attempt'], episode['transitions'])
```

`episodes.collected` yields each episode of the given runs once, in episode order, with the run, step and attempt it is taken from. `complete=False` adds the episodes that completed nowhere, with `error` set for a recorded failure and empty for an interruption.

For online RL, policy updates and distributed rollout/learner coordination belong to the learning framework. This release provides isolated local execution, reproducible episode assignment and recorded trajectories. It does not claim a distributed training cluster or universal solver support.

## Simulated and instrument episodes

[IOP](https://github.com/Cherish0925/IOP) records episodes from physical experiments with the same structure: an initial observation, then transitions whose observation is the state after the action. The files differ in identifiers and provenance:

| Field | This collector | IOP export |
| --- | --- | --- |
| Episode ID | integer `episode_id` | string `id` in the header, `episode_id` in transitions |
| Run | `run_id`, `step`, `attempt` when collected in a run | `run_id` |
| Reward | finite number | finite number, or `null` for an unscored record |
| Provenance | program, inputs and versions in the job record | `operation_ids` of completed instrument operations |
| End of episode | `episode_end` record | last transition with `terminated` or `truncated` |
| Arrays | NPY files referenced by `$array` | artifact IDs |

`optics_photonics.episodes.read` accepts sample directories, trajectory files and IOP exports in one call and yields the same dictionary for each episode: `source` (`simulation` or `instrument`), `run_id`, `step`, `attempt`, string `episode_id`, `definition`, `task`, `policy`, `seed`, initial `observation`, `info`, `transitions`, `complete` and `error`. Step, attempt and definition are empty for instrument episodes. Every transition has `sequence`, `action`, `observation`, `reward`, `terminated`, `truncated`, `info` and `operation_ids` (empty for simulation). Neither file format changes.

```python
from optics_photonics import episodes
data = episodes.read('runs/RUN/sampler-0/attempt-1/samples', 'iop/episode-0.jsonl', run_id='RUN')
for episode, transition in episodes.scored(data):
    consume(episode['source'], episode['task'], transition)
```

Unfinished episodes are omitted unless `complete=False`. `scored` drops transitions with `reward=None`. Observations keep their own units and keys; mapping a simulated observation onto a measured one (reference planes, calibration, noise) is part of the research program.
