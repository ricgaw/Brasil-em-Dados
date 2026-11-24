#!/usr/bin/env python3
"""Importa um CSV normalizado de dotação inicial/atualizada por FUNÇÃO federal.

Uso: python scripts/importar_dotacoes.py --arquivo arquivo.csv
     python scripts/importar_dotacoes.py --url https://.../arquivo.csv

Não mistura órgãos/unidades com funções, exige fonte oficial por registro,
valida esquema e preserva todas as observações anteriores (sem sobregravar).
"""
import argparse, csv, io, json, sys, urllib.request
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'data'/'alteracoes_orcamentarias.csv'
REQUIRED=('ano','funcao','dotacao_inicial_reais','dotacao_atualizada_reais','data_referencia','fonte')
OPTIONAL=('empenhado_reais','liquidado_reais','pago_reais','nota')
CURRENT_FIELDS=('ano','area','escopo','id_escopo','data_referencia','dotacao_inicial_reais','dotacao_atualizada_reais','empenhado_reais','liquidado_reais','pago_reais','fonte','nota')


def official_url(url):
    u=urlparse(url)
    host=(u.hostname or '').lower()
    return u.scheme=='https' and (host.endswith('.gov.br') or host=='gov.br' or host.endswith('.ibge.gov.br'))


def parse_int(v,field):
    s=str(v or '').strip()
    if not s or not s.isascii() or not s.isdecimal():
        raise ValueError(f'{field}: só aceitamos números inteiros em reais (sem separador, não em milhares): {s!r}')
    return int(s)


def read_text(args):
    if args.arquivo:
        path=Path(args.arquivo)
        if path.stat().st_size>10_000_000:raise ValueError('Arquivo maior que o limite de 10 MB')
        return path.read_text(encoding='utf-8-sig')
    if not official_url(args.url):raise ValueError('URL de download deve estar em domínio governamental HTTPS')
    with urllib.request.urlopen(urllib.request.Request(args.url, headers={'User-Agent':'BrasilEmDados/1.0; pesquisa publica'}),timeout=25) as res:
        blob=res.read(10_000_001)
    if len(blob)>10_000_000:raise ValueError('Resposta maior que 10 MB')
    return blob.decode('utf-8-sig')


def run(args):
    from build_alteracoes import load as validate_existing
    validate_existing()
    atlas=json.loads((ROOT/'data'/'atlas.json').read_text(encoding='utf-8'))
    areas={x['area'] for x in atlas['budget']}
    f=csv.DictReader(io.StringIO(read_text(args)),delimiter=';')
    if not f.fieldnames or any(field not in f.fieldnames for field in REQUIRED):
        raise ValueError('Cabeçalhos ausentes. Exija: '+';'.join(REQUIRED))
    if any(field not in REQUIRED+OPTIONAL for field in f.fieldnames):
        raise ValueError('Colunas inesperadas: '+','.join(x for x in f.fieldnames if x not in REQUIRED+OPTIONAL))
    rows=list(f)
    if not rows:raise ValueError('Arquivo vazio')
    if len(rows)>800:raise ValueError('Limite de 800 registros por importação')
    seen=set(); incoming=[]
    for row in rows:
        if None in row:raise ValueError('Quantidade incorreta de campos CSV')
        area=row['funcao'].strip()
        if area not in areas:raise ValueError(f'Função desconhecida ou grafia diferente: {area}')
        year=int(row['ano'])
        if not 2011<=year<=2026:raise ValueError('Ano fora de 2011–2026')
        day=row['data_referencia'].strip()
        from datetime import date
        parsed=date.fromisoformat(day)
        if parsed.year!=year:raise ValueError('Data de referência fora do exercício')
        if not official_url(row['fonte'].strip()):raise ValueError(f'Fonte não governamental para {area}: {row["fonte"]}')
        key=(year,area,day)
        if key in seen:raise ValueError(f'Duplicação na importação: {key}')
        seen.add(key)
        initial=parse_int(row['dotacao_inicial_reais'],'dotação inicial')
        updated=parse_int(row['dotacao_atualizada_reais'],'dotação atualizada')
        # não imputar dotação inicial 0 como alteração percentual calculável
        if initial<=0:raise ValueError('Dotação inicial 0 requer tratamento editorial específico')
        cleaned={'ano':str(year),'area':area,'escopo':f'União — função {area}',
                 'id_escopo':'funcao-'+area.lower().replace(' ','-'),
                 'data_referencia':day,'dotacao_inicial_reais':str(initial),
                 'dotacao_atualizada_reais':str(updated),
                 'empenhado_reais':'','liquidado_reais':'','pago_reais':'',
                 'fonte':row['fonte'].strip(),
                 'nota':row.get('nota','').strip() or 'Orçamento Fiscal e da Seguridade Social, por função. Confirmar período e detalhamento da exportação.'}
        for col in ('empenhado_reais','liquidado_reais','pago_reais'):
            v=(row.get(col) or '').strip()
            if v:cleaned[col]=str(parse_int(v,col))
        incoming.append(cleaned)
    with DEST.open(encoding='utf-8-sig',newline='') as file:
        current=list(csv.DictReader(file,delimiter=';'))
    lookup={(r['ano'],r['id_escopo'],r['data_referencia']):r for r in current}
    additions=0
    for r in incoming:
        key=(r['ano'],r['id_escopo'],r['data_referencia'])
        if key in lookup:
            if any(lookup[key].get(col,'')!=r[col] for col in CURRENT_FIELDS):
                raise ValueError(f'Possível revisão oficial: {key}. Verificar antes de substituir registro publicado.')
        else:
            lookup[key]=r;additions+=1
    if additions:
        import tempfile,os
        out=sorted(lookup.values(),key=lambda r:(int(r['ano']),r['area'],r['id_escopo'],r['data_referencia']))
        stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=CURRENT_FIELDS,delimiter=';',lineterminator='\n')
        writer.writeheader();writer.writerows(out)
        # preserva BOM histórico e apenas adiciona novos registros
        DEST.write_bytes(('\ufeff'+stream.getvalue()).encode('utf-8'))
        from build_alteracoes import load,main
        load();main()
    print(f'OK: {len(rows)} registros recebidos, {additions} novos, total {len(lookup)}; nenhuma linha existente sobrescrita.')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    src=ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--arquivo');src.add_argument('--url')
    ns=ap.parse_args()
    try:run(ns)
    except (ValueError, OSError,UnicodeError) as ex:
        print('IMPORTAÇÃO BLOQUEADA:',ex,file=sys.stderr);sys.exit(2)
