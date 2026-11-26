#!/usr/bin/env python3
"""Monitora DOCUMENTOS oficiais da SEST; não extrai lucro de PDFs/XLSX sem mapeamento auditado.

Mudanças no catálogo oficial são registradas; cifras não são publicadas sem checagem.
"""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data' / 'fontes_estatais_v18.json'
PAGES = [
    'https://www.gov.br/gestao/pt-br/assuntos/estatais/transparencia/defeso_relatorio%20agregado',
    'https://www.gov.br/gestao/pt-br/assuntos/estatais/transparencia/dados-abertos',
]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            href = dict(attrs).get('href')
            if href: self.hrefs.append(href)

def extract(html, page):
    p = Links(); p.feed(html)
    urls = set()
    for href in p.hrefs:
        u = urljoin(page, href).split('#', 1)[0]
        parsed = urlparse(u)
        if parsed.scheme != 'https' or parsed.hostname != 'www.gov.br': continue
        path = unquote(parsed.path).lower()
        if path.endswith(('.xlsx', '.xls', '.csv', '.zip', '.pdf')) or '@@download' in path or 'sestdadosfinanceiros' in path:
            urls.add(u)
    return sorted(urls)

def collect(fetch):
    output = {}
    for url in PAGES:
        body = fetch(url)
        links = extract(body, url)
        if not links: raise ValueError(f'Sem documentos reconhecidos em {url}: preservando catálogo anterior')
        output[url] = links
    return {'origem': 'SEST / Ministério da Gestão', 'paginas': output,
            'aviso': 'Catálogo de documentos, não dados financeiros extraídos. Publicação de valores requer metodologia validada.'}

def online_fetch(url):
    req = Request(url, headers={'User-Agent':'BrasilEmDados/1.0', 'Accept':'text/html'})
    with urlopen(req, timeout=35) as response:
        return response.read().decode('utf-8-sig', errors='replace')

def update(fetch=online_fetch, path=CATALOG):
    new = collect(fetch)
    if path.exists():
        old = json.loads(path.read_text(encoding='utf-8'))
        # Proteger contra falhas temporárias que fariam desaparecer fontes.
        for page, prev in old.get('paginas', {}).items():
            if page in new['paginas'] and set(prev) - set(new['paginas'][page]):
                # Remoções podem ser legítimas, mas exigem investigação.
                raise ValueError(f'Links oficiais desapareceram de {page}; catálogo anterior preservado')
    encoded = json.dumps(new, ensure_ascii=False, indent=2) + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != encoded:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(encoded, encoding='utf-8', newline='\n')
        return True
    return False

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--offline-dir',type=Path)
    args=parser.parse_args()
    if args.offline_dir:
        mapping={page:(args.offline_dir / f'pagina{i}.html').read_text(encoding='utf-8') for i,page in enumerate(PAGES)}
        changed=update(fetch=lambda url:mapping[url])
    else: changed=update()
    print('SEST: catálogo atualizado' if changed else 'SEST: catálogo sem mudanças')
