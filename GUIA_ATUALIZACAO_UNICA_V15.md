# Brasil em Dados — atualização editorial conjunta V14 + V15

Esta entrega substitui a atualização V14 anterior: monograma BR, panorama, ferramentas de busca e comparador orçamentário estão incluídos, além de dossiês por mandato, matriz anual de cobertura, fontes oficiais e dez fichas novas de medidas legislativas.

## Precaução antes de instalar

1. No VS Code: `git switch main`, `git status`, `git pull --ff-only origin main`. Se tiver alterações não registradas, resolva-as antes de copiar.
2. Extraia o ZIP incremental na raiz da pasta `Brasil em Dados`. Não substitua dados anuais do SIOP, `alteracoes.js`, arquivos de cartões já importados nem outros workflows.
3. Testes: `python -m unittest discover -s tests -p "test_*.py"`, `python scripts/validate.py`, `python scripts/validar_v5.py`, `python scripts/auditar_pipeline.py`.
4. Se tudo passar: `git add index.html styles.css app.js novos-paineis.js dossies-v15.js README.md GUIA_ATUALIZACAO_FINAL_V14.md GUIA_ATUALIZACAO_UNICA_V15.md scripts/build.py data/atlas.json data.js tests/test_v14_apresentacao.py tests/test_v15_editorial.py tests/test_coletar_siop.py .github/workflows/publicar.yml` e então commit/push.
5. Confira os GitHub Actions e os menus no site publicado.

## Conteúdo incluído

- Dez normas adicionais, com links para a legislação e ressalvas de resultados.
- Dossiês por mandato: resumo da cobertura efetiva do projeto, não avaliação dos presidentes.
- Matriz de 2011 a 2026: funções orçamentárias, indicadores sociais e arrecadação nacional disponível.
- Diretório temático das fontes oficiais e distinções de metodologia.
- V14 integral: monograma BR, busca e panorama.

## O que ainda não é possível chamar de completo

CPGF histórico, gastos de viagens e da Presidência, contratos, emendas, obras e histórico societário de familiares requerem coletores e revisão de fontes oficiais. A situação processual de investigações pode ter mudado. A arrecadação nacional só tem totais de 2024 e 2025 verificados na base; o contador próprio de 2026 é uma estimativa ilustrativa. Os índices sociais não abrangem todos os temas e anos. A série orçamentária recebida aqui não contém obrigatoriamente as incorporações mais recentes que estão no GitHub.

**Não é necessário reconstruir ou apagar as coletas de 2011–2026.**

O pacote também contém a correção isolada do teste de importação da V13; nenhuma fonte anual real é alterada por ela.
