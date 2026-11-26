import unittest,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
class EditorialV15(unittest.TestCase):
 def test_ten_new_policies(self):
  data=json.loads((root/'data/atlas.json').read_text(encoding='utf8'))
  self.assertEqual(len(data['policies']),34)
  for k in ('lai2011','anticorrupcao2013','lgpd2018','licitacoes2021','igualdade2023','mover2024'):
   self.assertIn(k,data['sources'])
  self.assertEqual(len(set((p['term'],p['title']) for p in data['policies'])),34)
 def test_new_panels(self):
  h=(root/'index.html').read_text(encoding='utf8')
  js=(root/'dossies-v15.js').read_text(encoding='utf8')
  for marker in ('mandate-deep-cards','year-coverage-body','source-directory','coverage-term','dossies-v15.js'):
   self.assertIn(marker,h)
  self.assertIn('const byYear=new Map()',js)
  self.assertIn('28',js)
 def test_deploy_includes_js(self):
  w=(root/'.github/workflows/publicar.yml').read_text(encoding='utf8')
  self.assertIn('dossies-v15.js _public/',w)
  self.assertIn('dossies-v15.js; do',w)
