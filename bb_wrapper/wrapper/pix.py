import uuid

from .bb import BaseBBWrapper


class PIXBBWrapper(BaseBBWrapper):
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
        url = self._construct_url(end_bar=True)

        self.authenticate()

        response = self._get(url)

        return response

    def consultar_pix(self, end_to_end_id):
        url = self._construct_url("pix", end_to_end_id)

        self.authenticate()

        response = self._get(url)

        return response

    def devolver_pix(self, end_to_end_id, valor):
        url = self._construct_url("pix", end_to_end_id, "devolucao", str(uuid.uuid4()))

        self.authenticate()

        response = self._put(
            url,
            {
                "valor": valor
            }
        )

        return response

    def consultar_devolucao_pix(self, end_to_end_id, id):
        url = self._construct_url("pix", end_to_end_id, "devolucao", id)

        self.authenticate()

        response = self._get(url)

        return response

    def criar_cobranca(self, data):
        url = self._construct_url("cob", end_bar=True)

        self.authenticate()

        response = self._put(url, data)

        return response

    def consultar_cobranca(self, txid):
        url = self._construct_url("cob", txid)

        self.authenticate()

        response = self._get(url)

        return response
