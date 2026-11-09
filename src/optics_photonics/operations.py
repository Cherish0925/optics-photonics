"""Small, inspectable calculations; native programs retain the complete upstream API."""
import math
from pathlib import Path


EXAMPLES = {
    'optiland': ('trace', {'surfaces': [{'radius_mm': None, 'thickness_mm': None}, {'radius_mm': 50, 'thickness_mm': 5, 'index': 1.5, 'stop': True}, {'radius_mm': -50, 'thickness_mm': 50}, {'radius_mm': None, 'thickness_mm': 0}], 'aperture_mm': 10, 'field_deg': [0, 0], 'wavelength_um': 0.55, 'pupil_points': [[0, 0], [0, 0.5], [0, -0.5], [0.5, 0], [-0.5, 0]]}),
    'gdsfactory': ('waveguide', {'length_um': 20, 'width_um': 0.5}),
    'py-pol': ('polarization', {'azimuth_deg': 0, 'intensity': 1, 'elements': [{'type': 'polarizer', 'azimuth_deg': 45}]}),
    'tmm': ('spectrum', {'n': [1, 1.45, 1.52], 'thickness_nm': [100], 'wavelength_nm': [450, 550, 650], 'polarization': 's', 'angle_deg': 0}),
    'miepython': ('sphere', {'index': [1.5, 0], 'diameter_nm': 200, 'wavelength_nm': [450, 550, 650], 'medium_index': 1}),
    'raytracing': ('abcd', {'elements': [{'space_m': 0.1}, {'focal_length_m': 0.05}, {'space_m': 0.1}], 'ray': [0.001, 0]}),
    'lightpipes': ('gaussian', {'wavelength_m': 532e-9, 'window_m': 0.01, 'waist_m': 0.001, 'distance_m': 1, 'samples': 128}),
    'poppy': ('psf', {'wavelength_m': 550e-9, 'diameter_m': 1, 'pixel_arcsec': 0.02, 'pixels': 64}),
    'hcipy': ('psf', {'wavelength_m': 550e-9, 'diameter_m': 1, 'samples': 128, 'pixels_per_lambda_over_d': 4, 'radius_lambda_over_d': 8}),
    'qutip': ('rabi', {'omega_rad_s': 1, 'times_s': [0, math.pi, 2 * math.pi]}),
    'sympy': ('abcd', {'focal_length': 'f', 'distance_before': 'a', 'distance_after': 'b'}),
    'scipy': ('fit_gaussian', {'x': [-2, -1, 0, 1, 2], 'y': [0.1353352832, 0.6065306597, 1, 0.6065306597, 0.1353352832], 'x_unit': 'mm'}),
    'scikitimage': ('registration', {'reference': [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0]], 'moving': [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 2], [0, 0, 0, 0]], 'upsample_factor': 1}),
    'klayout': ('layout', {'rectangles_um': [[0, 0, 10, 0.5], [12, 0, 22, 0.5]], 'layer': 1, 'datatype': 0, 'dbu_um': 0.001}),
    'grcwa': ('film', {'epsilon': [1, 2.1025, 2.3104], 'thickness_over_wavelength': [0, 0.1818181818, 0], 'polarization': 's', 'angle_deg': 0}),
    'legume': ('bands', {'epsilon': 12, 'thickness_over_period': 0.5, 'hole_radius_over_period': 0.2, 'kpoints': [[0.1, 0.5], [0, 0]], 'gmax': 2, 'numeig': 2}),
}

NOTES = {
    'optiland': 'Sequential real-ray tracing in millimetres, with wavelength in micrometres. A surface index describes the homogeneous medium after that surface. null radius is planar; null thickness is an object at infinity. Field is [x,y] in degrees; pupil_points are normalized entrance-pupil coordinates. Constant indices have no dispersion. Native programs support catalogs, freeforms and optimization.',
    'gdsfactory': 'Straight strip waveguide from the bundled generic PDK. All lengths in micrometres. Saves GDSII, port names, coordinates, widths and orientations. Fabrication uses the target foundry PDK through a native program.',
    'py-pol': 'Fully polarized monochromatic Jones field with linear input. Elements appear in propagation order; angles are in degrees from x. Supports ideal linear polarizers, quarter-wave and half-wave plates. Jones amplitudes retain the py-pol phase convention. Native programs provide arbitrary Jones and Mueller models.',
    'tmm': 'Coherent, isotropic planar layers. n may be a real number or [real, imaginary]. Exterior media are semi-infinite. Supply one thickness per internal layer. Indices here are constant across wavelength; use a native program for dispersion or incoherent layers. Returns power R, T and 1-R-T.',
    'miepython': 'Homogeneous spherical particle in a nonabsorbing medium. index is the absolute complex particle index [real, imaginary]; use nonpositive imaginary part for loss in miepython. Diameter and vacuum wavelength in nm. Returns dimensionless efficiencies and asymmetry g.',
    'raytracing': 'Paraxial ray vector [height in m, angle in rad]. Elements appear in propagation order. space_m and focal_length_m use metres. ABCD assumes equal entrance/exit index for the supplied free-space and thin-lens elements.',
    'lightpipes': 'Scalar paraxial Fresnel propagation of a Gaussian field. All lengths in metres; waist is the field 1/e radius. Output is relative intensity on a square grid. Increase the field window and grid independently to study sampling.',
    'poppy': 'Fraunhofer PSF of an unobscured circular pupil, normalized to entrance power. Wavelength and diameter in metres; detector angular sampling in arcsec/pixel. The finite detector need not contain all the power.',
    'hcipy': 'Fraunhofer PSF of an unobscured circular pupil. Wavelength and pupil in metres; focal coordinates are radians (unit focal length). Normalized numerical integral over the finite computed focal grid.',
    'qutip': 'Closed two-level system H=(omega/2)*sigma_x with hbar=1, initially basis(2,0). Reports basis(2,1) population. omega in rad/s and times in seconds. Native programs provide arbitrary Hamiltonians and collapse operators.',
    'sympy': 'Symbolic paraxial free space, thin lens, free space. Symbols are names, not expressions; outputs exact SymPy expressions for ABCD and determinant. Use one consistent length unit.',
    'scipy': 'Fit A*exp(-(x-center)^2/(2*sigma^2)) with zero background. x_unit names the supplied coordinate unit. This is a numerical fit, not an instrument calibration.',
    'scikitimage': 'Phase cross-correlation; returns the row/column translation in pixels to apply to moving so it aligns to reference. Periodic ambiguity and overlap need to be considered for real images.',
    'klayout': 'GDSII rectangles in micrometres on one layer/datatype; dbu_um sets integer-grid precision. Layout generation does not perform PDK design-rule checking.',
    'grcwa': 'RCWA uniform-layer example with real isotropic permittivities. Thickness divided by vacuum wavelength; first/last layers are exterior media. Returns power R and T. Patterned cells are available through native grcwa programs.',
    'legume': 'Guided-mode expansion for a square-periodic dielectric slab with one circular air hole. Lengths normalized by period; kpoints in radians/period; frequency is a/lambda. gmax and mode basis require convergence for each structure.',
}


def details(tool):
    if tool not in EXAMPLES:
        from . import native
        adapter = native.details(tool)
        return {'operations': [], 'native_program': True, **({'session_adapter': adapter} if adapter else {})}
    action, inputs = EXAMPLES[tool]
    return {'operations': [{'name': action, 'inputs_example': inputs, 'description': NOTES[tool]}], 'native_program': True}


def complex_number(value):
    return complex(*value) if isinstance(value, list) else complex(value)


def positive(value, name):
    if not math.isfinite(float(value)) or value <= 0:
        raise ValueError(name + ' must be positive and finite')
    return value


def count(value, name):
    if type(value) is not int or value < 2:
        raise ValueError(name + ' must be an integer >= 2')
    return value


def calculate(tool, action, p, output):
    """Execute upstream functions. Large results remain in scientific files."""
    if tool not in EXAMPLES or action != EXAMPLES[tool][0]:
        raise ValueError(f'Unknown operation {tool}/{action}; use software_details or a native program')
    import numpy as np
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    if tool == 'optiland':
        from optiland import optic
        from optiland.materials import IdealMaterial
        system = optic.Optic()
        for i, surface in enumerate(p['surfaces']):
            radius = surface.get('radius_mm')
            thickness = surface.get('thickness_mm', 0)
            system.surfaces.add(index=i, radius=np.inf if radius is None else radius,
                thickness=np.inf if thickness is None else thickness,
                material=IdealMaterial(positive(surface.get('index', 1), 'index')),
                is_stop=surface.get('stop', False))
        system.set_aperture('EPD', positive(p['aperture_mm'], 'aperture_mm'))
        system.fields.set_type('angle')
        fx, fy = p.get('field_deg', [0, 0])
        system.fields.add(x=fx, y=fy)
        wavelength = positive(p['wavelength_um'], 'wavelength_um')
        system.wavelengths.add(value=wavelength, is_primary=True)
        pupil = np.asarray(p['pupil_points'], dtype=float)
        if pupil.ndim != 2 or pupil.shape[1] != 2 or np.any(np.sum(pupil**2, axis=1) > 1):
            raise ValueError('pupil_points must be [x,y] pairs within the unit entrance pupil')
        system.trace_generic(Hx=1 if fx else 0, Hy=1 if fy else 0, Px=pupil[:,0], Py=pupil[:,1], wavelength=wavelength)
        x, y = np.asarray(system.surfaces.x), np.asarray(system.surfaces.y)
        np.savez_compressed(out/'rays.npz', x_mm=x, y_mm=y, pupil_xy=pupil, wavelength_um=wavelength)
        xy = np.column_stack([x[-1], y[-1]])
        np.savetxt(out/'image.csv', xy, delimiter=',', header='x_mm,y_mm', comments='')
        valid = np.isfinite(xy).all(axis=1)
        if not valid.any():
            raise ValueError('No finite image-plane intersections; inspect the surface prescription')
        centroid = xy[valid].mean(axis=0)
        rms = np.sqrt(np.mean(np.sum((xy[valid]-centroid)**2, axis=1)))
        return {'rays': len(xy), 'finite_intersections': int(valid.sum()), 'centroid_mm': centroid.tolist(), 'rms_spot_mm': float(rms), 'image_xy_mm': [[float(v) if np.isfinite(v) else None for v in row] for row in xy], 'data': 'rays.npz'}
    if tool == 'gdsfactory':
        import gdsfactory as gf
        from gdsfactory.gpdk import get_generic_pdk
        get_generic_pdk().activate()
        component = gf.components.straight(length=positive(p['length_um'], 'length_um'), width=positive(p['width_um'], 'width_um'))
        component.write_gds(out/'waveguide.gds', with_metadata=False)
        ports = [{'name': port.name, 'center_um': list(port.center), 'orientation_deg': float(port.orientation), 'width_um': float(port.width)} for port in component.ports]
        return {'pdk': 'generic', 'ports': ports, 'data': 'waveguide.gds'}
    if tool == 'py-pol':
        from py_pol.jones_vector import Jones_vector
        from py_pol.jones_matrix import Jones_matrix
        field = Jones_vector('input')
        field.linear_light(azimuth=math.radians(p.get('azimuth_deg', 0)), intensity=positive(p.get('intensity', 1), 'intensity'))
        methods = {'polarizer': 'diattenuator_perfect', 'quarter_waveplate': 'quarter_waveplate', 'half_waveplate': 'half_waveplate'}
        for element in p['elements']:
            if element['type'] not in methods:
                raise ValueError('Element type must be polarizer, quarter_waveplate or half_waveplate')
            matrix = Jones_matrix(element['type'])
            getattr(matrix, methods[element['type']])(azimuth=math.radians(element.get('azimuth_deg', 0)))
            field = matrix * field
        values = np.asarray(field.M).reshape(2)
        return {'intensity': float(field.parameters.intensity()), 'jones_xy': [[float(v.real), float(v.imag)] for v in values]}
    if tool == 'tmm':
        from tmm import coh_tmm
        n = [complex_number(v) for v in p['n']]
        d = [math.inf, *p['thickness_nm'], math.inf]
        if len(n) != len(d) or any(v < 0 for v in d):
            raise ValueError('Provide N indices and N-2 nonnegative internal thicknesses')
        rows = []
        for wavelength in p['wavelength_nm']:
            result = coh_tmm(p.get('polarization', 's'), n, d, math.radians(p.get('angle_deg', 0)), positive(wavelength, 'wavelength_nm'))
            r, t = float(result['R']), float(result['T'])
            rows.append([wavelength, r, t, 1-r-t])
        np.savetxt(out/'spectrum.csv', rows, delimiter=',', header='wavelength_nm,R,T,one_minus_R_minus_T', comments='')
        return {'columns': ['wavelength_nm', 'R', 'T', 'one_minus_R_minus_T'], 'samples': len(rows), 'first': rows[0], 'last': rows[-1], 'data': 'spectrum.csv'}
    if tool == 'miepython':
        import miepython
        m = complex_number(p['index'])
        if m.imag > 0:
            raise ValueError('miepython uses nonpositive imaginary index for loss')
        rows = []
        for wavelength in p['wavelength_nm']:
            vals = miepython.efficiencies(m, positive(p['diameter_nm'], 'diameter_nm'), positive(wavelength, 'wavelength_nm'), n_env=positive(p.get('medium_index', 1), 'medium_index'))
            rows.append([wavelength, *map(float, vals)])
        np.savetxt(out/'scattering.csv', rows, delimiter=',', header='wavelength_nm,Qext,Qsca,Qback,g', comments='')
        return {'samples': len(rows), 'first': rows[0], 'last': rows[-1], 'data': 'scattering.csv'}
    if tool == 'raytracing':
        from raytracing import Matrix, Space, Lens
        matrix = Matrix()
        for element in p['elements']:
            if set(element) == {'space_m'}:
                matrix = Space(element['space_m']) * matrix
            elif set(element) == {'focal_length_m'} and element['focal_length_m'] != 0:
                matrix = Lens(element['focal_length_m']) * matrix
            else:
                raise ValueError('Each element is space_m or a nonzero focal_length_m')
        a = np.array([[matrix.A, matrix.B], [matrix.C, matrix.D]])
        return {'matrix': a.tolist(), 'matrix_units': [['1','m'],['1/m','1']], 'ray_out': (a @ p.get('ray', [0, 0])).tolist(), 'ray_units': ['m','rad'], 'determinant': float(np.linalg.det(a))}
    if tool == 'lightpipes':
        from LightPipes import Begin, GaussBeam, Fresnel, Intensity
        size = positive(p['window_m'], 'window_m'); samples = count(p['samples'], 'samples')
        field = GaussBeam(Begin(size, positive(p['wavelength_m'], 'wavelength_m'), samples), positive(p['waist_m'], 'waist_m'))
        distance = p['distance_m']
        if distance < 0:
            raise ValueError('Use a native propagation program for negative distance')
        field = Fresnel(field, distance) if distance else field
        intensity = Intensity(field, 0)
        np.savez_compressed(out/'field.npz', field=field.field, intensity=intensity, x_m=np.arange(samples)*size/samples-size/2)
        return {'shape': list(intensity.shape), 'spacing_m': size/samples, 'integrated_intensity_m2': float(intensity.sum()*(size/samples)**2), 'data': 'field.npz'}
    if tool == 'poppy':
        import poppy
        system = poppy.OpticalSystem(oversample=1)
        system.add_pupil(poppy.CircularAperture(radius=positive(p['diameter_m'], 'diameter_m')/2))
        system.add_detector(pixelscale=positive(p['pixel_arcsec'], 'pixel_arcsec'), fov_pixels=count(p['pixels'], 'pixels'))
        psf = system.calc_psf(wavelength=positive(p['wavelength_m'], 'wavelength_m'))
        psf.writeto(out/'psf.fits', overwrite=True)
        return {'shape': list(psf[0].data.shape), 'captured_power': float(psf[0].data.sum()), 'pixel_arcsec': p['pixel_arcsec'], 'data': 'psf.fits'}
    if tool == 'hcipy':
        import hcipy as hp
        diameter = positive(p['diameter_m'], 'diameter_m'); wavelength = positive(p['wavelength_m'], 'wavelength_m')
        pupil = hp.make_pupil_grid(count(p['samples'], 'samples'), diameter)
        focal = hp.make_focal_grid(positive(p['pixels_per_lambda_over_d'], 'pixels_per_lambda_over_d'), positive(p['radius_lambda_over_d'], 'radius_lambda_over_d'), spatial_resolution=wavelength/diameter)
        wave = hp.Wavefront(hp.make_circular_aperture(diameter)(pupil), wavelength)
        image = hp.FraunhoferPropagator(pupil, focal)(wave).intensity
        total = float(np.sum(image * focal.weights))
        np.savez_compressed(out/'psf.npz', intensity=np.asarray(image.shaped)/total, x_rad=np.asarray(focal.x.shaped), y_rad=np.asarray(focal.y.shaped))
        return {'shape': list(image.shaped.shape), 'normalization': 'integral over computed focal grid = 1', 'data': 'psf.npz'}
    if tool == 'qutip':
        import qutip as qt
        times = np.asarray(p['times_s'], dtype=float)
        if len(times) < 2 or np.any(np.diff(times) <= 0) or times[0] != 0:
            raise ValueError('times_s must start at zero and increase strictly')
        excited = qt.basis(2, 1).proj()
        evolution = qt.sesolve(0.5*p['omega_rad_s']*qt.sigmax(), qt.basis(2, 0), times, e_ops=[excited], options={'atol': 1e-10, 'rtol': 1e-9})
        values = np.asarray(evolution.expect[0])
        np.savetxt(out/'population.csv', np.column_stack([times, values]), delimiter=',', header='time_s,population_1', comments='')
        return {'samples': len(times), 'first': float(values[0]), 'last': float(values[-1]), 'maximum': float(values.max()), 'data': 'population.csv'}
    if tool == 'sympy':
        import sympy as sp
        vals = [p[k] for k in ('focal_length', 'distance_before', 'distance_after')]
        if not all(isinstance(v, str) and v.isidentifier() for v in vals):
            raise ValueError('Provide three symbolic variable names')
        f,a,b = (sp.Symbol(v, nonzero=True) if i == 0 else sp.Symbol(v) for i,v in enumerate(vals))
        result = sp.Matrix([[1,b],[0,1]]) * sp.Matrix([[1,0],[-1/f,1]]) * sp.Matrix([[1,a],[0,1]])
        return {'matrix': [[str(sp.simplify(v)) for v in row] for row in result.tolist()], 'determinant': str(sp.simplify(result.det()))}
    if tool == 'scipy':
        from scipy.optimize import curve_fit
        x,y = np.asarray(p['x'], dtype=float), np.asarray(p['y'], dtype=float)
        def gaussian(x, amplitude, center, sigma):
            return amplitude*np.exp(-0.5*((x-center)/sigma)**2)
        pars, cov = curve_fit(gaussian, x, y, p0=[y.max(), x[y.argmax()], np.std(x)/2], bounds=([-np.inf,-np.inf,np.finfo(float).eps], [np.inf,np.inf,np.inf]))
        np.savetxt(out/'fit.csv', np.column_stack([x,y,gaussian(x,*pars)]), delimiter=',', header='x,observed,fitted', comments='')
        return {'amplitude': float(pars[0]), 'center': float(pars[1]), 'sigma': float(pars[2]), 'x_unit': p['x_unit'], 'parameter_covariance': cov.tolist(), 'data': 'fit.csv'}
    if tool == 'scikitimage':
        from skimage.registration import phase_cross_correlation
        shift, error, phase = phase_cross_correlation(np.asarray(p['reference']), np.asarray(p['moving']), upsample_factor=p.get('upsample_factor', 1))
        return {'shift_pixels': shift.tolist(), 'axis_order': ['row','column'], 'normalized_error': float(error), 'phase_difference_rad': float(phase)}
    if tool == 'klayout':
        import klayout.db as db
        layout = db.Layout(); layout.dbu = positive(p.get('dbu_um',0.001), 'dbu_um')
        top = layout.create_cell('TOP'); layer = layout.layer(int(p.get('layer',1)), int(p.get('datatype',0)))
        for rect in p['rectangles_um']:
            if len(rect) != 4 or rect[2] <= rect[0] or rect[3] <= rect[1]:
                raise ValueError('Rectangles are [left,bottom,right,top] in increasing order')
            top.shapes(layer).insert(db.DBox(*rect))
        layout.write(str(out/'layout.gds'))
        return {'cells': layout.cells(), 'rectangles': len(p['rectangles_um']), 'dbu_um': layout.dbu, 'data': 'layout.gds'}
    if tool == 'grcwa':
        import grcwa
        if len(p['epsilon']) != len(p['thickness_over_wavelength']) or len(p['epsilon']) < 2:
            raise ValueError('Provide matching permittivity and thickness lists including exterior media')
        # A uniform film has only the zeroth diffraction order. grcwa selects one
        # retained order from nG=2; no artificial grazing higher orders are needed.
        solver = grcwa.obj(2, [1,0], [0,1], 1.0, math.radians(p.get('angle_deg',0)), 0, verbose=0)
        for eps, thick in zip(p['epsilon'], p['thickness_over_wavelength']):
            solver.Add_LayerUniform(float(thick), float(eps))
        solver.Init_Setup()
        pol = p.get('polarization','s')
        if pol not in ('s','p'): raise ValueError('polarization is s or p')
        solver.MakeExcitationPlanewave(p_amp=int(pol=='p'), p_phase=0, s_amp=int(pol=='s'), s_phase=0)
        r,t = solver.RT_Solve(normalize=1)
        return {'R': float(r), 'T': float(t), 'one_minus_R_minus_T': float(1-r-t)}
    if tool == 'legume':
        import legume
        crystal = legume.PhotCryst(legume.Lattice('square'))
        crystal.add_layer(d=p['thickness_over_period'], eps_b=p['epsilon'])
        crystal.add_shape(legume.Circle(eps=1, r=p['hole_radius_over_period']))
        solver = legume.GuidedModeExp(crystal, gmax=p.get('gmax',2))
        solver.run(kpoints=np.asarray(p['kpoints'], dtype=float), gmode_inds=[0], numeig=p.get('numeig',2), compute_im=False, verbose=False)
        np.savez_compressed(out/'bands.npz', kpoints=p['kpoints'], frequencies=solver.freqs)
        return {'frequencies_a_over_lambda': solver.freqs.tolist(), 'data': 'bands.npz'}
