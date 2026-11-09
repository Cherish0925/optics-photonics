"""Run inside the licensed installation's lumapi environment.

Inputs: model_path, object_name, property, value, monitor, result_name.
Model paths belong to the computing host. Configure the analysis/model first.
"""
import lumapi
import numpy as np

with lumapi.FDTD(hide=True) as simulation:
    simulation.load(INPUTS['model_path'])
    simulation.switchtolayout()
    simulation.setnamed(INPUTS['object_name'], INPUTS['property'], INPUTS['value'])
    simulation.run()
    data = simulation.getresult(INPUTS['monitor'], INPUTS['result_name'])
    arrays = {key: value for key, value in data.items() if isinstance(value, np.ndarray)}
    np.savez_compressed(OUTPUT_DIR/'monitor.npz', **arrays)
    RESULT = {'monitor':INPUTS['monitor'], 'dataset':INPUTS['result_name'],
              'arrays':{key:list(value.shape) for key,value in arrays.items()},
              'data':'monitor.npz'}
