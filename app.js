'use strict';
const D=window.ATLAS;
const q=s=>document.querySelector(s);
const state={term:'2023',policyTerm:'all',area:'all',policySearch:'',caseSearch:'',chartArea:'Saúde',chartTerm:'all'};
const fmt=n=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:1}).format(n);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const source=(key,label='Fonte oficial')=>`<a target="_blank" rel="noopener noreferrer" href="${esc(D.sources[key])}">${esc(label)} ↗</a>`;
const pic=(p)=>{
 const ph=D.photos[p.img]||''; const name=esc(p.short||p.name); return `<div class="person-photo"><span>${esc(p.short.split(' ').map(s=>s[0]).join('').slice(0,2))}</span>${ph?`<img src="${encodeURI(ph).replaceAll('%25','%')}" alt="Retrato de ${name}" loading="lazy" onerror="this.remove()">`:''}</div>`;
};
function personCard(id,position,term){
 const p=D.people[id];return `<article class="person-card">${pic(p)}<div class="person-info"><span class="job">${esc(position)}</span><h4>${esc(p.name)}</h4><div class="party">${esc(p.party)}</div><p>${esc(p.bio)}</p><div class="profile-official"><span><b>Subsídio bruto legal de referência</b><strong>${esc(term.salary)}</strong><small>${esc(term.salary_note)} · não é contracheque</small></span><a href="${esc(D.sources[term.salary_src])}" target="_blank" rel="noopener noreferrer">Ato normativo ↗</a></div><div class="company-note"><b>Patrimônio eleitoral e sociedades:</b> verificação individual histórica pendente. A declaração de bens ao TSE não comprova a composição societária atual; parentesco não é prova de favorecimento. <a href="${esc(D.sources.receita)}" target="_blank" rel="noopener noreferrer">Consultar CNPJ ↗</a> · <a href="${esc(D.sources.tse_bens)}" target="_blank" rel="noopener noreferrer">Bens no TSE ↗</a></div></div></article>`;
}
function renderTerms(){
 q('#term-tabs').innerHTML=D.terms.map(t=>`<button class="term-tab ${state.term===t.id?'active':''}" role="tab" aria-selected="${state.term===t.id}" data-term="${t.id}"><strong>${t.period}</strong><small>${t.id==='2015'?'Dilma e Temer':D.people[t.presidents[0]].short}</small></button>`).join('');
 q('#term-tabs').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{state.term=b.dataset.term;renderTerms()}));
 const t=D.terms.find(x=>x.id===state.term);
 let people='';
 if(t.id==='2015') people=personCard('dilma','Presidente • 01/01/2015–31/08/2016',t)+personCard('temer','Vice até 31/08/2016 • presidente depois',t);
 else people=personCard(t.presidents[0],'Presidente',t)+personCard(t.vice[0],'Vice-presidente',t);
 const extras=t.id==='2015'?'<b>Nota institucional</b><p>Michel Temer assumiu em definitivo em 31/08/2016; o cargo de vice-presidente ficou vago até o fim do mandato. As medidas de Temer são identificadas como de seu governo, não da campanha de Dilma.</p>':'<b>Transparência patrimonial</b><p>O TSE publica bens declarados na eleição. Declaração patrimonial e quadro societário de empresa têm finalidades distintas. A ausência de vínculo validado nesta ficha não significa que a pessoa não possua participações.</p>';
 q('#term-body').innerHTML=`<div class="term-heading"><div><span class="overline">MANDATO ${t.period}</span><h3>${esc(t.title)}</h3><p>${esc(t.subtitle)}</p></div><span class="term-years">${t.period}</span></div><div class="people-grid">${people}</div><div class="term-note">${extras}</div><div class="salary-strip"><div><small>SUBSÍDIO LEGAL DE REFERÊNCIA (PRESIDENTE E VICE)</small><strong>${t.salary}</strong><small>${esc(t.salary_note)}</small></div>${source(t.salary_src,'Ver decreto legislativo')}</div>`;
}
function setupPolicies(){
 const by= q('#policy-term'); by.innerHTML='<option value="all">Todos os mandatos</option>'+D.terms.map(t=>`<option value="${t.id}">${t.period}</option>`).join('');
 const ar=q('#policy-area'); ar.innerHTML='<option value="all">Todas as áreas</option>'+[...new Set(D.policies.map(x=>x.area))].sort().map(x=>`<option>${esc(x)}</option>`).join('');
 by.onchange=()=>{state.policyTerm=by.value;renderPolicies()}; ar.onchange=()=>{state.area=ar.value;renderPolicies()};q('#policy-search').oninput=e=>{state.policySearch=e.target.value.toLocaleLowerCase('pt-BR');renderPolicies()};renderPolicies();
}
function renderPolicies(){
 const xs=D.policies.filter(p=>(state.policyTerm==='all'||p.term===state.policyTerm)&&(state.area==='all'||p.area===state.area)&&(!state.policySearch||[p.title,p.action,p.area,p.author,p.note].join(' ').toLocaleLowerCase('pt-BR').includes(state.policySearch)));
 q('#policy-count').textContent=`${xs.length} ficha(s) encontrada(s)`;q('#policy-list').innerHTML=xs.map(p=>`<article class="policy"><div class="policy-head"><span class="area">${esc(p.area)} · ${esc(D.terms.find(t=>t.id===p.term).period)}${p.author?" · "+esc(p.author):""}</span><span class="status">${esc(p.status)}</span></div><h3>${esc(p.title)}</h3><p>${esc(p.action)}</p><small>${esc(p.note)}</small>${source(p.source,'Ver documento')}</article>`).join('')||'<div class="empty-list">Nenhum registro documentado neste filtro.</div>';
}
function setupCases(){
 const term=q('#case-term');term.innerHTML='<option value="all">Todos os mandatos</option>'+D.terms.map(t=>`<option value="${t.id}">${esc(t.period)}</option>`).join('');
 const types=q('#case-type');types.innerHTML='<option value="all">Todas as naturezas</option>'+[...new Set(D.cases.map(x=>x.kind))].sort().map(x=>`<option>${esc(x)}</option>`).join('');
 term.onchange=renderCases;types.onchange=renderCases;q('#case-search').oninput=e=>{state.caseSearch=e.target.value.toLocaleLowerCase('pt-BR');renderCases()};renderCases();
}
function renderCases(){
 const term=q('#case-term').value,type=q('#case-type').value;
 const cases=D.cases.filter(c=>(term==='all'||c.term===term)&&(type==='all'||c.kind===type)&&(!state.caseSearch||[c.title,c.facts,c.actor,c.area,c.stage,c.boundary].join(' ').toLocaleLowerCase('pt-BR').includes(state.caseSearch))).sort((a,b)=>a.year-b.year);
 q('#case-count').textContent=`${cases.length} caso(s) encontrado(s)`;q('#case-list').innerHTML=cases.map(c=>`<article class="case-card"><div class="case-top"><span class="case-period">${esc(D.terms.find(x=>x.id===c.term).period)} · ${esc(c.period)}</span><span class="case-type">${esc(c.kind)}</span></div><h3>${esc(c.title)}</h3><p class="case-area">${esc(c.area)} · ${esc(c.actor)}</p><div class="case-divider"></div><span class="case-caption">O QUE A FONTE DOCUMENTA</span><p>${esc(c.facts)}</p><div class="case-stage"><b>Situação identificada</b><span>${esc(c.stage)}</span></div><div class="case-caveat"><b>O que NÃO conclui</b><p>${esc(c.boundary)}</p></div><a href="${esc(c.source)}" target="_blank" rel="noopener noreferrer">${esc(c.source_label)} ↗</a></article>`).join('')||'<div class="empty-list">Nenhum caso neste filtro.</div>';
}
function setupBudget(){
 const areas=[...new Set(D.budget.map(x=>x.area))],sel=q('#chart-area');
 sel.innerHTML=areas.map(x=>`<option>${esc(x)}</option>`).join('');
 q('#chart-term').innerHTML='<option value="all">Todos os anos disponíveis</option>'+D.terms.map(t=>`<option value="${t.id}">${t.period}</option>`).join('');
 sel.onchange=()=>{state.chartArea=sel.value;renderChart()};q('#chart-term').onchange=e=>{state.chartTerm=e.target.value;renderChart()};renderChart();
}
function renderChart(){
 let rows=D.budget.filter(x=>x.area===state.chartArea).sort((a,b)=>a.year-b.year);
 if(state.chartTerm!=='all'){const a=+state.chartTerm;rows=rows.filter(x=>x.year>=a&&x.year<=a+3)}
 q('#chart-title').textContent=state.chartArea+' · Despesa liquidada';
 const exceptional=state.chartArea==='Encargos especiais';
 q('#budget-explanation').textContent=exceptional?'Encargos especiais é função contábil (inclui dívida e outras obrigações), não uma área finalística de serviço público. Não compare esses valores como gasto direto com cidadãos.':'A série usa despesa liquidada da União em valores nominais. Os números não medem sozinhos a qualidade dos serviços.';
 q('#chart-table').innerHTML=rows.length?'<div class="data-list">'+rows.map(r=>`<span><b>${r.year}:</b> R$ ${fmt(r.liquidado_milhoes/1000)} bi</span>`).join('')+'</div>':'';
 if(!rows.length){q('#chart').innerHTML='<div class="chart-empty"><h3>Dados ainda não consolidados para este mandato</h3><p>Os valores históricos estão disponíveis no SIOP, mas ainda não foram extraídos e conferidos na mesma métrica. A ausência de pontos evita uma comparação enganosa.</p></div>';return}
 const W=760,H=310,left=78,right=32,top=24,bottom=56,max=Math.max(...rows.map(r=>r.liquidado_milhoes/1000))*1.15;
 const scaleX=i=>left+((W-left-right)/(Math.max(rows.length-1,1)))*i;
 const scaleY=y=>H-bottom-y/max*(H-top-bottom);
 const pts=rows.map((r,i)=>[scaleX(i),scaleY(r.liquidado_milhoes/1000)]);
 let inner='';for(let i=0;i<=4;i++){const v=max*i/4,y=scaleY(v);inner+=`<line class="gridline" x1="${left}" y1="${y}" x2="${W-right}" y2="${y}"/><text x="${left-12}" y="${y+4}" text-anchor="end">${fmt(v)}</text>`}
 inner+=`<path class="line" d="${pts.map((p,i)=>(i?'L':'M')+p[0]+','+p[1]).join(' ')}"/>`;
 inner+=pts.map((p,i)=>`<circle class="point" cx="${p[0]}" cy="${p[1]}" r="6"><title>${rows[i].year}: R$ ${fmt(rows[i].liquidado_milhoes/1000)} bilhões liquidados</title></circle><text text-anchor="middle" x="${p[0]}" y="${H-24}">${rows[i].year}</text>`).join('');
 q('#chart').innerHTML=`<svg class="chart-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Linha de despesa liquidada em ${state.chartArea} nos anos ${rows.map(x=>x.year).join(', ')}; R$ bilhões correntes"><text x="${left}" y="14">R$ bilhões</text>${inner}</svg>`;
}
function setupSources(){
 const keys=['presidencia','historico','ibge2020','ibge','siop','sal2011','sal2015','sal2023','tse','tse_bens','receita','dilma10','bolsonaro18'];
 const names=['Histórico oficial dos presidentes','Acervos de mandatos encerrados','IBGE — 2020, despesas liquidadas','IBGE — 2021–2024, despesas liquidadas','SIOP — orçamento federal','Salários — decreto 805/2010','Salários — decreto 277/2014','Salários — decreto 172/2022','TSE — candidaturas e programas','TSE — bens declarados','Receita — quadro societário','Propostas de campanha de Dilma (2010)','Propostas de Bolsonaro (2018)'];
 q('#sources').innerHTML=keys.map((k,i)=>`<a href="${esc(D.sources[k])}" target="_blank" rel="noopener noreferrer">${esc(names[i])} ↗</a>`).join('');
}
function boot(){if(!D){document.body.innerHTML='Não foi possível carregar o conjunto de dados.';return}renderTerms();setupPolicies();setupBudget();setupCases();setupSources();q('#menu-btn').onclick=()=>{let nav=q('#nav'),open=nav.classList.toggle('open');q('#menu-btn').setAttribute('aria-expanded',String(open))};document.querySelectorAll('#nav a').forEach(a=>a.onclick=()=>q('#nav').classList.remove('open'))}
boot();
