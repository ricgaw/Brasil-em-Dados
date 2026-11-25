#!/usr/bin/env python3
"""Importa exportação pública CPGF CGU, sem persistir dados pessoais.

Entrada: CSV ou ZIP baixado manualmente do Portal da Transparência.
Saída: resumos mensais por órgão, sem CPF, portador ou favorecido.
"""
from __future__ import annotations
import argparse
import csv
from collections import defaultdict
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import io
import json
from pathlib import Path
import re
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['periodo','ano','mes','codigo_orgao_superior','nome_orgao_superior','valor_centavos','transacoes','fonte','sha256_arquivo']
SOURCE='https://portaldatransparencia.gov.br/download-de-dados/cpgf/'


def normalize(label):
    return re.sub(r'[^A-Z0-9]+',' ',unicodedata.normalize('NFKD',str(label)).encode('ascii','ignore').decode().upper()).strip()


def column(names, *options, required=True):
    available={normalize(n): n for n in names}
    for key in options:
        if normalize(key) in available:
            return available[normalize(key)]
    if required:
        raise ValueError('Coluna oficial obrigatória ausente: '+ ' / '.join(options))
    return None


def amount_to_cents(value):
    raw=str(value).strip().replace('R$','').replace(' ','')
    if ',' in raw: raw=raw.replace('.','').replace(',','.')
    if not re.fullmatch(r'-?\d+(?:\.\d{1,2})?',raw): raise ValueError('Valor monetário inválido')
    try: cents=(Decimal(raw)*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP)
    except InvalidOperation as e: raise ValueError('Valor monetário inválido') from e
    return int(cents)


@contextmanager
def open_source(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            files=[x for x in archive.infolist() if not x.is_dir() and x.filename.lower().endswith('.csv')]
            if len(files)!=1: raise ValueError('ZIP deve conter exatamente um CSV do CPGF (não misturar origens)')
            if files[0].file_size>400_000_000: raise ValueError('Arquivo descompactado acima do limite de 400 MB')
            with archive.open(files[0]) as binary:
                yield binary
    else:
        with path.open('rb') as binary: yield binary


def rows_from_source(path):
    with open_source(path) as stream:
        sample=stream.read(32768)
        encoding='utf-8-sig'
        try: sample.decode(encoding)
        except UnicodeDecodeError: encoding='latin-1'
    with open_source(path) as stream:
        wrapper=io.TextIOWrapper(stream,encoding=encoding,newline='')
        try:
            sample_text=sample.decode(encoding)
            sep=';' if sample_text.splitlines()[0].count(';')>=sample_text.splitlines()[0].count(',') else ','
            reader=csv.DictReader(wrapper,delimiter=sep)
            if not reader.fieldnames: raise ValueError('Arquivo CSV sem cabeçalho')
            for row in reader: yield reader.fieldnames,row
        finally:
            wrapper.detach()


def parse(path:Path, periodo:str):
    if not re.fullmatch(r'20\d{2}(0[1-9]|1[0-2])',periodo): raise ValueError('Período inválido, use AAAAMM')
    year,month=int(periodo[:4]),int(periodo[4:])
    if year<2011 or year>2026: raise ValueError('Período fora do recorte do site')
    data=defaultdict(lambda:[0,0]); seen=0
    schema=None
    for names,row in rows_from_source(path):
        if schema is None:
            schema={
                'org_code':column(names,'CÓDIGO ÓRGÃO SUPERIOR','CODIGO ORGAO SUPERIOR'),
                'org_name':column(names,'NOME ÓRGÃO SUPERIOR','NOME ORGAO SUPERIOR'),
                'value':column(names,'VALOR TRANSAÇÃO','VALOR TRANSACAO'),
                'year':column(names,'ANO EXTRATO'),
                'month':column(names,'MÊS EXTRATO','MES EXTRATO'),
            }
            if bool(schema['year']) != bool(schema['month']): raise ValueError('Mês e ano de extrato precisam estar presentes juntos')
        if not any(v and str(v).strip() for v in row.values()):continue
        seen+=1
        if schema['year'] and schema['month']:
            ex_year=str(row[schema['year']]).strip(); ex_month=str(row[schema['month']]).strip()
            if not ex_year.isdigit() or not ex_month.isdigit() or int(ex_year)!=year or int(ex_month)!=month:
                raise ValueError('Arquivo contém competência diferente da solicitada; importação bloqueada')
        code=str(row[schema['org_code']]).strip()
        name=' '.join(str(row[schema['org_name']]).strip().split())
        if not re.fullmatch(r'\d{3,8}',code): raise ValueError('Código do órgão superior inválido')
        if len(name)<3: raise ValueError('Nome do órgão superior inválido')
        cents=amount_to_cents(row[schema['value']])
        data[(code,name)][0]+=cents
        data[(code,name)][1]+=1
    if seen==0: raise ValueError('Arquivo oficial sem transações')
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    result=[dict(periodo=periodo,ano=year,mes=month,codigo_orgao_superior=code,nome_orgao_superior=name,valor_centavos=value,transacoes=n,fonte=SOURCE,sha256_arquivo=sha) for (code,name),(value,n) in sorted(data.items())]
    return result


def read_existing(csvpath):
    if not csvpath.exists():return []
    with csvpath.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))


def write_aggregates(csvpath, jspath, old, new, revise=False):
    month=new[0]['periodo']
    old_month=[r for r in old if r['periodo']==month]
    if old_month and not revise:
        if old_month==[{k:str(v) for k,v in n.items()} for n in new]:return False
        raise ValueError('Competência já consolidada com conteúdo diferente. Exige revisão explícita.')
    allrows=[{k:str(r[k]) for k in FIELDS} for r in old if r['periodo']!=month]+[{k:str(r[k]) for k in FIELDS} for r in new]
    allrows.sort(key=lambda x:(x['periodo'],x['codigo_orgao_superior'],x['nome_orgao_superior']))
    csvpath.parent.mkdir(parents=True,exist_ok=True)
    with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS,delimiter=';',lineterminator='\n');writer.writeheader();writer.writerows(allrows)
    jsrows=[]
    for r in allrows:
        n=dict(r)
        for k in ('ano','mes','valor_centavos','transacoes'):n[k]=int(n[k])
        jsrows.append(n)
    jspath.write_text('window.CPGF_RESUMO='+json.dumps(jsrows,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
    return True


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--arquivo',required=True,type=Path,help='CSV ou ZIP oficial obtido na CGU (não será publicado)')
    ap.add_argument('--periodo',required=True,help='AAAAMM da competência do extrato')
    ap.add_argument('--revisao',action='store_true',help='Permite substituir competência publicada, para revisão humana')
    ap.add_argument('--csv',type=Path,default=ROOT/'data/cpgf_resumo.csv')
    ap.add_argument('--js',type=Path,default=ROOT/'cpgf-data.js')
    args=ap.parse_args()
    new=parse(args.arquivo,args.periodo)
    changed=write_aggregates(args.csv,args.js,read_existing(args.csv),new,args.revisao)
    print(f'CPGF {args.periodo}: {len(new)} órgãos; {sum(x["transacoes"] for x in new)} transações; '+('atualizado' if changed else 'sem alterações'))
    print('Somente dados agregados persistidos; não incluir o arquivo bruto no Git.')

if __name__=='__main__': main()
