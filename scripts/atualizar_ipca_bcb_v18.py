#!/usr/bin/env python3
"""Atualiza IPCA ANUAL somente depois que os 12 meses de 2026 são publicados.

Série SGS 433 (variação mensal do IPCA, base IBGE). NÃO cria estimativa nem dado parcial
rotulado como anual. Trabalha apenas com o exercício 2026 para não alterar histórico.
"""
import csv, json, io
from decimal import Decimal
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request
ROOT=Path(__file__).resolve().parents[1]
SRC='https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'
API='https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados'
YEAR=2026

def calculate(records):
    months={}
    for r in records:
        d=datetime.strptime(r['data'],'%d/%m/%Y').date()
        if d.year != YEAR: raise ValueError('Série fora de 2026')
        v=Decimal(str(r['valor']).replace(',','.'))
        if not v.is_finite() or not Decimal('-10') < v < Decimal('20'): raise ValueError('IPCA mensal fora da faixa')
        if d.month in months: raise ValueError('Mês duplicado')
        months[d.month]=v
    if sorted(months)!=list(range(1,13)):
        return None
    compounded=Decimal('1')
    for m in range(1,13):compounded*=Decimal('1')+months[m]/100
    return round((compounded-1)*100,2)

def update(root=ROOT,records=None,today=None):
    today=today or date.today()
    if today.year<=YEAR: return False  # Nunca anunciar fechamento anual antes de virar o ano.
    if records is None:
        params=urlencode({'formato':'json','dataInicial':'01/01/2026','dataFinal':'31/12/2026'})
        req=Request(API+'?'+params,headers={'Accept':'application/json','User-Agent':'BrasilEmDados/1.0'})
        with urlopen(req,timeout=35) as r:records=json.load(r)
    val=calculate(records)
    if val is None: return False
    data_path=root/'data/indicadores_sociais.json'
    base=json.loads(data_path.read_text(encoding='utf-8'))
    rows=base['series']
    matches=[r for r in rows if r['indicador']=='ipca' and r['ano']==YEAR]
    if matches:
        if abs(Decimal(str(matches[0]['valor']))-val)>Decimal('.02'):
            raise ValueError('2026 existente diverge da fonte BCB: revisão manual necessária')
        return False
    row={'indicador':'ipca','nome':'IPCA acumulado no ano','ano':YEAR,'valor':float(val),'unidade':'%',
        'fonte':'BCB SGS 433 (IPCA mensal IBGE, acumulado geométrico)', 'url':SRC,
        'nota':'Fechamento anual calculado dos 12 meses oficiais, nominal; conferência IBGE recomendada.'}
    rows.append(row);rows.sort(key=lambda r:(r['indicador'],r['ano']))
    base['meta']['observacao']='IPCA anual 2011–2026; desocupação anual quando divulgada oficialmente. Exige conferência IBGE.'
    text=json.dumps(base,ensure_ascii=False,indent=2)+'\n'
    # Criar todos os artefatos na memória antes de gravar.
    stream=io.StringIO(newline='')
    cols=['indicador','nome','ano','valor','unidade','fonte','url','nota'];writer=csv.DictWriter(stream,fieldnames=cols,delimiter=';',lineterminator='\n',quoting=csv.QUOTE_MINIMAL)
    writer.writeheader();writer.writerows(rows)
    js='window.INDICADORES='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n'
    data_path.write_text(text,encoding='utf-8',newline='\n')
    (root/'data/indicadores_sociais.csv').write_text('\ufeff'+stream.getvalue(),encoding='utf-8',newline='\n')
    (root/'indicadores.js').write_text(js,encoding='utf-8',newline='\n')
    return True
if __name__=='__main__':print('IPCA: atualizado' if update() else 'IPCA: aguardando 12 meses oficiais ou já publicado')
