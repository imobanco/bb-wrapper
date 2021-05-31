from datetime import date

from .bb import BaseBBWrapper


class PIXBBWrapper(BaseBBWrapper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _construct_base_url(self, *args):
        base_url = super()._construct_base_url()
        base_url += "/pix/v1"
        for arg in args:
            base_url += f"/{arg}"
        return base_url

    def lista_pix(self, data_inicio=date.today(), data_fim=date.today()):
        url = self._construct_url(search={
            "inicio": str(data_inicio),
            "fim": str(data_fim)
        })

        url = "https://api.sandbox.bb.com.br/pix/v1?inicio=2021-01-01&fim=2021-06-6&paginacao.itensPorPagina=100&gw-dev-app-key=d27b67790affabd01363e17d80050d56b901a5be"

        self.authenticate()

        response = self._get(url)

        return response
