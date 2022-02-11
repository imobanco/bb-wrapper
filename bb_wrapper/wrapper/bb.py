from .request import RequestsWrapper, requests
from ..constants import IS_SANDBOX, BASIC_TOKEN, GW_APP_KEY


class BaseBBWrapper(RequestsWrapper):
    """
    wrapper base do BB (Banco do Brasil)
    """

    BASE_SCHEMA = "https://"
    BASE_SUBDOMAIN = "api"
    BASE_SANDBOX_ADITION = ".sandbox"
    BASE_PROD_ADITION = ""
    BASE_DOMAIN = ".bb.com.br"

    SCOPE = ""

    def __init__(
        self,
        basic_token=None,
        is_sandbox=None,
        gw_app_key=None,
        verify_https=False,
        cert=None,
    ):
        if is_sandbox is None:
            is_sandbox = IS_SANDBOX

        if basic_token is None:
            basic_token = BASIC_TOKEN

        if gw_app_key is None:
            gw_app_key = GW_APP_KEY

        self.__basic_token = basic_token
        self.__gw_app_key = gw_app_key
        self._is_sandbox = is_sandbox
        self.__access_token = None
        self.__token_type = None

        if self.__basic_token == "" or self.__gw_app_key == "":
            raise ValueError("Configure o basic_token/gw_app_key do BB!")

        base_url = self._construct_base_url()

        super().__init__(base_url=base_url, verify_https=verify_https, cert=cert)

    def _construct_base_url(self):
        if self._is_sandbox:
            adition = self.BASE_SANDBOX_ADITION
        else:
            adition = self.BASE_PROD_ADITION
        base_url = (
            f"{self.BASE_SCHEMA}"
            f"{self.BASE_SUBDOMAIN}"
            f"{adition}"
            f"{self.BASE_DOMAIN}"
        )
        return base_url

    def _construct_url(self, *args, **kwargs):
        url = super()._construct_url(*args, **kwargs)

        search = kwargs.get("search")
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
        """
        https://forum.developers.bb.com.br/t/status-code-415-unsupported-media-type-somente-em-producao/1123

        O endpoint oauth recebe application/x-www-form-urlencoded!
        """
        url = (
            f"{BaseBBWrapper.BASE_SCHEMA}"
            f"oauth"
            f'{".sandbox" if self._is_sandbox else ""}'
            f"{BaseBBWrapper.BASE_DOMAIN}"
            f"/oauth/token"
        )
        header = {"Authorization": f"Basic {self.__basic_token}"}

        data = {
            "grant_type": "client_credentials",
            "scope": self.SCOPE,
        }
        kwargs = dict(headers=header, verify=False, data=data)

        response = requests.post(url, **kwargs)
        response = self._process_response(response)
        self.__access_token = response.data["access_token"]
        self.__token_type = response.data["token_type"]
        return response
