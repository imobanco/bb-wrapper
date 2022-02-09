from .bb import BaseBBWrapper
from ..models.pagamentos import (
    LoteTransferencias,
    TransferenciaPIX,
    TransferenciaTED,
    LoteBoletosETributos,
    Boleto,
    Tributo,
)


class PagamentoLoteBBWrapper(BaseBBWrapper):
    """
    Wrapper da API Pagamentos em Lote
    """

    SCOPE = "pagamentos-lote.lotes-requisicao pagamentos-lote.transferencias-info pagamentos-lote.transferencias-requisicao pagamentos-lote.cancelar-requisicao pagamentos-lote.devolvidos-info pagamentos-lote.lotes-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-info pagamentos-lote.pagamentos-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-requisicao pagamentos-lote.pagamentos-codigo-barras-info pagamentos-lote.boletos-requisicao pagamentos-lote.guias-codigo-barras-info pagamentos-lote.guias-codigo-barras-requisicao pagamentos-lote.transferencias-pix-info pagamentos-lote.transferencias-pix-requisicao pagamentos-lote.pix-info pagamentos-lote.boletos-info"  # noqa
    BASE_PROD_ADITION = "-ip"
    BASE_DOMAIN = ".bb.com.br/pagamentos-lote/v1"
    # VERIFY_HTTPS = True
    CERT = (
        "/home/rodrigondec/prog/imobanco/bb-wrapper/certs/cert-chain.pem",
        "/home/rodrigondec/prog/imobanco/bb-wrapper/certs/key-private.pem",
    )

    def cadastrar_transferencia(self, lote_data, pagamento_data, pix=True):
        LoteTransferencias(**lote_data)
        if pix:
            TransferenciaPIX(**pagamento_data)
        else:
            TransferenciaTED(**pagamento_data)
        self.authenticate()
        url = self._construct_url("lotes-transferencias")
        data = {**lote_data, "listaTransferencias": [{**pagamento_data}]}
        response = self._post(url, data)
        return response

    def consultar_transferencia(self, _id):
        self.authenticate()
        url = self._construct_url("transferencias", _id)
        response = self._get(url)
        return response

    # def consultar_transferencias(self, dv):
    #     """
    #
    #     Args:
    #         dv: dígito verificador da conta corrente origem
    #     """
    #     search = {
    #         "digitoVerificadorContaCorrente": dv
    #     }
    #     self.authenticate()
    #     url = self._construct_url("lotes-transferencias", search=search)
    #     response = self._get(url)
    #     return response

    def liberar_pagamentos(self, number, days_to_pay=0):
        """

        Args:
            number: número da requisição
            days_to_pay: quantidade de dias que esse pagamento pode ser
                efetivado com relação à data do pagamento
        """
        self.authenticate()
        url = self._construct_url("liberar-pagamentos")
        data = {"numeroRequisicao": number, "indicadorFloat": days_to_pay}
        response = self._post(url, data)
        return response

    # def consultar_lote(self, number):
    #     self.authenticate()
    #     url = self._construct_url(number)
    #     response = self._get(url)
    #     return response

    def cadastrar_pagamento_boleto(self, lote_data, pagamento_data):
        LoteBoletosETributos(**lote_data)
        Boleto(**pagamento_data)
        self.authenticate()
        url = self._construct_url("lotes-boletos")
        pagamento_data = {**lote_data, "lancamentos": [{**pagamento_data}]}
        response = self._post(url, pagamento_data)
        return response

    def consultar_pagamento_boleto(self, _id):
        self.authenticate()
        url = self._construct_url("boletos", _id)
        response = self._get(url)
        return response

    def cadastrar_pagamento_tributo(self, lote_data, pagamento_data):
        LoteBoletosETributos(**lote_data)
        Tributo(**pagamento_data)
        self.authenticate()
        url = self._construct_url("lotes-guias-codigo-barras")
        pagamento_data = {**lote_data, "lancamentos": [{**pagamento_data}]}
        response = self._post(url, pagamento_data)
        return response

    def consultar_pagamento_tributo(self, _id):
        self.authenticate()
        url = self._construct_url("guias-codigo-barras", _id)
        response = self._get(url)
        return response
