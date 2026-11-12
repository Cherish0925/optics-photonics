import io
import json
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from optics_photonics import mcp

ROOT = Path(__file__).resolve().parents[1]
NAMES = {name for name, _, _ in mcp.TOOLS}
ARGUMENTS = {key for _, _, spec in mcp.TOOLS for key in spec['properties']}
# Identifiers that belong to programs and records, not to the tool interface.
PROGRAM = {'optics_photonics', 'make_env', 'make_policy', 'episode_end', 'episode_error', 'inspect_project', 'solve_project',
           'opticstudio_directory', 'zosapi_nethelper'}


def call(name, arguments):
    return mcp.tool_result({'name': name, 'arguments': arguments})


class GuideCase(unittest.TestCase):
    def test_every_guide_is_served_and_every_link_is_a_topic(self):
        topics = mcp.guides()
        self.assertEqual(list(topics)[:2], ['optical-computation', 'optical-research'])
        self.assertEqual(next(spec for name, _, spec in mcp.TOOLS if name == 'read_guide')['properties']['topic']['enum'], list(topics))
        linked = set()
        for topic, file in topics.items():
            result = call('read_guide', {'topic': topic})
            self.assertFalse(result['isError'], topic)
            text = result['content'][0]['text']
            self.assertFalse(text.startswith('---'), topic)  # no Skill front matter
            self.assertEqual(result['structuredContent'], {'text': text})
            for label, target in re.findall(r'\[([^\]]+)\]\((references/[^)]+)\)', text):
                self.assertTrue((file.parent / target).is_file(), (topic, target))
                self.assertEqual(label, Path(target).stem, 'a link is named after its topic')
                linked.add(Path(target).stem)
        self.assertEqual(linked, set(topics) - {'optical-computation', 'optical-research'}, 'every reference is linked from a Skill')

    def test_guides_name_only_existing_tools_and_arguments(self):
        texts = {topic: mcp.guide(topic) for topic in mcp.guides()}
        for topic, text in texts.items():
            for token in re.findall(r'`([a-z]+(?:_[a-z]+)+)\(?', text):
                self.assertIn(token, NAMES | ARGUMENTS | PROGRAM, f'{topic} mentions {token}')
        for name in NAMES - {'read_guide'}:
            self.assertTrue(any('`' + name + '`' in text or '`' + name + '(' in text for text in texts.values()),
                            name + ' is explained in a guide')
        for token in re.findall(r'\b[a-z]+(?:_[a-z]+)+\b', mcp.INSTRUCTIONS):
            self.assertIn(token, NAMES, token)

    def test_resources_list_and_return_the_same_guides(self):
        requests = [{'jsonrpc': '2.0', 'id': 1, 'method': 'resources/list'},
                    {'jsonrpc': '2.0', 'id': 2, 'method': 'resources/read', 'params': {'uri': 'optics://guides/film'}},
                    {'jsonrpc': '2.0', 'id': 3, 'method': 'resources/read', 'params': {'uri': 'optics://guides/../secret'}}]
        output = io.StringIO()
        mcp.serve(io.StringIO('\n'.join(map(json.dumps, requests))), output)
        listed, film, outside = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual([r['uri'] for r in listed['result']['resources']], ['optics://guides/' + t for t in mcp.guides()])
        self.assertEqual(film['result']['contents'][0]['text'], mcp.guide('film'))
        self.assertIn('error', outside)

    def test_packaged_skills_match_the_source(self):
        for copy in ('connect/agentic-research-os/skills', 'connect/agentic-research-os/lib/optics_photonics/resources/skills'):
            for file in (ROOT / 'skills').rglob('*.md'):
                self.assertEqual((ROOT / copy / file.relative_to(ROOT / 'skills')).read_bytes(), file.read_bytes(), (copy, file.name))


class ArgumentCase(unittest.TestCase):
    def message(self, name, arguments):
        result = call(name, arguments)
        self.assertTrue(result['isError'], (name, arguments))
        return result['content'][0]['text']

    def test_mistaken_calls_say_what_to_send(self):
        self.assertEqual(self.message('software_search', {'q': 'film'}),
                         'software_search has no argument q; it takes: query, domain, license_group, offset, limit, language')
        self.assertEqual(self.message('software_details', {}), 'software_details needs: tool')
        self.assertIn('domain must be one of: ray, wave, em', self.message('software_search', {'domain': 'thin-film'}))
        self.assertEqual(self.message('run_status', {'run_id': 'r', 'wait': 40}), 'wait must be a number from 0 to 25')
        self.assertEqual(self.message('result_files', {'run_id': 'r', 'limit': 0}), 'limit must be an integer from 1 to 500')
        self.assertEqual(self.message('submit_calculation', {'tool': 'tmm', 'timeout': 0}), 'timeout must be a number above 0')
        self.assertEqual(self.message('bind_environment', {'tool': 'tmm', 'threads': 1.5}), 'threads must be an integer of at least 1')
        self.assertEqual(self.message('submit_workflow', {'steps': {'id': 'a'}}), 'steps must be a list')
        self.assertEqual(self.message('submit_workflow', {'steps': []}), 'steps must have 1 to any number of items')
        self.assertEqual(self.message('compute_resources', {'pools': {'gpu': 'two'}}), 'pools.gpu must be an integer of at least 1')
        self.assertEqual(self.message('read_array', {'run_id': 'r', 'file': 'a.npy', 'index': [[0, 'x']]}), 'index[0] has an unsupported form')
        self.assertEqual(self.message('environments', {'refresh': 'yes'}), 'refresh must be true or false')
        self.assertIn('Unknown tool: status. Tools: read_guide, software_search', self.message('status', {}))
        self.assertIn('Unknown software ID: tmmm. Similar: tmm', self.message('software_details', {'tool': 'tmmm'}))

    def test_numbers_and_booleans_sent_as_text_are_accepted(self):
        found = call('software_search', {'query': 'thin film', 'limit': '2', 'offset': '1'})
        self.assertFalse(found['isError'])
        self.assertEqual(len(found['structuredContent']['items']), 2)
        self.assertEqual(mcp.arguments('run_status', {'run_id': 'r', 'wait': '2.5', 'include_results': 'False', 'limit': 3.0},
                                       next(spec for name, _, spec in mcp.TOOLS if name == 'run_status')),
                         {'run_id': 'r', 'wait': 2.5, 'include_results': False, 'limit': 3})
        self.assertEqual(mcp.conform([None, 3, ['1', None]], next(spec for name, _, spec in mcp.TOOLS if name == 'read_array')
                                     ['properties']['index'], 'index'), [None, 3, [1, None]])


if __name__ == '__main__':
    unittest.main()
