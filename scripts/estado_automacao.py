#!/usr/bin/env python3
"""Resumo offline do que EXISTE no checkout; não consulta PRs nem a internet."""
import csv
import json
from pathlib import Path
from auditar_pipeline import ROOT, run as audit


def rows_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file, delimiter=';'))


def status(root=ROOT):
    root = Path(root)
    years_dir = root/'data'/'siop_anos'
    aud = audit(years_dir)
    years = sorted(set(a['ano'] for a in aud['observacoes']))
    consolidated = rows_csv(root/'data'/'alteracoes_orcamentarias.csv')
    rows = [r for r in consolidated if r.get('id_escopo','').startswith('funcao-')]
    consolidated_years = sorted(set(int(r['ano']) for r in rows))
    social = rows_csv(root/'data'/'indicadores_sociais.csv')
    cpgf = rows_csv(root/'data'/'cpgf_resumo.csv')
    return {
        'tipo': 'estado_do_checkout_nao_do_github',
        'anos_siop_presentes_na_main_local': years,
        'arquivos_siop_anuais_ou_snapshots': len(aud['observacoes']),
        'anos_siop_consolidados_no_csv_local': consolidated_years,
        'linhas_siop_consolidadas': len(rows),
        'linhas_indicadores_sociais': len(social),
        'linhas_cpgf_resumo': len(cpgf),
        'avisos': [
            'Não representa PRs abertas nem execuções remotas do GitHub.',
            'Presença de arquivo não equivale à conferência externa do número com a fonte original.',
            'Não concluir que gastos de cartões são pessoais do presidente.'
        ],
    }


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--saida', default='reports/estado_automacao.json')
    args = p.parse_args()
    result = status()
    dest = Path(args.saida)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('SIOP presentes:', result['anos_siop_presentes_na_main_local'])
    print('SIOP consolidados:', result['anos_siop_consolidados_no_csv_local'])
    print('Relatório:', dest)
