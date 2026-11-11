"""Write a DSH Discover index for an already published source revision."""
import argparse
import json
from pathlib import Path
import time

PACKAGE = 'connect/deepseek'
TITLE = 'Optics-Photonics-AI-Lab'
REPOSITORY = 'https://github.com/Cherish0925/Optics-Photonics-AI-Lab'
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--commit', required=True)
args = parser.parse_args()
package = json.loads((ROOT / PACKAGE / 'package.json').read_text())
index = {'format': 1, 'title': TITLE, 'plugins': [{
    'name': package['name'], 'title': TITLE, 'description': package['description'],
    'repository': {'url': REPOSITORY, 'directory': PACKAGE},
    'versions': [{'version': package['version'], 'publishTimestamp': int(time.time()),
        'source': {'type': 'git', 'url': REPOSITORY, 'commit': args.commit, 'path': PACKAGE}}]}]}
target = ROOT / 'docs/dsh/index.json'
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(index, indent=2)+'\n', encoding='utf-8')
print(target)
