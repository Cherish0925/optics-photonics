"""Local solver discovery and process-owned commercial software sessions."""
from contextlib import contextmanager
import importlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from . import environments


ADAPTERS = {
    'lumerical': {'modules': ['lumapi'], 'platforms': ['Windows', 'Linux'],
        'options': {'module': 'lumapi', 'product': 'FDTD', 'hide': True},
        'sources': ['https://optics.ansys.com/hc/en-us/articles/360041873053-Session-Management-Python-API',
                    'https://optics.ansys.com/hc/en-us/articles/360041579954-Script-Commands-as-Methods-Python-API'],
        'program': "SESSION.run()\nRESULT = EXPORT(SESSION.getresult(INPUTS['monitor'], INPUTS['quantity']), 'monitor')"},
    'comsol': {'modules': ['mph'], 'platforms': ['Windows', 'Linux', 'Darwin'],
        'options': {}, 'python_package': 'MPh>=1.2,<2',
        'sources': ['https://mph.readthedocs.io/en/stable/api/mph.start.html',
                    'https://mph.readthedocs.io/en/stable/api/mph.Model.html'],
        'program': "MODEL.parameter('wavelength', INPUTS['wavelength'])\nMODEL.solve()\nRESULT = EXPORT(MODEL.evaluate(INPUTS['expression']), 'field')"},
    'opticstudio': {'modules': ['zospy'], 'platforms': ['Windows'],
        'options': {}, 'python_package': 'zospy>=2.2,<3',
        'sources': ['https://zospy.readthedocs.io/en/stable/api/zospy.zpcore.ZOS.html',
                    'https://zospy.readthedocs.io/en/stable/api/zospy.zpcore.OpticStudioSystem.html'],
        'program': "from zospy.analyses.mtf import FFTMTF\nresult = FFTMTF(sampling='128x128').run(MODEL)\n(OUTPUT_DIR/'mtf.json').write_text(result.to_json(), encoding='utf-8')\nRESULT = {'data': 'mtf.json'}"},
    'cst': {'modules': ['cst.interface', 'cst.results'], 'platforms': ['Windows', 'Linux'],
        'options': {},
        'sources': ['https://events.3ds.com/python-driven-automation-electromagnetic-simulations',
                    'https://3dswym.3dexperience.3ds.com/question/simulia-community/cst-external-python-api-change-project-parameter-value_ud2NtNGqS-2d_ULgXSQfgQ'],
        'program': "MODEL.modeler.run_solver()\nRESULT = {'project': str(PROJECT_FILE)}"},
}


def details(tool):
    if tool not in ADAPTERS:
        return None
    return {**ADAPTERS[tool], 'tool': tool, 'actions': ['inspect_project'] + ([] if tool == 'opticstudio' else ['solve_project']),
            'inputs': {'project': 'Absolute path to an existing project; omit to create a new project.',
                       'parameters': 'COMSOL parameter names and values with units, or Lumerical object -> property -> value.',
                       'results': 'COMSOL expression list, Lumerical [{monitor, quantity}], or CST result-tree paths.'},
            'namespace': ['SDK', 'SESSION', 'MODEL', 'PROJECT_FILE', 'EXPORT', 'INPUTS', 'OUTPUT_DIR', 'RESULT'],
            'execution': 'One owned software session per background step. Keep optimization loops in one program. Save the model and arrays in the run directory.',
            'verification': 'Adapter lifecycle tests; licensed solver execution is required on the target workstation.'}


def discover(roots=None):
    """Inspect known installation layouts, without launching software or scanning whole disks."""
    folders = [Path(p).expanduser() for p in roots or []]
    folders += [Path(p) for p in ('/opt', '/opt/ansys_inc', '/usr/local', '/Applications')]
    folders += [Path(os.environ[k]) for k in ('ProgramFiles', 'ProgramFiles(x86)', 'LUMERICAL_HOME', 'CST_HOME', 'COMSOL_HOME', 'ZEMAX_ROOT') if os.environ.get(k)]
    patterns = {
        'lumerical': ['api/python/lumapi.py', '*/api/python/lumapi.py', '*/*/api/python/lumapi.py', 'Lumerical/*/api/python/lumapi.py'],
        'cst': ['AMD64/python_cst_libraries/cst/__init__.py', '*/AMD64/python_cst_libraries/cst/__init__.py', '*/python_cst_libraries/cst/__init__.py'],
        'comsol': ['bin/comsol', '*/bin/comsol', '*/*/bin/comsol', '*/Multiphysics/bin/win64/comsolbatch.exe', '*/*/bin/win64/comsolbatch.exe', '*/*/*/bin/win64/comsolbatch.exe'],
        'opticstudio': ['ZOSAPI.dll', '*/ZOSAPI.dll', '*/*/ZOSAPI.dll'],
    }
    found = {}
    for root in dict.fromkeys(folders):
        if not root.is_dir():
            continue
        for tool, globs in patterns.items():
            for glob in globs:
                for file in root.glob(glob):
                    if not file.is_file():
                        continue
                    full = str(file.resolve())
                    entry = {'tool': tool, 'file': full}
                    if tool == 'lumerical': entry['sdk_path'] = str(file.parent.resolve())
                    if tool == 'cst': entry['sdk_path'] = str(file.parent.parent.resolve())
                    if tool == 'opticstudio': entry['options'] = {'opticstudio_directory': str(file.parent.resolve())}
                    found[(tool, full)] = entry
    return {'platform': platform.system(), 'installations': list(found.values()),
            'adapters': [details(tool) for tool in ADAPTERS]}


def probe(connection):
    modules = ADAPTERS[connection['adapter']]['modules']
    if connection['adapter'] == 'lumerical': modules = [connection['options']['module']]
    code = """import importlib.util,json,sys
if sys.argv[1]: sys.path.insert(0,sys.argv[1])
found={}
for name in json.loads(sys.argv[2]):
 try: found[name]=importlib.util.find_spec(name) is not None
 except (ImportError,ValueError,ModuleNotFoundError): found[name]=False
print(json.dumps({'python':sys.executable,'modules':found,'importable':all(found.values())}))
"""
    result = subprocess.run([connection['python'], '-c', code, connection.get('sdk_path') or '', json.dumps(modules)],
                            capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'Could not inspect the selected SDK environment')
    return json.loads(result.stdout.strip().splitlines()[-1])


def bind(tool, *, python=None, sdk_path=None, options=None, threads=1, concurrency=1, path=None, requirements=None, env=None):
    if tool not in ADAPTERS:
        raise ValueError('Native session adapters: ' + ', '.join(ADAPTERS))
    if platform.system() not in ADAPTERS[tool]['platforms']:
        raise ValueError(tool + ' session adapter runs on ' + ', '.join(ADAPTERS[tool]['platforms']) + '. Run its MCP connection on that workstation.')
    if type(threads) is not int or threads < 1 or type(concurrency) is not int or concurrency < 1:
        raise ValueError('threads and concurrency must be positive integers')
    if options is not None and not isinstance(options, dict):
        raise ValueError('options must be a JSON object')
    allowed = {'lumerical': {'module', 'product', 'hide'}, 'comsol': {'version'},
               'opticstudio': {'opticstudio_directory', 'zosapi_nethelper'}, 'cst': set()}[tool]
    if set(options or {}) - allowed:
        raise ValueError('Supported options: ' + ', '.join(sorted(allowed)))
    settings = {**ADAPTERS[tool]['options'], **(options or {})}
    if tool == 'lumerical':
        if settings['module'] not in ('lumapi', 'ansys.lumerical.core') or settings['product'] not in ('FDTD', 'MODE', 'DEVICE', 'INTERCONNECT') or type(settings['hide']) is not bool:
            raise ValueError('Use lumapi or ansys.lumerical.core; product FDTD, MODE, DEVICE or INTERCONNECT; hide is boolean')
    if tool == 'opticstudio' and len(settings) > 1:
        raise ValueError('Choose opticstudio_directory or zosapi_nethelper')
    if sdk_path:
        sdk_path = str(Path(sdk_path).expanduser().resolve())
        if not Path(sdk_path).is_dir(): raise ValueError('SDK directory does not exist')
    connection = {'kind': 'native', 'adapter': tool, 'python': os.path.abspath(os.path.expanduser(str(python or sys.executable))),
                  'sdk_path': sdk_path, 'options': settings, 'threads': threads, 'concurrency': concurrency, 'cwd': None}
    from .jobs import quantities
    quantities(requirements or {})
    if env is not None and (not isinstance(env, dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in env.items())):
        raise ValueError('env must map environment variable names to strings')
    connection.update(requirements=requirements or {}, env=env or {})
    inspected = probe(connection)
    if not inspected['importable']:
        raise ValueError('Missing SDK modules: ' + ', '.join(k for k, v in inspected['modules'].items() if not v))
    connection['python'] = inspected['python']
    environments.update('tools', tool, connection, path)
    return {'tool': tool, **connection, 'sdk': inspected}


def export(value, name, output):
    """Keep multidimensional and complex data in files, with a small JSON description."""
    import numpy as np
    if not isinstance(name, str) or Path(name).name != name or name in ('', '.', '..'):
        raise ValueError('Use a filename without directory components')
    arrays = {}
    def encode(item):
        if isinstance(item, dict): return {str(k): encode(v) for k, v in item.items()}
        if isinstance(item, (list, tuple)): return [encode(v) for v in item]
        if isinstance(item, np.ndarray) or isinstance(item, (complex, np.generic)):
            data = np.asarray(item)
            if data.dtype.hasobject: raise ValueError('Export numeric arrays rather than opaque Python objects')
            key = 'array_' + str(len(arrays))
            arrays[key] = data
            return {'array': key, 'shape': list(data.shape), 'dtype': str(data.dtype)}
        return item
    structure = encode(value)
    (output / (name + '.json')).write_text(json.dumps(structure, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    if arrays: np.savez_compressed(output / (name + '.npz'), **arrays)
    return {'metadata': name + '.json', 'data': name + '.npz' if arrays else None, 'arrays': len(arrays)}


@contextmanager
def session(connection, inputs, output):
    """Own a session, save under OUTPUT_DIR before execution, and release it on exit."""
    tool, options = connection['adapter'], connection['options']
    sdk_path = connection.get('sdk_path')
    if sdk_path: sys.path.insert(0, sdk_path)
    original = inputs.get('project')
    if original:
        original = str(Path(original).expanduser().resolve())
        if not Path(original).is_file(): raise ValueError('Project file does not exist: ' + original)
    extension = {'lumerical': {'FDTD': '.fsp', 'MODE': '.lms', 'DEVICE': '.ldev', 'INTERCONNECT': '.icp'}.get(options.get('product'), '.fsp'),
                 'comsol': '.mph', 'opticstudio': '.zos', 'cst': '.cst'}[tool]
    target = output / ('model' + (Path(original).suffix if original else extension))
    sdk = owner = model = None
    try:
        if tool == 'lumerical':
            sdk = importlib.import_module(options['module'])
            owner = getattr(sdk, options['product'])(hide=options['hide'], serverArgs={'threads': str(connection['threads'])})
            model = owner
            if original: model.load(original)
            save = lambda: model.save(str(target))
        elif tool == 'comsol':
            sdk = importlib.import_module('mph')
            owner = sdk.start(cores=connection['threads'], **options)
            model = owner.load(original) if original else owner.create('optical_model')
            save = lambda: model.save(str(target))
        elif tool == 'opticstudio':
            sdk = importlib.import_module('zospy')
            owner = sdk.ZOS(**options)
            model = owner.connect(mode='standalone')
            if original: model.load(original, saveifneeded=False)
            save = lambda: model.save_as(str(target))
        else:
            sdk = importlib.import_module('cst.interface')
            owner = sdk.DesignEnvironment()
            model = owner.open_project(original) if original else owner.new_mws()
            save = lambda: model.save(str(target))
        save()
        yield {'SDK': sdk, 'SESSION': owner, 'MODEL': model, 'PROJECT_FILE': target,
               'EXPORT': lambda value, name='data': export(value, name, output)}
        save()
    finally:
        if owner is not None:
            if tool == 'comsol':
                # MPh owns its local server and registers its shutdown at Python exit.
                if model is not None: owner.remove(model)
            elif tool == 'opticstudio': owner.disconnect()
            else: owner.close()


def calculate(tool, action, inputs, namespace):
    model, output = namespace['MODEL'], namespace['OUTPUT_DIR']
    if action == 'inspect_project':
        result = {'project': str(namespace['PROJECT_FILE']), 'adapter': tool}
        if tool == 'comsol': result.update(studies=model.studies(), parameters=model.parameters(), physics=model.physics())
        elif tool == 'opticstudio': result.update(surfaces=model.LDE.NumberOfSurfaces, status=model.get_current_status())
        return result
    if action != 'solve_project' or tool == 'opticstudio':
        raise ValueError('Use inspect_project, solve_project, or a native source program; OpticStudio analyses use source')
    parameters = inputs.get('parameters', {})
    results = inputs.get('results', [])
    if not isinstance(parameters, dict) or not isinstance(results, list):
        raise ValueError('parameters is an object; results is an array')
    if tool == 'comsol':
        for key, value in parameters.items(): model.parameter(key, str(value))
        model.solve(inputs.get('study'))
        data = {expression: model.evaluate(expression) for expression in results}
    elif tool == 'lumerical':
        model.switchtolayout()
        for object_name, properties in parameters.items():
            for name, value in properties.items(): model.setnamed(object_name, name, value)
        model.run()
        data = {str(i): model.getresult(item['monitor'], item['quantity']) for i, item in enumerate(results)}
    else:
        if parameters: raise ValueError('Set CST geometry and parameters through a native source program and its installed API')
        model.modeler.run_solver()
        model.save(str(namespace['PROJECT_FILE']))
        api = importlib.import_module('cst.results')
        project = api.ProjectFile(str(namespace['PROJECT_FILE']), allow_interactive=True)
        data = {}
        for name in results:
            result = project.get_3d().get_result_item(name)
            import numpy as np
            data[name] = {'x': np.asarray(result.get_xdata()), 'y': np.asarray(result.get_ydata())}
    return {'project': str(namespace['PROJECT_FILE']), **export(data, 'results', output)}
