"""Run native scientific programs in their selected environments."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import uuid
from . import environments


class Cancelled(RuntimeError):
    pass


def binding(tool, path=None):
    configuration = environments.read(path)['tools']
    if tool not in configuration:
        raise ValueError('Configure this software first: optics-photonics prepare ' + tool + ' or bind ' + tool)
    return configuration[tool]


def stop_process(process):
    if process.poll() is not None:
        return
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        try: os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError: return
        try: process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try: os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError: pass
    process.wait()


def run(tool, request, *, output=None, path=None, timeout=None, cancel=None, configuration=None):
    selected = configuration or binding(tool, path)
    directory = Path(output or environments.home(path)/'runs'/str(uuid.uuid4())).expanduser().resolve()
    directory.mkdir(parents=True, exist_ok=True)
    if any(directory.iterdir()):
        raise ValueError('Use an empty output directory for each calculation')
    request_file = directory/'request.json'
    request_file.write_text(json.dumps(request, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    if selected['kind'] in ('python', 'native'):
        command = [selected['python'], '-B', str(Path(__file__).with_name('worker.py')), tool, str(request_file), str(directory)]
        if selected['kind'] == 'native':
            (directory/'native-connection.json').write_text(json.dumps(selected, ensure_ascii=False), encoding='utf-8')
    else:
        replacements = {'{request}': str(request_file), '{output}': str(directory), '{result}': str(directory/'result.json')}
        command = [replacements.get(arg, arg) for arg in selected['command']]
    env = {**os.environ, **{name: str(selected['threads']) for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')},
           'OPTICS_REQUEST_FILE': str(request_file), 'OPTICS_OUTPUT_DIR': str(directory), 'OPTICS_RESULT_FILE': str(directory/'result.json')}
    env.pop('OPTICS_NATIVE_CONNECTION', None)
    if selected['kind'] == 'native': env['OPTICS_NATIVE_CONNECTION'] = str(directory/'native-connection.json')
    options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
    started = time.monotonic()
    with request_file.open('rb') as incoming, (directory/'stdout.txt').open('wb') as stdout, (directory/'stderr.txt').open('wb') as stderr:
        process = subprocess.Popen(command, stdin=incoming, stdout=stdout, stderr=stderr,
                                   cwd=selected.get('cwd') or directory, env=env, **options)
        try:
            while process.poll() is None:
                if cancel and cancel():
                    raise Cancelled('Calculation cancelled')
                if timeout is not None and time.monotonic()-started >= timeout:
                    raise TimeoutError(f'Calculation exceeded {timeout:g} seconds')
                time.sleep(.05)
        except BaseException:
            stop_process(process)
            raise
    if process.returncode:
        message = (directory/'stderr.txt').read_text(encoding='utf-8', errors='replace')[-4000:]
        raise RuntimeError(f'{tool} exited with code {process.returncode}. Output: {directory}\n{message}')
    result = directory/'result.json'
    return {'output': str(directory), 'record': json.loads(result.read_text(encoding='utf-8')) if result.exists() else {'exit_code': 0}}
