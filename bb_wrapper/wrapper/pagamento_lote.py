from .bb import BaseBBWrapper


class PagamentoLoteBBWrapper(BaseBBWrapper):
    """
    Wrapper da API Pagamentos em Lote
    """

    SCOPE = "pagamentos-lote.lotes-requisicao pagamentos-lote.transferencias-info pagamentos-lote.transferencias-requisicao pagamentos-lote.cancelar-requisicao pagamentos-lote.devolvidos-info pagamentos-lote.lotes-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-info pagamentos-lote.pagamentos-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-requisicao pagamentos-lote.pagamentos-codigo-barras-info pagamentos-lote.boletos-requisicao pagamentos-lote.guias-codigo-barras-info pagamentos-lote.guias-codigo-barras-requisicao pagamentos-lote.transferencias-pix-info pagamentos-lote.transferencias-pix-requisicao pagamentos-lote.pix-info pagamentos-lote.boletos-info"  # noqa

    def _construct_base_url(self):
        base_url = super()._construct_base_url()
        base_url += "/pagamentos-lotes/v1"
        return base_url

    def criar_transferencia(self):
        self.authenticate()
        url = self._construct_url("lotes-transferencias")
        data = {}
        response = self._post(url, data)
        return response
