# Brasil em Dados — Coleta incremental SIOP V10

## O que mudou

O SIOP é consultado **um exercício por tarefa**. Cada ano pode falhar ou passar sem bloquear os demais. O exercício corrente recebe um registro por mês, e os históricos aprovados são guardados no repositório para não serem baixados novamente.

**A aprovação é em duas fases** e não é automática:

1. Coletor baixa o arquivo oficial da LOA, verifica SHA-256, extrai os valores por função, exclui da comparação a Reserva de Contingência (`99`) e propõe `data/siop_anos/AAAA.csv` + `AAAA.json`. Para o ano corrente, usa `AAAA-AAAAMM.csv/.json` (fotografia mensal).
2. Depois de revisão e *merge* dessa PR, o workflow `consolidar-siop.yml` lê os anos já aprovados, recusa alterações contraditórias nos registros publicados, e abre **outra PR** com `data/alteracoes_orcamentarias.csv` + `alteracoes.js`. Somente após o segundo *merge* o site recebe os novos números.

Se 2022 falhar, é possível aprovar 2011, 2012 e 2023 independentemente. Não é necessário repetir os anos já aprovados. Um arquivo coletado mas **ainda não aprovado** não é considerado cache confiável.

## Como instalar

Extraia `Atualizacao_V10_SIOP_Incremental.zip` na pasta local `Brasil em Dados`, mantendo a pasta `.git` existente. Execute em PowerShell:

```powershell
$env:PYTHONUTF8 = '1'
python -m unittest discover -s tests -p 'test_*.py'
python scripts/validate.py
python scripts/validar_v5.py
git add .github/workflows/coletar-siop-loa.yml .github/workflows/consolidar-siop.yml scripts/siop_incremental.py scripts/consolidar_siop.py tests/test_siop_incremental_v10.py data/siop_anos/README.md GUIA_COLETA_INCREMENTAL_V10.md README.md
git commit -m 'Coleta incremental SIOP por ano com PR e consolidacao'
git push origin main
```

O workflow atual de publicação continua intocado. A coleta não modifica o site automaticamente.

## Usar no GitHub Actions

1. Em **Actions → Coletar SIOP por ano - independente e revisavel → Run workflow** escolha um ano, por exemplo **2022**, com `lote_historico=false`. O relatório daquela execução mostra o bloqueio, se houver.
2. Para uma primeira carga mais ampla, marque `lote_historico=true`. O workflow executa até **16 tarefas independentes**, uma por vez para reduzir carga no servidor. `fail-fast=false` garante que uma falha não cancele o restante; a execução total pode ficar vermelha, mas os anos bem-sucedidos terão suas PRs individuais.
3. Em **Pull requests**, examine cada PR de ano (`automacao/siop-ano-AAAA`). A revisão deve conferir escopo, contagens, data de referência, valores nominais e auditoria SHA-256. Faça merge **apenas** dos anos corretos.
4. A cada merge na `main` de `data/siop_anos/`, o workflow **Consolidar anos aprovados do SIOP - PR revisavel** prepara a PR de consolidação. Revise a diferença e faça merge. O workflow de Pages já existente publicará.

## Cuidados e limites

- A disponibilidade real do SIOP e a criação de PRs no GitHub dependem da execução remota e das permissões. Em **Settings → Actions → General → Workflow permissions**, permita criação de PRs.
- Uma PR criada com `GITHUB_TOKEN` normalmente **não dispara por si mesma** outras validações configuradas em `pull_request`; por isso os testes rodam **antes de criar cada PR**. O merge humano em `main` aciona os workflows adequados.
- **Sem cache global no Actions:** os arquivos anuais aprovados são armazenados no próprio Git, com auditoria. Isso evita depender de caches temporários que podem ser eliminados pelo GitHub.
- A primeira coleta de cada ano ainda exige rede. Erros de conexão não geram registros fictícios.
- Não sobrescrevemos dados históricos. Revisões oficiais de anos já aceitos precisam de investigação e atualização editorial separada.
- O exercício de 2026 é parcial. A chave mensal é a data da captura, **não certifica** que o SIOP tenha atualizado o arquivo naquele mês.
- A dotação inicial, a atualizada e o liquidado são métricas distintas; diferenças de dotação não comprovam por si só cortes de serviços.
- Se houver mais de uma PR anual aprovada em sequência, a consolidação pode precisar ser rodada novamente para captar todos os anos já na `main`. O consolidador percorre sempre os arquivos aprovados.

## O que não foi ativado daqui

Nenhuma ação foi enviada ao seu GitHub. O funcionamento remoto e os valores reais só poderão ser confirmados após `git push` e execução dos workflows.
