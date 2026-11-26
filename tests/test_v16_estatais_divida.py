import json,unittest,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class V16Tests(unittest.TestCase):
 def test_bcb_years(self):
  d=json.loads((ROOT/'data/divida_pib_bcb.json').read_text(encoding='utf-8'))['observacoes']
  self.assertEqual([x['ano'] for x in d if x['estado']=='anual'][:15],list(range(2011,2026)))
  self.assertLessEqual(len([x for x in d if x['estado']=='parcial']),1)
  self.assertEqual([x['ano'] for x in d],list(range(2011,d[-1]['ano']+1)))
  self.assertTrue(all(x['codigo_sgs']==13762 and 0<x['dbgg_pct_pib']<200 for x in d))
 def test_statais_sources_and_missing(self):
  d=json.loads((ROOT/'data/estatais_resultados.json').read_text(encoding='utf-8'))
  self.assertEqual(len(d['empresas']),4)
  self.assertEqual(len({(x['empresa'],x['ano']) for x in d['registros']}),len(d['registros']))
  self.assertTrue(all(x['fonte'].startswith('https://') for x in d['registros']))
  self.assertTrue(all(x['endividamento_bi'] is None or x['moeda_endividamento'] in ('BRL','USD') for x in d['registros']))
  self.assertTrue(all(x['resultado_bi_brl'] is not None for x in d['registros']))
 def test_ui_removed_and_replaced(self):
  h=(ROOT/'index.html').read_text(encoding='utf-8')
  for x in ('divida-publica','estatais','debt-chart','state-cards','estatais-divida-data.js'):
   self.assertIn(x,h)
  for x in ('id="fiscalizacao"','id="cartoes"','href="#cartoes"','href="#fiscalizacao"'):
   self.assertNotIn(x,h)
 def test_publish_assets(self):
  w=(ROOT/'.github/workflows/publicar.yml').read_text(encoding='utf-8')
  for x in ('estatais-divida-app.js','estatais-divida-data.js','divida_pib_bcb.csv','estatais_resultados.csv'):
   self.assertIn(x,w)
if __name__=='__main__':unittest.main()
