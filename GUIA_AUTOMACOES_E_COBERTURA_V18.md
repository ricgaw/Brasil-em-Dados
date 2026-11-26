# Brasil em Dados — V18: dados e automações incrementais

## O que mudou

- Acrescentado o resultado **2025 do Banco do Brasil**: lucro líquido **ajustado** de R$ 20,685 bilhões, citado pela Agência Brasil com base no balanço publicado. O valor não é lucro contábil e não equivale a receita operacional.
- Dentro da seção **Estatais**, criado um quadro de **cobertura por empresa**, distinguindo anos com resultado, receita e endividamento documentados. O quadro é calculado a partir dos arquivos reais e não cria zeros para anos ausentes.
- Adicionado um panorama **agregado das empresas estatais federais em 2025**, informado pela SEST: lucro líquido agregado R$ 169,4 bilhões e faturamento agregado aproximadamente R$ 1,4 trilhão. **Não** corresponde à soma dos quatro cards e não pode ser atribuído causalmente ao governo.
- Nova automação `monitorar-estatais-v18.yml`: monitora **duas páginas oficiais da SEST**, registra links de novos anexos em `data/fontes_estatais_v18.json` e atualiza o catálogo. Não atribui automaticamente números encontrados em PDFs ou planilhas a uma empresa sem mapeamento contábil e auditoria.
- Nova automação `atualizar-ipca-v18.yml`: tenta mensalmente o **fechamento anual de 2026** pela série mensal **SGS 433** do BCB/IBGE; publica somente a partir de janeiro de 2027 e apenas se houver 12 meses válidos. Não extrapola ou inventa o valor de 2026.
- O workflow Pages agora recalcula a cobertura **com base na branch main real** antes de publicar (inclusive após merges SIOP); mantém as validações já existentes.
- **Nenhuma mudança** nos CSV/JSON anuais do SIOP, em `alteracoes_orcamentarias.csv`, nos workflows de coleta SIOP ou no desenho base aprovado.

## Abrangência comprovada x pendências

Na base disponível para preparar o pacote, a Petrobras tem cinco exercícios com resultado (2021–2025); o Banco do Brasil, três (2023–2025); a Caixa, quatro (2022–2025); os Correios, dois (2024–2025). Receita e dívida têm menos anos ainda. A V18 **não** preenche artificialmente 2011–2020. Os anexos históricos da SEST têm formatos e critérios que exigem extração e conciliação específica, inclusive separação de bancos e empresas não financeiras. A cobertura real de anos SIOP no seu GitHub deve ser gerada a partir da `main`, não do arquivo antigo usado no ambiente de testes.

As séries de pobreza, renda, desocupação anual 2026, arrecadação histórica ACSP, resultados de execução e revisões judiciais precisam de fonte/método próprio antes de uma rotina automática confiável. Não estão automatizadas por esta versão. A automação anterior **V17 para dívida/PIB** continua independente e não é substituída.

## Instalar sem descartar os anos do SIOP

1. Na pasta `C:\Users\ricar\Desktop\Brasil em Dados`, execute `git status` e verifique que não há edições pendentes. Em seguida `git pull --ff-only origin main`.
2. Extraia **somente este pacote incremental V18** sobre a pasta local, substituindo os arquivos correspondentes. Não reinstale V15/V16/V17.
3. Execute:

```powershell
$env:PYTHONUTF8 = "1"
python scripts/cobertura_v18.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/validate.py
python scripts/validar_v5.py
python scripts/auditar_pipeline.py
```

4. Se não houver erros:

```powershell
git add .
git commit -m "Adicionar cobertura de estatais e automacoes V18"
git push origin main
```

5. Confirme que **Validar site nacional** e **Validar e publicar Brasil em Dados** ficaram verdes. Depois execute **uma vez** os dois novos workflows na aba Actions: **Monitorar documentos das estatais (SEST, automático)** e **Atualizar IPCA anual (BCB/IBGE, automático)**. O primeiro acessará a rede do governo e deverá criar um catálogo; o segundo não deve mudar o IPCA em 2026, pois o ano não terminou. Nas próximas datas programadas eles rodarão sozinhos.

## Fontes principais

- Resultados BB 2025 (Agência Brasil, com base em balanço): https://agenciabrasil.ebc.com.br/economia/noticia/2026-02/banco-do-brasil-tem-lucro-de-r-2068-bilhoes-em-2025
- Relatório agregado 2026/2025 SEST: https://www.gov.br/gestao/pt-br/assuntos/noticias/2026/Julho/estatais-federais-lucram-r-169-4-bilhoes-em-2025-aumento-de-45-sobre-2024
- Anexos históricos SEST: https://www.gov.br/gestao/pt-br/assuntos/estatais/transparencia/defeso_relatorio%20agregado
- Dados financeiros SEST: https://www.gov.br/gestao/pt-br/assuntos/estatais/transparencia/dados-abertos
- IPCA mensal, Banco Central SGS 433: https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json

## Advertências de operação

- **Testes locais não confirmam conectividade nem permissões de escrita no GitHub Actions**. Verificar a primeira execução dos dois novos workflows.
- `GITHUB_TOKEN` deve ter permissão de escrita em `Contents`. Se o repositório bloquear pushes de bots, é necessário adaptar o fluxo para PRs.
- Caso o portal governamental altere URLs ou retire anexos, o monitor **falha sem eliminar links já armazenados**.
- Para números das estatais, a mera descoberta de novos anexos **não representa atualização automática do resultado**. Este método é deliberadamente conservador para evitar valores incorretos.
