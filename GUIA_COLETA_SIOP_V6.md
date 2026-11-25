# Brasil em Dados — integração oficial SIOP LOA (V6)

## O que foi implementado

O workflow `.github/workflows/coletar-siop-loa.yml` consulta os arquivos **oficiais** `loaANO.csv.gz` e `loaANO.sha256` divulgados pelo SIOP. Confere SHA-256, valida colunas, agrega as despesas por **código de função** e pelas esferas **Fiscal (10) e Seguridade Social (20)**, gera um arquivo temporário de importação e passa os dados pelo importador conservador já existente.

O importador **não substitui registros existentes**: se uma observação com a mesma chave (ano, função, data de referência) tiver mudança de valor, a execução falha para revisão. Quando há registros novos e consistentes, o workflow **abre Pull Request** — nunca faz merge automaticamente ou publica dados sem aprovação. O workflow de Pages já existente continua a publicar após o merge na `main`.

## Como ativar no seu repositório

1. Copie os arquivos desta atualização para sua pasta `Brasil em Dados` no VS Code, preservando as subpastas.
2. Execute:
   ```powershell
   $env:PYTHONUTF8 = "1"
   python -m unittest discover -s tests -p "test_*.py"
   python scripts/validate.py
   python scripts/validar_v5.py
   git add .
   git commit -m "Integrar coleta oficial da LOA do SIOP com validacao SHA256"
   git push origin main
   ```
3. Entre em **GitHub → Brasil-em-Dados → Actions → Coletar SIOP LOA por funcao - proposta revisavel → Run workflow**.
4. Para a carga completa, selecione `historico = true`; para 2025–2026, mantenha `false`.
5. Abra o job executado. Na aba **Artifacts**, baixe `siop-relatorio-coleta`: contém o CSV de proposta e um JSON com as URLs e checksums. Se falhar, a mensagem `COLETA BLOQUEADA` explica o motivo.
6. Se a coleta/validação terminar e gerar mudanças, abra o **Pull Request** da branch `automacao/siop-loa-funcoes`, confira as 28 funções, os valores e o recorte antes de mesclar.
7. Após o merge, o workflow **Validar e publicar Brasil em Dados** atualizará o GitHub Pages. Nenhuma configuração de domínio ou token é necessária para esse workflow.

**Importante:** Se a ação não conseguir criar PR, em Settings → Actions → General confira as permissões do `GITHUB_TOKEN` e habilite **Allow GitHub Actions to create and approve pull requests**, se disponível para o repositório. Isso exige ação do proprietário.

## Atualizações recorrentes

- A coleta padrão é **mensal** (dia 1 às 08:25 UTC), cobrindo 2025 e o exercício corrente 2026, que continua parcial.
- A carga completa 2011–2026 é **manual**, pois altera muitos registros e exige revisão histórica.
- A série de despesa liquidada **IBGE/Tesouro 2020–2024** permanece separada da série SIOP. Elas têm regras de liquidação que podem divergir; **não combinar automaticamente**.
- Para anos encerrados, `data_referencia=AAAA-12-31` é um **marcador do exercício**, e não a data em que o arquivo foi baixado. A data efetiva do download e o SHA-256 são registrados no relatório JSON.
- Para 2026, `data_referencia` corresponde ao dia UTC da coleta, que não garante a atualização do dado no próprio dia. O site deve apresentar esses valores como **parciais** e situados na data de download.
- Valores do CSV oficial têm duas casas decimais. A agregação ocorre em **centavos inteiros**, com arredondamento do **total da função**, não das linhas individuais, para reais. Funções com dotação inicial zero não são convertidas em percentuais; aparecem no relatório como requerendo tratamento editorial.
- Diferença LOA inicial vs dotação atualizada **não permite concluir**, sozinha, se houve bloqueio, contingenciamento ou prejuízo a um serviço.

## Fonte e método

- [Catálogo oficial de dados abertos do SIOP](https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:dados_abertos)
- [Dicionário CSV/Parquet e metodologia](https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:dados_abertos_loa)

O dicionário informa que a dotação fica em linhas do elemento de despesa `00` e execução em elementos detalhados. O script soma as colunas **independentemente do elemento**, evitando excluir valores de uma das duas séries. Valores negativos em ajustes/reversões são preservados na agregação; totais negativos/atípicos são revisados pelo importador e/ou pela etapa humana.

## Limitações

A lógica foi testada com **arquivos CSV.gz simulados** e SHA-256 de teste e com o validador real do projeto. Nesta entrega não foi possível acessar a rede externa a partir do executor local para baixar os CSVs numéricos oficiais do SIOP. Portanto **não incluí valores históricos novos**, e a coleta real/descoberta de URLs precisa ser confirmada no GitHub Actions. Se o formato de links do portal mudar, a etapa de descoberta bloqueará a importação sem alterar o site.
