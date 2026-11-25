# Relatório de cobertura — Brasil em Dados

**Corte:** 24/11/2026. **Finalidade:** discriminar informações verificadas, questões sem fonte homogênea e próximos passos. Não atribuir desempenho nem comparar presidentes por soma nominal de valores.

## Verificado e integrado

| Conteúdo | Cobertura | Origem/limitação |
|---|---|---|
| Mandatos e exercício presidencial | 2011–2026, quatro mandatos | Histórico institucional; 2015–2018 dividido entre Dilma e Temer |
| Fichas pessoais (presidente/vice) | Seis pessoas | Identidade, papel, partido eleitoral, fotos externas e nota de societárias pendentes |
| Subsídio legal bruto | Marcos normativos selecionados | Não é folha individual, líquido ou benefício adicional |
| Escândalos e investigações | 10 fichas documentadas, quatro mandatos | Fontes oficiais; situações processuais referidas à fonte, sem culpa por associação nem cobertura exaustiva |
| Medidas documentadas | 24 fichas selecionadas | Normas e programas; não são todas as promessas eleitorais |
| Despesa federal por função | 2020–2024 | 28 funções, 139 pontos; RREO/IBGE, despesa liquidada nominal |
| Transparência da lacuna de dados | Todas as páginas | 2011–2019 e 2025–2026 ausentes não são exibidos como zero |
| Publicação após commit | Configurada para GitHub Pages | Só funciona depois de criar e configurar novo repositório |
| Monitor de fontes | Semanal após publicação | URLs e status, não executa coleta de dados orçamentários |

## Limites do novo módulo de escândalos e investigações

- O número de fichas em cada mandato **não é estatística de corrupção** nem método de avaliação de governos: casos selecionados dependem da disponibilidade e do escopo das fontes.
- Mensalão: julgamento em 2012 de fatos anteriores a 2011. Lava Jato: iniciada em 2014 e relacionada a vários períodos. Emendas RP 9: decisões sobre regras institucionais com múltiplos poderes.
- INSS: operações em 2025 sobre descontos de 2019–2024; não transformar soma de descontos associativos em valor de fraude definitivamente confirmado.
- Câmara não autorizou abertura do processo contra Temer durante a Presidência em 2017; isso não corresponde a julgamento de mérito.
- A seção foi revisada a partir de fontes institucionais, mas não é um sistema de acompanhamento judicial em tempo real.

## Próximas integrações recomendadas

1. **Alta prioridade:** baixar e validar 2011–2019 da mesma classificação funcional e métrica liquidada da União. Conciliar eventuais revisões nas edições IBGE/STN antes da publicação. Não trocar por série de 'despesa paga' silenciosamente.
2. **Alta prioridade:** extrair 2025 (fechamento) e 2026 (acumulado até o último bimestre disponível) do Anexo 02 do RREO. Marcar 2026 parcial com período de referência.
3. **Alta prioridade:** vincular planos de governo registrados no TSE (2010, 2014, 2018 e 2022) a atos, entregas e indicadores mensuráveis. Exibir fonte e marco de cada classificação.
4. **Média prioridade:** tabelas por exercício do subsídio legal e contracheques públicos verificados por pessoa e cargo; preservar privacidade de dados pessoais irrelevantes.
5. **Média prioridade:** sociedades por pessoa após identificação documental do CNPJ e QSA histórico, distinguindo participação atual, encerrada, homônimos e entidades públicas. Sem inferir por sobrenome.
6. **Média prioridade:** séries de indicadores (IBGE, Banco Central, Ipea) e correção monetária por IPCA, sempre separando correlação de causalidade.
7. **Média prioridade:** coletores oficiais com validação de schema, versionamento, rastreabilidade, bloqueio em caso de inconsistência e revisão humana das classificações editoriais.

## Observações de metodologia

- *Alocação orçamentária* (dotação), *empenho*, *liquidação* e *pagamento* são fases diferentes. O gráfico atual é apenas liquidação.
- O acumulado de áreas federais não representa despesas de estados e municípios.
- A função **Habitação** tem valor não reportado como despesa liquidada em 2023 na tabela consultada; a lacuna é mantida como ausência, e não zero.
- O ano 2020 foi obtido da edição 2023 do Anuário; 2021–2024 da edição 2024. A unidade é milhões de reais correntes e o escopo exclui intraorçamentárias.
- 2016 foi ano dividido entre duas presidências. O gráfico por exercício do mandato 2015–2018 não deve atribuir integralmente o ano a um só presidente.

## Expansão rastreável desta edição

Foram incorporadas 12 funções adicionais: Legislativa, Judiciária, Essencial à Justiça, Relações exteriores, Direitos da cidadania, Urbanismo, Organização agrária, Indústria, Comércio e serviços, Comunicações, Desporto e lazer e Encargos especiais. Todas as observações possuem fonte `ibge2020` (2020) ou `ibge` (2021–2024).

Fonte AEB 2023: https://anuario.ibge.gov.br/images/aeb/2023/s7/2_pdf/s7t1102.pdf  
Fonte AEB 2024: https://anuario.ibge.gov.br/images/aeb/2024/s7/2_pdf/s7t1102.pdf

Foi incluída checagem no CI para impedir publicação sem o CSV de investigações. Valores de 2011–2019 e 2025–2026 continuam pendentes; nenhuma interpolação.

**Automação adicional:** detector semanal de novas tabelas do AEB (2025/2026) com artefato de execução e alerta editorial em issue; não faz ingestão numérica automática, pois uma nova edição pode revisar a metodologia da série e deve ser validada. Sem confirmação do valor por função, permanece lacuna.


## V4 — acompanhamento de dotações, 24/11/2026

Adicionado módulo para rastrear **orçamento inicialmente aprovado (LOA) × dotação atualizada**, cálculo de aumento/redução líquido em reais e percentual, com 2 observações verificadas do 1º quadrimestre de 2026 (MS total e Fiocruz). Dados oficiais do RQPC do Ministério da Saúde, não uma série anual fechada. As amostras são recortes **sobrepostos** e não podem ser somadas. Séries 2011–2025, Educação e Cultura ainda **não** têm preenchimento inicial/atualizado auditado neste pacote. O RREO/IBGE 2020–2024 continua separado porque mede **despesa liquidada por função**, não autorização orçamentária por unidade.

O SIOP permite consultar dotações desde antes de 2011, mas a coleta integral com critérios homogêneos **não foi realizada**. O gerador é determinístico e o teste impede números não inteiros, ano/data incorretos, duplicações e perda dos arquivos da implantação. A checagem visual automatizada foi bloqueada por política do navegador de teste (file:// e localhost), portanto essa revisão de interface ainda necessita inspeção no navegador do usuário.


## V5 — Cobertura por função e infraestrutura de atualização

**28 funções orçamentárias** podem ser pesquisadas no catálogo, com os **139 pontos de despesa liquidada 2020–2024** previamente verificados. Na **matriz de dotação inicial/atualizada por função de 2011–2026, ainda não existem linhas auditadas por função**; os dois recortes de 2026 referem-se ao Ministério da Saúde e à Fiocruz, que não são a função orçamentária inteira. Uma rotina de importação validada e workflow recorrente foram preparados, mas a ingestão automática depende de fonte oficial normalizada configurada e os PRs dependem de revisão antes do merge. Esta versão não declara concluída a série de dotações nem a automação numérica fim a fim.


## Integração SIOP V6 — coleta auditada e proposta de PR

Integração técnica com os arquivos oficiais SIOP LOA CSV.gz e SHA-256: scripts/coletar_siop_loa.py, workflow mensal .github/workflows/coletar-siop-loa.yml e testes em tests/test_coletar_siop.py. Os dados são agregados por função e esferas Fiscal/Seguridade; o coletor apresenta propostas para revisão por Pull Request sem sobrescrever a base anterior. Uma carga histórica 2011–2026 pode ser executada manualmente no Actions. Nesta entrega **não foram incorporados novos números**: a execução remota real do download oficial e da publicação ainda precisa ser confirmada. Orientações e limites: GUIA_COLETA_SIOP_V6.md.

## Novas seções (V7)

- **Indicadores sociais:** 14 valores anuais de desocupação (2012–2025), 5 valores do IPCA (2020–2024), fontes IBGE, CSV e filtros por mandato.
- **Cartões, Presidência, viagens, emendas, obras, dívida, vínculos:** sete frentes documentadas com fonte e metodologia proposta, **sem valores coletados/consolidados**.
- 2016: mandato com dois ocupantes, indicador anual não atribuído a um único presidente. 2026: ano em aberto.
- Novos arquivos são publicados pelo GitHub Pages e testados em `tests/test_paineis_v7.py`.
