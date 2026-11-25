# Correção da coleta SIOP — timeout de rede

A execução histórica #3 confirmou SHA-256 em 2011–2021 e falhou na conexão com o arquivo de 2022. Não se trata de uma divergência nos dados.

## Mudanças

- Repete até 3 vezes downloads com timeout/erro transitório e identifica o endereço que falhou.
- **Não** repete 404 e outros erros permanentes, nem ignora divergências de SHA-256.
- Grava o andamento em `reports/siop_coleta.json` ao fim de cada ano e registra o ano que falhou.
- Se a série ficar incompleta, o script retorna erro e o workflow **não importa nem publica** uma série parcial.
- Não altera interface, valores publicados ou workflows.

## Instalação

Copie as pastas `scripts/` e `tests/` deste ZIP para sua pasta local `Brasil em Dados`, substituindo os arquivos correspondentes.

No PowerShell do VS Code:

```powershell
$env:PYTHONUTF8 = "1"
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate.py
python scripts/validar_v5.py
```

Se passar:

```powershell
git add scripts/coletar_siop_loa.py tests/test_siop_rede_v9.py
git commit -m "Tratar timeout e preservar auditoria parcial da coleta SIOP"
git push origin main
```

Após a validação verde, abra o GitHub Actions e inicie uma **nova execução** da coleta com `historico=true`. Não use `Re-run jobs` na execução antiga, pois ela mantém o commit anterior.

Se falhar de novo, baixe `siop-relatorio-coleta` em Artifacts e compartilhe os detalhes do ano que falhou. Não faça merge de PR antes de validar os números.
