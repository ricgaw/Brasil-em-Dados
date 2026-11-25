# Brasil em Dados — quatro mandatos presidenciais (2011–2026)

**Versão editorial de 24 de novembro de 2026.** Site estático, independente, sem afiliação política. Mantido o layout aprovado na versão inicial.

## Abrir o site

Extraia todo o ZIP e abra **`index.html`** no navegador. `data.js` contém uma cópia embutida da base para funcionar também via `file://`. Retratos externos e fontes precisam de conexão com a internet.

## Conteúdo desta entrega

- **Quatro mandatos:** 2011–2014; 2015–2018 (Dilma até 31/08/2016 e Temer depois); 2019–2022; 2023–2026 (ano ainda em curso na data de corte).
- **Seis pessoas:** Dilma Rousseff, Michel Temer, Jair Bolsonaro, Hamilton Mourão, Luiz Inácio Lula da Silva, Geraldo Alckmin. Os vices aparecem em cada mandato; Temer aparece também como presidente durante a segunda parte de 2015–2018.
- **Subsídios legais de referência**, com links aos decretos; não representam o líquido recebido, nem exaurem reajustes e parcelas específicas.
- **10 fichas em “Escândalos e investigações”**, agrupadas por mandato, com distinção entre denúncia, investigação, julgamento e situação documentada. A inclusão não afirma culpa de presidentes.
- **24 fichas de políticas e atos**, classificadas como leis/normas, anúncios ou resultados ainda a verificar. Datas e normas são atribuídas ao período correspondente; atribuição de Dilma/Temer é separada dentro do mesmo mandato.
- **28 funções orçamentárias**, com **139 registros anuais validados de 2020–2024**, em R$ milhões correntes, métrica **despesa liquidada da União**. O gráfico mostra R$ bilhões. Para Habitação, **2023 permanece não disponível** na tabela oficial; não foi preenchido como zero.
- **Fontes primárias no site**, CSV e JSON para reprodução, testes de consistência e workflow de publicação por GitHub Pages após configurar um repositório novo.
- **Monitor semanal de disponibilidade de links**, agora incluindo as URLs das investigações, sem alterações automáticas nos valores (relatórios salvos como artefatos no GitHub Actions).

## Novo módulo — Escândalos e investigações

O site apresenta **10 casos com fonte**, agrupados pelos quatro mandatos. Há um filtro por mandato e natureza do procedimento. Cada card informa: período, fatos documentados, estado confirmado na fonte, limite probatório e link primário. Os casos foram selecionados para apresentar exemplos relevantes **sem estabelecer uma hierarquia entre governos**. Não se devem comparar contagens como se fossem quantidade total de irregularidades; a base não é exaustiva.

Para manter a transparência, o material classifica o julgamento do Mensalão em 2012 como relacionado a fatos anteriores; separa Dilma e Temer em 2015–2018; identifica processos relativos a emendas parlamentares como envolvendo Congresso e Executivo; e sinaliza que os descontos do INSS apurados em 2025 abrangem fatos de 2019 a 2024. Situações processuais podem mudar e exigem reconfirmação antes de afirmar uma conclusão atualizada.

A fonte controlada da seção é `data/casos_documentados.json`. O `scripts/build.py` a incorpora ao `data/atlas.json` e ao `data.js`; o `scripts/validate.py` garante a reprodução e integridade básica. O monitor semanal testa também a acessibilidade das fontes dos casos, sem alterar dados automaticamente.

## Limitações importantes — NÃO é uma auditoria exaustiva dos quatro mandatos

1. **Despesas 2011–2019:** não inseridas, porque não houve exportação e validação de uma série homogênea na mesma métrica. Nos gráficos esses anos aparecem como lacuna, não como zero.
2. **Despesas 2025–2026:** não inseridas ainda. Para 2026, os relatórios são parciais e não devem ser comparados com anos fechados sem avisos metodológicos. O Tesouro possui Anexo 02 do RREO com dados por função; falta consolidar o fechamento por exercício.
3. **Programas eleitorais 2010, 2014, 2018, 2022:** a base de 24 fichas representa *atos documentados e exemplos selecionados*, não todas as promessas de campanha. Precisa vincular cada promessa ao texto oficial registrado no TSE antes de classificá-la como entregue.
4. **Participações societárias:** não há vínculos individualizados confirmados por CNPJ/QSA histórico para os seis agentes. A ficha mostra a pendência e não afirma que a pessoa possui ou não empresas. Não publicar listas por correspondência de nomes.
5. **Salários individuais:** subsidio legal bruto ≠ remuneração líquida, diárias, benefícios ou total recebido. É preciso consultar folhas históricas e exceções normativas; os dados apresentados são *referências legais*.
6. **Indicadores de resultados e causalidade:** atos normativos não comprovam melhoria de serviço nem cumprimento integral de compromisso. Avaliar séries independentes por área.
7. **Automação de atualização dos números:** o monitor verifica a acessibilidade de fontes; ele **não coleta ou modifica séries do RREO/TSE automaticamente**. Publicação acontece após `push` ao repositório configurado.

## Reproduzir e testar

```bash
python scripts/build.py
python scripts/validate.py
```

`build.py` gera `data/atlas.json`, `data.js`, `data/orcamento_2020_2024_ibge.csv`. `validate.py` reconstrói os arquivos e exige bytes idênticos, além de conferir fontes, intervalos, ausência de duplicação e contagens.

## Arquivos

- `index.html`, `app.js`, `styles.css`, `data.js`: site estático e interativo
- `scripts/build.py`: base controlada e com fontes, reprodutível
- `scripts/validate.py`: testes locais e CI
- `scripts/monitorar_fontes.py`: verifica acesso a páginas de referência e registra indisponibilidade, não dados
- `data/atlas.json`: dados e metadados disponíveis no site
- `data/casos_documentados.json`: fichas editoriais de escândalos, investigações e decisões
- `data/escandalos_investigacoes.csv`: exportação legível das fichas e suas fontes
- `data/orcamento_2020_2024_ibge.csv`: despesas validadas, função/ano
- `RELATORIO_DE_COBERTURA.md`: distinção entre entregas e lacunas
- `.github/workflows/validar.yml`: testes automáticos
- `.github/workflows/publicar.yml`: publicação GitHub Pages ao enviar commit para main
- `.github/workflows/monitorar-fontes.yml`: monitor semanal apenas de URLs

## Publicar de forma independente

Crie um repositório **novo** (ex.: `Brasil-em-Dados`), copie estes arquivos para a raiz da branch `main` e ative **Settings > Pages > Source: GitHub Actions**. Não use o repositório do Maringá em Dados e não compartilhe secrets entre os projetos. Sem repositório configurado, os workflows ainda não estão ativos.

## Fontes principais

- [IBGE — despesas por função 2020–2023](https://anuario.ibge.gov.br/images/aeb/2023/s7/2_pdf/s7t1102.pdf)
- [IBGE — despesas por função 2021–2024](https://anuario.ibge.gov.br/images/aeb/2024/s7/2_pdf/s7t1102.pdf)
- [Tesouro Nacional — RREO da União](https://www.tesourotransparente.gov.br/temas/contabilidade-e-custos/relatorio-resumido-da-execucao-orcamentaria-rreo-uniao)
- [TSE — candidaturas e programas](https://divulgacandcontas.tse.jus.br/divulga/#/)
- [Receita Federal — CNPJ/QSA](https://www.gov.br/pt-br/servicos/consultar-cadastro-nacional-de-pessoas-juridicas)
- [Legislação — Presidência da República](https://legislacao.presidencia.gov.br/)

As demais fontes estão vinculadas diretamente a cada ficha e listadas em `data/atlas.json`.

## Atualização de 24/11/2026 — funções e arquivos publicados

- **139 observações anuais e 28 funções orçamentárias**: incluídas 12 funções adicionais diretamente das tabelas 7.1.1.2 do AEB 2023 (2020) e AEB 2024 (2021–2024), mantendo despesa **liquidada**, em R$ milhões nominais.
- A função **Encargos especiais** possui valores muito altos porque é rubrica contábil que inclui obrigações financeiras; não a interprete como serviço prestado.
- **Habitação/2023** continua não informada, jamais convertida para zero.
- **Corrigido deploy:** o workflow inclui `data/escandalos_investigacoes.csv` na pasta publicada, com verificações de presença para evitar links de download quebrados.
- A validação verifica quantidade de funções, anos, valores de controle e o conteúdo exportado.
- **Não foi adicionada série 2011–2019 nem 2025–2026**, pois ainda falta exportação homogênea validada.

## Monitoramento automático de edições do IBGE

O workflow `.github/workflows/novas-edicoes-orcamento.yml` consulta **toda quarta-feira** os índices de 2025 e 2026 e disponibiliza um relatório no GitHub Actions. Se encontrar menção a uma tabela nova, tenta criar **uma única issue de revisão editorial**. Não integra números sem verificações; falhas de acesso permanecem inconclusivas. Esse monitor depende da disponibilidade do portal e de Issues habilitadas para os alertas, mas o relatório sempre é gerado quando a ação executa. Execute `python scripts/verificar_novas_edicoes.py --self-test` para testar o detector offline.


## Atualização V4 — Orçamento inicial, aumentos e reduções (24/11/2026)

A nova seção `#alteracoes` foi acrescentada **sem alterar o desenho nem os dados anteriores**. Ela apresenta dotações iniciais e atualizadas de um mesmo recorte administrativo, com variação líquida em R$ e %, filtros por ano/área/direção, barras comparativas, referências e exportação CSV.

- **2 exemplos oficiais reproduzíveis:** Ministério da Saúde (órgão 36000, total) e Fundação Oswaldo Cruz (unidade 36201, subconjunto do ministério), no **1º quadrimestre de 2026**. O ministério reduziu a dotação líquida em R$ 427.049.850 (−0,16%), e a Fiocruz aumentou em R$ 614.726.417 (+6,43%). São escopos sobrepostos, **não se somam**.
- **Fonte:** Ministério da Saúde, [1º Relatório Quadrimestral de Prestação de Contas de 2026](https://bvsms.saude.gov.br/bvs/publicacoes/1_rqpc_2026.pdf), Quadro de Execução Orçamentária, posição de abril de 2026 / Tesouro Gerencial. A posição não equivale ao fechamento de 2026 nem à situação corrente em novembro.
- **Limite:** não temos ainda série homogênea de **dotação inicial x atualizada por função orçamentária para os anos 2011–2026**, especialmente Educação e Cultura. O gráfico inicial da seção não deve ser confundido com o gráfico histórico de **despesa liquidada por função de governo**, obtido do IBGE/Tesouro e preservado na área Orçamento.
- **Distinções:** (a) PLOA = proposta; (b) LOA/dotação inicial = autorizado inicialmente; (c) dotação atualizada = autorizado após alterações; (d) empenhado, liquidado e pago são etapas de execução; (e) bloqueio/contingenciamento não equivale necessariamente a redução de dotação.
- **Evolução em linha:** a nova seção está preparada para gerar linha anual de dotação inicial/atualizada quando forem importados pelo menos dois anos do **mesmo recorte**. Lacunas não viram zero. Para fins de análise de aumento/redução por mandato, serão necessários dados oficiais e metodologia igual em todos os exercícios, com ajuste opcional pela inflação.

### Reproduzir a seção

```bash
python scripts/build_alteracoes.py
python scripts/validate.py
```

A fonte controlada é `data/alteracoes_orcamentarias.csv`. São obrigatórios ano, área, escopo, identificação do recorte, data, dotações inicial/atualizada, fonte URL e nota metodológica. O script valida números inteiros em reais e gera `alteracoes.js` para abrir offline com `index.html`. Não realiza coleta automática nem insere registros sem revisão documental.

A publicação no GitHub Pages inclui `alteracoes.js`, `alteracoes-app.js` e `data/alteracoes_orcamentarias.csv`. Nenhum repositório foi alterado automaticamente nesta entrega.

**Para ampliar:** use o [Painel do Orçamento/SIOP](https://www1.siop.planejamento.gov.br/) ou [Orçamento Cidadão](https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:orcamento_cidadao) para extrair, por função e exercício, as colunas Dotação Inicial/Atual, Empenhado/Liquidado/Pago. Identifique esfera, órgão/UO, função, data de atualização e trate mudanças na classificação histórica antes de reunir diferentes anos.


## V5 — Catálogo orçamentário e fluxo de ingestão (24/11/2026)

Foram incorporadas as **28 funções** a uma nova visualização no módulo de alterações, com minigráficos de liquidação 2020–2024 e matriz de disponibilidade 2011–2026. O CSV de alterações continua com **2 observações de órgãos/unidade** de abril de 2026; não foram criadas dotações de função sem fonte. O workflow de importação semanal só opera após configurar uma URL oficial normalizada `SIOP_CSV_URL`; cria PR para revisão, não faz merge de valores não auditados. Consulte `GUIA_AUTOMACAO_V5.md`.


## Integração SIOP V6 — coleta auditada e proposta de PR

Integração técnica com os arquivos oficiais SIOP LOA CSV.gz e SHA-256: scripts/coletar_siop_loa.py, workflow mensal .github/workflows/coletar-siop-loa.yml e testes em tests/test_coletar_siop.py. Os dados são agregados por função e esferas Fiscal/Seguridade; o coletor apresenta propostas para revisão por Pull Request sem sobrescrever a base anterior. Uma carga histórica 2011–2026 pode ser executada manualmente no Actions. Nesta entrega **não foram incorporados novos números**: a execução remota real do download oficial e da publicação ainda precisa ser confirmada. Orientações e limites: GUIA_COLETA_SIOP_V6.md.
