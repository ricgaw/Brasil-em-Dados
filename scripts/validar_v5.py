"""Valida extensão do catálogo de funções, publicações e esquema de importação."""
import csv,json,subprocess,sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data'/'atlas.json').read_text(encoding='utf8'))
areas={r['area'] for r in d['budget']}
assert len(areas)==28
assert len({(r['area'],r['year']) for r in d['budget']})==len(d['budget'])
assert all(2020<=r['year']<=2024 for r in d['budget'])
assert not any(r['area']=='Habitação' and r['year']==2023 for r in d['budget'])
assert 'areas-app.js' in (root/'index.html').read_text(encoding='utf8')
assert 'areas-app.js' in (root/'.github/workflows/publicar.yml').read_text(encoding='utf8')
assert (root/'.github/workflows/importar-dotacoes.yml').exists()
from importar_dotacoes import official_url,parse_int
assert official_url('https://orcamento.dados.gov.br/example.csv')
assert not official_url('https://example.com/not-government.csv')
assert not official_url('http://orcamento.dados.gov.br/a.csv')
try:parse_int('12.3','d')
except ValueError:pass
else:raise AssertionError('Valores em milhares/decimais não devem ser aceitos como reais inteiros')
assert all(not r.get('id_escopo','').startswith('funcao-') for r in csv.DictReader((root/'data/alteracoes_orcamentarias.csv').open(encoding='utf-8-sig'),delimiter=';'))
subprocess.check_call(['node','--check',str(root/'areas-app.js')])
print('OK: 28 funções, lacunas transparentes, importação conservadora, monitoramento e publicação preparados.')
