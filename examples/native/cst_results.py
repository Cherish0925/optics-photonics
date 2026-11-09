"""Inputs: project, result_paths from its result tree; optional history VBA text."""
import numpy as np
import cst.results

if INPUTS.get('history'):
    MODEL.modeler.add_to_history('Research model update', INPUTS['history'])
MODEL.modeler.run_solver()
MODEL.save(str(PROJECT_FILE))
results = cst.results.ProjectFile(str(PROJECT_FILE), allow_interactive=True)
data = {}
for name in INPUTS['result_paths']:
    curve = results.get_3d().get_result_item(name)
    data[name] = {'x': np.asarray(curve.get_xdata()), 'y': np.asarray(curve.get_ydata())}
RESULT = EXPORT(data, 'curves')
