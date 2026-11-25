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
