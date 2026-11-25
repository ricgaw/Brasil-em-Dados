import csv,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class NovosPaineis(unittest.TestCase):
 def test_indicadores(self):
  d=json.loads((ROOT/'data/indicadores_sociais.json').read_text(encoding='utf8'))['series']
  work=[x for x in d if x['indicador']=='desocupacao'];infl=[x for x in d if x['indicador']=='ipca']
  self.assertEqual([r['ano'] for r in work],list(range(2012,2026)))
  self.assertEqual([r['ano'] for r in infl],list(range(2011,2026)))
  self.assertEqual(next(r['valor'] for r in work if r['ano']==2025),5.6)
  self.assertEqual(next(r['valor'] for r in infl if r['ano']==2024),4.83)
  self.assertEqual(len(d),len({(r['indicador'],r['ano']) for r in d}))
  self.assertTrue(all(r['url'].startswith('https://') for r in d))
 def test_fiscalizacao_e_publicacao(self):
  with (ROOT/'data/frentes_fiscalizacao.csv').open(encoding='utf-8-sig',newline='') as f:items=list(csv.DictReader(f,delimiter=';'))
  self.assertEqual(len(items),7)
  self.assertTrue(all(r['situacao']=='Aguardando série consolidada' for r in items))
  html=(ROOT/'index.html').read_text(encoding='utf8')
  self.assertIn('id="indicadores"',html);self.assertIn('id="fiscalizacao"',html)
  wf=(ROOT/'.github/workflows/publicar.yml').read_text(encoding='utf8')
  for path in ('indicadores.js','frentes.js','novos-paineis.js','data/indicadores_sociais.csv','data/frentes_fiscalizacao.csv'):self.assertIn(path,wf)
if __name__=='__main__':unittest.main()
