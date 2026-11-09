"""One catalogue for the website, command line, plugins and MCP."""
from functools import lru_cache
import json
import re
import unicodedata
from pathlib import Path


def resources():
    installed = Path(__file__).parent / 'resources'
    return installed if installed.is_dir() else Path(__file__).resolve().parents[2]


@lru_cache(maxsize=2)
def catalogue(language='en'):
    if language not in {'en', 'zh'}:
        raise ValueError('Use en or zh for language')
    return json.loads((resources() / 'data' / f'catalogue.{language}.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def connections():
    return json.loads((resources() / 'data' / 'connections.json').read_text(encoding='utf-8'))


def software(tool, language='en'):
    item = next((x for x in catalogue(language) if x['id'] == tool), None)
    if item is None:
        raise ValueError('Unknown software ID: ' + str(tool))
    return {**item, 'connection': connections()[tool]}


def normalized(value):
    return re.sub(r'[\W_]+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()


@lru_cache(maxsize=1)
def search_index():
    index = {}
    fields = ('id','name','method','summary','api','usage','compute','license')
    for language in ('en','zh'):
        domains = {row[0]: ' '.join(row[1:]) for row in json.loads((resources()/'data'/f'domains.{language}.json').read_text(encoding='utf-8'))}
        for item in catalogue(language):
            text = ' '.join(str(item[key]) for key in fields)
            text += ' ' + ' '.join(domains[key] for key in item['cats'])
            index[item['id']] = index.get(item['id'], '') + ' ' + normalized(text)
    return index


def search(query='', domain=None, license_group=None, offset=0, limit=20, language='en'):
    if not isinstance(limit, int) or not 1 <= limit <= 100 or not isinstance(offset, int) or offset < 0:
        raise ValueError('Use offset >= 0 and limit from 1 to 100')
    terms = normalized(query).split()
    matches = []
    for item in catalogue(language):
        if domain and domain not in item['cats'] or license_group and item['group'] != license_group:
            continue
        text = search_index()[item['id']]
        if not all(term in text for term in terms):
            continue
        connection = connections()[item['id']]
        matches.append({k: item[k] for k in ('id', 'name', 'group', 'cats', 'summary')} |
                       {'connection': connection['kind'], 'operations': connection.get('operations', []),
                        'upstream_mcp': item['mcp']['kind']})
    return {'total': len(matches), 'items': matches[offset:offset + limit],
            'next_offset': offset + limit if offset + limit < len(matches) else None}
