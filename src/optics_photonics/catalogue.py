"""One catalogue for the website, command line, plugins and MCP."""
import difflib
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
        similar = difflib.get_close_matches(str(tool), [x['id'] for x in catalogue(language)], n=3)
        raise ValueError('Unknown software ID: ' + str(tool) + ('. Similar: ' + ', '.join(similar) if similar else '') +
                         '. software_search finds IDs; register_software adds a tool outside the catalogue')
    return {**item, 'connection': connections()[tool]}


def normalized(value):
    return re.sub(r'[\W_]+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()


SUFFIXES = ('ical', 'ation', 'ing', 'ies', 'es', 'al', 'ed', 's', 'e')


def stem(term):
    """A short form shared by related words: bands/band, scattering/scatterer, sphere/spherical."""
    for suffix in SUFFIXES:
        if term.endswith(suffix) and len(term) - len(suffix) >= 4:
            return term[:-len(suffix)]
    return term


def words(text):
    """Normalized words, then each adjacent pair joined, so x-ray is also found as xray."""
    parts = normalized(text).split()
    return ' ' + ' '.join(parts + [a + b for a, b in zip(parts, parts[1:])]) + ' '


def pattern(term):
    """What to look for in indexed text: Chinese anywhere, one or two characters as a whole word, else a word start."""
    if re.search(r'[\u3400-\u9fff]', term):
        return term
    return ' ' + term + ' ' if len(term) < 3 else ' ' + stem(term)


def domain_names(language):
    rows = json.loads((resources() / 'data' / f'domains.{language}.json').read_text(encoding='utf-8'))
    return {row[0]: ' '.join(row[1:]) for row in rows}


@lru_cache(maxsize=1)
def search_index():
    """Per software ID, all searchable text in both languages; the web pages embed it."""
    index = {}
    fields = ('id', 'name', 'method', 'summary', 'api', 'usage', 'compute', 'license')
    for language in ('en', 'zh'):
        domains = domain_names(language)
        for item in catalogue(language):
            text = ' '.join(str(item[key]) for key in fields)
            text += ' ' + ' '.join(domains[key] for key in item['cats'])
            index[item['id']] = index.get(item['id'], '') + ' ' + normalized(text)
    return index


@lru_cache(maxsize=1)
def ranked_index():
    """Per software ID, in both languages: its names, its method and summary, its domains, and the remaining text."""
    index = {}
    for language in ('en', 'zh'):
        domains = domain_names(language)
        for item in catalogue(language):
            texts = (item['id'] + ' ' + item['name'], item['method'] + ' ' + item['summary'],
                     ' '.join(domains[key] for key in item['cats']),
                     ' '.join(str(item[key]) for key in ('api', 'usage', 'compute', 'license')))
            before = index.get(item['id'], ('', '', '', ''))
            index[item['id']] = tuple(a + words(b) for a, b in zip(before, texts))
    return index


def search(query='', domain=None, license_group=None, offset=0, limit=20, language='en'):
    """Rank software by the query words it matches; a word matches the start of a word, in related forms.

    Software matching every word comes first; a match in the name outranks one
    in the method or summary, then the domain, then other text. A query of
    three or more words also returns software one word short, and each such
    item lists the words it lacks in ``missing``.
    """
    if not isinstance(limit, int) or not 1 <= limit <= 100 or not isinstance(offset, int) or offset < 0:
        raise ValueError('Use offset >= 0 and limit from 1 to 100')
    terms = list(dict.fromkeys(normalized(query).split()))
    patterns = [pattern(term) for term in terms]
    index = ranked_index()
    ranked = []
    for position, item in enumerate(catalogue(language)):
        if domain and domain not in item['cats'] or license_group and item['group'] != license_group:
            continue
        weights = [next((weight for weight, text in zip((4, 3, 2, 1), index[item['id']]) if wanted in text), 0) for wanted in patterns]
        ranked.append((sum(map(bool, weights)), sum(weights), position, item, weights))
    best = max((entry[0] for entry in ranked), default=0)
    need = best if len(terms) < 3 else min(best, max(best - 1, (len(terms) + 1) // 2))
    ranked = sorted((entry for entry in ranked if entry[0] >= need and (best or not terms)), key=lambda entry: (-entry[0], -entry[1], entry[2]))
    matches = []
    for count, _, _, item, weights in ranked:
        connection = connections()[item['id']]
        missing = [] if count == len(terms) else [term for term, weight in zip(terms, weights) if not weight]
        matches.append({k: item[k] for k in ('id', 'name', 'group', 'cats', 'summary')} |
                       {'connection': connection['kind'], 'operations': connection.get('operations', []),
                        'upstream_mcp': item['mcp']['kind']} | ({'missing': missing} if missing else {}))
    return {'total': len(matches), 'items': matches[offset:offset + limit],
            'next_offset': offset + limit if offset + limit < len(matches) else None}
