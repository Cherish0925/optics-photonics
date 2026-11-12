# Episodes

`sample_episodes` collects complete episodes for learning. Use it for an environment with explicitly defined initialization and feedback.

The `source` program defines `make_env()` and `make_policy(seed)`. The environment implements Gymnasium-style `reset(seed, options)`, `step(action)` and `close()`; the policy is a function from observation to action, created anew for every episode. Supply `task` and `policy` with `id` and `version`, the number of `episodes`, `workers` and `max_steps`. Each worker keeps its solver context and runs whole episodes; no MCP call is made per step. Episode `i` uses `seed + i`, whatever the worker count.

Each worker writes `samples/trajectory.jsonl` (records `episode`, `transition`, `episode_end`, `episode_error`), `samples/index.jsonl` (one line per completed episode with its byte range) and typed NPY arrays. Read them with `result_files`, `read_result` and `read_array`; in Python, `optics_photonics.episodes.collected(run_id, ...)` yields every episode of the given runs once.

Three outcomes stay distinct: a low reward is a completed episode; an exception from the environment or policy writes `episode_error` and ends that worker, or goes on with the next episode when `on_error="continue"`; an interrupted collection leaves an episode without an end or error record.

Completed episodes are not collected twice. `resume_run` reruns a failed worker without repeating them. `continue_from=[run_id]` in a new call leaves out the episodes those runs completed, with any worker count or more episodes. Both require the same task and policy versions, seed, step limit, options and inputs; change a version when the environment or policy changes.
