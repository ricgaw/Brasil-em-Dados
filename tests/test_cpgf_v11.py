import csv,io,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from importar_cpgf import parse,read_existing,write_aggregates,amount_to_cents
class CPGFTests(unittest.TestCase):
 def make_csv(self,folder,year='2025',month='01'):
  p=Path(folder)/'official.csv'
  p.write_text('CÓDIGO ÓRGÃO SUPERIOR;NOME ÓRGÃO SUPERIOR;ANO EXTRATO;MÊS EXTRATO;CPF PORTADOR;VALOR TRANSAÇÃO\n20000;Presidência da República;'+year+';'+month+';00011122233;1.234,56\n20000;Presidência da República;'+year+';'+month+';11122233344;100,00\n26000;Ministério da Educação;'+year+';'+month+';22233344455;20,50\n',encoding='utf-8')
  return p
 def test_money(self):
  self.assertEqual(amount_to_cents('1.234,56'),123456)
  self.assertEqual(amount_to_cents('-50,01'),-5001)
  with self.assertRaises(ValueError):amount_to_cents('abc')
 def test_aggregation_privacy_and_idempotence(self):
  with tempfile.TemporaryDirectory() as d:
   source=self.make_csv(d);items=parse(source,'202501')
   self.assertEqual(len(items),2);self.assertEqual(sum(x['valor_centavos'] for x in items),135506)
   target=Path(d)/'out.csv';js=Path(d)/'out.js'
   self.assertTrue(write_aggregates(target,js,[],items));self.assertFalse(write_aggregates(target,js,read_existing(target),items))
   self.assertNotIn('00011122233',target.read_text(encoding='utf-8-sig'))
   self.assertNotIn('11122233344',js.read_text(encoding='utf-8'))
   self.assertIn('window.CPGF_RESUMO=',js.read_text(encoding='utf-8'))
 def test_period_mismatch_blocks(self):
  with tempfile.TemporaryDirectory() as d:
   source=self.make_csv(d)
   with self.assertRaises(ValueError):parse(source,'202502')
 def test_zip_supported(self):
  with tempfile.TemporaryDirectory() as d:
   src=self.make_csv(d);z=Path(d)/'official.zip'
   with zipfile.ZipFile(z,'w') as f:f.write(src,arcname='202501_CPGF.csv')
   self.assertEqual(sum(x['transacoes'] for x in parse(z,'202501')),3)
 def test_layout_sources_and_blank_state(self):
  self.assertNotIn('id="cartoes"',(ROOT/'index.html').read_text(encoding='utf-8'))
  self.assertNotIn('cpgf-data.js _public/',(ROOT/'.github/workflows/publicar.yml').read_text(encoding='utf-8'))
  self.assertNotIn('data/cpgf_resumo.csv _public/data/',(ROOT/'.github/workflows/publicar.yml').read_text(encoding='utf-8'))
  self.assertTrue(all('cpf' not in r and 'portador' not in r for r in read_existing(ROOT/'data/cpgf_resumo.csv')))
 def test_ipca_15_years(self):
  j=json.loads((ROOT/'data/indicadores_sociais.json').read_text(encoding='utf-8'))
  ipca=[x for x in j['series'] if x['indicador']=='ipca']
  self.assertEqual([x['ano'] for x in ipca],list(range(2011,2026)))
  self.assertEqual([x['valor'] for x in ipca if x['ano']==2015],[10.67])
  self.assertEqual([x['valor'] for x in ipca if x['ano']==2025],[4.26])
if __name__=='__main__':unittest.main()
