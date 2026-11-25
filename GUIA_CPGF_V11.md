# Brasil em Dados — Importação do CPGF (Versão 11)

## Objetivo

Preparar a visualização de despesas do **Cartão de Pagamento do Governo Federal (CPGF)** por órgão superior e competência. Não confundir CPGF com CPDC/CPCC; não tratar gasto do órgão como despesa pessoal do presidente.

## Fonte

Portal da Transparência da CGU: https://portaldatransparencia.gov.br/download-de-dados/cpgf/

A CGU fornece exportações **mensais** e dicionário de dados. Baixe manualmente o arquivo oficial de uma competência, anotando o período **AAAAMM** do extrato. O endpoint de download automático ainda **não foi confirmado/testado**; por isso este pacote não agenda downloads externos.

## Etapas

1. Guarde o arquivo ZIP/CSV original em `dados_brutos/cpgf/` na raiz do projeto. Esta pasta está no `.gitignore` para evitar publicação de CPFs e nomes.
2. No terminal do VS Code, a partir da raiz do repositório, execute:

   ```powershell
   $env:PYTHONUTF8 = "1"
   python scripts/importar_cpgf.py --arquivo "dados_brutos/cpgf/202501_CPGF.zip" --periodo 202501
   ```

   Adapte o nome e o período à exportação efetivamente obtida.
3. O importador confere os campos `CÓDIGO ÓRGÃO SUPERIOR`, `NOME ÓRGÃO SUPERIOR`, `ANO EXTRATO`, `MÊS EXTRATO`, `VALOR TRANSAÇÃO`. Ele recusa competências misturadas, arquivos vazios e cabeçalhos desconhecidos.
4. O resultado gera apenas `data/cpgf_resumo.csv` e `cpgf-data.js`, agregados por **órgão e mês**. Todos os valores são armazenados em **centavos inteiros**; inclui SHA-256 do arquivo bruto para rastreabilidade. Não publica CPF, portador, fornecedor ou cada transação.
5. Revise a soma, a competência, a origem e eventuais divergências. Rode:

   ```powershell
   python -m unittest discover -s tests -p "test_*.py"
   python scripts/validate.py
   python scripts/validar_v5.py
   git status --short
   ```

6. Faça o commit **somente** dos dois arquivos agregados, preferencialmente em uma branch revisável. Não faça `git add .` quando houver brutos fora de `dados_brutos/`.

   ```powershell
   git add data/cpgf_resumo.csv cpgf-data.js
   git commit -m "Incorporar CPGF agregado 202501"
   ```

## Limitações importantes

- Um mês importado não representa o ano inteiro. O painel exibe quantas competências foram importadas.
- O modelo utiliza a competência da **fatura (mês/ano de extrato)**, e não a data individual da transação. Não compare com séries por data de gasto sem harmonização.
- O total do órgão **Presidência da República** não é gasto pessoal do presidente.
- Transações sigilosas ou dados ausentes podem limitar a cobertura. Não inferir zero de ausência.
- Para reimportar uma competência com bytes diferentes, é necessário usar `--revisao` e revisar o diff.
- Nunca enviar o bruto ao repositório público, mesmo que conste de uma fonte aberta.

## Continuidade

Depois de verificar o formato real e a estabilidade de um endereço público mensal, podemos criar um workflow que baixe o arquivo temporariamente, descarte o bruto, anexe auditoria e proponha PR. A coleta deve ser incremental por mês, sem reprocessar toda a história.
