# Brasil em Dados 🇧🇷

**Quatro mandatos presidenciais · 2011 a 2026 · Fontes públicas e contexto.**

Um portal independente para entender atos de governo, orçamento federal, indicadores sociais e investigações documentadas, sem notas para presidentes e sem atribuir automaticamente a um governante todos os resultados de seu período.

**[Acessar o site](https://ricgaw.github.io/Brasil-em-Dados/)**

## Explore o portal

- **Panorama por mandato:** fichas documentadas, cobertura orçamentária e indicadores disponíveis.
- **Presidentes e vice-presidentes:** trajetória, período no cargo e subsídio de referência legal.
- **Políticas públicas:** programas, leis e medidas com busca e filtros por período e área.
- **Orçamento:** despesas liquidadas (IBGE/Tesouro, 2020–2024) e dotações iniciais, atualizadas e liquidadas por função, quando os exercícios já estiverem consolidados no SIOP.
- **Indicadores sociais:** IPCA anual (2011–2025) e desocupação anual (2012–2025), com fontes do IBGE.
- **Dívida pública:** DBGG/PIB anual de 2011–2025, com 2026 parcial e fonte Banco Central (SGS 13762).
- **Estatais:** Petrobras, Banco do Brasil, Caixa e Correios, com resultados oficiais documentados e lacunas claramente identificadas.
- **Escândalos e investigações:** casos com fontes, contexto, estado documental e limites de atribuição.
- **Impostômetro:** projeção ilustrativa identificada e link para a contagem oficial da ACSP.

## Princípios

Orçamento previsto, atualizado, empenhado, liquidado e pago são etapas diferentes. Valores ausentes não equivalem a zero. Em 2016 houve dois presidentes, e 2026 permanece um exercício parcial. Fontes, metodologia e recortes devem ser conferidos antes de qualquer comparação causal. Investigação não é condenação; vínculo familiar ou societário não demonstra, sozinho, irregularidade.

## Código e atualização

O site está hospedado no GitHub Pages. Os arquivos aprovados entram em `main` e passam por testes antes da publicação. Os dados SIOP são coletados por ano e dependem de revisão e consolidação antes de aparecer nos gráficos. Os painéis de cartões, viagens, emendas, obras e contratos foram retirados da interface pública a pedido do mantenedor; seus coletores não foram apagados do histórico.

- [Guia de coleta incremental SIOP](GUIA_COLETA_INCREMENTAL_V10.md)
- [Reorganização das automações](GUIA_REORGANIZACAO_AUTOMACAO_V12.md)
- [Atualização editorial final V14](GUIA_ATUALIZACAO_FINAL_V14.md)
- [Cobertura e limitações](RELATORIO_DE_COBERTURA.md)

## Transparência

Este é um projeto cívico independente, sem vínculo com partidos, candidatos ou órgãos públicos, e não constitui auditoria oficial. Para indicar erro factual ou desdobramento documental, [abra uma solicitação de correção](https://github.com/ricgaw/Brasil-em-Dados/issues/new) com fontes verificáveis.


### Última ampliação editorial — V15

O portal contém dossiês de cobertura por mandato, matriz anual de disponibilidade e diretório de fontes oficiais. A seleção de atos normativos foi ampliada com legislação federal e ressalvas sobre o que ainda não é demonstrável. Os painéis distinguem despesa institucional, dados sociais e arrecadação das três esferas. **Valores ausentes não são tratados como zero.**

A base de arquivos do SIOP aprovada posteriormente à cópia utilizada para esta atualização **não deve ser substituída** pelo ZIP. Instale somente os arquivos alterados; confira a `main` antes do commit.
