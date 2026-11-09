"""Prepare a scientific environment as an ordinary background job."""
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from optics_photonics.environments import prepare

request=json.loads(Path(os.environ['OPTICS_REQUEST_FILE']).read_text(encoding='utf-8'))['inputs']
result=prepare(request['tool'],python=request.get('python'),path=request['home'])
Path(os.environ['OPTICS_RESULT_FILE']).write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
