#!/usr/bin/env python3
"""Gera JS offline a partir de CSV de dotações verificadas; não busca números na web."""
import csv, json
from pathlib import Path
from decimal import Decimal
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'data' / 'alteracoes_orcamentarias.csv'
OUTPUT = ROOT / 'alteracoes.js'
REQUIRED = ('ano','area','escopo','id_escopo','data_referencia','dotacao_inicial_reais','dotacao_atualizada_reais','fonte','nota')
NUM = ('dotacao_inicial_reais','dotacao_atualizada_reais','empenhado_reais','liquidado_reais','pago_reais')

def load():
    with INPUT.open('r',encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f,delimiter=';')
        if not reader.fieldnames or any(x not in reader.fieldnames for x in REQUIRED):
            raise ValueError('Cabeçalhos de alterações orçamentárias ausentes')
        rows=list(reader)
    seen=set()
    out=[]
    for r in rows:
        if None in r or not all(str(r.get(k,'')).strip() for k in REQUIRED):
            raise ValueError(f'Linha incompleta ou separador CSV indevido: {r}')
        k=(r['ano'],r['id_escopo'],r['data_referencia'])
        if k in seen: raise ValueError(f'Registro duplicado: {k}')
        seen.add(k)
        if not (2011<=int(r['ano'])<=2026): raise ValueError('Ano inválido')
        if not r['data_referencia'].startswith(r['ano']+'-'): raise ValueError('Data e exercício divergem')
        if not r['fonte'].startswith('https://'): raise ValueError('Fonte sem HTTPS')
        item={k:r[k] for k in REQUIRED if k not in NUM}
        for num in NUM:
            s=(r.get(num) or '').strip()
            if s and (not s.isascii() or not s.isdecimal()):
                raise ValueError(f'{num} inválido: {s}')
            item[num] = int(s) if s else None
        if item['dotacao_inicial_reais']<=0 or item['dotacao_atualizada_reais']<0:
            raise ValueError('Dotação inicial/atualizada inválida')
        item['delta_reais']=item['dotacao_atualizada_reais']-item['dotacao_inicial_reais']
        item['delta_pct']=float((Decimal(item['delta_reais'])/Decimal(item['dotacao_inicial_reais'])*100).quantize(Decimal('0.0001')))
        item['ano']=int(r['ano'])
        out.append(item)
    return sorted(out,key=lambda x:(x['ano'],x['area'],x['id_escopo']))

def main():
    rows=load()
    OUTPUT.write_text('window.BUDGET_CHANGES='+json.dumps(rows,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
    print(f'OK: {len(rows)} observações orçamentárias revisadas; alterações.js gerado')

if __name__=='__main__': main()
