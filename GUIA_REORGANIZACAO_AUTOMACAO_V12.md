# Brasil em Dados — reorganização da automação (V12)

## O que este pacote realmente faz

Trabalha sobre o código da `main` recebido no ZIP do usuário em 25/11/2026. **Não substitui nem apaga** dados anuais, conteúdo editorial, CSS, gráficos ou site publicado. Não faz merge nem fecha as Pull Requests atualmente abertas.

| Responsabilidade | Workflow | Comportamento |
|---|---|---|
| Validação (código e dados) | `validar.yml` | Em push/PR; acrescenta auditoria offline dos arquivos SIOP presentes |
| Publicação | `publicar.yml` | Em push na `main`; testa e publica apenas o site, sem dados brutos |
| Coleta anual | `coletar-siop-loa.yml` | Por ano, PR independente; preserva históricos aceitos |
| Consolidação | `consolidar-siop.yml` | Audita os anos na `main`, consolida, guarda relatório e cria PR para revisão |
| Cartões corporativos | `scripts/importar_cpgf.py` | Importação manual/assistida; não há ingestão automática de dados reais da CGU |
| Indicadores sociais | Arquivos locais + site | Séries históricas já publicadas, sem coletor automático novo |
| Monitoramento | `monitorar-fontes.yml` e `novas-edicoes-orcamento.yml` | Apenas alertas; não alteram números |
| Importador legado de dotações | `importar-dotacoes.yml` | **Somente execução manual**; eliminado agendamento concorrente com SIOP |

## Correções de segurança e consistência

1. `scripts/auditar_pipeline.py` confere offline os pares CSV/JSON anuais existentes, fontes e exercícios, estrutura das funções, contagem do JSON, e checksum *do CSV normalizado* para identificação exata de sua versão. O checksum do arquivo original bruto **é declarado no JSON do coletor**, mas não é revalidado aqui; isso exigiria baixar o original novamente.
2. A auditoria é executada antes da consolidação, nas validações de Pull Request e antes do deploy.
3. A consolidação usa grupo de concorrência exclusivo, para não executar duas propostas simultaneamente.
4. `scripts/estado_automacao.py` gera um relatório legível dos anos presentes na cópia local (`main` do ZIP), distinguidos dos anos efetivamente consolidados em `data/alteracoes_orcamentarias.csv`.
5. O importador legado deixou de rodar semanalmente; evita dois workflows tentando modificar `alteracoes.js` e seu CSV.

## Instalação segura

1. Deixe as PRs existentes abertas. Na pasta do VS Code execute:

   ```powershell
   git switch main
   git status
   git pull --ff-only origin main
   ```

   Se o `git status` mostrar alterações locais que não reconhece, **não substitua** arquivos; confira antes.

2. Extraia o ZIP incremental da V12 por cima da pasta `Brasil em Dados` (preserve `.git`). Somente workflows, scripts, testes e este guia devem ser alterados.
3. Rode:

   ```powershell
   $env:PYTHONUTF8 = '1'
   python -m unittest discover -s tests -p 'test_*.py'
   python scripts/auditar_pipeline.py
   python scripts/estado_automacao.py
   python scripts/validate.py
   python scripts/validar_v5.py
   git diff --stat
   ```

4. Se passar, envie **somente** a atualização:

   ```powershell
   git add .github/workflows/coletar-siop-loa.yml .github/workflows/consolidar-siop.yml .github/workflows/importar-dotacoes.yml .github/workflows/publicar.yml .github/workflows/validar.yml scripts/auditar_pipeline.py scripts/estado_automacao.py tests/test_auditar_pipeline.py GUIA_REORGANIZACAO_AUTOMACAO_V12.md
   git commit -m 'Reorganizar pipeline e auditar SIOP sem alterar dados'
   git push origin main
   ```

5. Confira **Validar site nacional** e **Validar e publicar Brasil em Dados** no GitHub Actions.
6. Não execute coleta histórica novamente. Primeiro revise o relatório de consolidação no Action e a PR de consolidação já existente. Após revisão, pode executar manualmente uma nova consolidação se realmente houver anos novos incorporados na `main`.

## Limites importantes

- Os dados presentes no ZIP têm **2011 e 2012 aprovados como arquivos anuais**, mas `data/alteracoes_orcamentarias.csv` nesse ZIP ainda contém apenas os dois recortes institucionais de 2026. Portanto os gráficos de dotação por função desses anos **ainda não estão publicados pela consolidação**.
- Os anos 2013–2026 nas PRs abertas **não estão no ZIP da `main`**. Uma PR aberta não significa dado incorporado.
- GitHub suprime alguns acionamentos automáticos decorrentes de eventos gerados com `GITHUB_TOKEN`; após uma PR criada por Action, uma revisão/execução manual pode continuar necessária. Não foram introduzidos tokens pessoais.
- Auditoria estrutural e hashes não substituem uma conferência dos totais consolidados com os arquivos oficiais. Mantenha revisão antes do merge.
- `2026` é exercício em andamento. Snapshots mensais não devem ser misturados com exercícios encerrados ou somados entre si.

## Próximas fases

**Fase 2:** testar numa PR de demonstração a auditoria cruzada de totais por função contra relatório oficial do SIOP sem alterar a produção; conferir cenários de revisões históricas e snapshots de 2026.

**Fase 3:** incorporar um mês real do CPGF, com agregação por órgão, supressão de dados pessoais, validação editorial e PR revisável. Indicadores sociais podem receber coleta própria posteriormente. Nada disso está fingidamente ativo nesta V12.
