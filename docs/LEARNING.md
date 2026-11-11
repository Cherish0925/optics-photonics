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
| `episode` | Task/policy identities and versions, seed, initial observation and context. |
| `transition` | Episode ID, sequence, action, next observation, scalar reward, terminated/truncated and info. |
| `episode_end` | Completed step count, total return and termination information. |

NumPy arrays are stored as NPY files with dtype and shape references; object arrays are not used. The native job also retains the full program, inputs, software versions, execution output and attempt number. Files remain readable while other workers continue.

```python
from optics_photonics.sampling import records
for record in records('PATH/TO/samples', arrays=True):
    # Numerical references become NumPy arrays, one record at a time.
    consume(record)
```

`terminated` denotes the task's own terminal state; `truncated` denotes an external collection limit. The collector keeps the final observation. A solver error leaves an incomplete episode and the job's error; it does not synthesize a successful terminal transition. `records` ignores an unfinished final line after process interruption.

`resume_run` preserves completed worker steps and reruns unfinished worker steps in a new attempt. It does not restore the internal state of an interrupted solver. Assemble a dataset from one chosen attempt per episode; do not concatenate retries as additional independent episodes. Software that supports state restoration can implement it explicitly in its research program.

For online RL, policy updates and distributed rollout/learner coordination belong to the learning framework. This release provides isolated local execution, reproducible episode assignment and recorded trajectories. It does not claim a distributed training cluster or universal solver support.

## Simulated and instrument episodes

[IOP](https://github.com/Cherish0925/IOP) records episodes from physical experiments with the same structure: an initial observation, then transitions whose observation is the state after the action. The files differ in identifiers and provenance:

| Field | This collector | IOP export |
| --- | --- | --- |
| Episode ID | integer `episode_id` | string `id` in the header, `episode_id` in transitions |
| Run | not recorded | `run_id` |
| Reward | finite number | finite number, or `null` for an unscored record |
| Provenance | program, inputs and versions in the job record | `operation_ids` of completed instrument operations |
| End of episode | `episode_end` record | last transition with `terminated` or `truncated` |
| Arrays | NPY files referenced by `$array` | artifact IDs |

`optics_photonics.episodes.read` accepts sample directories, trajectory files and IOP exports in one call and yields the same dictionary for each episode: `source` (`simulation` or `instrument`), `run_id`, string `episode_id`, `task`, `policy`, `seed`, initial `observation`, `info`, `transitions` and `complete`. Every transition has `sequence`, `action`, `observation`, `reward`, `terminated`, `truncated`, `info` and `operation_ids` (empty for simulation). Neither file format changes.

```python
from optics_photonics import episodes
data = episodes.read('runs/RUN/sampler-0/attempt-1/samples', 'iop/episode-0.jsonl', run_id='RUN')
for episode, transition in episodes.scored(data):
    consume(episode['source'], episode['task'], transition)
```

Interrupted episodes are omitted unless `complete=False`. `scored` drops transitions with `reward=None`. Observations keep their own units and keys; mapping a simulated observation onto a measured one (reference planes, calibration, noise) is part of the research program.
