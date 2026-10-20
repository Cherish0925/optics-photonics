"""Check the shared bilingual contract and self-contained release artifacts."""
import json,re,unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]

class Text(HTMLParser):
    def __init__(self):super().__init__();self.text=[];self.skip=False;self.remote=[]
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag in ('style','script'):self.skip=True
        if tag in ('script','img') and values.get('src','').startswith(('http:','https:')):self.remote.append(values['src'])
    def handle_endtag(self,tag):
        if tag in ('style','script'):self.skip=False
    def handle_data(self,text):
        if not self.skip:self.text.append(text)

class CatalogueTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data={l:json.loads((ROOT/f'data/catalogue.{l}.json').read_text(encoding='utf-8')) for l in ('en','zh')}
    def test_bilingual_identity_and_provenance(self):
        en,zh=self.data['en'],self.data['zh']
        self.assertEqual([x['id'] for x in en],[x['id'] for x in zh])
        self.assertEqual(len({x['id'] for x in en}),len(en))
        for a,b in zip(en,zh):
            for key in ('id','group','cats','route'):self.assertEqual(a[key],b[key],a['id'])
            self.assertEqual([x['url'] for x in a['sources']],[x['url'] for x in b['sources']],a['id'])
            for key in ('mcp','skill'):
                self.assertEqual(a[key]['kind'],b[key]['kind'])
                self.assertEqual(a[key].get('url'),b[key].get('url'))
    def test_contract_and_connector_evidence(self):
        domains={x[0] for x in json.loads((ROOT/'data/domains.en.json').read_text())}
        for lang,entries in self.data.items():
            for d in entries:
                self.assertRegex(d['id'],r'^[a-z][a-z0-9-]*$')
                self.assertIn(d['group'],('paid','open','limited'))
                self.assertIn(d['route'],('api','script','gui'))
                self.assertTrue(set(d['cats'])<=domains)
                for key in ('name','method','summary','api','license','compute','usage','limit'):self.assertTrue(d[key].strip())
                self.assertTrue(d['sources'])
                for s in d['sources']:self.assertTrue(s['url'].startswith('https://'))
                for key in ('mcp','skill'):
                    self.assertIn(d[key]['kind'],('official','community','unverified'))
                    if d[key]['kind']!='unverified':self.assertTrue(d[key]['url'].startswith('https://'))
    def test_english_and_embedded_data(self):
        self.assertFalse(re.search(r'[\u4e00-\u9fff]',json.dumps(self.data['en'],ensure_ascii=False)))
        for lang,file in [('en','index.html'),('zh','index.zh.html')]:
            page=(ROOT/'docs'/file).read_text(encoding='utf-8')
            for id in ('catalogue-data','resource-data','domain-data'):
                raw=re.search(r'<script type="application/json" id="'+id+r'">(.*?)</script>',page,re.S).group(1)
                parsed=json.loads(raw)
                if id=='catalogue-data':self.assertEqual(parsed,self.data[lang])
            p=Text();p.feed(page);self.assertFalse(p.remote)
            if lang=='en':self.assertEqual(set(re.findall(r'[\u4e00-\u9fff]+',''.join(p.text))),{'中文'})
    def test_resource_index_covers_all_urls(self):
        for lang,entries in self.data.items():
            resources=json.loads((ROOT/f'data/resources.{lang}.json').read_text(encoding='utf-8'))
            urls={r['url'] for r in resources}
            required={s['url'] for d in entries for s in d['sources']}
            required|={d[k]['url'] for d in entries for k in ('mcp','skill') if 'url' in d[k]}
            self.assertEqual(urls,required)
            self.assertEqual(len(urls),len(resources))
if __name__=='__main__':unittest.main()
