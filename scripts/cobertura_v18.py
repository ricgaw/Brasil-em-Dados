#!/usr/bin/env python3
"""Cobertura calculada a partir dos arquivos; nenhum valor ausente é convertido em zero."""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def report(root=ROOT):
    state=json.loads((root/'data/estatais_resultados.json').read_text(encoding='utf-8'))
    debt=json.loads((root/'data/divida_pib_bcb.json').read_text(encoding='utf-8'))
    with (root/'data/indicadores_sociais.csv').open(encoding='utf-8-sig', newline='') as f:
        social=list(csv.DictReader(f,delimiter=';'))
    companies=[]
    valid={'petrobras','bb','caixa','correios'}
    years={}
    for item in state['registros']:
        company=item['empresa'];year=item['ano']
        if company not in valid or not 2011 <= year <= 2026: raise ValueError('Estatal/ano não reconhecido')
        if (company,year) in years: raise ValueError('Exercício duplicado')
        if not item['fonte'].startswith('https://'): raise ValueError('Registro sem fonte HTTPS')
        if item['resultado_bi_brl'] is None: raise ValueError('Resultado sem valor verificado')
        years[(company,year)] = item
    for c in state['empresas']:
        entries=[r for (company,year),r in years.items() if company==c['id']]
        companies.append({'id':c['id'],'nome':c['nome'],
          'anos_resultado':sorted(r['ano'] for r in entries),
          'anos_receita':sorted(r['ano'] for r in entries if r['receita_bi_brl'] is not None),
          'anos_endividamento':sorted(r['ano'] for r in entries if r['endividamento_bi'] is not None),
          'fonte':c['fonte_geral']})
    budget = sorted(int(p.stem) for p in (root/'data/siop_anos').glob('*.csv') if p.stem.isdigit())
    indicator={k:sorted(int(r['ano']) for r in social if r['indicador']==k) for k in ('ipca','desocupacao')}
    return {'periodo':[2011,2026], 'estatais':companies, 'divida_anos': sorted({int(r['ano']) for r in debt['observacoes']}),
        'indicadores_anos':indicator,'siop_anos_com_arquivo':budget,
        'ressalva':'Cobertura documental não valida automaticamente a metodologia nem confirma que o ano esteja consolidado no site.'}

def render(root=ROOT):
    result=report(root)
    js='window.COBERTURA_V18='+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n'
    target=root/'cobertura-v18.js'
    if not target.exists() or target.read_text(encoding='utf-8')!=js:
        target.write_text(js,encoding='utf-8',newline='\n')
    return result
if __name__=='__main__':
    d=render();print('Cobertura: '+', '.join(f"{x['nome']} {len(x['anos_resultado'])}/16" for x in d['estatais']))
