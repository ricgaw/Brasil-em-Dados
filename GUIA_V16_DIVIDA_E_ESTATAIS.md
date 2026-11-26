# Brasil em Dados — V16 · dívida/PIB e estatais

Esta atualização é incremental sobre a V15. Substitua somente os arquivos do ZIP de atualização, mantendo `.git`, arquivos de `data/siop_anos` e os workflows de coleta.

## Conteúdo
- Dívida Bruta do Governo Geral em % do PIB (SGS 13762, BCB), observações de dezembro de 2011–2025 e junho de 2026 como dado parcial.
- Quatro cards de estatais: Petrobras, Banco do Brasil, Caixa e Correios. Resultados documentados disponíveis, sem preencher anos ou conceitos contábeis faltantes.
- Receita da Petrobras e dívida bruta em USD para 2024–2025; outros indicadores não padronizados não são apresentados como zero.
- Painéis públicos de cartões corporativos, viagens, emendas, obras e contratos retirados do menu e da página. Seu código antigo permanece no repositório e o fluxo SIOP fica intacto.

## Metodologia e limites
A DBGG não inclui a dívida própria das estatais e não é a Dívida Pública Federal (DPF), nem a Dívida Líquida do Setor Público. Dados do BCB são percentuais mensais: dezembro representa fechamento anual; junho de 2026 é parcial.
As fontes de Petrobras usam lucro líquido divulgado em 2021–2023 e lucro atribuível aos acionistas em 2024–2025; comparabilidade interanual exige exame das notas. Banco do Brasil usa lucro ajustado, Caixa lucro recorrente, Correios prejuízo líquido indicado pelo TCU. Não somar os resultados ou comparar diretamente bancos com empresas não financeiras.

## Instalação
1. `git switch main; git status; git pull --ff-only origin main` (somente com a árvore de trabalho limpa).
2. Extrair o ZIP incremental sobre a pasta do projeto.
3. `$env:PYTHONUTF8 = "1"`
4. `python -m unittest discover -s tests -p "test_*.py"`
5. `python scripts/validate.py` e `python scripts/validar_v5.py`, além de `python scripts/auditar_pipeline.py` se existir.
6. Se tudo passar, `git add .; git commit -m "Adicionar divida PIB e estatais V16"; git push origin main`.
7. Confirmar publicação e revisar os cards no GitHub Pages.

## Automação futura
Adicionar atualização revisável mensal da série SGS 13762; importar séries anuais comparáveis de cada empresa a partir dos respectivos demonstrativos, mantendo auditoria, revisão e a identificação de dados parciais.
