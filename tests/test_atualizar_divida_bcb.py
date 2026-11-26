"""Testes offline para impedir publicação automática indevida."""
import importlib.util
import json
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('auto_bcb', ROOT / 'scripts/atualizar_divida_bcb.py')
bcb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bcb)

class AutomaticDebtTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT/'data/divida_pib_bcb.json').read_text(encoding='utf8'))
        self.old = self.payload['observacoes']
        self.months = {(r['ano'], r['mes']): str(r['dbgg_pct_pib']) for r in self.old}

    def test_regular_revision_and_monthly_progression(self):
        from decimal import Decimal
        months = {k:Decimal(v) for k,v in self.months.items()}
        months[(2026, 9)] = Decimal('82.95')
        rows = bcb.transform(months, self.old, date(2026,11,26))
        self.assertEqual(rows[-1]['mes'],9)
        self.assertEqual(rows[-1]['estado'],'parcial')
        self.assertEqual(len(rows),16)

    def test_failure_rejects_outlier_and_missing_year(self):
        from decimal import Decimal
        months = {k:Decimal(v) for k,v in self.months.items()}
        months[(2013,12)] = Decimal('100')
        with self.assertRaisesRegex(ValueError,'Revisão excepcional'):
            bcb.transform(months, self.old, date(2026,11,26))
        del months[(2013,12)]
        with self.assertRaisesRegex(ValueError,'não contém o ano'):
            bcb.transform(months, self.old, date(2026,11,26))

    def test_preserves_state_company_data_in_js(self):
        js = (ROOT/'estatais-divida-data.js').read_text(encoding='utf8')
        values = bcb.render(self.old, self.payload, js, date(2026,11,26))
        self.assertEqual(js[js.index('window.ESTATAIS_DADOS='):], values['js'].decode('utf8')[values['js'].decode('utf8').index('window.ESTATAIS_DADOS='):])
        self.assertTrue(values['csv'].startswith(b'ano;mes;'))

    def test_fetch_rejects_non_api_response(self):
        with self.assertRaisesRegex(ValueError, 'não é lista'):
            bcb.fetch_values(date(2026,11,26), fetch=lambda _: {'erro':'fora do ar'})

if __name__ == '__main__':
    unittest.main()
