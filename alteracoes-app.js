'use strict';
(function(){
 const data=Array.isArray(window.BUDGET_CHANGES)?window.BUDGET_CHANGES:[];
 const $=id=>document.getElementById(id);
 const brl=n=>new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:2}).format(n);
 const compact=n=>Math.abs(n)>=1e9?`R$ ${new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2}).format(n/1e9)} bi`:Math.abs(n)>=1e6?`R$ ${new Intl.NumberFormat('pt-BR',{maximumFractionDigits:2}).format(n/1e6)} mi`:brl(n);
 const pct=n=>new Intl.NumberFormat('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2}).format(Math.abs(n))+'%';
 const escape=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function options(items,heading){return `<option value="all">${heading}</option>`+items.map(x=>`<option value="${escape(x)}">${escape(x)}</option>`).join('')}
 function boot(){
  if(!$('changes-list'))return;
  const years=[...new Set(data.map(d=>d.ano))].sort((a,b)=>b-a),areas=[...new Set(data.map(d=>d.area))].sort();
  $('changes-year').innerHTML=options(years,'Todos os anos verificados');
  $('changes-area').innerHTML=options(areas,'Todas as áreas');
  for(const k of ['changes-year','changes-area','changes-direction'])$(k).onchange=render;
  render();
 }
 function render(){
   const year=$('changes-year').value,area=$('changes-area').value,dir=$('changes-direction').value;
   const rows=data.filter(r=>(year==='all'||String(r.ano)===year)&&(area==='all'||r.area===area)&&(dir==='all'||(dir==='decrease'&&r.delta_reais<0)||(dir==='increase'&&r.delta_reais>0)||(dir==='unchanged'&&r.delta_reais===0)));
   const inc=rows.filter(x=>x.delta_reais>0).length,dec=rows.filter(x=>x.delta_reais<0).length;
   $('changes-stats').innerHTML=`<div><span>OBSERVAÇÕES DOCUMENTADAS</span><strong>${rows.length}</strong><small>Não é o universo de despesas do país</small></div><div><span>COM AUMENTO LÍQUIDO</span><strong>${inc}</strong><small>Somente recortes publicados</small></div><div><span>COM REDUÇÃO LÍQUIDA</span><strong>${dec}</strong><small>Somente recortes publicados</small></div>`;
   if(!rows.length){$('changes-list').innerHTML='<div class="changes-empty">Não há observações verificadas neste filtro. A ausência de valores não significa que não tenha havido mudança orçamentária.</div>';$('changes-history').innerHTML='';return;}
   $('changes-list').innerHTML=rows.map(r=>{
     const sign=r.delta_reais>0?'Aumento':r.delta_reais<0?'Redução':'Sem alteração',cl=r.delta_reais>0?'increase':r.delta_reais<0?'decrease':'unchanged';
     const base=Math.max(r.dotacao_inicial_reais,r.dotacao_atualizada_reais)||1;
     const initial=100*r.dotacao_inicial_reais/base,updated=100*r.dotacao_atualizada_reais/base;
     const executed=r.liquidado_reais==null?'':`<span>Liquidado até a data: <b>${compact(r.liquidado_reais)}</b></span>`;
     return `<article class="change-card"><div class="change-head"><div><span class="overline">${escape(r.area)} · ${r.ano} · POSIÇÃO ${escape(r.data_referencia.split('-').reverse().join('/'))}</span><h4>${escape(r.escopo)}</h4></div><div class="change-tag ${cl}">${sign} líquido<br><strong>${r.delta_reais>0?'+':r.delta_reais<0?'−':''}${compact(r.delta_reais)}</strong><small>${r.delta_reais>0?'+':r.delta_reais<0?'−':''}${pct(r.delta_pct)}</small></div></div>
       <div class="budget-bars"><div><div class="bar-head"><span>Dotação inicial (LOA)</span><strong>${compact(r.dotacao_inicial_reais)}</strong></div><div class="bar-track"><i style="width:${initial.toFixed(3)}%;background:#93aaa0"></i></div></div><div><div class="bar-head"><span>Dotação atualizada</span><strong>${compact(r.dotacao_atualizada_reais)}</strong></div><div class="bar-track"><i style="width:${updated.toFixed(3)}%;background:${cl==='decrease'?'#b78b5b':'#27795c'}"></i></div></div></div>
       <div class="change-extra">${executed}<span>${escape(r.nota)}</span></div><a class="change-source" href="${escape(r.fonte)}" target="_blank" rel="noopener noreferrer">Consultar relatório original ↗</a></article>`
   }).join('');
   // Forma curva anual somente se a série possuir >=2 anos no mesmo recorte; nunca preencher lacunas.
   const groups=Object.groupBy?Object.groupBy(rows,r=>r.id_escopo):rows.reduce((a,r)=>((a[r.id_escopo]??=[]).push(r),a),{});
   const lines=Object.entries(groups).filter(([,arr])=>new Set(arr.map(x=>x.ano)).size>=2);
   $('changes-history').innerHTML=lines.length?lines.map(([id,arr])=>renderHistory(id,arr)).join(''):'<p class="changes-no-line">A linha de evolução anual será exibida quando houver pelo menos dois anos verificados do mesmo recorte. Não interpolamos exercícios sem dados.</p>';
 }
 function renderHistory(id,rows){
   const list=[...rows].sort((a,b)=>a.ano-b.ano),top=Math.max(...list.flatMap(x=>[x.dotacao_inicial_reais,x.dotacao_atualizada_reais]))*1.15;
   const W=710,H=260,l=60,r=30,t=20,b=38,x=i=>l+(W-l-r)*i/(list.length-1),y=n=>H-b-(H-t-b)*n/top;
   const path=key=>list.map((v,i)=>(i?'L':'M')+x(i)+' '+y(v[key])).join(' ');
   const lab=list.map((r,i)=>`<text x="${x(i)}" y="${H-10}" text-anchor="middle">${r.ano}</text>`).join('');
   return `<div class="changes-line"><h4>Evolução das dotações · ${escape(list[0].escopo)}</h4><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Dotação inicial e atualizada entre ${list[0].ano} e ${list.at(-1).ano}"><path d="${path('dotacao_inicial_reais')}" stroke="#93aaa0" fill="none" stroke-width="3"/><path d="${path('dotacao_atualizada_reais')}" stroke="#27795c" fill="none" stroke-width="3"/>${lab}</svg><small>Linha cinza: inicial · Linha verde: atualizada · valores nominais · lacunas não interpoladas</small></div>`;
 }
 boot();
})();
