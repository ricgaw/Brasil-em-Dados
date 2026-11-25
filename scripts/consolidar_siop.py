#!/usr/bin/env python3
"""Consolida somente anos SIOP que já passaram pela revisão e estão na main.

Conservador: qualquer revisão de linha existente bloqueia toda a proposta.
"""
import argparse
from pathlib import Path
from siop_incremental import STORE, validate_pair
from importar_dotacoes import run
from types import SimpleNamespace

def consolidate():
    if not STORE.is_dir():
        print('Nenhum ano aprovado para consolidar')
        return 0
    files=sorted((p for p in STORE.glob('*.csv') if p.stem[:4].isdecimal()),key=lambda p:(int(p.stem[:4]),p.stem))
    if not files:
        print('Nenhum ano aprovado para consolidar')
        return 0
    for csv_file in files:
        year=int(csv_file.stem[:4])
        audit_file=csv_file.with_suffix('.json')
        rows=validate_pair(year,csv_file,audit_file)
        print(f'Consolidar {year}: {len(rows)} funções aprovadas')
        run(SimpleNamespace(arquivo=str(csv_file),url=None))
    print(f'Consolidação validada de {len(files)} arquivo(s) de anos/snapshots, sem sobrescrita de histórico')
    return len(files)

if __name__=='__main__':
    try:consolidate()
    except Exception as exc:raise SystemExit(f'CONSOLIDACAO BLOQUEADA: {exc}')
