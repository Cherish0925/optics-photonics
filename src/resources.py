"""Build the self-contained source index and data-export controls."""
import html,json
from urllib.parse import urlsplit
E=html.escape

def collect_resources(entries):
    result={}
    for entry in entries:
        sources=list(entry['sources'])
        for key in ('mcp','skill'):
            value=entry[key]
            if value.get('url'):
                sources.append({'label':value['text'],'url':value['url'],'kind':key})
        for source in sources:
            url=source['url'];label=source['label']
            if source.get('kind'):kind='agent'
            elif any(x in (url+' '+label).lower() for x in ('license','licence','copying','许可','cc0')):kind='license'
            elif any(x in (url+' '+label).lower() for x in ('mcp','skill','agenttools','plugin-marketplace')):kind='agent'
            elif 'github.com' in url:kind='code'
            else:kind='docs'
            if url not in result:
                result[url]={'url':url,'label':label,'kind':kind,'software_ids':[],'software_names':[]}
            r=result[url]
            if kind=='agent':r['kind']=kind
            if entry['id'] not in r['software_ids']:
                r['software_ids'].append(entry['id']);r['software_names'].append(entry['name'])
    return list(result.values())

def render_resources(entries,lang):
    en=lang=='en';R=collect_resources(entries)
    labels={'all':'All resources' if en else '全部资料','docs':'Websites & documentation' if en else '官网与文档','code':'Code repositories' if en else '代码仓库','license':'License sources' if en else '许可原文','agent':'MCP & Skills'}
    rows=[]
    for r in R:
        tools=' · '.join(f'<a href="#tool-{i}" data-jump="{i}">{E(n)}</a>' for i,n in zip(r['software_ids'],r['software_names']))
        shown=urlsplit(r['url']).netloc+urlsplit(r['url']).path
        rows.append(f'<tr data-resource-kind="{r["kind"]}"><td><a href="{E(r["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{E(r["label"])} ↗</a><small>{E(shown)}</small></td><td>{labels[r["kind"]]}</td><td>{tools}</td></tr>')
    title='Resources for people and agents' if en else '资料、网站与 Agent 数据入口'
    intro=('A searchable index of every linked website, manual, repository, license and agent integration. The HTML embeds the complete catalogue and this index; source pages open at their original publishers.' if en else '将官网、文档、代码、许可与 Agent 接入资料集中索引，关联到具体软件。HTML 内嵌完整目录和资源索引；原始页面直接在发布方网站打开。')
    paragraph=('Use JSON for integration, Markdown for reading, and the original source for version-specific details. Website content is not mirrored into the atlas.' if en else '集成时读取 JSON，学习时阅读 Markdown，核对版本细节时打开原始资料。这里保留结构化说明与资料索引，不复制整站内容。')
    block=f'''<section class="section" id="resources"><div class="section-head"><div><div class="section-kicker">07 / DOCUMENTATION & MACHINE ACCESS</div><h2>{title}</h2><p class="section-intro">{intro}</p></div><span class="section-no">07</span></div>
<div class="resource-actions"><button class="small-button" id="export-json">{'Download catalogue + sources JSON' if en else '导出完整目录与资料 JSON'}</button><a class="small-button" href="https://github.com/Cherish0925/optics-photonics/blob/main/llms.txt" target="_blank" rel="noopener noreferrer">llms.txt ↗</a><a class="small-button" href="https://github.com/Cherish0925/optics-photonics/blob/main/docs/catalogue.{lang}.md" target="_blank" rel="noopener noreferrer">{'Readable Markdown' if en else '完整 Markdown'} ↗</a><a class="small-button" href="https://github.com/Cherish0925/optics-photonics/blob/main/data/schema.json" target="_blank" rel="noopener noreferrer">JSON Schema ↗</a></div>
<div class="resource-filter"><input id="resource-search" type="search" aria-label="{'Search resources' if en else '检索资料'}" placeholder="{'Search documentation, websites or software…' if en else '检索文档、网站、软件名称…'}"><select id="resource-kind" aria-label="{'Resource type' if en else '资料类型'}">{''.join(f'<option value="{k}">{v}</option>' for k,v in labels.items())}</select><span><b id="resource-count">{len(R)}</b> {'links' if en else '个入口'}</span></div>
<div class="table-wrap resource-table"><table><thead><tr><th>{'Source & URL' if en else '资料与网址'}</th><th>{'Type' if en else '类型'}</th><th>{'Related software' if en else '对应软件'}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><p class="note">{paragraph}</p>
<details class="agent-recipe"><summary>{'Agent quick start: select tools, follow primary sources, execute through native APIs' if en else 'Agent 使用方式：检索工具、读取原始文档、通过原生 API 执行'}</summary><p>{'The static files need no server API or account. Read stable IDs and the review date; retrieve the linked documentation before choosing installation or solver parameters.' if en else '静态数据不需要额外 API 或账号。读取稳定编号和核查日期，安装与设置求解参数前继续读取对应原始文档。'}</p><pre><code>import json, urllib.request
url = "https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/catalogue.en.json"
tools = json.load(urllib.request.urlopen(url))
candidates = [t for t in tools if t["group"] == "open"
              and "periodic" in t["cats"] and t["route"] == "api"]
for t in candidates:
    print(t["id"], t["name"], t["api"], t["sources"])</code></pre></details></section>'''
    js='''
const resourceRows=Array.from(document.querySelectorAll('[data-resource-kind]'));
function filterResources(){const q=document.querySelector('#resource-search').value.trim().toLowerCase(),k=document.querySelector('#resource-kind').value;let n=0;for(const row of resourceRows){row.hidden=!((k==='all'||row.dataset.resourceKind===k)&&(!q||row.textContent.toLowerCase().includes(q)));if(!row.hidden)n++}document.querySelector('#resource-count').textContent=n}
document.querySelector('#resource-search').addEventListener('input',filterResources);document.querySelector('#resource-kind').addEventListener('change',filterResources);
document.querySelector('#export-json').onclick=()=>{const payload={schema_version:'1.0',reviewed:'2026-10-20',locale:document.documentElement.lang,entries:JSON.parse(document.querySelector('#catalogue-data').textContent),resources:JSON.parse(document.querySelector('#resource-data').textContent)};const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='optics-photonics.'+payload.locale+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};
'''
    css='''.resource-actions{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}.resource-filter{display:flex;gap:10px;align-items:center;margin:14px 0}.resource-filter input{max-width:660px;flex:1;padding-left:13px}.resource-filter>span{font-size:12px;white-space:nowrap}.resource-table{max-height:520px}.resource-table table{min-width:680px}.resource-table thead{position:sticky;top:0;z-index:1;background:#eef4ee}.resource-table td:first-child{width:51%;max-width:520px}.resource-table td small{display:block;color:var(--muted);font-size:10px;overflow-wrap:anywhere;line-height:1.6;margin-top:4px}.resource-table tr[hidden]{display:none}.agent-recipe{background:#eaf2ed;border:1px solid var(--line);padding:18px 21px;border-radius:7px;margin-top:20px}.agent-recipe summary{cursor:pointer;font-weight:600}.agent-recipe p{font-size:12px}.agent-recipe pre{overflow:auto;font-size:11px}@media(max-width:600px){.resource-filter{flex-wrap:wrap}.resource-filter input{flex-basis:100%}.resource-actions a,.resource-actions button{font-size:10px}}@media print{.resource-table{max-height:none}.resource-filter,.resource-actions{display:none}.resource-table table{min-width:0}}'''
    return block,js,css,R
