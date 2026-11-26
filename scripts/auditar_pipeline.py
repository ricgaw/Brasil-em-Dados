#!/usr/bin/env python3
"""Auditoria *offline* dos exercícios SIOP aprovados na branch examinada.

Não baixa fontes, não revisa números nem modifica o site. A verificação do
checksum do arquivo bruto é feita na coleta; aqui se preserva a rastreabilidade
entre CSV anual, auditoria e painel consolidado.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / 'data' / 'siop_anos'
FIELDS = ('ano', 'funcao', 'dotacao_inicial_reais', 'dotacao_atualizada_reais',
          'data_referencia', 'fonte', 'empenhado_reais', 'liquidado_reais',
          'pago_reais', 'nota')
NUMERIC = ('dotacao_inicial_reais', 'dotacao_atualizada_reais',
           'empenhado_reais', 'liquidado_reais', 'pago_reais')


def audit_year(csv_path):
    path = Path(csv_path)
    year = int(path.name[:4])
    if not 2011 <= year <= 2026:
        raise ValueError(f'Exercício fora do intervalo: {path.name}')
    audit_path = path.with_suffix('.json')
    if not audit_path.is_file():
        raise ValueError(f'Arquivo de auditoria ausente: {audit_path}')
    raw = path.read_bytes()
    with path.open(encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(f'Esquema inesperado: {path}')
        rows = list(reader)
    if not 1 <= len(rows) <= 28:
        raise ValueError(f'Quantidade de funções inesperada: {path}')
    doc = json.loads(audit_path.read_text(encoding='utf-8'))
    observations = doc.get('exercicios', [])
    if doc.get('status') != 'completa' or len(observations) != 1:
        raise ValueError(f'Auditoria incompleta: {audit_path}')
    audit = observations[0]
    if audit.get('ano') != year or audit.get('status') != 'validado':
        raise ValueError(f'Auditoria divergente: {audit_path}')
    digest = audit.get('sha256', '')
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
        raise ValueError(f'Checksum bruto ausente: {audit_path}')
    if audit.get('funcoes_com_dotacao_inicial_positiva') != len(rows):
        raise ValueError(f'Contagem divergente: {path}')
    if 'linhas' in audit and (not isinstance(audit['linhas'], int) or audit['linhas'] <= 0):
        raise ValueError(f'Contagem de linhas brutas inválida: {audit_path}')
    if 'reservas_contingencia_excluidas_do_painel' in audit and not isinstance(audit['reservas_contingencia_excluidas_do_painel'], dict):
        raise ValueError(f'Reserva de Contingência sem separação: {audit_path}')
    expected_source = audit.get('url')
    seen = set()
    for row in rows:
        if None in row or row['ano'] != str(year):
            raise ValueError(f'Registro malformado em {path}')
        f = row['funcao']
        if not f or f in seen:
            raise ValueError(f'Função duplicada/vazia em {path}: {f}')
        seen.add(f)
        source = row['fonte']
        p = urlsplit(source)
        host = p.hostname or ''
        if p.scheme != 'https' or not (host == 'gov.br' or host.endswith('.gov.br')):
            raise ValueError(f'Fonte não oficial: {source}')
        if expected_source and source != expected_source:
            raise ValueError(f'Fonte do CSV não coincide com a auditoria: {path}')
        if not row['data_referencia'].startswith(str(year) + '-'):
            raise ValueError(f'Data divergente em {path}')
        for col in NUMERIC:
            v = row[col]
            if v and (not v.isascii() or not v.isdecimal()):
                raise ValueError(f'{col} inválido em {path}: {v}')
        if int(row['dotacao_inicial_reais'] or 0) <= 0:
            raise ValueError(f'Dotação inicial não positiva em {path}')
    return {'ano': year, 'arquivo': path.name,
            'funcoes': len(rows), 'checksum_csv_normalizado': hashlib.sha256(raw).hexdigest(),
            'checksum_fonte_declarado': digest, 'fonte': expected_source or rows[0]['fonte'],
            'linhas_fonte_reportadas': audit.get('linhas'),
            'status': 'estrutura_e_rastreabilidade_conferidas'}


def run(store=STORE):
    store = Path(store)
    files = sorted(store.glob('*.csv')) if store.exists() else []
    records = [audit_year(p) for p in files]
    missing = [str(p) for p in store.glob('*.json') if not p.with_suffix('.csv').exists()]
    if missing:
        raise ValueError('Auditorias sem CSV correspondente: ' + ', '.join(missing))
    unique = [x['arquivo'] for x in records]
    if len(unique) != len(set(unique)):
        raise ValueError('Arquivos anuais duplicados')
    return {'tipo': 'auditoria_offline', 'exercicios_ou_snapshots': len(records),
            'observacoes': records,
            'limite': 'Checksums dos arquivos brutos são declarações do coletor; esta auditoria não baixa nem confere novamente a fonte oficial.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', default='', help='Salvar relatório JSON fora do site (opcional)')
    args = p.parse_args()
    try:
        result = run()
        if args.saida:
            out = Path(args.saida)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        print(f"OK: {result['exercicios_ou_snapshots']} arquivos anuais/snapshots auditados; sem alterar site.")
    except Exception as e:
        raise SystemExit(f'AUDITORIA BLOQUEADA: {e}')
