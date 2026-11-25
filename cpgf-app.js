(() => {
'use strict';
const records=Array.isArray(window.CPGF_RESUMO)?window.CPGF_RESUMO:[];
const byId=id=>document.getElementById(id);
const text=(tag,s)=>{const e=document.createElement(tag);e.textContent=String(s);return e;};
const reais=c=>Number(c/100).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
const termOf=y=>y<=2014?'2011':y<=2018?'2015':y<=2022?'2019':'2023';
const org=byId('cpgf-org'),term=byId('cpgf-term'),status=byId('cpgf-status');if(!org||!term||!status)return;
const orgs=[...new Map(records.map(r=>[String(r.codigo_orgao_superior),String(r.nome_orgao_superior)])).entries()].sort((a,b)=>a[1].localeCompare(b[1],'pt-BR'));
for(const [code,name] of orgs){const opt=document.createElement('option');opt.value=code;opt.textContent=`${name} (${code})`;org.append(opt);}
function render(){
 const filtered=records.filter(r=>(term.value==='todos'||termOf(Number(r.ano))===term.value)&&(org.value==='todos'||String(r.codigo_orgao_superior)===org.value));
 const months=new Set(filtered.map(r=>r.periodo)), total=filtered.reduce((n,r)=>n+Number(r.valor_centavos),0), ntrans=filtered.reduce((n,r)=>n+Number(r.transacoes),0);
 const coverage=byId('cpgf-overview'),chart=byId('cpgf-bars'),table=byId('cpgf-table');coverage.replaceChildren();chart.replaceChildren();table.replaceChildren();status.replaceChildren();
 if(!records.length){const empty=text('div','');empty.className='cpgf-empty';empty.append(text('strong','Aguardando primeira importação oficial'),text('p','A infraestrutura para os cartões corporativos está preparada. Nenhum total será exibido até que um arquivo CPGF oficial seja validado e incorporado.'));status.append(empty);return;}
 status.append(text('strong',`Cobertura disponível: ${months.size} competência(s) nesta seleção.`),text('span',' Atenção: totais parciais, não são necessariamente anuais completos.'));
 for(const [label,val] of [['Total das competências importadas',reais(total)],['Transações publicadas',ntrans.toLocaleString('pt-BR')],['Meses representados',String(months.size)]]){const box=document.createElement('div');box.append(text('span',label),text('strong',val));coverage.append(box);}
 const years=new Map();for(const r of filtered){const y=Number(r.ano);years.set(y,(years.get(y)||0)+Number(r.valor_centavos));}
 const entries=[...years.entries()].sort((a,b)=>a[0]-b[0]),max=Math.max(1,...entries.map(x=>x[1]));
 for(const [year,amount] of entries){const row=document.createElement('div');row.className='cpgf-row';row.append(text('span',year));const track=document.createElement('div');track.className='cpgf-track';const fill=document.createElement('div');fill.className='cpgf-fill';fill.style.width=`${100*amount/max}%`;track.append(fill);row.append(track,text('strong',reais(amount)));chart.append(row);}
 const tbl=document.createElement('table');tbl.className='v7-table';const head=document.createElement('thead'),hr=document.createElement('tr');['Mês','Órgão','Transações','Valor'].forEach(x=>hr.append(text('th',x)));head.append(hr);tbl.append(head);const body=document.createElement('tbody');
 filtered.slice().sort((a,b)=>String(b.periodo).localeCompare(String(a.periodo))).forEach(r=>{const row=document.createElement('tr');[r.periodo,r.nome_orgao_superior,r.transacoes,reais(Number(r.valor_centavos))].forEach(v=>row.append(text('td',v)));body.append(row);});tbl.append(body);table.append(tbl);
}org.addEventListener('change',render);term.addEventListener('change',render);render();
})();
