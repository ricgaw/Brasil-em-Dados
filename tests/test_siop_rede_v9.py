import io
import unittest
import urllib.error
from unittest.mock import patch
from scripts import coletar_siop_loa as siop

URL='https://orcamento.dados.gov.br/exemplo.csv.gz'

class FakeResponse:
    def __init__(self, payload=b'csv'):
        self.payload=payload
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def geturl(self): return URL
    def read(self, n): return self.payload

class NetworkTests(unittest.TestCase):
    def test_retry_after_timeout(self):
        with patch.object(siop.urllib.request,'urlopen',side_effect=[urllib.error.URLError('timed out'),FakeResponse()]) as fetch, patch.object(siop.time,'sleep'):
            self.assertEqual(siop.get(URL),b'csv')
            self.assertEqual(fetch.call_count,2)
    def test_stop_after_three_timeouts(self):
        with patch.object(siop.urllib.request,'urlopen',side_effect=urllib.error.URLError('timed out')) as fetch, patch.object(siop.time,'sleep'):
            with self.assertRaisesRegex(RuntimeError,'3 tentativas'):
                siop.get(URL)
            self.assertEqual(fetch.call_count,3)
    def test_no_retry_on_404(self):
        failure=urllib.error.HTTPError(URL,404,'Not found',{},None)
        with patch.object(siop.urllib.request,'urlopen',side_effect=failure) as fetch:
            with self.assertRaises(urllib.error.HTTPError):
                siop.get(URL)
            self.assertEqual(fetch.call_count,1)
    def test_reject_external_host(self):
        with self.assertRaises(ValueError):
            siop.get('https://example.com/loa2022.csv.gz')

if __name__=='__main__': unittest.main()
