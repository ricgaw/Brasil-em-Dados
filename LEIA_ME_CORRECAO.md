# Correção do teste de consolidação SIOP

## Problema
O workflow conseguia consolidar exercícios aprovados (por exemplo, 2011 e 2012), mas o teste `test_end_to_end_consolidation_in_isolated_copy` falhava ao tentar importar registros fictícios de 2011 sobre uma cópia da base que já possuía dotações reais de 2011. O importador bloqueia divergências corretamente; a falha estava no teste, não na política de não sobrescrita.

## Modificação
Somente `tests/test_siop_incremental_v10.py`:
- cria uma cópia temporária do projeto;
- limpa os arquivos anuais copiados **na cópia temporária**;
- remove da base temporária apenas observações de funções de 2011, para inserir o registro fictício do teste;
- executa consolidação e validações e exibe os logs completos quando houver falha.

Nenhum arquivo real de `data/`, gráfico, workflow ou coletor é modificado.

## Testes
Foram executados 28 testes e os validadores `scripts/validate.py` e `scripts/validar_v5.py`. Também foi simulado um repositório com 2011 e 2012 previamente consolidados; os 28 testes passaram.

## Instalação
Extraia o arquivo ZIP na pasta raiz do projeto, substituindo `tests/test_siop_incremental_v10.py`.

No terminal PowerShell do VS Code:

```powershell
$env:PYTHONUTF8 = "1"
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate.py
python scripts/validar_v5.py
```

Se passar:

```powershell
git add tests/test_siop_incremental_v10.py
git commit -m "Isolar teste de consolidacao dos anos SIOP"
git push origin main
```

Após os checks ficarem verdes, em Actions, execute **Consolidar anos aprovados do SIOP - PR revisavel** com *Run workflow*. Não aprove a PR de consolidação sem revisar os dados reais por função.
