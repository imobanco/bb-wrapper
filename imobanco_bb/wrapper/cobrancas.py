from .bb import BaseBBWrapper
from ..models.boleto import Boleto


class CobrancasBBWrapper(BaseBBWrapper):
    def _construct_base_url(self):
        base_url = super()._construct_base_url()
        base_url += "/cobrancas/v1/boletos"
        return base_url

    def registra_boleto(self, data):
        """"""
        Boleto(**data)
        self.authenticate()
        url = self._construct_url()
        response = self._post(url, data)
        return response

    def consulta_boleto(self, numero):
        """"""
        self.authenticate()
        url = self._construct_url(
            identifier=numero, search={"numeroConvenio": self._convenio_number}
        )
        response = self._get(url)
        return response
