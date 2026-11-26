#!/usr/bin/env python3
"""Atualiza a DBGG / PIB pelo BCB SGS 13762, com travas de integridade e publicação reprodutível.

Sem dependências externas. Nunca inventa observações nem substitui por zero quando a API falha.
"""
import argparse
import csv
import io
import json
import re
import time
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SERIES = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.13762/dados'
SOURCE = 'https://dadosabertos.bcb.gov.br/dataset/13762-divida-bruta-do-governo-geral--pib---metodologia-utilizada-a-partir-de-2008'
START = 2011
PATHS = {
    'json': ROOT / 'data/divida_pib_bcb.json',
    'csv': ROOT / 'data/divida_pib_bcb.csv',
    'js': ROOT / 'estatais-divida-data.js',
}
FIELDS = ['ano', 'mes', 'dbgg_pct_pib', 'periodo', 'fonte', 'codigo_sgs', 'estado']


def get_json(url, *, opener=urlopen, sleep=time.sleep):
    last = None
    for attempt in range(3):
        try:
            request = Request(url, headers={'User-Agent': 'BrasilEmDados/1.0 (dados publicos)', 'Accept': 'application/json'})
            with opener(request, timeout=35) as response:
                return json.loads(response.read().decode('utf-8-sig'))
        except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
            last = exc
            if attempt != 2:
                sleep(2 * (attempt + 1))
    raise RuntimeError(f'Falha ao consultar BCB; arquivos originais preservados: {last}')


def fetch_values(today, fetch=get_json):
    # O BC impõe janelas de consulta; segmentos abaixo de dez anos evitam erro HTTP 400.
    months = {}
    for start in range(START, today.year + 1, 8):
        end = min(today.year, start + 7)
        first = date(start, 1, 1)
        last = min(today, date(end, 12, 31))
        params = urlencode({'formato': 'json', 'dataInicial': first.strftime('%d/%m/%Y'), 'dataFinal': last.strftime('%d/%m/%Y')})
        block = fetch(f'{SERIES}?{params}')
        if not isinstance(block, list):
            raise ValueError(f'Resposta não é lista do BCB, intervalo {start}–{end}')
        for record in block:
            if not isinstance(record, dict) or 'data' not in record or 'valor' not in record:
                raise ValueError('Observação oficial incompleta')
            d = datetime.strptime(record['data'], '%d/%m/%Y').date()
            if not (first <= d <= last):
                raise ValueError(f'Observação fora da janela: {d}')
            try:
                value = Decimal(str(record['valor']).replace(',', '.'))
            except InvalidOperation as exc:
                raise ValueError(f'Valor de dívida não numérico: {record}') from exc
            if not value.is_finite() or not Decimal('1') < value < Decimal('200'):
                raise ValueError(f'Valor de dívida fora de limites: {d}={value}')
            key = (d.year, d.month)
            if key in months and months[key] != value:
                raise ValueError(f'Conflito no período {key}')
            months[key] = value
    return months


def transform(months, existing, today):
    old = {int(row['ano']): row for row in existing}
    result = []
    for year in range(START, min(today.year, max(y for (y, m) in months)) + 1):
        values = [(m, v) for (y, m), v in months.items() if y == year]
        if not values:
            raise ValueError(f'A série oficial não contém o ano {year}; preservando a base atual')
        month, value = max(values)
        if year < today.year and month != 12:
            raise ValueError(f'Ano encerrado {year} sem dezembro; preservando a base atual')
        # Para exercício corrente, dezembro só é final quando já encerrou o ano.
        annual = year < today.year or (month == 12 and today.month == 12)
        if year in old:
            previous = Decimal(str(old[year]['dbgg_pct_pib']))
            if abs(value - previous) > Decimal('5'):
                raise ValueError(f'Revisão excepcional em {year}: {previous} para {value} p.p.; requer auditoria')
            if year == today.year and month < int(old[year]['mes']):
                raise ValueError(f'API retornou período anterior ao publicado para {year}')
        result.append({
            'ano': year,
            'mes': month,
            'dbgg_pct_pib': float(value),
            'periodo': 'Fechamento de dezembro' if annual else f'{month:02d}/{year} · parcial',
            'fonte': SOURCE,
            'codigo_sgs': 13762,
            'estado': 'anual' if annual else 'parcial',
        })
    return result


def render(rows, existing_json, existing_js, today):
    payload = dict(existing_json)
    payload['observacoes'] = rows
    payload['data_consulta'] = today.isoformat()
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=FIELDS, delimiter=';', lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    first = 'window.DIVIDA_PUBLICA=' + json.dumps(rows, ensure_ascii=False, separators=(',', ':')) + ';'
    if not re.match(r'^window\.DIVIDA_PUBLICA=.*?;\s*window\.ESTATAIS_DADOS=', existing_js, flags=re.S):
        raise ValueError('Formato JS inesperado; não substituir dados das estatais')
    new_js = re.sub(r'^window\.DIVIDA_PUBLICA=.*?;', lambda _: first, existing_js, count=1, flags=re.S)
    return {'json': encoded.encode('utf-8'), 'csv': output.getvalue().encode('utf-8'), 'js': new_js.encode('utf-8')}


def update(*, today=None, fetch=get_json, dry_run=False):
    today = today or datetime.now(timezone.utc).date()
    original = {k: path.read_bytes() for k, path in PATHS.items()}
    document = json.loads(original['json'])
    old_rows = document['observacoes']
    months = fetch_values(today, fetch=fetch)
    rows = transform(months, old_rows, today)
    # Sem mudanças numéricas ou de estado, não atualizar a data de consulta nem criar commit vazio.
    normalized_old = [{k: row[k] for k in FIELDS} for row in old_rows]
    if rows == normalized_old:
        print('SEM ALTERAÇÕES: BCB não publicou observações/revisões novas para o painel.')
        return False
    rendered = render(rows, document, original['js'].decode('utf-8'), today)
    # Todos os bytes são construídos/validados antes de qualquer gravação.
    assert len(rows) >= 15 and len(set(row['ano'] for row in rows)) == len(rows)
    if dry_run:
        print('SIMULAÇÃO: alterações detectadas; nenhum arquivo gravado')
        return True
    for kind, output in rendered.items():
        PATHS[kind].write_bytes(output)
    print(f'ATUALIZADO: {len(rows)} exercícios; última observação {rows[-1]["mes"]:02d}/{rows[-1]["ano"]}.')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    update(dry_run=args.dry_run)
