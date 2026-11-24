from pathlib import Path
import json,csv,re,subprocess
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'data'/'atlas.json').read_text(encoding='utf-8'))
assert len(d['terms'])==4
assert [t['period'] for t in d['terms']]==['2011–2014','2015–2018','2019–2022','2023–2026']
assert all(k in d['people'] for t in d['terms'] for k in t['presidents']+t['vice'])
assert len(d['policies'])>=24
assert all(p['source'] in d['sources'] for p in d['policies'])
assert all(p['status']!='Cumprida' for p in d['policies'])
assert all(p.get('author') in ('Dilma Rousseff','Michel Temer') for p in d['policies'] if p['term']=='2015')
assert len(d['budget'])==139
assert set(r['year'] for r in d['budget'])=={2020,2021,2022,2023,2024}
assert all(isinstance(r['liquidado_milhoes'],int) and r['liquidado_milhoes']>0 and r['fonte'] in ('ibge','ibge2020') for r in d['budget'])
assert len(set((r['year'],r['area']) for r in d['budget']))==len(d['budget'])
# Casos editoriais com documentação e estado processual explicitados.
assert len(d['cases']) >= 10
assert len({c['id'] for c in d['cases']}) == len(d['cases'])
assert set(c['term'] for c in d['cases']) == {t['id'] for t in d['terms']}
assert all(sum(c['term']==t['id'] for c in d['cases']) >= 2 for t in d['terms'])
assert all(c['source'].startswith('https://') for c in d['cases'])
assert all(all(isinstance(c.get(k),str) and len(c[k]) > 15 for k in
    ('title','facts','boundary','stage','actor','source_label')) for c in d['cases'])
assert d['cases'] == json.loads((root/'data'/'casos_documentados.json').read_text(encoding='utf-8'))
with (root/'data'/'escandalos_investigacoes.csv').open(encoding='utf-8-sig',newline='') as file:
 assert len(list(csv.DictReader(file,delimiter=';')))==len(d['cases'])
assert 'id="escandalos"' in (root/'index.html').read_text(encoding='utf-8')
assert 'function renderCases()' in (root/'app.js').read_text(encoding='utf-8')
assert d['meta']['cutoff']=='2026-11-24'
assert (root/'data.js').read_text(encoding='utf-8').startswith('window.ATLAS=')
for n in ('index.html','styles.css','app.js','data.js'):
 assert (root/n).is_file(),n
with (root/'data'/'orcamento_2020_2024_ibge.csv').open(encoding='utf-8-sig') as f:
 rows=list(csv.DictReader(f,delimiter=';'))
assert len(rows)==len(d['budget'])
assert len(d['budget'])==139
assert len(set(r['area'] for r in d['budget']))==28
assert any(p['source']=='ir2025' for p in d['policies'])
assert any(p['source']=='auxilio2020' for p in d['policies'])

# Integridade das 28 funções, 5 anos e lacuna oficial não preenchida (Habitação em 2023).
areas=set(r['area'] for r in d['budget'])
assert all(sum(r['area']==area for r in d['budget'])== (4 if area=='Habitação' else 5) for area in areas)
assert not any(r['year']==2023 and r['area']=='Habitação' for r in d['budget'])
spot={(r['area'],r['year']):r['liquidado_milhoes'] for r in d['budget']}
assert spot['Legislativa',2020]==6305
assert spot['Judiciária',2024]==42933
assert spot['Relações exteriores',2023]==3892
assert spot['Desporto e lazer',2024]==268
assert spot['Encargos especiais',2023]==1091740
# O CSV das investigações é parte do site publicado, não só do repositório de código.
public_workflow=(root/'.github/workflows/publicar.yml').read_text(encoding='utf8')
assert 'data/escandalos_investigacoes.csv' in public_workflow and '_public/data/' in public_workflow
assert 'cp data/atlas.json' in public_workflow
assert 'data/orcamento_2020_2024_ibge.csv' in public_workflow
assert 'test -f _public/data/escandalos_investigacoes.csv' in public_workflow

# Testar reproduzibilidade sem alterar arquivos: recompilação deve ser idêntica.
orig=[(root/p).read_bytes() for p in ('data/atlas.json','data.js','data/orcamento_2020_2024_ibge.csv','data/escandalos_investigacoes.csv')]
subprocess.check_call(['python',str(root/'scripts'/'build.py')],cwd=root)
new=[(root/p).read_bytes() for p in ('data/atlas.json','data.js','data/orcamento_2020_2024_ibge.csv','data/escandalos_investigacoes.csv')]
assert orig==new,'Artefatos não reproduzíveis: scripts/build.py deve regenerar mesmos bytes'
print(f"OK: 4 mandatos, {len(d['policies'])} fichas, {len(d['budget'])} registros, 28 áreas, {len(d['cases'])} dossiês, 2020–2024 e arquivos reproduzíveis.")

# Dotação inicial x atualizada: amostras oficiais com mesmo recorte e data.
from build_alteracoes import load as load_alteracoes
changes=load_alteracoes()
assert len(changes)>=2
assert len(set((c['ano'],c['id_escopo'],c['data_referencia']) for c in changes))==len(changes)
assert all(c['delta_reais']==c['dotacao_atualizada_reais']-c['dotacao_inicial_reais'] for c in changes)
assert all(c['fonte'].startswith('https://') and c['nota'] for c in changes)
examples={c['id_escopo']:c for c in changes}
assert examples['36000']['dotacao_inicial_reais']==270348227077
assert examples['36000']['dotacao_atualizada_reais']==269921177227
assert examples['36201']['dotacao_inicial_reais']==9557183503
assert examples['36201']['dotacao_atualizada_reais']==10171909920
assert examples['36000']['delta_reais']<0 and examples['36201']['delta_reais']>0
assert 'id="alteracoes"' in (root/'index.html').read_text(encoding='utf8')
assert 'alteracoes-app.js' in (root/'index.html').read_text(encoding='utf8')
assert 'data/alteracoes_orcamentarias.csv' in public_workflow
assert '_public/alteracoes-app.js' in public_workflow
before=(root/'alteracoes.js').read_bytes()
subprocess.check_call(['python',str(root/'scripts'/'build_alteracoes.py')],cwd=root)
assert (root/'alteracoes.js').read_bytes()==before,'Série de dotações deve ser reproduzível'
print(f'OK: {len(changes)} observações de alterações de dotações, fontes, magnitude, sinais e deploy verificados.')
