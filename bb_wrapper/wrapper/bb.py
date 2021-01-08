import requests

from .request import RequestsWrapper
from ..constants import IS_SANDBOX, BASIC_TOKEN, GW_APP_KEY


class BaseBBWrapper(RequestsWrapper):
    """
    wrapper base do BB (Banco do Brasil)
    """

    BASE_SCHEMA = "https://"
    BASE_DOMAIN = ".bb.com.br"

    def __init__(self, basic_token=None, is_sandbox=None, gw_app_key=None):
        if is_sandbox is None:
            is_sandbox = IS_SANDBOX

        if basic_token is None:
            basic_token = BASIC_TOKEN

        if gw_app_key is None:
            gw_app_key = GW_APP_KEY

        self.__basic_token = basic_token
        self.__gw_app_key = gw_app_key
        self.__is_sandbox = is_sandbox
        self.__access_token = None
        self.__token_type = None

        if self.__basic_token == "" or self.__gw_app_key == "":
            raise ValueError("Configure o basic_token/gw_app_key do BB!")

        base_url = self._construct_base_url()

        super().__init__(base_url=base_url)

    def _construct_base_url(self):
        base_url = (
            f"{self.BASE_SCHEMA}"
            f"api"
            f'{".sandbox" if self.__is_sandbox else ""}'
            f"{self.BASE_DOMAIN}"
        )
        return base_url

    def _construct_url(self, *args, search=None):
        url = super()._construct_url(*args, search=search)
        if search is None:
            url += "?"
        else:
            url += "&"
        url += f"gw-dev-app-key={self.__gw_app_key}"
        return url

    @property
    def _auth(self):
        """
        Propriedade de autenticação.

        Returns:
            string de autenticação para o header
            Authorization
        """
        return f"{self.__token_type} {self.__access_token}"

    def authenticate(self):
        url = (
            f"{self.BASE_SCHEMA}"
            f"oauth"
            f'{".sandbox" if self.__is_sandbox else ""}'
            f"{self.BASE_DOMAIN}"
            f"/oauth/token"
        )
        header = {"Authorization": f"Basic {self.__basic_token}"}

        data = {
            "grant_type": "client_credentials",
            "scope": "cobrancas.boletos-info cobrancas.boletos-requisicao",
        }

        # https://superuser.com/a/1426579 => verify=False
        response = requests.post(url, data=data, headers=header, verify=False)
        response = self._process_response(response)
        self.__access_token = response.data["access_token"]
        self.__token_type = response.data["token_type"]
        return response
