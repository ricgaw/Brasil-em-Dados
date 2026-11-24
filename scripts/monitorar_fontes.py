"""Verifica acessibilidade de URLs primárias, sem alterar a base nem interpretar indisponibilidade como dado falso.
Gera relatório para auditoria; não faz scrape oculto, nem marca promessas como cumpridas.
"""
from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import datetime as dt
import json
import os

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
KEYS=['presidencia','historico','ibge2020','ibge','rreo','siop','tse','receita','sal2011','sal2015','sal2023']
results=[]
URLS=[(key,DATA['sources'][key]) for key in KEYS]
URLS += [('caso:'+c['id'],c['source']) for c in DATA.get('cases',[])]
for key,url in URLS:
    item={'fonte':key,'url':url,'estado':'não testado','http_status':None}
    for method in ('HEAD','GET'):
        try:
            req=Request(url,method=method,headers={'User-Agent':'BrasilEmDados/1.1 (verificacao editorial de fontes; sem coleta de dados)'})
            with urlopen(req,timeout=12) as r:
                item.update(estado='acessível',http_status=r.status)
            break
        except HTTPError as e:
            item.update(estado='verificação inconclusiva',http_status=e.code)
            if method=='GET' or e.code not in (403,405,429):break
        except (URLError, TimeoutError, OSError) as e:
            item.update(estado='verificação inconclusiva',observacao=str(e)[:160])
            if method=='GET':break
    results.append(item)
out={'gerado_utc':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),'tipo':'checagem de acessibilidade, não validação do conteúdo','resultados':results}
p=ROOT/'reports';p.mkdir(exist_ok=True)
(p/'fontes_status.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in results:print(r['fonte'],r['estado'],r['http_status'])
print('Relatório em reports/fontes_status.json; não altera dados publicados.')
