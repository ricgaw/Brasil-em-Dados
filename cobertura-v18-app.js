/* Transparência V18 — cobertura real, sem interpolação de métricas ausentes. */
(()=>{'use strict';
const source=window.COBERTURA_V18, box=document.getElementById('state-coverage-v18');
if(!source||!box)return;
const title=document.createElement('h3');title.textContent='Cobertura dos demonstrativos por empresa';box.append(title);
const note=document.createElement('p');note.textContent='Número de anos com registros documentados entre 2011 e 2026. Resultado, receita e dívida têm disponibilidades diferentes; campos ausentes não representam zero.';box.append(note);
const grid=document.createElement('div');grid.className='v18-grid';
for(const c of source.estatais){
 const card=document.createElement('article');card.className='v16-mini';
 const h=document.createElement('strong');h.textContent=c.nome;card.append(h);
 for(const [key,label] of [['anos_resultado','Resultado'],['anos_receita','Receita'],['anos_endividamento','Dívida']]){
  const p=document.createElement('p');p.textContent=`${label}: ${c[key].length}/16 anos`;card.append(p);
 }
 const years=document.createElement('small');years.textContent=c.anos_resultado.length?'Exercícios com resultado: '+c.anos_resultado.join(', '):'Nenhum ano com resultado verificado';card.append(years);
 grid.append(card);
}
box.append(grid);
const group=document.createElement('div');group.className='editorial-note';
const h=document.createElement('strong');h.textContent='Estatais federais · panorama agregado de 2025 (SEST)';
const p=document.createElement('p');p.textContent='Lucro líquido agregado: R$ 169,4 bilhões; faturamento agregado: cerca de R$ 1,4 trilhão. São cifras do conjunto de estatais analisado pela SEST, não soma dos quatro cards acima nem desempenho exclusivo de um presidente.';
const a=document.createElement('a');a.href='https://www.gov.br/gestao/pt-br/assuntos/noticias/2026/Julho/estatais-federais-lucram-r-169-4-bilhoes-em-2025-aumento-de-45-sobre-2024';a.target='_blank';a.rel='noopener noreferrer';a.textContent='Fonte: Relatório Agregado SEST 2026, ano-base 2025 ↗';
group.append(h,p,a);box.append(group);
const src=document.createElement('p');src.className='v7-footnote';src.textContent='Fontes históricas: ';
const link=document.createElement('a');link.href='https://www.gov.br/gestao/pt-br/assuntos/estatais/transparencia/defeso_relatorio%20agregado';link.target='_blank';link.rel='noopener noreferrer';link.textContent='Anexos históricos e relatórios da SEST ↗';src.append(link);box.append(src);
})();
