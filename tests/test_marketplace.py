"""Execute published plugin layouts after moving them outside the repository."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MarketplaceTests(unittest.TestCase):
    def test_native_marketplaces_and_research_os_launch_after_relocation(self):
        requests = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': 'marketplace-install', 'version': '1'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {
                'name': 'software_search', 'arguments': {'query': 'tmm'}}},
        ]
        with tempfile.TemporaryDirectory(prefix='Optics installed package ') as temporary:
            root = Path(temporary)
            native = root / 'native plugin'
            native.mkdir()
            for directory in ('src', 'data', 'skills', '.codex-plugin', '.claude-plugin', '.agents'):
                shutil.copytree(ROOT / directory, native / directory,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            for filename in ('server.py', '.mcp.json', 'mcp.codex.json'):
                shutil.copy2(ROOT / filename, native / filename)
            research = root / 'Research OS plugin'
            shutil.copytree(ROOT / 'connect/agentic-research-os', research)
            for folder in ('.agents/plugins', '.claude-plugin'):
                market = json.loads((native / folder / 'marketplace.json').read_text())
                self.assertEqual(market['plugins'][0]['name'], 'optics-photonics')
            specs = [
                (native, json.loads((native / 'mcp.codex.json').read_text())['mcpServers']['optics']),
                (native, json.loads((native / '.mcp.json').read_text())['mcpServers']['optics']),
                (research, json.loads((research / 'plugin.json').read_text())['mcpServers']['optics']),
            ]
            for package, spec in specs:
                with self.subTest(command=spec):
                    args = [arg.replace('${PLUGIN_ROOT}', str(package))
                            .replace('${CLAUDE_PLUGIN_ROOT}', str(package))
                            .replace('${PACKAGE_ROOT}', str(package)) for arg in spec['args']]
                    command = sys.executable if spec['command'] == '${RESEARCH_PYTHON}' else spec['command']
                    env = {key: value for key, value in os.environ.items() if key != 'PYTHONPATH'}
                    env['OPTICS_HOME'] = str(root / 'state')
                    process = subprocess.run([command, *args], cwd=root, env=env,
                        input='\n'.join(map(json.dumps, requests))+'\n', capture_output=True,
                        text=True, timeout=30, check=True)
                    replies = [json.loads(line) for line in process.stdout.splitlines()]
                    self.assertEqual([reply['id'] for reply in replies], [1, 2, 3])
                    self.assertGreaterEqual(len(replies[1]['result']['tools']), 17)
                    result = replies[2]['result']['structuredContent']
                    self.assertEqual(result['items'][0]['id'], 'tmm')


if __name__ == '__main__':
    unittest.main()
