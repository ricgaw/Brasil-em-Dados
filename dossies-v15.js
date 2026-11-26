(function(){
 'use strict';
 const $=id=>document.getElementById(id);
 const esc=x=>String(x??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
 const atlas=window.ATLAS||{};
 const change=Array.isArray(window.BUDGET_CHANGES)?window.BUDGET_CHANGES:[];
 const infl=Array.isArray(window.INDICADORES)?window.INDICADORES:[];
 const cases=Array.isArray(atlas.cases)?atlas.cases:[];
 const policy=Array.isArray(atlas.policies)?atlas.policies:[];
 // Totais nacionais publicados no CSV: apenas 2024 e 2025 têm valor verificado.
 const taxYears=[2024,2025];
 const years=Array.from({length:16},(_,i)=>i+2011);
 const mandateFor=y=>y<=2014?'2011':y<=2018?'2015':y<=2022?'2019':'2023';
 const termLabel={'2011':'2011–2014 · Dilma','2015':'2015–2018 · Dilma / Temer','2019':'2019–2022 · Bolsonaro','2023':'2023–2026 · Lula'};
 const byYear=new Map();
 const funcs=change.filter(x=>String(x.id_escopo||'').startsWith('funcao-'));
 for(const x of funcs){const year=+x.ano;let row=byYear.get(year);if(!row){row=new Set();byYear.set(year,row)}row.add(x.area)}
 const revenueByYear=new Set(taxYears);
 const socialByYear=new Map(); for(const x of infl){const year=+x.ano;const s=socialByYear.get(year)||new Set();s.add(x.indicador);socialByYear.set(year,s)}
 function cards(){
  const el=$('mandate-deep-cards'); if(!el)return;
  el.innerHTML=(atlas.terms||[]).map(t=>{
   const id=t.id,yearsThis=years.filter(y=>mandateFor(y)===id);
   const p=policy.filter(x=>x.term===id),c=cases.filter(x=>x.term===id);
   const withBudget=yearsThis.filter(y=>byYear.get(y)?.size===28).length;
   return `<article class="deep-card"><span class="overline">MANDATO ${esc(t.period)}</span><h3>${esc(t.title)}</h3><p>${esc(t.subtitle)}</p><div class="deep-metrics"><div><b>${p.length}</b><small>Atos e políticas selecionados</small></div><div><b>${c.length}</b><small>Casos documentados</small></div><div><b>${withBudget}/4</b><small>Anos com 28 funções SIOP publicadas</small></div></div><p class="deep-disclaimer">Contagens indicam cobertura deste projeto, não desempenho, êxito ou responsabilidade pessoal.</p><div class="deep-links"><a href="#mandatos" data-select-term="${esc(id)}">Ver governantes ↗</a><a href="#politicas" data-policy-term="${esc(id)}">Ver atos ↗</a><a href="#escandalos" data-case-term="${esc(id)}">Ver documentação ↗</a></div></article>`;
  }).join('');
  el.querySelectorAll('[data-select-term]').forEach(a=>a.addEventListener('click',()=>{const b=document.querySelector(`#term-tabs [data-term="${a.dataset.selectTerm}"]`);b?.click()}));
  el.querySelectorAll('[data-policy-term]').forEach(a=>a.addEventListener('click',()=>{const s=$('policy-term');if(s){s.value=a.dataset.policyTerm;s.dispatchEvent(new Event('change'))}}));
  el.querySelectorAll('[data-case-term]').forEach(a=>a.addEventListener('click',()=>{const s=$('case-term');if(s){s.value=a.dataset.caseTerm;s.dispatchEvent(new Event('change'))}}));
 }
 function coverage(){
  const el=$('year-coverage-body');if(!el)return;
  const term=$('coverage-term')?.value||'all';
  const selected=years.filter(y=>term==='all'||mandateFor(y)===term);
  el.innerHTML=selected.map(y=>{
   const n=byYear.get(y)?.size||0;
   const socials=socialByYear.get(y)?.size||0;
   const r=revenueByYear.has(y);
   const note=y===2026?'Exercício em andamento; fotografias podem mudar.':y===2016?'Transição entre Dilma e Temer em agosto.':'Ano de referência civil.';
   return `<tr><td><strong>${y}</strong><small>${esc(note)}</small></td><td>${esc(termLabel[mandateFor(y)])}</td><td>${n===28?'<span class="cover-yes">28/28 funções</span>':n?`<span class="cover-partial">${n}/28 funções</span>`:'<span class="cover-missing">Pendente</span>'}</td><td>${socials?`${socials} indicador(es)`:'Pendente'}</td><td>${r?'Valor nacional documentado':'Pendente'}</td></tr>`;
  }).join('');
  $('coverage-count').textContent=`${selected.length} exercício(s) · ${selected.filter(y=>byYear.get(y)?.size===28).length} com 28 funções publicadas`;
 }
 function sourceDirectory(){
  const el=$('source-directory');if(!el)return;
  const ds=[
   ['Planejamento e LOA','SIOP · dados abertos','https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:dados_abertos','Dotação e execução federal por função; arquivos originais e auditoria'],
   ['Execução orçamentária','Tesouro Transparente · RREO','https://www.tesourotransparente.gov.br/temas/contabilidade-e-custos/relatorio-resumido-da-execucao-orcamentaria-rreo-uniao','Outra série com recorte próprio; não fundir diretamente ao SIOP'],
   ['Mercado de trabalho','IBGE · PNAD Contínua','https://www.ibge.gov.br/estatisticas/sociais/trabalho/17270-pnad-continua.html','Desocupação: metodologia da pesquisa domiciliar'],
   ['Inflação','IBGE · IPCA','https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html','Inflação acumulada por ano'],
   ['Cartões corporativos','CGU · CPGF','https://portaldatransparencia.gov.br/download-de-dados/cpgf','Transações divulgadas; restrições e lacunas precisam ser identificadas'],
   ['Contratos e despesas','Portal da Transparência','https://portaldatransparencia.gov.br/','Pagamentos, despesas e órgãos pagadores'],
   ['Eleições e bens declarados','TSE · DivulgaCandContas','https://divulgacandcontas.tse.jus.br/divulga/#/','Bens declarados na eleição; não comprovam quadro societário atual'],
   ['Empresas e QSA','Receita Federal · CNPJ','https://www.gov.br/pt-br/servicos/consultar-cadastro-nacional-de-pessoas-juridicas','Consulta societária requer identificação específica e data'],
   ['Legislação','Planalto · Legislação federal','https://www4.planalto.gov.br/legislacao','Texto legal original de medidas descritas'],
   ['Arrecadação tributária','Impostômetro · ACSP','https://impostometro.com.br/','Total nacional das três esferas, não receita federal apenas'],
  ];
  el.innerHTML=ds.map(([group,title,url,desc])=>`<article class="source-card"><span class="overline">${esc(group)}</span><h3>${esc(title)}</h3><p>${esc(desc)}</p><a href="${esc(url)}" target="_blank" rel="noopener noreferrer">Consultar fonte ↗</a></article>`).join('');
 }
 function start(){cards();coverage();sourceDirectory();$('coverage-term')?.addEventListener('change',coverage)}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
