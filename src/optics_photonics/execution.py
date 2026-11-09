"""Local execution and IOP registration share the same scientific program process."""
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
from . import environments


def definition(tool, path=None):
    configuration = environments.read(path)['tools']
    if tool not in configuration:
        raise ValueError('Configure this software first: optics-photonics bind ' + tool + ' --python /path/to/python')
    binding = configuration[tool]
    if binding['kind'] == 'python':
        command = [binding['python'], '-B', str(Path(__file__).with_name('worker.py')), tool, '{request}', '{output}']
    else:
        command = binding['command']
    env = {name: str(binding['threads']) for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')}
    operation = {'command': command, 'parameters': {
        'action': {'type': 'string', 'default': ''},
        'inputs': {'type': 'object', 'default': {}},
        'source': {'type': 'string', 'default': ''}}}
    config = {'name': tool, 'mode': 'software', 'concurrency': binding['concurrency'],
              'requirements': {'cpu': binding['threads']}, 'env': env, 'operations': {'calculate': operation}}
    if binding.get('cwd'):
        config['cwd'] = binding['cwd']
    return {'id': 'optics-' + tool, 'driver': 'command', 'config': config}


def run(tool, request, *, output=None, path=None, timeout=None):
    record = definition(tool, path)
    directory = Path(output or environments.home(path)/'runs'/str(uuid.uuid4())).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    if any(directory.iterdir()):
        raise ValueError('Use an empty output directory for each calculation')
    request_file = directory/'request.json'
    request_file.write_text(json.dumps(request, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    replacements = {'{request}': str(request_file), '{output}': str(directory), '{result}': str(directory/'result.json')}
    command = [replacements.get(arg, arg) for arg in record['config']['operations']['calculate']['command']]
    env = {**os.environ, **record['config']['env'], 'IOP_REQUEST_FILE':str(request_file), 'IOP_OUTPUT_DIR':str(directory), 'IOP_RESULT_FILE':str(directory/'result.json')}
    with (directory/'stdout.txt').open('wb') as stdout, (directory/'stderr.txt').open('wb') as stderr:
        completed = subprocess.run(command, input=request_file.read_bytes(), stdout=stdout, stderr=stderr,
                                   cwd=record['config'].get('cwd', directory), env=env, timeout=timeout)
    if completed.returncode:
        message = (directory/'stderr.txt').read_text(encoding='utf-8', errors='replace')[-4000:]
        raise RuntimeError(f'{tool} exited with code {completed.returncode}. Output: {directory}\n{message}')
    result = directory/'result.json'
    return {'output': str(directory), 'record': json.loads(result.read_text(encoding='utf-8')) if result.exists() else {'exit_code': 0}}
