"""Inputs: project, monitor, quantity; optional object -> properties mapping."""
SESSION.switchtolayout()
for object_name, properties in INPUTS.get('parameters', {}).items():
    for name, value in properties.items():
        SESSION.setnamed(object_name, name, value)
SESSION.run()
RESULT = EXPORT(SESSION.getresult(INPUTS['monitor'], INPUTS['quantity']), 'monitor')
