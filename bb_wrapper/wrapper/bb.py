from datetime import datetime
import threading

from .request import RequestsWrapper, requests
from ..constants import IS_SANDBOX, BASIC_TOKEN, GW_APP_KEY


class BaseBBWrapper(RequestsWrapper):
    """
    wrapper base do BB (Banco do Brasil)
    """

    BASE_SCHEMA = "https://"
    BASE_SUBDOMAIN = "api"
    BASE_SANDBOX_ADDITION = ".sandbox"
    BASE_PROD_ADDITION = ""
    BASE_DOMAIN = ".bb.com.br"

    SCOPE = ""

    UNAUTHORIZED = [401, 403]

    TOKEN_EXPIRE_TIME = (10 * 60) - 30  # 9:30 minutos

    __data = threading.local()

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

        self.access_token = None
        self.token_type = None
        self.token_time = None

        if self.__basic_token == "" or self.__gw_app_key == "":
            raise ValueError("Configure o basic_token/gw_app_key do BB!")

        base_url = self._construct_base_url()

        super().__init__(base_url=base_url, verify_https=verify_https, cert=cert)

    @classmethod
    def clear_data(cls):
        cls.__data = threading.local()

    def _construct_base_url(self):
        if self._is_sandbox:
            addition = self.BASE_SANDBOX_ADDITION
        else:
            addition = self.BASE_PROD_ADDITION
        base_url = (
            f"{self.BASE_SCHEMA}"
            f"{self.BASE_SUBDOMAIN}"
            f"{addition}"
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
        return f"{self.token_type} {self.access_token}"

    @property
    def access_token(self):
        return self.__data.access_token

    @access_token.setter
    def access_token(self, value):
        if not hasattr(self.__data, "access_token") or not self.__data.access_token:
            self.__data.access_token = value

    @property
    def token_type(self):
        return self.__data.token_type

    @token_type.setter
    def token_type(self, value):
        if not hasattr(self.__data, "token_type") or not self.__data.token_type:
            self.__data.token_type = value

    @property
    def token_time(self):
        return self.__data.token_time

    @token_time.setter
    def token_time(self, value):
        if not hasattr(self.__data, "token_time") or not self.__data.token_time:
            self.__data.token_time = value

    def __should_authenticate(self):
        """
        A autenticação deve ser realizada se não houver Access Token
        ou se o tempo do token estiver expirado.
        """
        try:
            elapsed_time = datetime.now() - self.token_time
            is_token_expired = elapsed_time.total_seconds() >= self.TOKEN_EXPIRE_TIME
        except TypeError:
            is_token_expired = False
        is_token_missing = not self.access_token
        return is_token_missing or is_token_expired

    def __authenticate(self):
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

        if self.__should_authenticate():
            response = requests.post(url, **kwargs)
            response = self._process_response(response)
            self.__data.access_token = response.data["access_token"]
            self.__data.token_type = response.data["token_type"]
            self.__data.token_time = datetime.now()

        return True

    def _delete(self, url, headers=None) -> requests.Response:
        self.__authenticate()
        return super()._delete(url, headers)

    def _get(self, url, headers=None) -> requests.Response:
        self.__authenticate()
        return super()._get(url, headers)

    def _post(self, url, data, headers=None, use_json=True) -> requests.Response:
        self.__authenticate()
        return super()._post(url, data, headers, use_json)

    def _put(self, url, data, headers=None, use_json=True) -> requests.Response:
        self.__authenticate()
        return super()._put(url, data, headers, use_json)

    def _patch(self, url, data, headers=None, use_json=True) -> requests.Response:
        self.__authenticate()
        return super()._patch(url, data, headers, use_json)
