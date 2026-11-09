"""Inputs: project, parameter, values (with units), expression, optional study."""
import json

outputs = []
for index, value in enumerate(INPUTS['values']):
    MODEL.parameter(INPUTS['parameter'], str(value))
    MODEL.solve(INPUTS.get('study'))
    data = EXPORT(MODEL.evaluate(INPUTS['expression']), f'field-{index:04d}')
    outputs.append({'parameter': value, **data})
    (OUTPUT_DIR/'sweep.json').write_text(json.dumps(outputs), encoding='utf-8')
RESULT = {'points': len(outputs), 'index': 'sweep.json', 'project': str(PROJECT_FILE)}
