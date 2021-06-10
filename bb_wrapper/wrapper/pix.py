import uuid

from .bb import BaseBBWrapper


class PIXCobBBWrapper(BaseBBWrapper):
    """
    Wrapper da API PIX de cobranças (recebimento na conta berço)
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _construct_base_url(self, *args):
        base_url = (
            f"{self.BASE_SCHEMA}"
            f"api"
            f'{".hm" if self._is_sandbox else ""}'
            f"{self.BASE_DOMAIN}"
        )
        base_url += "/pix/v1"
        for arg in args:
            base_url += f"/{arg}"
        return base_url

    def listar_pix(self):
        """
        Método para consultar todos os pix recebidos.
        """
        url = self._construct_url(end_bar=True)

        self.authenticate()

        response = self._get(url)

        return response

    def consultar_pix(self, end_to_end_id):
        """
        Método para consultar um pix recebido.

        Args:
            end_to_end_id: identificador end_to_end do pix
        """
        url = self._construct_url("pix", end_to_end_id)

        self.authenticate()

        response = self._get(url)

        return response

    def devolver_pix(self, end_to_end_id, valor, _id):
        """
        Método para devolver uma quantia de um pix recebido.

        Args:
            end_to_end_id: identificador end_to_end do pix
            valor: valor a ser devolvido (formato int vulgo 10.00 para R$ 10,00)
            _id: identificador único da devolução
        """
        url = self._construct_url("pix", end_to_end_id, "devolucao", _id)

        self.authenticate()

        response = self._put(url, {"valor": valor})

        return response

    def consultar_devolucao_pix(self, end_to_end_id, _id):
        """
        Método para consultar uma devolução feita.

        Args:
            end_to_end_id: identificador end_to_end do pix
            _id: identificador único da devolução
        """
        url = self._construct_url("pix", end_to_end_id, "devolucao", _id)

        self.authenticate()

        response = self._get(url)

        return response

    def criar_cobranca(self, data):
        """
        Criar uma cobrança PIX
        """
        url = self._construct_url("cob", end_bar=True)

        self.authenticate()

        response = self._put(url, data)

        return response

    def criar_cobranca_qrcode(self, data):
        """
        Criar uma cobrança PIX com QRCode dinâmico
        """
        url = self._construct_url("cobqrcode", end_bar=True)

        self.authenticate()

        response = self._put(url, data)

        return response

    def consultar_cobranca(self, txid):
        url = self._construct_url("cob", txid)

        self.authenticate()

        response = self._get(url)

        return response
