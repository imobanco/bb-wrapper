from .bb import BaseBBWrapper


class CobrancasBBWrapper(BaseBBWrapper):
    def _construct_base_url(self):
        base_url = super()._construct_base_url()
        base_url += "/cobrancas/v1/boletos"
        return base_url

    def registra_boleto(self, data):
        """"""
        self.authenticate()
        url = self._construct_url()
        response = self._post(url, data)
        return response
