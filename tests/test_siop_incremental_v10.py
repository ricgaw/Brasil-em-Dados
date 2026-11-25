"""Testes offline: isolamento anual, cache de aprovado, bloqueio e fluxos GitHub."""
import csv
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import siop_incremental as inc
import consolidar_siop as con


def fixtures(where, year, key=None):
    key=key or str(year)
    where.mkdir(parents=True,exist_ok=True)
    csv_path=where/f'{key}.csv'
    audit_path=where/f'{key}.json'
    with csv_path.open('w',encoding='utf-8',newline='') as out:
        w=csv.DictWriter(out,fieldnames=inc.FIELDS,delimiter=';',lineterminator='\n')
        w.writeheader()
        w.writerow({'ano':str(year),'funcao':'Saúde','dotacao_inicial_reais':'100',
                    'dotacao_atualizada_reais':'110','data_referencia':f'{year}-12-31',
                    'fonte':f'https://orcamento.dados.gov.br/dados/loa{year}.csv.gz'})
    payload={'status':'completa','exercicios':[{'ano':year,'status':'validado',
             'sha256':'a'*64,'funcoes_com_dotacao_inicial_positiva':1}]}
    audit_path.write_text(json.dumps(payload),encoding='utf-8')
    return csv_path,audit_path

class IncrementalTests(unittest.TestCase):
    def test_skip_approved_without_contacting_network(self):
        with tempfile.TemporaryDirectory() as d:
            store=Path(d)
            fixtures(store,2011)
            with patch.object(inc,'STORE',store),patch.object(inc,'coletar') as net:
                self.assertEqual(inc.run(2011,today=date(2026,11,25)),'aprovado')
                net.assert_not_called()
    def test_one_year_failure_does_not_write_approved_files(self):
        with tempfile.TemporaryDirectory() as d:
            store=Path(d)/'approved'
            with patch.object(inc,'STORE',store),patch.object(inc,'coletar',side_effect=RuntimeError('Connection refused')):
                with self.assertRaisesRegex(RuntimeError,'Connection refused'):
                    inc.run(2022,today=date(2026,11,25))
                self.assertFalse(list(store.glob('*.csv')))
    def test_collect_single_year_and_current_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            temp=Path(d)
            store=temp/'approved'
            reports=temp/'reports'
            reports.mkdir()
            def fake_collector(argv):
                year=int(argv[argv.index('--anos')+1]);fixtures(reports,year,f'siop_{year}')
            with patch.object(inc,'STORE',store),patch.object(inc,'ROOT',temp),patch.object(inc,'coletar',side_effect=fake_collector):
                self.assertEqual(inc.run(2018,today=date(2026,11,25)),'novo')
                self.assertTrue((store/'2018.csv').exists())
                self.assertEqual(inc.run(2026,today=date(2026,11,25)),'novo')
                self.assertTrue((store/'2026-202611.json').exists())
                self.assertEqual(inc.run(2026,today=date(2026,11,25)),'aprovado')
    def test_partial_pair_and_corrupt_audit_block(self):
        with tempfile.TemporaryDirectory() as d:
            store=Path(d)
            csv_path,audit_path=fixtures(store,2014)
            audit_path.unlink()
            with patch.object(inc,'STORE',store):
                with self.assertRaisesRegex(ValueError,'somente um'):
                    inc.run(2014,today=date(2026,11,25))
            _,audit_path=fixtures(store,2014)
            payload=json.loads(audit_path.read_text());payload['exercicios'][0]['sha256']='invalid'
            audit_path.write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError,'SHA256'):
                inc.validate_pair(2014,csv_path,audit_path)
    def test_consolidation_uses_each_approved_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            store=Path(d)
            fixtures(store,2011)
            fixtures(store,2026,'2026-202611')
            seen=[]
            with patch.object(con,'STORE',store),patch.object(con,'run',side_effect=lambda x:seen.append(x.arquivo)):
                self.assertEqual(con.consolidate(),2)
            self.assertEqual([Path(x).name for x in seen],['2011.csv','2026-202611.csv'])
    def test_end_to_end_consolidation_in_isolated_copy(self):
        import shutil
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            copied=Path(d)/'repo'
            shutil.copytree(ROOT,copied,ignore=shutil.ignore_patterns('.git','reports','__pycache__'))
            fixtures(copied/'data'/'siop_anos',2011)
            subprocess.run([sys.executable,'scripts/consolidar_siop.py'],cwd=copied,
                           check=True,capture_output=True,text=True)
            with (copied/'data'/'alteracoes_orcamentarias.csv').open(encoding='utf-8-sig',newline='') as f:
                records=list(csv.DictReader(f,delimiter=';'))
            self.assertTrue(any(x['ano']=='2011' and x['area']=='Saúde' for x in records))
            subprocess.run([sys.executable,'scripts/validate.py'],cwd=copied,
                           check=True,capture_output=True,text=True)
            subprocess.run([sys.executable,'scripts/validar_v5.py'],cwd=copied,
                           check=True,capture_output=True,text=True)
    def test_workflows_are_independent_and_reviewable(self):
        wf=(ROOT/'.github/workflows/coletar-siop-loa.yml').read_text(encoding='utf-8')
        merged=(ROOT/'.github/workflows/consolidar-siop.yml').read_text(encoding='utf-8')
        self.assertIn('fail-fast: false',wf)
        self.assertIn('max-parallel: 1',wf)
        self.assertIn('matrix.ano',wf)
        self.assertIn('pull-requests: write',wf)
        self.assertIn('data/siop_anos/**',merged)
        self.assertIn('peter-evans/create-pull-request@v7',merged)
        self.assertIn('peter-evans/create-pull-request@v7',wf)
        self.assertIn('automacao/siop-ano-',wf)
        self.assertNotIn('data/alteracoes_orcamentarias.csv',wf)

if __name__=='__main__':unittest.main()
