# Brasil em Dados — Plano de cobertura V7

**Data de revisão:** 25/11/2026. Esta atualização preserva o site e a coleta SIOP existente.

## Inserido com dados oficiais
- Indicador PNAD Contínua: taxa anual de desocupação 2012–2025, Brasil, 14 observações (fonte: retrospectiva IBGE).
- IPCA acumulado em cada ano, 2020–2024, 5 observações, séries históricas IBGE.
- Filtro por mandato e gráfico de linhas; 2016 assinalado como ano de transição Dilma–Temer.

## Estruturado mas ainda sem totais oficiais validados
- Cartão de Pagamento do Governo Federal (CPGF); despesas de órgãos e unidades da Presidência; viagens; emendas; obras; dívida pública; vínculos empresariais documentados.
- Base de fontes revisáveis `data/frentes_fiscalizacao.csv`, publicada no site. Não há valores numéricos inventados, rankings de governos ou acusações.

## Próximas coletas necessárias
1. CPGF: baixar CSVs mensais da CGU; identificar exatamente o recorte do órgão da Presidência, competência, cobertura, dados reservados e variações de estrutura administrativa. Somente após isso calcular valores.
2. Viagens: cruzar tabelas Viagem/Passagem/Pagamento/Trecho sem somar a mesma despesa duas vezes.
3. Presidência: criar dicionário de órgãos e unidades com histórico de códigos; distinguir remuneração e despesas institucionais.
4. Emendas e obras: integrar Transferegov/Obrasgov, com ID estável, estágio e datas; não contar anúncio como entrega.
5. Dívida pública: usar série temporal e conceito consistente do Banco Central, preferencialmente dívida bruta/PIB.
6. Empresas/familiares: confirmar identidade, datas, CNPJ/QSA, vínculos e contratos oficiais; não declarar favorecimento sem investigação/decisão ou evidência sólida e direito de resposta.
7. Retomar SIOP para dotação inicial/atualizada em 2011–2026, preservando auditoria das funções especiais, depois de inspecionar a primeira coleta completa.

## Limitações
Os novos indicadores mostram condições do país **durante** os mandatos, não causalidade pessoal. Não há dados PNAD de desocupação para 2011 com a mesma série. 2026 é incompleto e não está no gráfico anual. IPCA 2011–2019 e 2025–2026 ainda não foram importados nesta versão, embora existam fontes oficiais.

## Fontes
- PNAD anual: https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Principais_destaques_PNAD_continua/2012_2025/PNAD_continua_retrospectiva_2012_2025.pdf
- IPCA: https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html?=&t=series-historicas
- CPGF: https://portaldatransparencia.gov.br/download-de-dados/cpgf
- Viagens: https://portaldatransparencia.gov.br/download-de-dados/viagens
- Transferegov / Obrasgov: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/paineis-gerenciais
- Banco Central: https://www.bcb.gov.br/estatisticas/estatisticasfiscais
