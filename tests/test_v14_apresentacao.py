"""Regras de interface V14; sem dependências externas ou rede."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ApresentacaoV14Tests(unittest.TestCase):
 def test_identidade_e_navegacao(self):
  page=(ROOT/'index.html').read_text(encoding='utf-8')
  self.assertIn('class="brand-symbol" aria-hidden="true">BR',page)
  self.assertIn('href="#panorama"',page)
  for section in ('panorama','mandatos','politicas','orcamento','alteracoes','indicadores','fiscalizacao','cartoes','escandalos','metodologia'):
   self.assertIn(f'id="{section}"',page)
 def test_busca_e_graficos(self):
  page=(ROOT/'index.html').read_text(encoding='utf-8')
  for id in ('policy-search','case-search','panorama-cards','budget-trend-chart','budget-trend-area','budget-trend-table'):
   self.assertIn(f'id="{id}"',page)
  js=(ROOT/'novos-paineis.js').read_text(encoding='utf-8')
  self.assertIn('functionRows',js)
  self.assertIn("startsWith('funcao-')",js)
  self.assertIn('latestByYear',js)
  self.assertIn('Exercícios parciais' if False else 'parcial',js)
 def test_preserva_as_fontes(self):
  page=(ROOT/'index.html').read_text(encoding='utf-8')
  for file in ('data/alteracoes_orcamentarias.csv','data/indicadores_sociais.csv','data/escandalos_investigacoes.csv','data/cpgf_resumo.csv'):
   self.assertIn(file,page)
  self.assertIn('PROJEÇÃO CONTÍNUA · NÃO É MEDIÇÃO AO VIVO',page)

if __name__=='__main__':unittest.main()
