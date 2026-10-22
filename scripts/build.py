#!/usr/bin/env python3
"""Generate the bilingual catalogue and machine-readable resource views (stdlib)."""
from pathlib import Path
import collections,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from resources import collect_resources
REVIEWED='2026-10-20'
RAW='https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/'

def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def markdown(entries,domains,lang):
    en=lang=='en';names={d[0]:d[1] for d in domains}
    groups={'paid':'Commercial / paid' if en else '商业付费','open':'Free & open source' if en else '免费与开源','limited':'Free / restricted' if en else '免费或授权受限'}
    lines=['# Optics · Photonics — '+('software catalogue' if en else '软件目录'),'',f'{"Reviewed" if en else "核查日期"}: {REVIEWED} | {len(entries)} '+('tools and product families' if en else '个工具与产品族'),'',('Original descriptions and code: MIT. Linked products retain their own licenses.' if en else '原创目录说明与代码采用 MIT；被收录软件遵循各自许可。'),'',('Select by physical method, licensing and native interface. Primary sources accompany each entry.' if en else '按物理方法、许可和原生接口选择工具；原始资料随条目列出。'),'']
    fields=[('method','Physical method','物理方法'),('summary','Purpose','用途'),('api','Programmable interface','编程入口'),('compute','Compute','计算环境'),('license','License','许可'),('usage','Application basis','应用依据'),('limit','Limitations','适用边界')]
    for group in ('paid','open','limited'):
        lines.extend(['## '+groups[group],''])
        for d in [x for x in entries if x['group']==group]:
            lines.extend(['### '+d['name'],'',f'ID: `{d["id"]}` | '+', '.join(names[c] for c in d['cats']),''])
            for key,eng,zh in fields:lines.append(f'- **{eng if en else zh}:** {d[key]}')
            for key in ('mcp','skill'):
                value=d[key];description=value['text']
                if 'url' in value:description=f'[{description}]({value["url"]})'
                lines.append(f'- **{key.upper() if key=="mcp" else "Agent Skill"} ({value["kind"]}):** {description}')
            lines.extend(['',('Sources:' if en else '原始资料：')])
            lines.extend(f'- [{s["label"]}]({s["url"]})' for s in d['sources'])
            lines.append('')
    return '\n'.join(lines)+'\n'

def main():
    sets={}
    for lang in ('zh','en'):
        entries=json.loads((ROOT/f'data/catalogue.{lang}.json').read_text(encoding='utf-8'))
        domains=json.loads((ROOT/f'data/domains.{lang}.json').read_text(encoding='utf-8'))
        resources=collect_resources(entries);sets[lang]=entries
        write_json(ROOT/f'data/resources.{lang}.json',resources)
        (ROOT/f'docs/catalogue.{lang}.md').write_text(markdown(entries,domains,lang),encoding='utf-8')
        subprocess.run([sys.executable,str(ROOT/'src/render.py'),lang],check=True)
    counts=dict(collections.Counter(x['group'] for x in sets['en']))
    source_count=len({s['url'] for d in sets['en'] for s in d['sources']})
    write_json(ROOT/'data/manifest.json',{'schema_version':'1.0','reviewed':REVIEWED,'project':'https://github.com/Cherish0925/optics-photonics','description_license':'MIT','languages':['en','zh'],'entries':len(sets['en']),'domains':14,'groups':counts,'primary_source_urls':source_count,'resource_urls_including_connectors':len(collect_resources(sets['en'])),'catalogues':{lang:RAW+f'data/catalogue.{lang}.json' for lang in ('en','zh')}})
    llms='''# Optics · Photonics

> Bilingual catalogue of optical and photonic software: physical models, licenses, programmable interfaces, sources, MCP and agent Skills.

Reviewed: 2026-10-20. Schema version: 1.0. 96 tools / product families in 14 task domains.

## Foundations

- [Field · Matter · Interaction](https://cherish0925.github.io/optics-photonics/foundations.html): unified physical framework across classical and quantum optics.
- [场 · 物质 · 相互作用](https://cherish0925.github.io/optics-photonics/foundations.zh.html): 中文统一物理基础。
- [Foundation Markdown](https://github.com/Cherish0925/optics-photonics/blob/main/foundations/README.md): maintainable English source.

## Read

- [Complete English catalogue](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/llms-full.txt): all entries, interfaces, limits and sources.
- [中文完整目录](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/docs/catalogue.zh.md): Chinese equivalent.
- [English interactive catalogue](https://cherish0925.github.io/optics-photonics/): models, workflows, examples and resource search.
- [中文交互目录](https://cherish0925.github.io/optics-photonics/index.zh.html): full Chinese edition.

## Integrate

- [English JSON](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/catalogue.en.json): complete structured entries.
- [中文 JSON](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/catalogue.zh.json): same IDs and source URLs.
- [Resource index](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/resources.en.json): documentation, code, licenses and connector URLs linked to software IDs.
- [Schema](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/schema.json): fields and classifications.
- [Manifest](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/manifest.json): review date, version, counts and endpoints.
- [Contributing](https://github.com/Cherish0925/optics-photonics/blob/main/CONTRIBUTING.md): source and update conventions.

## Interpretation

Start from the physical task and representation, then filter by licensing, compute and native interfaces. Follow primary sources for current installation and API details. Each entry records the scope of MCP and Skills, their provenance status, and the software license. Execute through the linked native interfaces in the required environment.
'''
    (ROOT/'llms.txt').write_text(llms,encoding='utf-8')
    (ROOT/'llms-full.txt').write_text((ROOT/'docs/catalogue.en.md').read_text(encoding='utf-8'),encoding='utf-8')
    for filename in ('llms.txt','llms-full.txt'):
        (ROOT/'docs'/filename).write_text((ROOT/filename).read_text(encoding='utf-8'),encoding='utf-8')
    print(f'Built two HTML editions, two Markdown catalogues, resource indexes and agent entry points: {len(sets["en"])} entries.')

if __name__=='__main__':main()
