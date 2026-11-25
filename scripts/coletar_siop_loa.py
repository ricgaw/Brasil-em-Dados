#!/usr/bin/env python3
"""Extrai os arquivos tabulares oficiais SIOP LOA por função (sem substituir dados publicados).

Fluxo: página pública -> URLs CSV.gz/sha256 -> SHA256 -> CSV streaming ->
R$ por função -> CSV normalizado temporário, pronto para importar_dotacoes.py.

Exige conferência humana de alterações históricas e diferenças entre metodologias.
"""
import argparse
import csv
from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import gzip
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import urllib.request
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = 'https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:dados_abertos'
DOC = 'https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:dados_abertos_loa'
FIELDS = ('ano','funcao','dotacao_inicial_reais','dotacao_atualizada_reais','data_referencia','fonte','empenhado_reais','liquidado_reais','pago_reais','nota')
NUMBERS = ('valor_dotacao_inicial','valor_lei_mais_creditos','valor_empenhado','valor_liquidado','valor_pago')
MAX_DOWNLOAD = 30_000_000
MAX_UNCOMPRESSED = 500_000_000

# Códigos oficiais das funções: descrição usada no ano histórico pode variar.
CODES = {
 '01':'Legislativa','02':'Judiciária','03':'Essencial à Justiça','04':'Administração',
 '05':'Defesa nacional','06':'Segurança pública','07':'Relações exteriores','08':'Assistência social',
 '09':'Previdência social','10':'Saúde','11':'Trabalho','12':'Educação','13':'Cultura',
 '14':'Direitos da cidadania','15':'Urbanismo','16':'Habitação','17':'Saneamento',
 '18':'Gestão ambiental','19':'Ciência e tecnologia','20':'Agricultura','21':'Organização agrária',
 '22':'Indústria','23':'Comércio e serviços','24':'Comunicações','25':'Energia',
 '26':'Transporte','27':'Desporto e lazer','28':'Encargos especiais',
}


def official_https(url):
    p=urlparse(url)
    host=(p.hostname or '').lower()
    return p.scheme == 'https' and (host=='gov.br' or host.endswith('.gov.br')) and not p.username and not p.password


def get(url, limit=MAX_DOWNLOAD):
    if not official_https(url):
        raise ValueError('Download fora de domínio oficial HTTPS: '+url)
    req=urllib.request.Request(url, headers={'User-Agent':'BrasilEmDados/2.0 (pesquisa publica)','Accept':'*/*'})
    # Não permitir redirecionamento silencioso a servidor não oficial.
    with urllib.request.urlopen(req, timeout=60) as response:
        if not official_https(response.geturl()):
            raise ValueError('Redirecionamento para servidor não governamental: '+response.geturl())
        data=response.read(limit+1)
    if len(data)>limit:
        raise ValueError(f'Download excede {limit} bytes: {url}')
    return data


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.href=None; self.label=[]
    def handle_starttag(self, tag, attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.label=[]
    def handle_data(self, data):
        if self.href is not None: self.label.append(data)
    def handle_endtag(self, tag):
        if tag=='a' and self.href is not None:
            self.links.append((self.href,''.join(self.label).strip()))
            self.href=None


def discover(html, year, base=CATALOG):
    parser=Anchors(); parser.feed(html)
    urls={}
    for href,label in parser.links:
        target=urljoin(base,href)
        candidate=unquote(href)+' '+label
        for ext in ('csv.gz','sha256'):
            filename=f'loa{year}.{ext}'
            if re.search(r'(?<![\w])'+re.escape(filename)+r'(?![\w])',candidate,re.I):
                if not official_https(target):
                    raise ValueError('Link SIOP fora de domínio oficial: '+target)
                if ext in urls and urls[ext]!=target:
                    raise ValueError('Mais de um link para '+filename)
                urls[ext]=target
    if set(urls)!={'csv.gz','sha256'}:
        raise ValueError(f'Links oficiais não encontrados para {year}: {list(urls)}')
    return urls


def verify_digest(blob, manifest, year):
    filename=f'loa{year}.csv.gz'
    entries=re.findall(r'(?m)^\s*([0-9a-fA-F]{64})\s+\*?([^\s]+)\s*$',manifest)
    candidates=[h.lower() for h,name in entries if Path(name).name==filename]
    if len(candidates)!=1:
        raise ValueError(f'Checksum SHA-256 do {filename} ausente ou ambíguo')
    actual=hashlib.sha256(blob).hexdigest()
    if actual!=candidates[0]:
        raise ValueError(f'Checksum divergente para {filename}; download bloqueado')
    return actual


def to_cents(raw):
    try:
        d=Decimal(str(raw).strip())
    except InvalidOperation:
        raise ValueError('Valor monetário não numérico: '+str(raw)[:35])
    if not d.is_finite() or d.as_tuple().exponent < -2:
        raise ValueError('Formato monetário inválido, esperado reais com até 2 casas')
    cents=d*100
    if cents!=cents.to_integral_value():
        raise ValueError('Valor não representável em centavos')
    return int(cents)


def aggregate(blob, year):
    totals=defaultdict(lambda:[0]*len(NUMBERS))
    seen_rows=0
    with gzip.GzipFile(fileobj=io.BytesIO(blob)) as zipped:
        with io.TextIOWrapper(zipped,encoding='utf-8-sig',newline='') as inp:
            rdr=csv.DictReader(inp,delimiter=',')
            required={'exercicio','esfera_codigo','funcao_codigo',*NUMBERS}
            if not rdr.fieldnames or not required.issubset(set(rdr.fieldnames)):
                raise ValueError('Esquema inesperado do SIOP: '+str(rdr.fieldnames))
            for row in rdr:
                seen_rows+=1
                if seen_rows>1_000_000:
                    raise ValueError('Limite de linhas excedido; revisar estrutura')
                if not row or None in row:
                    raise ValueError('Linha CSV corrompida')
                if int(row['exercicio'])!=year:
                    raise ValueError('Exercício divergente: '+str(row['exercicio']))
                if row['esfera_codigo'].strip() not in ('10','20'):
                    raise ValueError('Esfera não Fiscal/Seguridade identificada')
                code=row['funcao_codigo'].strip().zfill(2)
                if code not in CODES:
                    raise ValueError('Código de função desconhecido: '+code)
                amount=totals[code]
                for idx,col in enumerate(NUMBERS):
                    amount[idx]+=to_cents(row[col])
    if seen_rows<28 or len(totals)<20:
        raise ValueError('Cobertura orçamentária insuficiente: linhas/funções inesperadas')
    return totals,seen_rows


def reais_rounded(cents):
    return str((Decimal(cents)/100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))


def normalized_rows(year, totals, url, today):
    reference=(today if year==today.year else date(year,12,31)).isoformat()
    note=('SIOP LOA por função, esferas Fiscal (10) e Seguridade (20); '
          'somatório de todas as classificações, incluindo linhas distintas de dotação e execução; '
          'valores agregados em centavos e arredondados a reais. '
          +('Exercício em curso, posição do arquivo da coleta.' if year==today.year else
            'Exercício encerrado: 31/12 é marcador do ano, NÃO data de download do arquivo histórico.'))
    results=[]
    for code,nums in sorted(totals.items()):
        if nums[0]<=0:
            # O importador atual não suporta variação % em dotação inicial zero.
            # Não transformar ausência/zero em aumento mensurável.
            continue
        results.append(dict(zip(FIELDS,(
            str(year), CODES[code], *[reais_rounded(x) for x in nums[:2]],
            reference,url, *[reais_rounded(x) for x in nums[2:]],note
        ))))
    return results


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--anos',nargs='+',type=int,default=[2025,2026]);
    ap.add_argument('--saida',default='reports/siop_proposta.csv')
    ap.add_argument('--relatorio',default='reports/siop_coleta.json')
    args=ap.parse_args(argv)
    if any(not 2011<=y<=2026 for y in args.anos) or len(set(args.anos))!=len(args.anos):
        ap.error('Anos devem estar entre 2011 e 2026, sem repetições')
    atlas=json.loads((ROOT/'data'/'atlas.json').read_text(encoding='utf-8'))
    areas={x['area'] for x in atlas['budget']}
    assert set(CODES.values())==areas, 'Mapa de funções precisa coincidir com catálogo do site'
    today=datetime.now(timezone.utc).date()
    catalog=get(CATALOG,limit=2_000_000).decode('utf-8','replace')
    all_rows=[];report=[]
    for year in args.anos:
        if year>today.year: raise ValueError(f'Exercício futuro: {year}')
        urls=discover(catalog,year)
        blob=get(urls['csv.gz'])
        manifest=get(urls['sha256'],limit=300_000).decode('utf-8-sig')
        sha=verify_digest(blob,manifest,year)
        totals,num_lines=aggregate(blob,year)
        rows=normalized_rows(year,totals,urls['csv.gz'],today)
        all_rows.extend(rows)
        report.append({'ano':year,'url':urls['csv.gz'],'sha256':sha,'linhas':num_lines,
                       'funcoes_com_dotacao_inicial_positiva':len(rows),
                       'funcoes_sem_dotacao_inicial_positiva':[CODES[k] for k,v in sorted(totals.items()) if v[0]<=0],
                       'parcial':year==today.year})
        print(f'{year}: {num_lines} linhas; {len(rows)} funções com dotação inicial > 0; SHA256 OK')
    target=ROOT/args.saida;target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,delimiter=';',lineterminator='\n')
        w.writeheader();w.writerows(all_rows)
    audit=ROOT/args.relatorio;audit.parent.mkdir(parents=True,exist_ok=True)
    audit.write_text(json.dumps({'coletado_em_utc':today.isoformat(),'fonte_catalogo':CATALOG,
                'metodologia':DOC,'exercicios':report},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'Salvos {len(all_rows)} registros em {target}; auditoria em {audit}')

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print('COLETA BLOQUEADA:',exc,file=sys.stderr)
        sys.exit(2)
