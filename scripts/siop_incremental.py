#!/usr/bin/env python3
"""Coleta UM ano do SIOP, com artefatos independentes para PR e auditoria.

Aprovação do PR por ano guarda dados verificados no repositório. Não altera os
números publicados; consolidar_siop.py propõe uma segunda PR revisável.
"""
import argparse
import csv
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone
from tempfile import TemporaryDirectory
from coletar_siop_loa import ROOT, main as coletar, FIELDS, CODES

STORE = ROOT / 'data' / 'siop_anos'


def validate_pair(year, csv_path, json_path):
    audit=json.loads(Path(json_path).read_text(encoding='utf-8'))
    observations=audit.get('exercicios', [])
    if audit.get('status')!='completa' or len(observations)!=1:
        raise ValueError('Auditoria de coleta incompleta ou misturando anos')
    obs=observations[0]
    if obs.get('ano')!=year or obs.get('status')!='validado':
        raise ValueError(f'Auditoria divergente para {year}')
    sha=obs.get('sha256','')
    if len(sha)!=64 or any(ch not in '0123456789abcdef' for ch in sha):
        raise ValueError('SHA256 ausente ou inválido na auditoria')
    with Path(csv_path).open(encoding='utf-8-sig', newline='') as f:
        reader=csv.DictReader(f,delimiter=';')
        if tuple(reader.fieldnames or [])!=FIELDS:
            raise ValueError('Esquema CSV de ano incorreto')
        rows=list(reader)
    if not rows or len(rows)>28:
        raise ValueError('Quantidade inválida de funções por ano')
    seen=set()
    for row in rows:
        if None in row or row['ano']!=str(year) or row['funcao'] not in CODES.values():
            raise ValueError('Ano, função ou linha inesperados')
        if row['funcao'] in seen: raise ValueError('Função duplicada no ano')
        seen.add(row['funcao'])
        if not row['fonte'].startswith('https://'):
            raise ValueError('Fonte não HTTPS')
    if len(rows)!=obs.get('funcoes_com_dotacao_inicial_positiva'):
        raise ValueError('Contagem divergente entre CSV e auditoria')
    return rows


def run(year, force=False, today=None):
    if year not in range(2011,2027): raise ValueError('Ano fora do escopo 2011–2026')
    today = today or datetime.now(timezone.utc).date()
    # Exercício corrente recebe uma fotografia mensal; histórico fica imutável por ano.
    key = f"{year}-{today:%Y%m}" if year == today.year else str(year)
    csv_final=STORE / f"{key}.csv"
    json_final=STORE / f"{key}.json"
    if csv_final.exists() or json_final.exists():
        if not (csv_final.exists() and json_final.exists()):
            raise ValueError(f'Ano {year}: somente um dos arquivos foi encontrado; revisar')
        rows=validate_pair(year,csv_final,json_final)
        if not force:
            print(f'ANO {year} JA APROVADO: {len(rows)} funções; download dispensado. Sem alterações.')
            return 'aprovado'
        # Uma recoleta nunca substitui automaticamente um ano previamente aprovado.
        # O operador deve abrir uma revisão histórica editorial separada.
        raise ValueError('Recoleta de ano já aprovado requer revisão editorial separada; substituição bloqueada')
    STORE.mkdir(parents=True, exist_ok=True)
    # Saída no diretório reports para sobreviver a erros como artefato do workflow.
    csv_out=ROOT / 'reports' / f'siop_{year}.csv'
    audit_out=ROOT / 'reports' / f'siop_{year}.json'
    coletar(['--anos',str(year),'--saida',str(csv_out.relative_to(ROOT)),
                 '--relatorio',str(audit_out.relative_to(ROOT))])
    rows=validate_pair(year,csv_out,audit_out)
    # Somente após checksum, agregação e conferência de ambos os arquivos.
    shutil.copyfile(csv_out,csv_final)
    shutil.copyfile(audit_out,json_final)
    print(f'ANO {year} VALIDADO: {len(rows)} funções; proposta {key} pronta.')
    return 'novo'


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ano',type=int,required=True)
    args=p.parse_args()
    try:run(args.ano)
    except Exception as exc:
        raise SystemExit(f'COLETA DO ANO {args.ano} BLOQUEADA: {exc}')
