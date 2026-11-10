"""Use installed scientific environments, or prepare a separate Python environment."""
import json
import re
from contextlib import contextmanager
import time
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import venv
from .catalogue import software as catalogue_software, catalogue


def home(path=None):
    return Path(path or os.environ.get('OPTICS_HOME') or Path.home() / '.optics-photonics').expanduser().resolve()


@contextmanager
def editing(path=None):
    directory = home(path)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory/'connections.lock').open('a+b') as stream:
        if stream.tell() == 0:
            stream.write(b'0'); stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            while True:
                try:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    time.sleep(.02)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == 'nt':
                stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def read(path=None):
    file = home(path) / 'connections.json'
    return json.loads(file.read_text(encoding='utf-8')) if file.exists() else {'tools': {}}


def save(value, path=None):
    directory = home(path)
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=directory, delete=False) as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        temporary = stream.name
    os.replace(temporary, directory / 'connections.json')


def register(tool, name, description, *, kind='python', modules=None, distributions=None, sources=None, path=None):
    """Describe a local research tool without changing the published software catalogue."""
    if not isinstance(tool, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_.-]{0,99}', tool):
        raise ValueError('Use a lowercase software ID with letters, digits, dots, hyphens or underscores')
    if any(item['id'] == tool for item in catalogue()):
        raise ValueError('This ID belongs to the published catalogue; bind its environment directly')
    if not isinstance(name, str) or not name.strip() or not isinstance(description, str) or not description.strip():
        raise ValueError('Provide a software name and description')
    if kind not in ('python', 'command'):
        raise ValueError('kind must be python or command')
    values = {'modules': [] if modules is None else modules, 'distributions': [] if distributions is None else distributions, 'sources': [] if sources is None else sources}
    for key, items in values.items():
        if not isinstance(items, list) or any(not isinstance(item, str) or not item.strip() for item in items):
            raise ValueError(key + ' must be an array of nonempty strings')
    definition = {'id': tool, 'name': name, 'summary': description, 'origin': 'local',
                  'connection': {'kind': kind, 'pip': [], 'operations': [], **values}}
    with editing(path):
        configuration = read(path)
        configuration.setdefault('software', {})[tool] = definition
        save(configuration, path)
    return definition


def software(tool, language='en', path=None):
    local = read(path).get('software', {}).get(tool)
    if local is not None:
        return local
    return catalogue_software(tool, language)


def registered(path=None):
    return list(read(path).get('software', {}).values())


def probe(tool, python=None, path=None):
    record = software(tool, path=path)['connection']
    # Resolving a venv's symlink would select the base interpreter and lose its packages.
    interpreter = os.path.abspath(os.path.expanduser(str(python or sys.executable)))
    modules = record.get('modules', [])
    code = """import importlib.util, importlib.metadata, json, sys
modules=json.loads(sys.argv[1]); distributions=json.loads(sys.argv[2])
found={}
for name in modules:
 try: found[name]=importlib.util.find_spec(name) is not None
 except (ImportError,ModuleNotFoundError,ValueError): found[name]=False
versions={}
for name in distributions:
 try: versions[name]=importlib.metadata.version(name)
 except importlib.metadata.PackageNotFoundError: versions[name]=None
print(json.dumps({'python':sys.executable,'python_version':sys.version.split()[0], 'prefix':sys.prefix,'base_prefix':sys.base_prefix,'modules':found,'versions':versions}))
"""
    result = subprocess.run([interpreter, '-c', code, json.dumps(modules), json.dumps(record.get('distributions', []))],
                            capture_output=True, text=True, timeout=20)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'Could not inspect this interpreter')
    status = json.loads(result.stdout)
    status.update(tool=tool, available=all(status['modules'].values()))
    return status


def bind(tool, *, python=None, command=None, path=None, threads=1, concurrency=1, cwd=None):
    item = software(tool, path=path)
    if type(threads) is not int or threads < 1 or type(concurrency) is not int or concurrency < 1:
        raise ValueError('threads and concurrency must be positive integers')
    if command:
        if not isinstance(command, list) or not all(isinstance(v, str) and v for v in command):
            raise ValueError('command must be an executable and argument array')
        executable = shutil.which(command[0]) or (str(Path(command[0]).resolve()) if Path(command[0]).is_file() else None)
        if not executable:
            raise ValueError('Executable was not found: ' + command[0])
        connection = {'kind': 'command', 'command': [executable, *command[1:]]}
    else:
        if item['connection']['kind'] != 'python':
            raise ValueError('Provide the native executable and arguments from this software’s documentation')
        inspected = probe(tool, python, path)
        if not inspected['available']:
            missing = [k for k, v in inspected['modules'].items() if not v]
            raise ValueError('Missing modules in the selected interpreter: ' + ', '.join(missing))
        connection = {'kind': 'python', 'python': inspected['python'], 'versions': inspected['versions']}
    if cwd is not None:
        cwd = str(Path(cwd).expanduser().resolve())
        if not Path(cwd).is_dir():
            raise ValueError('Working directory does not exist')
    connection.update(threads=threads, concurrency=concurrency, cwd=cwd)
    if item.get('origin') == 'local':
        connection['definition'] = item
    with editing(path):
        configuration = read(path)
        configuration['tools'][tool] = connection
        save(configuration, path)
    return {'tool': tool, **connection}


def prepare(tool, *, path=None, python=None):
    record = software(tool, path=path)['connection']
    requirements = record.get('pip', [])
    if not requirements:
        raise ValueError('This software uses its own installer. Follow its installation source, then use bind.')
    target = home(path) / 'environments' / tool
    executable = target / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not executable.exists():
        if python:
            subprocess.run([str(Path(python).expanduser()), '-m', 'venv', str(target)], check=True)
        else:
            venv.EnvBuilder(with_pip=True).create(target)
    subprocess.run([str(executable), '-m', 'pip', 'install', *requirements], check=True, stdout=sys.stderr)
    return bind(tool, python=executable, path=path)


def available(path=None):
    entries = []
    for tool, value in read(path)['tools'].items():
        item = {'id': tool, **value}
        try:
            if value['kind'] == 'python':
                item['environment'] = probe(tool, value['python'], path)
            elif value['kind'] == 'native':
                from . import native
                item['environment'] = native.probe(value)
            else:
                item['environment'] = {'available': bool(shutil.which(value['command'][0]))}
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            item['environment'] = {'available': False, 'error': str(error)}
        entries.append(item)
    return entries
