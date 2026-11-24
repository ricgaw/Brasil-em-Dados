'use strict';
/* Exploração das funções orçamentárias, sem inventar LOA em anos não coletados. */
(function () {
  const atlas=window.ATLAS||{};
  const history=Array.isArray(atlas.budget)?atlas.budget:[];
  const changes=Array.isArray(window.BUDGET_CHANGES)?window.BUDGET_CHANGES:[];
  const el=id=>document.getElementById(id);
  const escaped=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const nf=n=>new Intl.NumberFormat('pt-BR',{maximumFractionDigits:1}).format(n);
  const money=n=>`R$ ${nf(n/1000)} bi`;
  const budgetYears=[2020,2021,2022,2023,2024];
  const allYears=Array.from({length:16},(_,i)=>2011+i);
  const areas=[...new Set(history.map(x=>x.area))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  const fixed=new Map(history.map(x=>[`${x.area}|${x.year}`,x]));
  function lineSvg(area){
    const values=budgetYears.map(y=>fixed.get(`${area}|${y}`)?.liquidado_milhoes??null);
    const available=values.filter(v=>v!==null);
    if(available.length<2)return '';
    const ceiling=Math.max(...available)*1.14||1,W=250,H=76, pad=8;
    const points=values.map((v,i)=>v===null?null:[pad+i*(W-2*pad)/4,H-pad-v/ceiling*(H-2*pad)]);
    // Segmentos desconectados: lacunas nunca são interpoladas.
    const paths=[];let curr=[];
    for(const p of [...points,null]){if(p)curr.push(p);else if(curr.length){if(curr.length>1)paths.push(curr.map((xy,i)=>`${i?'L':'M'} ${xy[0].toFixed(2)} ${xy[1].toFixed(2)}`).join(' '));curr=[];}}
    const dots=points.map((p,i)=>p?`<circle cx="${p[0]}" cy="${p[1]}" r="3.4"><title>${budgetYears[i]}: ${money(values[i])} liquidado</title></circle>`:'').join('');
    const pathsHtml=paths.map(p=>`<path d="${p}"/>`).join('');
    return `<svg class="areas-spark" viewBox="0 0 ${W} ${H}" role="img" aria-label="Série de despesa liquidada de ${escaped(area)} entre 2020 e 2024, sem ligar valores ausentes">${pathsHtml}${dots}</svg>`;
  }
  function init(){
    if(!el('areas-grid'))return;
    el('areas-count').textContent=`${areas.length} funções orçamentárias`;
    const select=el('areas-year');
    select.innerHTML='<option value="all">2020–2024 (série)</option>'+budgetYears.map(y=>`<option value="${y}">${y}</option>`).join('');
    el('areas-search').addEventListener('input',render);
    select.addEventListener('change',render);
    render();
  }
  function render(){
    const search=el('areas-search').value.trim().toLocaleLowerCase('pt-BR');
    const year=el('areas-year').value;
    const listed=areas.filter(a=>a.toLocaleLowerCase('pt-BR').includes(search));
    el('areas-result').textContent=`${listed.length} de ${areas.length} áreas · Despesa liquidada, não dotação inicial`;
    el('areas-grid').innerHTML=listed.map(area=>{
      const existing=budgetYears.map(y=>fixed.get(`${area}|${y}`)).filter(Boolean).sort((a,b)=>a.year-b.year);
      const latest=year==='all'?existing.at(-1):fixed.get(`${area}|${year}`);
      const coverage=existing.length;
      const yearLabel=latest?latest.year:'sem observação';
      // Nenhuma mudança em 2026 foi registrada para a função Saúde: apenas órgãos/UO.
      const changesInArea=changes.filter(x=>x.area===area);
      const changesText=changesInArea.length ? `${changesInArea.length} recortes institucionais de dotação verificados — não equivalem à função inteira`:'Dotação inicial/atualizada por função: ainda não importada';
      return `<article class="area-catalogue-card"><div class="area-catalogue-top"><span class="overline">FUNÇÃO ORÇAMENTÁRIA</span><span>${coverage}/5 anos</span></div><h4>${escaped(area)}</h4>${lineSvg(area)}<div class="area-last"><span>${year==='all'?'Último valor disponível':yearLabel}</span><strong>${latest?money(latest.liquidado_milhoes):'Não disponível'}</strong></div><small>Despesa liquidada · ${latest?latest.year:'sem valor para o ano escolhido'} · R$ correntes</small><p>${escaped(changesText)}</p></article>`;
    }).join('')||'<p class="area-no-data">Não encontramos áreas com esse nome.</p>';
  }
  function coverageMatrix(){
    if(!el('areas-coverage'))return;
    const units=new Map();
    for(const r of changes){if(!r.id_escopo.startsWith('funcao-'))continue;units.set(`${r.area}|${r.ano}`,true);}
    el('areas-coverage').innerHTML=`<div class="coverage-map-scroll"><table class="coverage-map"><caption>Cobertura auditada de dotações por FUNÇÃO — não confundir com órgãos e unidades</caption><thead><tr><th scope="col">Função</th>${allYears.map(y=>`<th scope="col">${y}</th>`).join('')}</tr></thead><tbody>${areas.map(area=>`<tr><th scope="row">${escaped(area)}</th>${allYears.map(y=>units.has(`${area}|${y}`)?'<td class="covered" title="Dotação validada">●</td>':'<td class="missing" title="Dotação ainda não validada">—</td>').join('')}</tr>`).join('')}</tbody></table></div><p class="coverage-note">— = ainda não incorporado, NÃO significa orçamento zero ou corte. A dotação dos órgãos Ministério da Saúde e Fiocruz não preenche a linha da função Saúde. Fonte para novas exportações: <a href="https://orcamento.dados.gov.br/siopdoc/doku.php/acesso_publico:consulta_livre" target="_blank" rel="noopener noreferrer">consulta livre SIOP ↗</a>.</p>`;
  }
  init();coverageMatrix();
})();
