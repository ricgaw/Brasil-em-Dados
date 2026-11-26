import csv, importlib.util, json, tempfile, unittest
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/f'scripts/{name}.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
mon=load('monitorar_estatais_v18')
cov=load('cobertura_v18')
ipca=load('atualizar_ipca_bcb_v18')

class V18Tests(unittest.TestCase):
    def test_coverage_rebuild_is_reproducible(self):
        self.assertEqual(len(cov.report()['estatais']),4)
        cov.render()
        before=(ROOT/'cobertura-v18.js').read_bytes()
        cov.render()
        self.assertEqual(before,(ROOT/'cobertura-v18.js').read_bytes())
        self.assertEqual(cov.report()['estatais'][0]['id'],'petrobras')

    def test_documents_allowlist(self):
        html='<a href="sestdadosfinanceiros.zip">Finanças</a><a href="https://evil.example.org/data.xlsx">Outros</a><a href="Anexo.xlsx">Anexo</a>'
        docs=mon.extract(html,mon.PAGES[1]);self.assertEqual(len(docs),2)
        self.assertTrue(all('www.gov.br' in x for x in docs))

    def test_monitor_preserves_catalog_if_source_disappears(self):
        html='<a href="https://www.gov.br/gestao/dados/AnexoI.xlsx">Anexo</a>'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'sources.json'
            self.assertTrue(mon.update(fetch=lambda _:html,path=path))
            self.assertFalse(mon.update(fetch=lambda _:html,path=path))
            original=path.read_bytes()
            with self.assertRaises(ValueError):mon.update(fetch=lambda _:'<div>sem links</div>',path=path)
            self.assertEqual(original,path.read_bytes())

    def test_ipca_requires_twelve_months_and_next_year(self):
        rows=[{'data':f'01/{m:02}/2026','valor':'0.50'} for m in range(1,13)]
        self.assertIsNone(ipca.calculate(rows[:-1]))
        self.assertTrue(ipca.calculate(rows)>0)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'data').mkdir()
            for f in ('indicadores_sociais.json','indicadores_sociais.csv'):
                (root/'data'/f).write_bytes((ROOT/'data'/f).read_bytes())
            self.assertFalse(ipca.update(root,rows,date(2026,12,31)))
            self.assertTrue(ipca.update(root,rows,date(2027,1,15)))
            self.assertFalse(ipca.update(root,rows,date(2027,1,15)))
            loaded=json.loads((root/'data/indicadores_sociais.json').read_text(encoding='utf-8'))
            self.assertEqual(len([r for r in loaded['series'] if r['indicador']=='ipca' and r['ano']==2026]),1)

    def test_new_2025_bb_source(self):
        d=json.loads((ROOT/'data/estatais_resultados.json').read_text(encoding='utf-8'))
        self.assertEqual([r['resultado_bi_brl'] for r in d['registros'] if r['empresa']=='bb' and r['ano']==2025],[20.685])
        with (ROOT/'data/estatais_resultados.csv').open(encoding='utf-8',newline='') as f:
            rows=list(csv.DictReader(f,delimiter=';'))
        self.assertEqual(len(rows),len(d['registros']))

    def test_publication_includes_coverage_scripts(self):
        h=(ROOT/'index.html').read_text(encoding='utf-8')
        wf=(ROOT/'.github/workflows/publicar.yml').read_text(encoding='utf-8')
        for x in ('cobertura-v18-app.js','cobertura-v18.js'):
            self.assertIn(x,h);self.assertIn(x,wf)

if __name__=='__main__':unittest.main()
