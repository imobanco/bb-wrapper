from unittest import TestCase
from unittest.mock import MagicMock

from bb_wrapper.wrapper.pagamento_lote import PagamentoLoteBBWrapper
from bb_wrapper.constants import GW_APP_KEY
from bb_wrapper.services import QRCodeService, BarcodeService


class PagamentoLoteBBWrapperTestCase(TestCase):
    maxDiff = None

    def test_construct_url_1(self):
        """
        Dado:
            -
        Quando:
            - for chamado PagamentoLoteBBWrapper()._construct_url(end_bar=True)
        Então:
            - o resultado deve ter pelo menos o texto
                'https://api.hm.bb.com.br/pagamentos-lote/v1/?gw-dev-app-key='
        """
        result = PagamentoLoteBBWrapper()._construct_url(end_bar=True)

        expected = "https://api.sandbox.bb.com.br/pagamentos-lote/v1/?gw-dev-app-key="

        self.assertIn(expected, result)
