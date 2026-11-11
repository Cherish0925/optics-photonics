"""File-backed program execution with completion-driven waiting."""
from contextlib import nullcontext
import json
import os
import platform
import stat
from pathlib import Path
import subprocess
import threading
import time


class Cancelled(RuntimeError):
    pass


def native_binary():
    explicit = os.environ.get('OPTICS_EXECUTOR')
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file(): raise ValueError('OPTICS_EXECUTOR does not name a program')
        return path
    path = Path(__file__).with_name('bin') / ('optics-execd.exe' if os.name == 'nt' else 'optics-execd')
    if not path.is_file():
        machine = platform.machine().lower()
        arch = {'amd64':'x86_64','aarch64':'arm64'}.get(machine,machine)
        path = path.parent/(platform.system().lower()+'-'+arch)/path.name
    if path.is_file():
        if os.name != 'nt' and not os.access(path,os.X_OK): path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path
    return None


def execute(command, *, directory, cwd, env, timeout, cancel, stop):
    binary = native_binary()
    if binary is not None and (cancel is None or hasattr(cancel, 'subscribe')):
        return native(binary, command, directory, cwd, env, timeout, cancel)
    changed = threading.Event()
    options = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
    with (directory/'request.json').open('rb') as incoming, (directory/'stdout.txt').open('wb') as stdout, (directory/'stderr.txt').open('wb') as stderr:
        process = subprocess.Popen(command, stdin=incoming, stdout=stdout, stderr=stderr, cwd=cwd, env=env, **options)
        monitor = threading.Thread(target=lambda: (process.wait(), changed.set()), daemon=True)
        monitor.start()
        deadline = time.monotonic()+timeout if timeout is not None else None
        subscription = cancel.subscribe(changed.set) if hasattr(cancel, 'subscribe') else nullcontext()
        try:
            with subscription:
                while process.poll() is None:
                    changed.clear()
                    if cancel and cancel(): raise Cancelled('Calculation cancelled')
                    remaining = None if deadline is None else deadline-time.monotonic()
                    if remaining is not None and remaining <= 0: raise TimeoutError(f'Calculation exceeded {timeout:g} seconds')
                    if cancel and not hasattr(cancel, 'subscribe'): remaining = min(remaining or .1, .1)
                    if process.poll() is None: changed.wait(remaining)
        except BaseException:
            stop(process)
            raise
        finally:
            monitor.join()
    return process.returncode


def native(binary, command, directory, cwd, env, timeout, cancel):
    lock = threading.Lock()
    with (directory/'executor.txt').open('wb') as log:
        process = subprocess.Popen([str(binary)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=log, text=True, encoding='utf-8', bufsize=1)
        def send(value):
            with lock:
                try:
                    process.stdin.write(json.dumps(value, ensure_ascii=False, allow_nan=False)+'\n')
                    process.stdin.flush()
                except (BrokenPipeError, OSError): pass
        send({'id':1, 'params':{'command':command, 'cwd':str(cwd), 'env':env,
              'stdin':str(directory/'request.json'), 'stdout':str(directory/'stdout.txt'),
              'stderr':str(directory/'stderr.txt'), 'timeout':timeout or 0}})
        def stop(): send({'method':'cancel','params':{'id':1}})
        subscription = cancel.subscribe(stop) if hasattr(cancel, 'subscribe') else nullcontext()
        try:
            with subscription:
                for line in process.stdout:
                    value = json.loads(line)
                    if value.get('event') == 'started':
                        if cancel and cancel(): stop()
                        continue
                    if value.get('cancelled'): raise Cancelled('Calculation cancelled')
                    if value.get('timed_out'): raise TimeoutError(f'Calculation exceeded {timeout:g} seconds')
                    if value.get('error'): raise RuntimeError(value['error'])
                    return value['result']['exit_code']
                raise RuntimeError('Native executor stopped before returning a result: '+str(directory/'executor.txt'))
        finally:
            process.stdin.close()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait()
            process.stdout.close()
