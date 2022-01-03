from .bb import BaseBBWrapper
from ..models.pagamentos import LoteTransferencias, TransferenciaPIX, TransferenciaTED


class PagamentoLoteBBWrapper(BaseBBWrapper):
    """
    Wrapper da API Pagamentos em Lote
    """

    SCOPE = "pagamentos-lote.lotes-requisicao pagamentos-lote.transferencias-info pagamentos-lote.transferencias-requisicao pagamentos-lote.cancelar-requisicao pagamentos-lote.devolvidos-info pagamentos-lote.lotes-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-info pagamentos-lote.pagamentos-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-requisicao pagamentos-lote.pagamentos-codigo-barras-info pagamentos-lote.boletos-requisicao pagamentos-lote.guias-codigo-barras-info pagamentos-lote.guias-codigo-barras-requisicao pagamentos-lote.transferencias-pix-info pagamentos-lote.transferencias-pix-requisicao pagamentos-lote.pix-info pagamentos-lote.boletos-info"  # noqa

    def _construct_base_url(self):
        base_url = super()._construct_base_url()
        base_url += "/pagamentos-lote/v1"
        return base_url

    def criar_transferencia(self, lote_data, transferencia_data, pix=True):
        LoteTransferencias(**lote_data)
        if pix:
            TransferenciaPIX(**transferencia_data)
        else:
            TransferenciaTED(**transferencia_data)
        self.authenticate()
        url = self._construct_url("lotes-transferencias")
        data = {**lote_data, "listaTransferencias": [{**transferencia_data}]}
        response = self._post(url, data)
        return response

    def consultar_transferencia(self, _id):
        pass
