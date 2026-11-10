"""An isolated scientific program process, used by local and background calculations."""
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys
import time
from contextlib import nullcontext

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from optics_photonics import __version__
from optics_photonics.catalogue import software
from optics_photonics.operations import calculate


def execute(tool, request, output):
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    inputs = request.get('inputs', {})
    if not isinstance(inputs, dict):
        raise ValueError('inputs must be a JSON object')
    (output/'inputs.json').write_text(json.dumps(request, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    started = time.time()
    source = request.get('source', '')
    native_path = os.environ.get('OPTICS_NATIVE_CONNECTION')
    if native_path:
        from optics_photonics import native
        context = native.session(json.loads(Path(native_path).read_text(encoding='utf-8')), inputs, output)
    else:
        context = nullcontext({})
    with context as session:
        namespace = {'__name__': '__main__', '__file__': str(output/'program.py'), 'INPUTS': inputs, 'OUTPUT_DIR': output, 'RESULT': None, **session}
        if source:
            (output/'program.py').write_text(source, encoding='utf-8')
            exec(compile(source, str(output/'program.py'), 'exec'), namespace)
            result = namespace['RESULT']
            if result is None:
                raise ValueError('Set RESULT to the compact JSON result; write arrays and models under OUTPUT_DIR')
        elif native_path:
            result = native.calculate(tool, request.get('action', ''), inputs, namespace)
        else:
            result = calculate(tool, request.get('action', ''), inputs, output)
    # Distribution names are taken from the active interpreter, including native-program dependencies.
    versions = {}
    package_map = importlib.metadata.packages_distributions()
    for module in set(name.split('.')[0] for name in sys.modules):
        for distribution in package_map.get(module, []):
            try: versions[distribution] = importlib.metadata.version(distribution)
            except importlib.metadata.PackageNotFoundError: pass
    record = {'software': tool, 'operation': 'program' if source else request.get('action'),
              'result': result, 'elapsed_s': time.time()-started,
              'environment': {'python': platform.python_version(), 'platform': platform.platform(), 'versions': versions, 'connector': __version__},
              'files': sorted(str(p.relative_to(output)) for p in output.rglob('*') if p.is_file() and p.name not in {'result.json','stdout.txt','stderr.txt','progress.json'})}
    text = json.dumps(record, ensure_ascii=False, indent=2, allow_nan=False)+'\n'
    (output/'result.json').write_text(text, encoding='utf-8')
    return record


def main():
    tool = sys.argv[1]
    request_path = os.environ.get('OPTICS_REQUEST_FILE') or sys.argv[2]
    raw = json.loads(Path(request_path).read_text(encoding='utf-8'))
    request = raw.get('arguments', raw)
    if not request.get('source'):
        software(tool)
    output = os.environ.get('OPTICS_OUTPUT_DIR') or sys.argv[3]
    execute(tool, request, output)


if __name__ == '__main__':
    main()
