"""Inputs: project, optional sampling (for example 128x128), field and wavelength."""
from zospy.analyses.mtf import FFTMTF

analysis = FFTMTF(sampling=INPUTS.get('sampling', '128x128'),
                  field=INPUTS.get('field', 'All'), wavelength=INPUTS.get('wavelength', 'All'))
result = analysis.run(MODEL)
(OUTPUT_DIR/'mtf.json').write_text(result.to_json(), encoding='utf-8')
if result.data is not None:
    result.data.to_csv(OUTPUT_DIR/'mtf.csv')
RESULT = {'analysis': 'FFT MTF', 'data': 'mtf.json', 'project': str(PROJECT_FILE)}
