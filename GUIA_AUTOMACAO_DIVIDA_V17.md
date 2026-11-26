# Brasil em Dados — Automação de dívida pública (etapa 1)

## O que o pacote faz

- Consulta a **série SGS 13762** do Banco Central, DBGG como porcentagem do PIB, em blocos de até oito anos, sem interpolação.
- Mantém dezembro para anos encerrados e o mês mais recente disponível para o ano em andamento, marcado como **parcial**.
- Atualiza `data/divida_pib_bcb.json`, `data/divida_pib_bcb.csv` e `estatais-divida-data.js` **somente se houver mudança real**.
- Preserva a seção de estatais no mesmo arquivo JS, seus resultados e demais dados do site.
- Bloqueia lacunas anuais, valores implausíveis, recuo da referência mensal e revisões superiores a 5 pontos percentuais sem análise.
- Faz a validação do projeto **antes** de publicar, cria um commit somente se houver novidades e dispara `publicar.yml` explicitamente, pois um push com `GITHUB_TOKEN` não aciona outro workflow `push`.
- Agenda duas consultas mensais, **dias 7 e 21, 08h15 UTC**. Há acionamento manual opcional.

## Instalação (sobre V16 já publicada)

1. Na pasta local, use `git status` para verificar se há mudanças pendentes; não descarte alterações de outras tarefas.
2. Extraia os arquivos do ZIP na raiz do repositório, preservando o conteúdo anterior.
3. Execute:

```powershell
$env:PYTHONUTF8 = '1'
python -m unittest discover -s tests -p 'test_*.py'
python scripts/validate.py
python scripts/validar_v5.py
python scripts/auditar_pipeline.py
```

4. Se todos passarem:

```powershell
git add .github/workflows/atualizar-divida-bcb.yml scripts/atualizar_divida_bcb.py tests/test_atualizar_divida_bcb.py tests/test_v16_estatais_divida.py estatais-divida-app.js GUIA_AUTOMACAO_DIVIDA_V17.md
git commit -m 'Automatizar divida publica BCB e publicacao segura'
git push origin main
```

5. Em **Actions**, escolha **Atualizar dívida pública (BCB, automático)** → **Run workflow** → `main`. Confira o histórico e, havendo alterações, o disparo de **Validar e publicar Brasil em Dados**. Se nenhuma observação mudou, não há novo commit, e isso é esperado.
6. As próximas execuções são automáticas. No GitHub, confira em **Settings → Actions → General → Workflow permissions** se as políticas da organização/repositório permitem as permissões do workflow para gravar os dados e iniciar a publicação.

## Limites importantes

- O Banco Central pode revisar retroativamente períodos anteriores; a rotina importa revisões dentro do limite configurado e exige conferência humana se a revisão for excepcional. Essa é uma proteção, não uma falha de automação.
- Em ausência de dados da API, o workflow fica vermelho e **não publica dados inventados**. Pode ser executado novamente quando a fonte voltar.
- Agendamentos do GitHub Actions não são garantidos em minuto exato; em repositórios públicos inativos por longo período o GitHub pode desabilitar os agendamentos.
- Essa primeira automação cobre **somente a dívida pública/PIB**. A coleta de demonstrações das estatais requer extratores próprios para os relatórios auditados e conciliação por empresa; não foi ativada neste pacote.
- Esta revisão foi testada offline com as cópias V15/V16 e workflows disponíveis no ambiente. Não foi possível executar uma chamada real à API do BCB nem inspecionar a `main` atual do GitHub diretamente do ambiente de execução; a primeira execução no Actions será o teste real de rede e permissões.

Fonte: https://dadosabertos.bcb.gov.br/dataset/13762-divida-bruta-do-governo-geral--pib---metodologia-utilizada-a-partir-de-2008
