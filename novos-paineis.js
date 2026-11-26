(() => {
'use strict';
const SOCIAL=window.INDICADORES||[];
const FRENTES=window.FRENTES||[];
const el=id=>document.getElementById(id);
const pct=v=>Number(v).toLocaleString('pt-BR',{minimumFractionDigits:1,maximumFractionDigits:2})+'%';
const termOf=y=>y<=2014?'2011':y<=2018?'2015':y<=2022?'2019':'2023';
const periodOf=y=>y===2016?'2015–2018 · Dilma / Temer':y<=2014?'2011–2014 · Dilma':y<=2018?'2015–2018 · Dilma / Temer':y<=2022?'2019–2022 · Bolsonaro':'2023–2026 · Lula';
function svgNode(tag,attrs={},content){const n=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,String(v)));if(content!==undefined)n.textContent=content;return n;}
function cell(tag,content){const n=document.createElement(tag);n.textContent=String(content);return n;}
function draw(){
 const metric=el('social-metric')?.value||'desocupacao',term=el('social-term')?.value||'todos';
 const data=SOCIAL.filter(d=>d.indicador===metric&&(term==='todos'||termOf(+d.ano)===term)).sort((a,b)=>a.ano-b.ano);
 const plot=el('social-chart');if(!plot)return;plot.replaceChildren();
 if(!data.length){plot.append(cell('p','Ainda não há valores oficiais revisados para o indicador nesse mandato.'));el('social-summary').replaceChildren();el('social-table').replaceChildren();return;}
 const width=920,height=290,left=55,right=25,top=32,bottom=55;
 const values=data.map(d=>+d.valor),ymin=Math.max(0,Math.min(...values)-2),ymax=Math.max(...values)+2;
 const x=i=>left+(data.length===1?(width-left-right)/2:i*(width-left-right)/(data.length-1));
 const y=v=>top+(ymax-v)*(height-top-bottom)/(ymax-ymin||1);
 const svg=svgNode('svg',{viewBox:`0 0 ${width} ${height}`,role:'img','aria-label':`Evolução de ${metric} com ${data.length} observações`});
 for(let i=0;i<=4;i++){const val=ymin+(ymax-ymin)*i/4,yy=y(val);svg.append(svgNode('line',{x1:left,y1:yy,x2:width-right,y2:yy,stroke:'#dfebe2','stroke-width':1}));svg.append(svgNode('text',{x:9,y:yy+4,fill:'#6e8177','font-size':12},pct(val)));}
 data.forEach((d,i)=>{if(data.length<=9||i%2===0){svg.append(svgNode('text',{x:x(i),y:height-20,fill:'#59766b','font-size':12,'text-anchor':'middle'},d.ano));}});
 if(data.length>1)svg.append(svgNode('polyline',{points:data.map((d,i)=>`${x(i)},${y(+d.valor)}`).join(' '),stroke:'#21805e','stroke-width':3.4,fill:'none','stroke-linejoin':'round','stroke-linecap':'round'}));
 data.forEach((d,i)=>{const c=svgNode('circle',{cx:x(i),cy:y(+d.valor),r:4.8,fill:'#21805e',stroke:'#fff','stroke-width':2});c.append(svgNode('title',{},`${d.ano}: ${pct(d.valor)}`));svg.append(c);});plot.append(svg);
 const summary=el('social-summary');summary.replaceChildren();
 const first=data[0],last=data[data.length-1];
 for(const [label,value] of [['Início da seleção',`${first.ano} · ${pct(first.valor)}`],['Último ano disponível',`${last.ano} · ${pct(last.valor)}`],['Variação entre observações',data.length>1?`${(+last.valor-(+first.valor)).toLocaleString('pt-BR',{maximumFractionDigits:2})} p.p.`:'Indisponível (um ano)']]){const div=cell('div','');div.append(cell('span',label),cell('strong',value));summary.append(div);}
 const tab=document.createElement('table');tab.className='v7-table';const tr=document.createElement('tr');['Ano','Resultado','Mandato / contexto','Fonte'].forEach(h=>tr.append(cell('th',h)));const thead=document.createElement('thead');thead.append(tr);tab.append(thead);const tbody=document.createElement('tbody');data.forEach(d=>{const row=document.createElement('tr');[d.ano,pct(d.valor),periodOf(+d.ano)].forEach(t=>row.append(cell('td',t)));const td=document.createElement('td'),a=cell('a','IBGE ↗');a.href=d.url;a.target='_blank';a.rel='noopener noreferrer';td.append(a);row.append(td);tbody.append(row);});tab.append(tbody);el('social-table').replaceChildren(tab);
}
function renderFronts(){const container=el('fiscalizacao-grid');if(!container)return;const selection=el('fiscalizacao-filter')?.value||'todos';container.replaceChildren();FRENTES.filter(x=>selection==='todos'||x.id===selection).forEach(f=>{const article=document.createElement('article');article.className='v7-card';const tag=cell('span','FONTE LOCALIZADA · DADOS A CONSOLIDAR');tag.className='v7-tag';const h=cell('h3',f.titulo),detail=cell('p',f.descricao);const desc=cell('small',f.recorte);const note=cell('p',f.cautela);note.className='v7-caution';const a=cell('a',f.fonte+' ↗');a.href=f.url;a.target='_blank';a.rel='noopener noreferrer';article.append(tag,h,desc,detail,note,a);container.append(article);});}
if(el('social-chart')){el('social-metric').addEventListener('change',draw);el('social-term').addEventListener('change',draw);draw();}
if(el('fiscalizacao-grid')){el('fiscalizacao-filter').addEventListener('change',renderFronts);renderFronts();}
})();

/* Brasil em Dados V14 — painéis derivados somente dos dados já publicados. */
(() => {
 'use strict';
 const $ = id => document.getElementById(id);
 const atlas = window.ATLAS || {};
 const changes = Array.isArray(window.BUDGET_CHANGES) ? window.BUDGET_CHANGES : [];
 const social = Array.isArray(window.INDICADORES) ? window.INDICADORES : [];
 const terms = Array.isArray(atlas.terms) ? atlas.terms : [];
 const escape = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
 const period = year => year <= 2014 ? '2011' : year <= 2018 ? '2015' : year <= 2022 ? '2019' : '2023';
 const isFunction = item => typeof item.id_escopo === 'string' && item.id_escopo.startsWith('funcao-') && Number.isInteger(+item.ano);
 const functionRows = changes.filter(isFunction);
 const fmt = value => Number(value).toLocaleString('pt-BR', {maximumFractionDigits:2});
 const bi = value => `R$ ${fmt(value / 1e9)} bi`;
 const metricEnd = (metric, selection) => social.filter(x => x.indicador === metric && (selection === 'all' || period(+x.ano) === selection)).sort((a,b) => a.ano - b.ano).at(-1);
 function panorama() {
  const holder = $('panorama-cards');
  if (!holder) return;
  const selection = $('panorama-term').value;
  const matches = year => selection === 'all' || period(+year) === selection;
  const policies = (atlas.policies || []).filter(x => selection === 'all' || x.term === selection);
  const cases = (atlas.cases || []).filter(x => selection === 'all' || x.term === selection);
  const relevant = functionRows.filter(x => matches(x.ano));
  const years = [...new Set(relevant.map(x => +x.ano))].sort((a,b) => a-b);
  const completeYears = years.filter(year => relevant.filter(x => +x.ano === year).length === 28);
  const endIPCA = metricEnd('ipca', selection), endEmployment = metricEnd('desocupacao', selection);
  const ipcaLabel = endIPCA ? `${fmt(endIPCA.valor)}%` : 'Sem valor';
  const employmentLabel = endEmployment ? `${fmt(endEmployment.valor)}%` : 'Sem valor';
  const tiles = [
   ['Atos e medidas',String(policies.length),'Fichas selecionadas com documento de referência','#politicas'],
   ['Casos documentados',String(cases.length),'Fichas, não sentenças contra governantes','#escandalos'],
   ['Exercícios SIOP',`${completeYears.length}`,`${completeYears.length ? completeYears.join(', ') : 'Nenhum ano com 28 funções'} · dotação por função publicada`,'#alteracoes'],
   ['IPCA mais recente',ipcaLabel,endIPCA?`${endIPCA.ano} · acumulado anual (IBGE)`:'Nenhum ano para o período','#indicadores'],
   ['Desocupação mais recente',employmentLabel,endEmployment?`${endEmployment.ano} · taxa média anual (IBGE)`:'Nenhum ano para o período','#indicadores']
  ];
  holder.innerHTML = tiles.map(([label,value,note,url]) => `<a class="panorama-card" href="${url}"><span>${escape(label)}</span><strong>${escape(value)}</strong><small>${escape(note)}</small><b aria-hidden="true">↗</b></a>`).join('');
  const t = terms.find(x => x.id === selection);
  $('panorama-period-note').textContent = selection === 'all' ? 'Cobertura publicada: não equivale à totalidade das ações governamentais.' : `${t ? t.period : ''}${selection === '2015' ? ' · dois presidentes em 2016' : ''}. Dados por exercício, não nota de governo.`;
 }
 const years = Array.from({length:16},(_,i) => 2011+i);
 function chartSvg(rows,area){
  const vals = rows.flatMap(x => [x.dotacao_inicial_reais,x.dotacao_atualizada_reais,x.liquidado_reais]).filter(x => typeof x === 'number' && Number.isFinite(x) && x >= 0);
  if (!vals.length) return '<p>Sem valores numéricos validados para essa função.</p>';
  const W=940,H=290,l=76,r=26,t=28,b=47,top=Math.max(...vals)*1.12 || 1;
  const xx=y=>l+(+y-2011)*(W-l-r)/15, yy=v=>H-b-(v/top)*(H-t-b);
  let g='';for(let i=0;i<=4;i++){const v=top*i/4,y=yy(v);g+=`<line x1="${l}" y1="${y}" x2="${W-r}" y2="${y}" stroke="#e0e9e1"/><text x="${l-9}" y="${y+4}" text-anchor="end" fill="#63786e" font-size="11">${escape(fmt(v/1e9))}</text>`}
  years.forEach((year,i)=>{if(i%2===0||i===15)g+=`<text x="${xx(year)}" y="${H-18}" text-anchor="middle" fill="#63786e" font-size="11">${year}</text>`});
  const defs=[['dotacao_inicial_reais','#9baead','Inicial'],['dotacao_atualizada_reais','#14735b','Atualizada'],['liquidado_reais','#b38c50','Liquidada']];
  defs.forEach(([key,color,name])=>{
   let points=[];
   const flush=()=>{if(points.length>1)g+=`<polyline points="${points.join(' ')}" stroke="${color}" fill="none" stroke-width="3" stroke-linejoin="round"/>`;points=[]};
   for(const y of years){const item=rows.find(x=>+x.ano===y);const v=item&&typeof item[key]==='number'?item[key]:null;if(v===null){flush();continue;}points.push(`${xx(y)},${yy(v)}`);g+=`<circle cx="${xx(y)}" cy="${yy(v)}" r="4.3" fill="${color}" stroke="white" stroke-width="1.5"><title>${y} · ${name} · ${bi(v)}${y===2026?' · parcial':''}</title></circle>`}flush();
  });
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Séries por ano de dotação inicial, atualizada e liquidada da função ${escape(area)}, em bilhões de reais nominais"><text x="${l}" y="15" fill="#63786e" font-size="11">R$ bilhões</text>${g}</svg>`;
 }
 function budgetTrend(){
  const area = $('budget-trend-area')?.value;
  const chart = $('budget-trend-chart'), table = $('budget-trend-table');
  if(!chart || !table || !area)return;
  const latestByYear = new Map();
  functionRows.filter(x=>x.area===area).forEach(x=>{const key=+x.ano, previous=latestByYear.get(key);if(!previous||String(x.data_referencia||'')>String(previous.data_referencia||''))latestByYear.set(key,x);});
  const rows=[...latestByYear.values()].sort((a,b)=>+a.ano-+b.ano);
  chart.innerHTML= rows.length ? chartSvg(rows,area) : '<div class="panorama-empty">Ainda não há exercício consolidado para esta área.</div>';
  table.innerHTML= rows.length ? `<div class="budget-scroll"><table><thead><tr><th>Ano</th><th>Inicial</th><th>Atualizada</th><th>Variação</th><th>Liquidada</th><th>Origem</th></tr></thead><tbody>${rows.map(x=>`<tr><td>${escape(x.ano)}${+x.ano===2026?'*':''}</td><td>${bi(x.dotacao_inicial_reais)}</td><td>${bi(x.dotacao_atualizada_reais)}</td><td class="${x.delta_reais < 0?'budget-negative':'budget-positive'}">${x.delta_reais>0?'+':''}${fmt(x.delta_pct)}%</td><td>${typeof x.liquidado_reais==='number'?bi(x.liquidado_reais):'Não informada'}</td><td><a target="_blank" rel="noopener noreferrer" href="${escape(x.fonte)}">SIOP ↗</a></td></tr>`).join('')}</tbody></table></div>` : '';
  const latest = rows.at(-1);
  $('budget-trend-note').textContent = `Fonte SIOP; ${rows.length} exercício(s) publicado(s) para ${area}. Valores em reais nominais. ${latest?.ano === 2026?'* 2026 é parcial, sujeito a revisão. ':''}Variação percentual = (dotação atualizada − dotação inicial) / dotação inicial. Isso não mede isoladamente gastos adicionais ou cortes de serviços.`;
 }
 function init(){
  const sel=$('panorama-term');if(sel){sel.addEventListener('change',panorama);panorama()}
  const areaSelect=$('budget-trend-area');if(areaSelect){
   const fromChanges=[...new Set(functionRows.map(x=>x.area))];
   const fromBudget=[...new Set((atlas.budget||[]).map(x=>x.area))];
   const all=[...new Set([...fromChanges,...fromBudget])].sort((a,b)=>a.localeCompare(b,'pt-BR'));
   areaSelect.innerHTML=all.map(area=>`<option value="${escape(area)}" ${area==='Saúde'?'selected':''}>${escape(area)}</option>`).join('');
   areaSelect.addEventListener('change',budgetTrend);budgetTrend();
  }
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
