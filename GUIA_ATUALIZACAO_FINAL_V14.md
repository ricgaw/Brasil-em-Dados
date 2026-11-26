# Brasil em Dados — Atualização editorial V14

Esta entrega é a **última grande atualização planejada de apresentação e navegação**. As próximas etapas podem priorizar coleta e automação, sem redesenhar o site.

## Conteúdo da atualização

- Marca `BR` no cabeçalho e ícone da aba (substitui o monograma `B`).
- Panorama por mandato calculado com base nas fichas e nos valores **efetivamente publicados** no próprio site. Contagens de fichas não são notas de desempenho.
- Busca por texto nas políticas públicas e nos casos documentados, combinada com os filtros existentes.
- Comparador anual de orçamento SIOP: dotação inicial, atualizada e liquidada por função, com lacunas reais, fonte por ano e distinção de 2026 parcial. Não mistura a função orçamentária com recortes de ministérios e unidades vinculadas.
- Notas de interpretação sobre gastos da Presidência, cartão corporativo, decisões e investigações, inflação, transparência e direito de correção.
- Glossário de termos financeiros e links para fontes e para registrar correções documentadas.
- Melhorias de responsividade e navegação no cabeçalho.

## Instalação segura

Aplique **somente** os arquivos do ZIP incremental. Eles são arquivos de apresentação (`index.html`, `styles.css`, `app.js`, `novos-paineis.js`, `README.md`) mais este guia e o teste `tests/test_v14_apresentacao.py`. Não substitua `data/`, `scripts/` ou `.github/workflows/` por versões anteriores.

1. Em `C:\Users\ricar\Desktop\Brasil em Dados`, execute `git switch main`, `git status` e `git pull --ff-only origin main` **antes** de extrair o ZIP. Se houver mudanças locais importantes, não as descarte.
2. Extraia a atualização V14 sobre a pasta do projeto, substituindo os arquivos indicados.
3. Execute os testes:

   ```powershell
   $env:PYTHONUTF8 = "1"
   python -m unittest discover -s tests -p "test_*.py"
   python scripts/validate.py
   python scripts/validar_v5.py
   ```

4. Se estiverem verdes, execute:

   ```powershell
   git add index.html styles.css app.js novos-paineis.js README.md GUIA_ATUALIZACAO_FINAL_V14.md tests/test_v14_apresentacao.py
   git commit -m "Finalizar apresentacao BR e paineis comparativos V14"
   git push origin main
   ```

5. Confira a publicação em `https://github.com/ricgaw/Brasil-em-Dados/actions` e depois em `https://ricgaw.github.io/Brasil-em-Dados/`.

## Limites e próximos passos

- **Não há nova coleta numérica nesta entrega**. O comparador mostra os anos que já estiverem na base `alteracoes.js` publicada.
- O painel CPGF permanece sem totais até haver importação oficial e auditoria das competências mensais.
- As fichas de programas, casos judiciais e vínculos societários não foram alteradas por alegações sem novos documentos.
- O contador ilustrativo de arrecadação continua identificado como **projeção**, com link para o Impostômetro da ACSP.
- Os dados orçamentários SIOP por função e a série IBGE/Tesouro devem permanecer separados. Conferir a metodologia antes de usar esses dados como evidência de desempenho dos governos.
- **2026 é exercício em andamento**. Não comparar como se fosse um exercício fechado.
- As Pull Requests pendentes do SIOP devem continuar sendo analisadas individualmente; não fazer merge automático de informações financeiras sem revisão.

## O que foi testado

Rodada local de testes Python do código fornecido, validadores e sintaxe dos JavaScript. Também foi realizada checagem de navegação e renderização do HTML com navegador Chromium de teste. Isso **não** garante que a publicação remota passou: confirmar no GitHub Actions após `push`.
