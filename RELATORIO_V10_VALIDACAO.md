# Relatório de validação da Versão 10

Data de preparação: 25/11/2026.

## Concluído

- Coleta SIOP isolada por exercício, com persistência revisada em `data/siop_anos/`.
- Fotografias mensais para 2026, sem sobrescrita de histórico aprovado.
- Workflow matricial `fail-fast: false`, `max-parallel: 1` e 16 anos selecionáveis.
- Primeira PR por exercício: apenas arquivos anuais e auditoria (o site não muda).
- Segundo workflow e segunda PR consolidam apenas anos aceitos na `main`.
- Bloqueio de colisão e de revisões divergentes durante importação.
- Site e workflow de publicação preservados.
- 22 testes automatizados aprovados, incluindo simulação de integração ponta a ponta em cópia isolada; `validate.py` e `validar_v5.py` aprovados.

## Não concluído remotamente

- Downloads reais do SIOP não foram executados neste ambiente.
- Criação/merge remoto de PRs e publicação em GitHub não foram executados daqui.
- Limitações temporárias do servidor do SIOP podem continuar afetando anos individuais.
- A comprovação de que aumentos/reduções se referem a alterações efetivas de cada exercício exige inspeção dos documentos e validação editorial antes do merge.

## Limites importantes

Os arquivos anuais só são considerados aprovados após o merge de sua PR. As PRs podem aparecer em sequência, e a PR de consolidação pode precisar de nova execução caso haja diversas aprovações em pouco tempo. Valores de execução e dotação não medem, isoladamente, o desempenho de políticas públicas.
