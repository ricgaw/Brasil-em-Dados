import sys,unittest,gzip,io,csv,hashlib
from pathlib import Path
from datetime import date
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from coletar_siop_loa import discover,verify_digest,aggregate,normalized_rows,to_cents,official_https,CODES,SPECIAL_CODES

class SIOPTests(unittest.TestCase):
    def test_discover(self):
        sample='''<a href="https://orcamento.dados.gov.br/files/loa2025.csv.gz">CSV</a>
        <a href="https://orcamento.dados.gov.br/files/loa2025.sha256">SHA256</a>'''
        urls=discover(sample,2025)
        self.assertEqual(urls['csv.gz'],'https://orcamento.dados.gov.br/files/loa2025.csv.gz')
        with self.assertRaises(ValueError):discover(sample,2024)
    def test_url(self):
        self.assertFalse(official_https('https://orcamento.dados.gov.br.attacker.org/x'))
        self.assertFalse(official_https('http://orcamento.dados.gov.br/a'))
        self.assertTrue(official_https('https://orcamento.dados.gov.br/a'))
    def test_digest(self):
        b=b'arquivo';h=hashlib.sha256(b).hexdigest()
        self.assertEqual(verify_digest(b,f'{h}  loa2025.csv.gz',2025),h)
        with self.assertRaises(ValueError):verify_digest(b,'0'*64+'  loa2025.csv.gz',2025)
    def test_aggregate_and_rows(self):
        out=io.StringIO();w=csv.writer(out)
        cols=['exercicio','esfera_codigo','funcao_codigo','valor_dotacao_inicial','valor_lei_mais_creditos','valor_empenhado','valor_liquidado','valor_pago']
        w.writerow(cols)
        for code in CODES:
            w.writerow([2025,'10',code,'100.15','150.25','0.00','0.00','0.00'])
            w.writerow([2025,'20',code,'0.00','0.00','90.01','70.01','60.01'])
        gz=gzip.compress(out.getvalue().encode())
        amounts,number=aggregate(gz,2025)
        self.assertEqual(number,56)
        self.assertEqual(amounts['10'],[10015,15025,9001,7001,6001])
        rows=normalized_rows(2025,amounts,'https://gov.br/loa2025.csv.gz',date(2026,11,24))
        self.assertEqual(len(rows),28)
        self.assertEqual(rows[9]['dotacao_inicial_reais'],'100')
        self.assertEqual(rows[9]['dotacao_atualizada_reais'],'150')
        self.assertEqual(rows[9]['data_referencia'],'2025-12-31')
    def test_reserva_contingencia_separada_das_28_funcoes(self):
        self.assertEqual(SPECIAL_CODES['99'],'Reserva de Contingência')
        output=io.StringIO(); writer=csv.writer(output)
        writer.writerow(['exercicio','esfera_codigo','funcao_codigo',*('valor_dotacao_inicial','valor_lei_mais_creditos','valor_empenhado','valor_liquidado','valor_pago')])
        for code in CODES:
            writer.writerow([2025,'10',code,'100.00','110.00','80.00','70.00','60.00'])
        writer.writerow([2025,'10','99','9999.00','8888.00','0.00','0.00','0.00'])
        totals,count=aggregate(gzip.compress(output.getvalue().encode()),2025)
        self.assertEqual(count,29)
        self.assertEqual(totals['99'][0],999900)
        rows=normalized_rows(2025,totals,'https://orcamento.dados.gov.br/loa2025.csv.gz',date(2026,11,25))
        self.assertEqual(len(rows),28)
        self.assertTrue(all(row['funcao']!='Reserva de Contingência' for row in rows))
        output_bad=output.getvalue().replace(',99,9999.00',',98,9999.00')
        with self.assertRaisesRegex(ValueError,'Código de função desconhecido: 98'):
            aggregate(gzip.compress(output_bad.encode()),2025)
    def test_errors(self):
        with self.assertRaises(ValueError):to_cents('1,5')
        with self.assertRaises(ValueError):to_cents('0.001')
        with self.assertRaises(ValueError):aggregate(gzip.compress(b'exercicio,foo\n2025,1\n'),2025)

if __name__=='__main__':unittest.main()

class IntegrationTests(unittest.TestCase):
    def test_import_rebuild_validate_without_modifying_source(self):
        import shutil, tempfile, subprocess, json
        src=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'repo'
            shutil.copytree(src,root,ignore=shutil.ignore_patterns('reports','__pycache__','.git'))
            # Isolar a base fictícia de 2025. O repositório publicado pode
            # conter todas as 28 funções reais desse exercício, e o importador
            # corretamente proíbe substituí-las por valores de teste.
            budget=root/'data'/'alteracoes_orcamentarias.csv'
            with budget.open(encoding='utf-8-sig',newline='') as f:
                existing=csv.DictReader(f,delimiter=';')
                fields=existing.fieldnames
                rows=[row for row in existing if not (
                    row['ano']=='2025' and row['id_escopo'].startswith('funcao-'))]
            with budget.open('w',encoding='utf-8-sig',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fields,delimiter=';',lineterminator='\n')
                writer.writeheader()
                writer.writerows(rows)
            output=root/'coleta_exemplo.csv'
            with output.open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=['ano','funcao','dotacao_inicial_reais',
                    'dotacao_atualizada_reais','data_referencia','fonte','empenhado_reais',
                    'liquidado_reais','pago_reais','nota'],delimiter=';',lineterminator='\n')
                w.writeheader()
                for area in ('Saúde','Educação','Cultura'):
                    w.writerow({'ano':'2025','funcao':area,'dotacao_inicial_reais':'123456',
                        'dotacao_atualizada_reais':'120000','data_referencia':'2025-12-31',
                        'fonte':'https://orcamento.dados.gov.br/dados/loa2025.csv.gz',
                        'nota':'Teste de ponta a ponta: valores fictícios e não destinados ao site real.'})
            subprocess.run([sys.executable,'scripts/importar_dotacoes.py','--arquivo',str(output)],
                cwd=root,check=True,capture_output=True,text=True)
            subprocess.run([sys.executable,'scripts/validate.py'],cwd=root,check=True,capture_output=True,text=True)
            subprocess.run([sys.executable,'scripts/validar_v5.py'],cwd=root,check=True,capture_output=True,text=True)
            output_js=(root/'alteracoes.js').read_text(encoding='utf8')
            self.assertIn('funcao-saúde',output_js)
            self.assertIn('2025',output_js)
