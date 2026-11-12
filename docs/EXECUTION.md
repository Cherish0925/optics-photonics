# Research execution

Each calculation uses its selected Python interpreter or native executable. The
software catalogue is a discovery aid; `register_software` adds a library or
program outside it. The same job, resource and result APIs apply to both.

| Component | Responsibility |
| --- | --- |
| TypeScript client | Host integration, typed submissions, reconnecting to saved runs |
| Rust executor | Child process ownership, completion, cancellation, deadlines, file-backed I/O |
| Python | Scientific SDKs, native programs, dependencies between jobs and MCP |
| SQLite | Cross-process resource admission and persistent research records |

The release carries executors for Windows, macOS and Linux, on x86_64 and ARM64.
Windows executors include the C runtime. Linux executors are built on Ubuntu 22.04. The package selects its native binary
on the computing host. A source installation can use the Python process runner
or set `OPTICS_EXECUTOR` to a locally built binary. Python 3.10+ runs the connector;
scientific programs keep their independently selected environments.

## Share actual computing resources

```json
{"cpu":16,"pools":{"gpu-0":1,"solver-license":2}}
```

Pass this object to `compute_resources`. Bind a solver with `threads`,
`concurrency`, `requirements` and `env`; a workflow step may add requirements.
The effective requirement is the greater of the binding and step values for
each named resource. CPU and named requirements are admitted together across
runs, so a calculation never reserves half its resources while waiting for the
rest. Reducing capacity affects new admissions; active programs retain theirs.

Resource names have no vendor-specific meaning. Select actual GPU IDs, MPI ranks,
cluster queues and license servers in the native launch environment/program.
The shared quantity represents the capacity administered by this computing host.

## Keep scientific loops close to the solver

Submit a full program for a coupled optimization, sweep or episode. Keep its
live model/session in that program. Separate independent work into steps, declare
`after` and `bindings`, and let the worker coordinate them. Notifications wake
scheduling on completion, cancellation and resource changes; fixed 100 ms waits
are removed. Local notifications carry no program data; saved state stays in SQL.

MCP `run_status` defaults to compact state and accepts `wait` up to 25 seconds.
Read result files only when needed; `include_results=true` returns inline step
values. Python's existing status function retains its detailed default.
Environment listing is paginated and does not start every interpreter unless
`refresh=true`. Only referenced predecessor results are loaded for a step. A
binding with `file` passes the location of a predecessor's file instead of a
value, so large arrays are not copied through JSON.

One MCP connection answers tool calls as each completes; replies carry their
request ID and may arrive in a different order. Up to 16 calls execute at once.
`run_status` waits use their own threads, so any number of them leaves a
search, a file read or `cancel_run` sent afterwards unaffected. A connection
accepts 256 unanswered requests. MCP `notifications/cancelled` ends that
request's wait without a reply; `cancel_run` stops the calculation itself. When
the host closes the connection, pending waits return their current state and
accepted calculations continue.

## Read large results

`result_files` lists a run page by page; `prefix` such as `sweep/attempt-1/`
walks only that step or folder. Folders are read one at a time and sizes only
for the returned page. NPY and NPZ entries carry dtype and shape.
`read_array` returns part of an NPY array or NPZ member without NumPy and
without loading the file: per axis, `index` takes an integer to select one
position, `[start, stop, step]` for a range, or `null` for the whole axis;
`member` names an NPZ array. A selection
larger than `max_elements` (default 10000, at most 100000) is thinned: each axis
keeps at most c elements by a uniform step, with the largest c that fits, so
short axes such as ports or field components stay whole. The response states
the steps used. Complex values
return `real` and `imag`. An array still being written reports how many bytes
are present; an NPZ file is readable once the solver has closed it. Boolean,
integer, real and complex arrays are supported. Use `read_result` for other
formats.

```json
{"run_id": "RUN", "file": "solve/attempt-1/field.npz", "member": "Ex", "index": [[0, null, 4], 128]}
```

## Keep the meaning of arrays between programs

A program saves arrays with what they are: quantity, unit, axes, and the
conventions another program must know (time dependence of complex amplitudes,
sign of a path difference, normalization, port order, reference planes,
material source).

```python
from optics_photonics import data
data.save(OUTPUT_DIR / 'pupil', {
    'opd': data.quantity(opd, 'optical path difference', unit='nm', axes=['y', 'x'], wavefront='positive lags'),
    'x': data.quantity(x, 'pupil coordinate', unit='m'),
    'y': data.quantity(y, 'pupil coordinate', unit='m')})
```

`pupil.npz` holds the numbers and `pupil.json` the descriptions. A later step
that receives the file through a binding reads both with `data.load` and
converts explicitly: `.to('m')`, `.axis('x')`, `.phasor('exp(+i omega t)')`,
`.wavefront('positive leads')`. A conversion is recorded in the description; one
the description does not support is refused. `result_files` shows each array's
quantity, unit and axis names, and `read_array` returns the coordinates and
units of the values it returns.

[`examples/exchange`](../examples/exchange/) runs this between two libraries.
HCIPy writes an aberrated pupil (tilt 100 nm RMS, defocus 20 nm, coma 15 nm, at
550 nm on a 1 m aperture); POPPY computes the image from the file. HCIPy's
path difference is positive where the wavefront lags and is stored in
nanometres; POPPY takes metres, positive where it leads. Run on Linux with
HCIPy 0.7.1 and POPPY 1.2.0:

| | image shift along x | along y | Strehl ratio |
| --- | --- | --- | --- |
| HCIPy, its own propagation | 3.913e-7 rad | 7.70e-8 rad | 0.917 (sampled maximum) |
| POPPY, from the file with both conversions | 3.922e-7 rad | 7.48e-8 rad | 0.9225 |
| POPPY, unit converted, sign not converted | -3.922e-7 rad | -7.48e-8 rad | 0.9225 |
| Analytic | 4σ/D = 4.0e-7 rad | | exp(-(2πσ/λ)²) = 0.9217 |

## TypeScript

Install the `.tgz` from the release with npm, then:

```ts
import { OpticsLab } from '@optics-photonics/lab';
const lab = await OpticsLab.connect({command: '/path/to/python'});
const run = await lab.submit(steps, {request_id: 'study-001'});
const state = await lab.wait(run.run_id);
lab.close();
```

Closing a client leaves accepted work running. Reconnect and read the same run ID.
To stop a calculation, call `cancel`; closing a client is not a cancellation.
Requests on one client run concurrently. `wait`, `status` and `call` accept an
`AbortSignal`: aborting stops that request's wait on the server, not the run.
`lab.download(run_id, file, destination)` copies a result file to the client's
computer through the connection, also when the server runs on another machine;
`lab.array(run_id, file, {index})` reads part of an array.
The native MCP interface remains available to other languages and hosts.
