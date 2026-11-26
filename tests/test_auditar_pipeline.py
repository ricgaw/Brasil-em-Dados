"""Testes offline da auditoria; não usam rede nem arquivos reais como fixtures."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from scripts.auditar_pipeline import FIELDS, audit_year, run


class AuditTests(unittest.TestCase):
    def fixture(self, directory, *, source='https://www1.siop.planejamento.gov.br/downloads/rdf/loa2011.csv.gz'):
        where = Path(directory)
        where.mkdir(exist_ok=True, parents=True)
        csv_path = where / '2011.csv'
        with csv_path.open('w', encoding='utf-8', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=FIELDS, delimiter=';', lineterminator='\n')
            writer.writeheader()
            writer.writerow({'ano': '2011', 'funcao': 'Saúde', 'dotacao_inicial_reais': '100',
                             'dotacao_atualizada_reais': '110', 'data_referencia': '2011-12-31',
                             'fonte': source, 'empenhado_reais': '90', 'liquidado_reais': '80',
                             'pago_reais': '75', 'nota': 'Teste sintético'})
        audit = {'status': 'completa', 'exercicios': [{'ano': 2011, 'status': 'validado',
                 'sha256': 'a' * 64, 'url': source, 'linhas': 100,
                 'funcoes_com_dotacao_inicial_positiva': 1,
                 'reservas_contingencia_excluidas_do_painel': {}}]}
        (where / '2011.json').write_text(json.dumps(audit), encoding='utf-8')
        return csv_path

    def test_valid_pair(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            self.assertEqual(audit_year(p)['funcoes'], 1)
            self.assertEqual(run(tmp)['exercicios_ou_snapshots'], 1)

    def test_mismatch_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            content = p.read_text()
            p.write_text(content.replace('loa2011.csv.gz', 'outro2011.csv.gz'))
            with self.assertRaisesRegex(ValueError, 'não coincide'):
                audit_year(p)

    def test_missing_json_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            p.with_suffix('.json').unlink()
            with self.assertRaisesRegex(ValueError, 'ausente'):
                run(tmp)

    def test_no_data_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run(tmp)['exercicios_ou_snapshots'], 0)


if __name__ == '__main__':
    unittest.main()
