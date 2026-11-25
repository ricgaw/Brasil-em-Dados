import csv, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Impostos(unittest.TestCase):
 def test_fontes_e_lacunas(self):
  with (ROOT/'data/arrecadacao_tributaria.csv').open(encoding='utf-8',newline='') as f:r=list(csv.DictReader(f,delimiter=';'))
  self.assertEqual([int(x['ano']) for x in r],list(range(2011,2027)))
  self.assertEqual({int(x['ano']):int(x['valor_reais']) for x in r if x['valor_reais']},{2024:3600000000000,2025:3980000000000})
  self.assertTrue(all(x['fonte'].startswith('https://') for x in r))
 def test_publicacao(self):
  html=(ROOT/'index.html').read_text(encoding='utf-8');js=(ROOT/'impostos.js').read_text(encoding='utf-8');wf=(ROOT/'.github/workflows/publicar.yml').read_text(encoding='utf-8')
  self.assertIn('id="arrecadacao"',html)
  self.assertIn('NÃO É MEDIÇÃO AO VIVO',html)
  self.assertIn("timeZone:'America/Sao_Paulo'",js)
  self.assertIn('impostos.js',wf)
  self.assertIn('data/arrecadacao_tributaria.csv',wf)
if __name__=='__main__':unittest.main()
