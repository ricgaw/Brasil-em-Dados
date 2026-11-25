# Brasil em Dados 🇧🇷

**Quatro mandatos presidenciais, dados públicos e contexto para entender o Brasil.**

O **Brasil em Dados** é um projeto independente de informação e transparência pública. Reúne documentos oficiais sobre a Presidência da República e os governos federais de **2011 a 2026**, com linguagem acessível, gráficos e links para as fontes originais.

### 🌐 Acesse o site

**[Abrir o Brasil em Dados](https://ricgaw.github.io/Brasil-em-Dados/)**

## O que você encontra

- **Presidentes e vice-presidentes:** perfis, períodos no cargo e referências legais de remuneração.
- **Mandatos:** 2011–2014, 2015–2018, 2019–2022 e 2023–2026, com a transição entre Dilma Rousseff e Michel Temer identificada em 2016.
- **Políticas públicas:** leis, programas e medidas documentadas, com indicação do que ainda precisa ser verificado.
- **Orçamento federal:** evolução das despesas por função, incluindo Saúde, Educação, Cultura e outras áreas.
- **Mudanças no orçamento:** comparação entre dotação inicial e atualizada quando há dados oficiais compatíveis.
- **Escândalos e investigações:** casos documentados, com contexto, fontes e distinção entre investigação, acusação e decisão judicial.

## Como interpretamos os dados

O projeto **não é vinculado a partidos políticos** e não atribui automaticamente a um presidente todos os acontecimentos de seu mandato. Procuramos distinguir:

- **Orçamento autorizado** de **despesa efetivamente executada**;
- **Aumento ou redução de dotação** de **bloqueio, contingenciamento ou saldo não gasto**;
- **Promessa, medida adotada e resultado comprovado**;
- **Investigação, denúncia, julgamento e condenação**.

Dados ausentes não são tratados como zero. Um vínculo familiar ou societário, por si só, não é prova de irregularidade.

## Fontes e cobertura

Utilizamos documentos e dados públicos do **Tesouro Nacional**, **SIOP**, **IBGE**, **TSE**, **Receita Federal**, legislação federal e órgãos de controle. Cada informação do site deve permitir rastrear a fonte utilizada.

A série orçamentária histórica e os levantamentos de promessas e vínculos societários **ainda estão em ampliação**. O exercício de 2026 não está encerrado; números parciais não são apresentados como totais anuais.

**[Relatório de cobertura e limitações](RELATORIO_DE_COBERTURA.md)**

## Atualização dos dados

O GitHub Actions executa testes e publica o site quando as alterações validadas chegam à branch `main`. Há também monitoramento de fontes e um coletor do SIOP em fase de integração. **A coleta histórica completa ainda depende de validação**, e os resultados novos devem ser revisados antes da publicação.

Para detalhes de operação, consulte o [guia de coleta do SIOP](GUIA_COLETA_SIOP_V6.md) e o [guia de automação](GUIA_AUTOMACAO_V5.md).

## Sobre o projeto

O Brasil em Dados é uma iniciativa cívica independente, com finalidade informativa. Não constitui auditoria oficial, investigação criminal ou recomendação de voto. Correções devem ser sustentadas por documentação verificável.

**[Visitar o site](https://ricgaw.github.io/Brasil-em-Dados/)** · **[Consultar as fontes e limitações](RELATORIO_DE_COBERTURA.md)**

### Novas áreas (V7)

- **Indicadores sociais por governo:** série anual nacional da desocupação (2012–2025) e IPCA (2020–2024), com fontes IBGE, gráfico, filtros e CSV.
- **Gastos e controle social:** fontes e critérios para cartões corporativos, despesas institucionais, viagens, emendas, obras, dívida e vínculos documentados. **Os valores dessas frentes ainda não foram consolidados**; não são exibidos números estimados.

Para ampliar a cobertura, veja [Plano de atualização V7](PLANO_ATUALIZACOES_V7.md).
