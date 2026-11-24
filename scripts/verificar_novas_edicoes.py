"""Detecta edições de tabelas orçamentárias do IBGE potencialmente novas.

Não extrai números, modifica arquivos do site, nem afirma atualização quando houve
bloqueio HTTP. Apenas sinaliza a possibilidade de revisar uma edição oficial.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
URL_PATTERN='https://anuario.ibge.gov.br/{year}/agregados-macroeconomicos/financas-publicas.html'
REPORT=ROOT/'reports'/'novas_edicoes_ibge.json'


def detect_year(html: str, year: int) -> bool:
    """True apenas se a página contiver uma referência à TABELA de funções terminada no ano."""
    normalized=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',html)).lower()
    year=str(year)
    # Anuário pode usar hífen ou travessão e prefixar o número da tabela.
    return bool(re.search(r'despesa(?:s)? realizada(?:s)? da união,? segundo as funções\s*[-–—]\s*\d{4}\s*[-–—]\s*'+year+r'\b',normalized))


def scan(year: int) -> dict:
    url=URL_PATTERN.format(year=year)
    result={'edicao':year,'url':url,'estado':'inconclusivo','referencia_tabela_detectada':False}
    try:
        req=Request(url,headers={'User-Agent':'BrasilEmDados/1.2 (+monitoramento de publicacoes estatisticas)'})
        with urlopen(req,timeout=20) as res:
            content=res.read(1_000_000).decode('utf-8',errors='replace')
            result['http_status']=res.status
        result['referencia_tabela_detectada']=detect_year(content,year)
        result['estado']='nova_tabela_indicada' if result['referencia_tabela_detectada'] else 'sem_tabela_identificada'
    except HTTPError as exc:
        result['http_status']=exc.code
        result['observacao']='HTTP não permite concluir sobre edição publicada'
    except (URLError,TimeoutError,OSError) as exc:
        result['observacao']=type(exc).__name__
    return result


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args()
    if args.self_test:
        yes='<p>7.1.1.2 - Despesa realizada da União, segundo as funções - 2022-2025</p>'
        assert detect_year(yes,2025)
        assert not detect_year(yes,2026)
        assert not detect_year('<p>Despesas realizadas pela União 2006-2025</p>',2025)
        print('OK: detector de edições sem acesso à internet')
        return
    results=[scan(y) for y in (2025,2026)]
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps({'gerado_utc':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),'nota':'Detecção de edição, não coleta ou validação de números','resultados':results},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    for r in results:print(r['edicao'],r['estado'])
    # O GITHUB_OUTPUT permite que o workflow alerte uma vez, sem publicar números.
    import os
    output=os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output,'a',encoding='utf8') as f:
            f.write('nova_tabela='+('true' if any(r['referencia_tabela_detectada'] for r in results) else 'false')+'\n')

if __name__=='__main__':main()
