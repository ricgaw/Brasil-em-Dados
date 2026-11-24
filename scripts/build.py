from pathlib import Path
import csv,json
root=Path(__file__).resolve().parents[1]
source={
 'ibge2020':'https://anuario.ibge.gov.br/images/aeb/2023/s7/2_pdf/s7t1102.pdf',
 'cotas2012':'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12711.htm',
 'pne2014':'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13005.htm',
 'royalties2013':'https://legis.senado.gov.br/norma/591306/publicacao/41149650',
 'terceirizacao2017':'https://legislacao.presidencia.gov.br/atos/?ano=2017&ato=d64gXQU5EeZpWTc21&numero=13429&tipo=LEI',
 'auxilio2020':'https://legislacao.presidencia.gov.br/atos/?ano=2020&ato=e4fcXQ61EMZpWT2e6&numero=13982&tipo=LEI',
 'auxiliobrasil2021':'https://legislacao.presidencia.gov.br/atos/?ano=2021&ato=8ebk3YU9UMZpWT35a&numero=14284&tipo=LEI',
 'solar2022':'https://legislacao.presidencia.gov.br/atos/?ano=2022&ato=c34MTQE1kMZpWT17f&data=06%2F01%2F2022&numero=14300&tipo=LEI',
 'pedeMeia2024':'https://www2.camara.leg.br/legin/fed/lei/2024/lei-14818-16-janeiro-2024-795255-norma-pl.html',
 'ensinoMedio2024':'https://legislacao.presidencia.gov.br/atos/?ano=2024&ato=841UTSU5ENZpWT3a9&data=31%2F07%2F2024&tipo=LEI',
 'celular2025':'https://www.camara.leg.br/noticias/1126717-sancionada-lei-que-proibe-o-uso-de-celular-em-escolas',
 'ir2025':'https://legis.senado.gov.br/norma/41758136/publicacao/41762089',
 'rreo':'https://www.tesourotransparente.gov.br/temas/contabilidade-e-custos/relatorio-resumido-da-execucao-orcamentaria-rreo-uniao',
 'presidencia':'https://www.gov.br/cti/pt-br/trajetoria-historica/presidentes-da-republica-desde-a-criacao-do-cti',
 'historico':'https://www.gov.br/casacivil/pt-br/acesso-a-informacao/receitas-e-despesas/acervos-de-mandatos-presidenciais-encerrados',
 'sal2011':'https://www2.camara.leg.br/legin/fed/decleg/2010/decretolegislativo-805-20-dezembro-2010-609780-publicacaooriginal-131088-pl.html',
 'sal2015':'https://www2.camara.leg.br/legin/fed/decleg/2014/decretolegislativo-277-18-dezembro-2014-779807-publicacaooriginal-145683-pl.html',
 'sal2023':'https://www2.camara.leg.br/legin/fed/decleg/2022/decretolegislativo-172-21-dezembro-2022-793529-publicacaooriginal-166604-pl.html',
 'tse':'https://www.tse.jus.br/comunicacao/noticias/2022/Novembro/quer-saber-mais-sobre-os-candidatos-acesse-o-divulgacandcontas',
 'ibge':'https://anuario.ibge.gov.br/images/aeb/2024/s7/2_pdf/s7t1102.pdf',
 'siop':'https://www.gov.br/planejamento/pt-br/assuntos/orcamento/sistema-integrado-de-planejamento-e-orcamento-siop',
 'pronatec':'https://www2.camara.leg.br/legin/fed/lei/2011/lei-12513-26-outubro-2011-611700-normaatualizada-pl.html',
 'mcmv':'https://legis.senado.gov.br/norma/585421',
 'dilma10':'https://assets-institucional-ipg.sfo2.cdn.digitaloceanspaces.com/2010/11/g1_011110_principaispropostascampanhadilma.pdf',
 'lbi':'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm',
 'ec95':'https://www12.senado.leg.br/noticias/materias/2016/12/15/promulgada-emenda-constitucional-do-teto-de-gastos',
 'trabalho':'https://www2.camara.leg.br/legin/fed/lei/2017/lei-13467-13-julho-2017-785204-norma-pl.html',
 'prev':'https://www12.senado.leg.br/noticias/materias/2019/11/12/promulgada-emenda-constitucional-da-reforma-da-previdencia',
 'saneamento':'https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/l14026.htm',
 'autonomia':'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp179.htm',
 'bolsonaro18':'https://agenciabrasil.ebc.com.br/politica/noticia/2018-10/veja-propostas-de-governo-de-jair-bolsonaro',
 'bolsa':'https://www.gov.br/mds/pt-br/noticias-e-conteudos/Noticias/2023/presidente-lula-sanciona-lei-que-institui-a-nova-versao-do-programa-bolsa-familia',
 'tributaria':'https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm',
 'arcabouco':'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp200.htm',
 'pac':'https://www.gov.br/casacivil/pt-br/novo-pac',
 'receita':'https://www.gov.br/pt-br/servicos/consultar-cadastro-nacional-de-pessoas-juridicas',
 'tse_bens':'https://www.tse.jus.br/comunicacao/noticias/2022/Agosto/eleicoes-2022-consulte-o-patrimonio-dos-candidatos-no-portal-do-tse',
 'plano_tse':'https://divulgacandcontas.tse.jus.br/divulga/#/',
 'temer_posse':'https://www12.senado.leg.br/noticias/materias/2016/08/31/dilma-rousseff-perde-o-mandato-e-temer-e-confirmado-presidente',
}
photos={
 'dilma':'https://commons.wikimedia.org/wiki/Special:FilePath/Dilma_Rousseff_-_foto_oficial_2011-01-09_(cropped2).jpg',
 'temer':'https://commons.wikimedia.org/wiki/Special:FilePath/Presidente_Michel_Temer_(foto_oficial)_-_cortada_(cropped_2).jpg',
 'bolsonaro':'https://commons.wikimedia.org/wiki/Special:FilePath/2019-01-10_Retrato_Oficial_do_Presidente_da_República_-_Jair_Messias_Bolsonaro_(cropped).jpg',
 'mourao':'https://commons.wikimedia.org/wiki/Special:FilePath/Hamilton_Mourão_(3x4).jpg',
 'lula':'https://upload.wikimedia.org/wikipedia/commons/f/f3/Foto_oficial_de_Luiz_In%C3%A1cio_Lula_da_Silva_%282023%E2%80%932027%29.jpg',
 'alckmin':'https://commons.wikimedia.org/wiki/Special:FilePath/Vice_Presidente_da_Rep%C3%BAblica_do_Brasil,_Geraldo_Alckmin_em_2023.jpg'
}
people={
 'dilma':{'name':'Dilma Vana Rousseff','short':'Dilma Rousseff','party':'PT','role':'Presidente','bio':'Economista e ex-ministra; presidente de 01/01/2011 a 31/08/2016.','img':'dilma'},
 'temer':{'name':'Michel Elias Temer Lulia','short':'Michel Temer','party':'PMDB (atual MDB)','role':'Vice-presidente / presidente','bio':'Vice eleito nas duas chapas de Dilma. Presidente de 31/08/2016 a 31/12/2018.','img':'temer'},
 'bolsonaro':{'name':'Jair Messias Bolsonaro','short':'Jair Bolsonaro','party':'PSL (eleição de 2018); posteriormente PL','role':'Presidente','bio':'Presidente de 01/01/2019 a 31/12/2022.','img':'bolsonaro'},
 'mourao':{'name':'Antônio Hamilton Martins Mourão','short':'Hamilton Mourão','party':'PRTB (eleição de 2018)','role':'Vice-presidente','bio':'Vice-presidente de 2019 a 2022.','img':'mourao'},
 'lula':{'name':'Luiz Inácio Lula da Silva','short':'Lula','party':'PT','role':'Presidente','bio':'Presidente no período 2023–2026 analisado; mandato em curso na data de corte.','img':'lula'},
 'alckmin':{'name':'Geraldo José Rodrigues Alckmin Filho','short':'Geraldo Alckmin','party':'PSB (eleição de 2022)','role':'Vice-presidente','bio':'Vice-presidente desde 01/01/2023; médico e ex-governador de São Paulo.','img':'alckmin'}
}
terms=[
 {'id':'2011','period':'2011–2014','title':'Primeiro mandato de Dilma','presidents':['dilma'],'vice':['temer'],'subtitle':'Ampliação de programas sociais, educação técnica e habitação.','salary':'R$ 26.723,13','salary_note':'subsídio bruto mensal de referência vigente desde fev/2011','salary_src':'sal2011'},
 {'id':'2015','period':'2015–2018','title':'Segundo mandato de Dilma · governo Temer','presidents':['dilma','temer'],'vice':['temer'],'subtitle':'Mandato iniciado por Dilma; Temer assume definitivamente em 31/08/2016 e não nomeia outro vice.','salary':'R$ 30.934,70','salary_note':'subsídio mensal fixado a partir de jan/2015; verificar atos posteriores','salary_src':'sal2015'},
 {'id':'2019','period':'2019–2022','title':'Governo Bolsonaro','presidents':['bolsonaro'],'vice':['mourao'],'subtitle':'Reformas previdenciária e regulatórias; período da pandemia de Covid-19.','salary':'R$ 30.934,70','salary_note':'subsídio legal de referência do período, conforme decreto de 2014','salary_src':'sal2015'},
 {'id':'2023','period':'2023–2026','title':'Governo Lula (terceiro mandato)','presidents':['lula'],'vice':['alckmin'],'subtitle':'Políticas de transferência de renda, reformas tributária e fiscal e investimentos anunciados.','salary':'R$ 46.366,19','salary_note':'subsídio bruto mensal legal a partir de fev/2025; não é contracheque líquido','salary_src':'sal2023'}
]
# Distinção central: 'lei instituída' não equivale a promessa totalmente entregue ou resultado.
policies=[
 ('2011','Educação','Ampliação do ensino profissionalizante','Pronatec instituído pela Lei 12.513/2011.','Norma instituída','pronatec','Não demonstra cobertura ou conclusão das vagas prometidas.'),
 ('2011','Habitação','Ampliação do Minha Casa, Minha Vida','Lei 12.424/2011 atualizou regras do Minha Casa, Minha Vida.','Norma instituída','mcmv','Não demonstra número de moradias entregues.'),
 ('2011','Combate à pobreza','Redução da pobreza extrema','Compromisso registrado em resumo da campanha de 2010. Indicador de resultado ainda não integrado.','Resultado a verificar','dilma10','Evitar afirmar erradicação sem série de pobreza comparável.'),
 ('2015','Direitos','Inclusão de pessoas com deficiência','Lei Brasileira de Inclusão (Lei 13.146/2015).','Norma instituída','lbi','Medida de governo; não tratada aqui como promessa específica de campanha.'),
 ('2015','Contas públicas','Novo Regime Fiscal / teto de gastos','EC 95/2016, promulgada durante o governo Temer.','Norma instituída','ec95','Medida de Temer após a mudança de presidente; não atribuir à plataforma eleitoral de Dilma.'),
 ('2015','Trabalho','Reforma trabalhista','Lei 13.467/2017, sancionada no governo Temer.','Norma instituída','trabalho','Efeitos econômicos e sociais requerem estudos separados.'),
 ('2019','Previdência','Reforma previdenciária','Emenda Constitucional 103/2019.','Norma instituída','prev','A reforma aprovada difere em aspectos da proposta original.'),
 ('2019','Saneamento','Atualização do marco legal do saneamento','Lei 14.026/2020.','Norma instituída','saneamento','Metas efetivas dependem de implementação por diferentes entes.'),
 ('2019','Economia','Autonomia do Banco Central','Lei Complementar 179/2021.','Norma instituída','autonomia','Aprovação normativa não é avaliação de resultados.'),
 ('2023','Assistência social','Retomada do Bolsa Família','Lei 14.601/2023 instituiu nova versão do programa.','Norma instituída','bolsa','Cobertura e valores pagos devem ser analisados em dados próprios.'),
 ('2023','Tributos','Reforma tributária sobre o consumo','Emenda Constitucional 132/2023.','Norma instituída','tributaria','Implantação é gradual e necessita de regulamentação.'),
 ('2023','Contas públicas','Novo regime fiscal','Lei Complementar 200/2023.','Norma instituída','arcabouco','Efeitos fiscais dependem da execução anual.'),
 ('2023','Infraestrutura','Novo PAC','Programa de investimentos anunciado e detalhado em portal oficial.','Programa anunciado','pac','Não confundir valores anunciados, contratados e efetivamente pagos.'),
]
policies.extend([
 ('2011', 'Educação', 'Lei de Cotas em universidades e institutos federais', 'Lei 12.711/2012 definiu regras de reserva de vagas nas instituições federais.', 'Norma instituída', 'cotas2012', 'Não equivale à mensuração de acesso, permanência ou conclusão.'),
 ('2011', 'Educação', 'Plano Nacional de Educação 2014', 'Lei 13.005/2014 aprovou o PNE e fixou metas para dez anos.', 'Norma instituída', 'pne2014', 'Metas, investimento e cumprimento devem ser avaliados separadamente.'),
 ('2011', 'Educação', 'Destinação dos royalties do petróleo', 'Lei 12.858/2013 fixou destinação de parte das receitas de petróleo para educação e saúde.', 'Norma instituída', 'royalties2013', 'Não demonstra o valor efetivamente aplicado em cada área.'),
 ('2015', 'Trabalho', 'Terceirização e trabalho temporário', 'Lei 13.429/2017 alterou regras de trabalho temporário e prestação de serviços.', 'Norma instituída', 'terceirizacao2017', 'Ato aprovado na presidência Temer; resultado sobre emprego exige evidências independentes.'),
 ('2019', 'Assistência social', 'Auxílio emergencial na pandemia', 'Lei 13.982/2020 criou medidas excepcionais de proteção social durante a pandemia.', 'Norma instituída', 'auxilio2020', 'O Congresso participou da formulação; avaliar pagamentos e cobertura separadamente.'),
 ('2019', 'Assistência social', 'Auxílio Brasil', 'Lei 14.284/2021 instituiu o Auxílio Brasil e o Alimenta Brasil.', 'Norma instituída', 'auxiliobrasil2021', 'Não confundir com os valores executados de assistência social na função orçamentária.'),
 ('2019', 'Energia', 'Marco legal da geração distribuída', 'Lei 14.300/2022 instituiu o marco da micro e minigeração distribuída.', 'Norma instituída', 'solar2022', 'Capacidade instalada e alcance do programa são indicadores distintos.'),
 ('2023', 'Educação', 'Programa Pé-de-Meia', 'Lei 14.818/2024 instituiu incentivo financeiro-educacional à permanência e conclusão do ensino médio.', 'Norma instituída', 'pedeMeia2024', 'Não inferir evasão evitada sem avaliação específica.'),
 ('2023', 'Educação', 'Reorganização do ensino médio', 'Lei 14.945/2024 alterou diretrizes e componentes curriculares do ensino médio.', 'Norma instituída', 'ensinoMedio2024', 'Execução envolve redes estaduais e implementação gradual.'),
 ('2023', 'Educação', 'Uso de dispositivos eletrônicos nas escolas', 'Lei 15.100/2025 restringiu o uso de aparelhos eletrônicos pessoais na educação básica.', 'Norma instituída', 'celular2025', 'Não significa, por si, mudança comprovada em aprendizagem ou saúde mental.'),
 ('2023', 'Tributos', 'Alterações no imposto de renda da pessoa física', 'Lei 15.270/2025 instituiu redutor do IRPF para rendas mensais de até R$ 5 mil a partir de 2026.', 'Norma instituída', 'ir2025', 'Regras de transição e impacto arrecadatório requerem avaliação própria.'),
])
policies=[dict(term=a,area=b,title=c,action=d,status=e,source=f,note=g) for a,b,c,d,e,f,g in policies]
# Atribuição pelo exercício da presidência, sem tratar ato normativo como cumprimento eleitoral.
for pol in policies:
    if pol['term']=='2015':
        pol['author']='Dilma Rousseff' if pol['source']=='lbi' else 'Michel Temer'

# IBGE/Tesouro RREO, despesa liquidada por função, valores em R$ milhões correntes (2021-2024)
budget={
 'Saúde':{2021:161393,2022:137881,2023:162410,2024:194761},
 'Educação':{2021:90094,2022:114580,2023:136081,2024:132551},
 'Assistência social':{2021:161127,2022:196871,2023:265424,2024:283135},
 'Previdência social':{2021:804532,2022:895358,2023:974117,2024:1046816},
 'Defesa nacional':{2021:78192,2022:81671,2023:82791,2024:87215},
 'Transporte':{2021:6432,2022:7866,2023:12984,2024:14898},
}
budget_expansion = {'Saúde': {2020: 151123}, 'Educação': {2020: 82166}, 'Assistência social': {2020: 412349}, 'Previdência social': {2020: 764239}, 'Defesa nacional': {2020: 76588}, 'Transporte': {2020: 7757}, 'Trabalho': {2020: 75875, 2021: 65833, 2022: 92793, 2023: 95745, 2024: 108934}, 'Segurança pública': {2020: 9872, 2021: 9614, 2022: 12408, 2023: 13873, 2024: 16049}, 'Cultura': {2020: 581, 2021: 585, 2022: 647, 2023: 2358, 2024: 2017}, 'Ciência e tecnologia': {2020: 6011, 2021: 4729, 2022: 8404, 2023: 12742, 2024: 14759}, 'Gestão ambiental': {2020: 3433, 2021: 2894, 2022: 3059, 2023: 4042, 2024: 14152}, 'Agricultura': {2020: 12439, 2021: 16037, 2022: 22449, 2023: 22076, 2024: 20356}, 'Administração': {2020: 22229, 2021: 22504, 2022: 26288, 2023: 27099, 2024: 24608}, 'Saneamento': {2020: 826, 2021: 446, 2022: 317, 2023: 150, 2024: 250}, 'Energia': {2020: 1224, 2021: 1568, 2022: 1368, 2023: 1108, 2024: 989}, 'Habitação': {2020: 2, 2021: 2, 2022: 3, 2023: None, 2024: 14}}
# Tabela 7.1.1.2, IBGE/Tesouro: liquidação, 2020 (AEB 2023) e 2021-2024 (AEB 2024).
# As funções abaixo não constavam dos 79 registros da edição anterior.
# Encargos especiais é função contábil, NÃO gasto finalístico com serviços públicos.
budget_additional = {
 'Legislativa': {2020:6305,2021:6428,2022:7521,2023:8119,2024:8179},
 'Judiciária': {2020:31448,2021:31549,2022:39813,2023:42202,2024:42933},
 'Essencial à Justiça': {2020:6636,2021:6663,2022:8318,2023:9137,2024:8608},
 'Relações exteriores': {2020:3647,2021:3652,2022:3892,2023:3892,2024:4618},
 'Direitos da cidadania': {2020:886,2021:598,2022:746,2023:886,2024:1231},
 'Urbanismo': {2020:1271,2021:1123,2022:1482,2023:1275,2024:1686},
 'Organização agrária': {2020:1288,2021:983,2022:1484,2023:2744,2024:2613},
 'Indústria': {2020:1458,2021:1471,2022:1768,2023:2050,2024:1928},
 'Comércio e serviços': {2020:6909,2021:1683,2022:1589,2023:2085,2024:3030},
 'Comunicações': {2020:1491,2021:1961,2022:3242,2023:2525,2024:2266},
 'Desporto e lazer': {2020:102,2021:214,2022:293,2023:351,2024:268},
 'Encargos especiais': {2020:1874551,2021:2408955,2022:2452484,2023:1091740,2024:1397526},
}
for area, years in budget_additional.items():
    assert area not in budget_expansion and area not in budget
    budget[area] = years

for area, years in budget_expansion.items():
    budget.setdefault(area, {}).update({y:v for y,v in years.items() if v is not None})
rows=[{'year':year,'area':area,'liquidado_milhoes':n,'fonte':('ibge2020' if year==2020 else 'ibge'),'metrica':'Despesa liquidada; União; função orçamentária; R$ milhões correntes'} for area,years in budget.items() for year,n in years.items()]
obj={'meta':{'title':'Brasil em Dados','cutoff':'2026-11-24','scope':'Quatro mandatos 2011–2026. Exercício 2026 ainda não concluído.','budget_info':'Série orçamentária parcialmente consolidada: 2020–2024, 28 funções (exceto reserva sem liquidação); fonte IBGE/RREO Tesouro Nacional. Despesa liquidada nominal, não orçamento aprovado, nem gasto por ministro/presidente. Não ajustado pela inflação.','budget_accounting_note':'A função Encargos especiais inclui operações financeiras e transferências contábeis; não deve ser somada como gasto finalístico em área de serviço.','company_info':'Participações societárias: nenhum vínculo atual individual foi confirmado por consulta histórica oficial de QSA nesta versão. Campo permanece a verificar; ausência de comprovação não significa inexistência.'},'sources':source,'photos':photos,'people':people,'terms':terms,'policies':policies,'budget':rows}
obj['cases']=json.loads((root/'data'/'casos_documentados.json').read_text(encoding='utf-8'))

with (root/'data'/'escandalos_investigacoes.csv').open('w',encoding='utf-8-sig',newline='') as file:
 fields=['id','term','year','period','title','area','kind','stage','actor','facts','boundary','source','source_label']
 writer=csv.DictWriter(file,fieldnames=fields,delimiter=';',lineterminator='\n');writer.writeheader();writer.writerows(obj['cases'])

(root/'data'/'atlas.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
with (root/'data'/'orcamento_2020_2024_ibge.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['year','area','liquidado_milhoes','fonte','metrica'],delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
# Embed JSON to work both file:// and GitHub Pages
(root/'data.js').write_text('window.ATLAS='+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
print('Generated',len(policies),'policies,',len(rows),'budget records')
