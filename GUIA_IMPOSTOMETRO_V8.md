# Impostômetro · Atualização V8

## O que foi entregue
- Seção no início do site com projeção animada **explicitamente não oficial**. A projeção usa o total anual aproximado de 2025 (R$ 3,98 trilhões) como uma taxa média fixa, não a arrecadação real de 2026; é demonstração visual e não deve ser usada como dado econômico.
- Botão para abrir o contador oficial da Associação Comercial de São Paulo (ACSP), que publica sua própria contagem dinâmica.
- Série histórica nacional com 2024 (aprox. R$ 3,6 trilhões) e 2025 (aprox. R$ 3,98 trilhões), dados divulgados pela ACSP; demais anos marcados **pendentes**.
- Tabela por mandato e exportação `data/arrecadacao_tributaria.csv`.

## Para ter o valor oficial diretamente na página
A ACSP fornece um gerador de código para inclusão do Impostômetro em sites: https://impostometro.com.br/Home/Impostometro/. Selecione Brasil, tamanho desejado e gere o código. A API de dados está sujeita a convênio com a ACSP; não tentamos copiar ou simular sua API. A incorporação oficial deve respeitar as condições do fornecedor e precisa ser testada após colar o código na seção no lugar da projeção.

## Próximas coletas
Para 2011–2023 e 2026, é necessário levantar uma série **nacional de todas as esferas**, revisada e compatível. A série da Receita Federal se refere apenas à União e **não é substituta** dessa série. Revisar anos mistos (2016), dados nominais, inflação e mudanças metodológicas.

## Fontes
- https://impostometro.com.br/home/metodologiaimpostometro
- https://impostometro.com.br/Noticias/Interna?idNoticia=1401
- https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/dados-abertos/receitadata/arrecadacao/serie-historica
