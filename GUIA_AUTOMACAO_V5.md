# Brasil em Dados — importação e automação das dotações (V5)

**Corte editorial:** 24/11/2026. A identidade visual V4 foi preservada.

## Implementado nesta entrega

1. **Catálogo das 28 funções federais** na seção de orçamento e aumentos/reduções, com filtro por nome e ano, minigráficos de despesa liquidada de 2020–2024 e identificação de valores não disponíveis.
2. **Matriz 2011–2026 das dotações** por função. Mostra “—” quando falta orçamento inicial/atualizado auditado; não trata ausência como zero. Os dados de órgãos e UO (Ministério da Saúde e Fiocruz) ficam apartados da função Saúde.
3. **Importador conservador** `scripts/importar_dotacoes.py`, que exige exportação normalizada de 28 funções, valor em **reais inteiros**, fonte governamental HTTPS, referência temporal e identificador de função. Ele bloqueia registros duplicados e revisões dos dados existentes; não inventa nem sobrescreve valores.
4. **Workflow programado** às terças-feiras para buscar novo CSV **somente se** `SIOP_CSV_URL` estiver configurado com uma URL governamental que entregue exatamente o modelo normalizado. Abre PR para revisão, sem merge automático de alterações não verificadas.
5. **Testes CI e publicação GitHub Pages** com novo módulo `areas-app.js` e fontes anteriores preservadas.

## O que ainda não foi extraído

**Nenhuma série adicional de dotação inicial/atualizada foi inserida sem verificação.** Permanecem dois exemplos oficiais relativos a órgãos/unidade da Saúde em abril de 2026, e **nenhuma linha completa por função para 2011–2026**. As 28 funções foram incorporadas no catálogo e na matriz de disponibilidade, com despesa liquidada 2020–2024 do IBGE/Tesouro. Isso NÃO é uma série orçamentária integral dos quatro mandatos.

## Consultar e exportar do SIOP

1. Consulte [SIOP — Consulta Livre](https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:consulta_livre), que documenta a seleção de PLOA, Dotação Inicial, Dotação Atual, Empenhado, Liquidado e Pago desde 2000.
2. Selecione **Orçamentos Fiscal e Seguridade Social, União**, exercícios 2011–2026 e **Função** como classificador. Uma tabela por ano e função, evitando somar grupos/subfunções já incluídas.
3. Mantenha a mesma data de referência entre funções de um ano; para 2026, indicar que a execução é parcial. Preserve a URL exata da fonte e a data da extração.
4. Normalizar o CSV em UTF-8, delimitado por ponto e vírgula, seguindo `docs/MODELO_EXPORTACAO_SIOP.csv`. Os valores **devem estar em reais inteiros, sem pontos, vírgulas ou símbolo de moeda**. O CSV do SIOP em formato nativo pode exigir transformação para este modelo; não use o arquivo bruto indiscriminadamente.
5. A coluna `funcao` deve coincidir com uma das 28 denominações do catálogo (`data/atlas.json`). Não incluir Total Geral, Reserva de Contingência, órgão, UO ou subfunção como se fossem funções independentes.

### Importação local após normalização

```bash
python scripts/importar_dotacoes.py --arquivo CAMINHO/serie_validada.csv
python scripts/build_alteracoes.py
python scripts/validate.py
python scripts/validar_v5.py
```

Faça `git diff`, confira a fonte e o período, depois commit e push à branch de desenvolvimento. `main` publicará automaticamente se os testes passarem.

### Automação opcional via CSV oficial normalizado

No novo repositório do **Brasil em Dados**, em `Settings > Secrets and variables > Actions > Variables`, crie a variável de repositório `SIOP_CSV_URL` **apenas depois de identificar um endereço HTTPS governamental que entregue os campos do modelo**. Não cole endereço de página HTML, planilha com cabeçalhos diferentes, ou CSV criado pelo próprio site (evita circularidade). Essa URL não foi localizada/validada nesta entrega.

O workflow `importar-dotacoes.yml` executará semanalmente. Se não tiver variável, somente registra que falta uma origem configurada. Se houver CSV compatível, valida e cria uma Pull Request. Para criar PR com `GITHUB_TOKEN`, habilite as permissões apropriadas em Settings > Actions > General (Allow GitHub Actions to create and approve pull requests), se a opção estiver disponível. Se detectar mudança que contradiga um registro anterior, **falha explicitamente** em vez de alterar silenciosamente uma série publicada.

O workflow `publicar.yml` publica ao GitHub Pages após commits em `main`, uma vez que um repositório independente esteja criado e o Pages configurado para GitHub Actions.

## Proibições metodológicas deliberadas

- Não tratar dotação não executada como redução na dotação; bloqueio/contingenciamento é outro indicador.
- Não somar órgãos e unidades ao total de uma função, ou somar Fiocruz ao Ministério da Saúde.
- Não transformar valores em milhares em valores em reais sem documentação.
- Não atribuir a um presidente sozinho o exercício integral de 2016.
- Não calcular aumento real sem IPCA e método de deflação documentados.
- Não completar lacunas com zeros, médias ou aproximações.

## Testes

```bash
python scripts/validate.py
python scripts/validar_v5.py
```

O catálogo apresenta dados existentes e novas lacunas visíveis. A ingestão automática integral depende da **origem estruturada governamental e de sua documentação**, que ainda não estão configuradas. Esta versão não simula completude.
