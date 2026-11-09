"""Optimize a lossless, constant-index single layer using tmm and SciPy.

Inputs: refractive_indices [air,film,substrate], wavelength_min_nm,
wavelength_max_nm, thickness_bounds_nm, spectrum_points (optional).
The objective is mean power reflectance under a uniform wavelength weighting.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import minimize_scalar
from tmm import coh_tmm

n = INPUTS['refractive_indices']
lo, hi = INPUTS['wavelength_min_nm'], INPUTS['wavelength_max_nm']
dlo, dhi = INPUTS['thickness_bounds_nm']
if len(n) != 3 or not 0 < lo < hi or not 0 <= dlo < dhi:
    raise ValueError('Provide three indices and increasing positive wavelength/thickness intervals')
x, weight = leggauss(96)
wavelengths = (lo+hi)/2 + (hi-lo)*x/2

def solve(d, wavelength):
    return coh_tmm('s', n, [np.inf, d, np.inf], 0, wavelength)

def objective(d):
    return float(np.dot(weight,[solve(d,w)['R'] for w in wavelengths])/2)

# Search separated minima before refining them; include both interval endpoints.
grid = np.linspace(dlo, dhi, 201)
values = np.array([objective(d) for d in grid])
candidates = [(dlo,values[0]),(dhi,values[-1])]
for i in range(1,len(grid)-1):
    if values[i] <= values[i-1] and values[i] <= values[i+1]:
        result = minimize_scalar(objective,bounds=(grid[i-1],grid[i+1]),method='bounded')
        if not result.success: raise RuntimeError(result.message)
        candidates.append((result.x,result.fun))
thickness, mean_R = min(candidates,key=lambda x:x[1])
wave = np.linspace(lo,hi,INPUTS.get('spectrum_points',1001))
rows = [[w,solve(thickness,w)['R'],solve(thickness,w)['T']] for w in wave]
np.savetxt(OUTPUT_DIR/'spectrum.csv',rows,delimiter=',',header='wavelength_nm,R,T',comments='')
np.savetxt(OUTPUT_DIR/'thickness_scan.csv',np.column_stack([grid,values]),delimiter=',',header='thickness_nm,mean_R',comments='')
RESULT = {'thickness_nm':float(thickness),'mean_reflectance':float(mean_R),
          'wavelength_interval_nm':[lo,hi],'weighting':'uniform per nm',
          'model':'coherent single layer; constant isotropic lossless indices; normal incidence',
          'maximum_power_residual':float(max(abs(1-r-t) for w,r,t in rows))}
