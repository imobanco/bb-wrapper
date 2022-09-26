from datetime import datetime
import threading

from .request import RequestsWrapper, requests
from ..constants import IS_SANDBOX, BASIC_TOKEN, GW_APP_KEY
from requests.adapters import HTTPAdapter, Retry


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

    TOKEN_EXPIRE_TIME = (10 * 60) - 30  # 9:30 minutos
    AUTH_MAX_RETRY_ATTEMPTS = 5

    def __init__(
        self,
        *args,
        basic_token=None,
        is_sandbox=None,
        gw_app_key=None,
        verify_https=True,
        cert=None,
        **kwargs,
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

        if self.__basic_token == "" or self.__gw_app_key == "":
            raise ValueError("Configure o basic_token/gw_app_key do BB!")

        base_url = self._construct_base_url()

        super().__init__(
            *args,
            base_url=base_url,
            verify_https=verify_https,
            cert=cert,
            **kwargs,
        )

    def __new__(cls, *args, **kwargs):
        """
        Quando se fala de múltiplas classes com herança fazer:
            >>> getattr(self, f"_{self.__class__.__name__}__data", None)

        tem comportamento diferente de
            >>> self.__data

        Testado com BaseBBWrapper e PIXCobBBWrapper!

        Mesmo na classe filha (PIXCobBBWrapper), o
        'self.__data' é traduzido para '_BaseBBWrapper__data' ao invés
        de '_PIXCobBBWrapper__data'!
        """
        if not getattr(cls, f"_{cls.__name__}__data", None):
            cls.reset_data()
        return super().__new__(cls)

    @classmethod
    def reset_data(cls):
        """
        Quando se fala de múltiplas classes com herança fazer:
            >>> setattr(cls, f'_{cls.__name__}__data', threading.local())

        tem comportamento diferente de
            >>> cls.__data = threading.local()

        Testado com BaseBBWrapper e PIXCobBBWrapper!

        Mesmo na classe filha (PIXCobBBWrapper), o
        'cls.__data' é traduzido para '_BaseBBWrapper__data' ao invés
        de '_PIXCobBBWrapper__data'!
        """
        setattr(cls, f"_{cls.__name__}__data", threading.local())

    @property
    def _data(self):
        """
        Quando se fala de múltiplas classes com herança fazer:
            >>> getattr(self, f"_{self.__class__.__name__}__data", None)

        tem comportamento diferente de
            >>> self.__data

        Testado com BaseBBWrapper e PIXCobBBWrapper!

        Mesmo na classe filha (PIXCobBBWrapper), o
        'self.__data' é traduzido para '_BaseBBWrapper__data' ao invés
        de '_PIXCobBBWrapper__data'!
        """
        return getattr(self, f"_{self.__class__.__name__}__data", None)

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
        return f"{self._token_type} {self._access_token}"

    @property
    def _access_token(self):
        try:
            return self._data.access_token
        except AttributeError:
            return None

    @_access_token.setter
    def _access_token(self, access_token):
        self._data.access_token = access_token

    @property
    def _token_type(self):
        try:
            return self._data.token_type
        except AttributeError:
            return None

    @_token_type.setter
    def _token_type(self, token_type):
        self._data.token_type = token_type

    @property
    def _token_time(self):
        try:
            return self._data.token_time
        except AttributeError:
            return None

    @_token_time.setter
    def _token_time(self, token_time):
        self._data.token_time = token_time

    def __should_authenticate(self):
        """
        A autenticação deve ser realizada se não houver Access Token
        ou se o tempo do token estiver expirado.
        """
        try:
            elapsed_time = datetime.now() - self._token_time
            is_token_expired = elapsed_time.total_seconds() >= self.TOKEN_EXPIRE_TIME
        except TypeError:
            is_token_expired = False
        is_token_missing = not self._access_token
        return is_token_missing or is_token_expired

    def __oauth_url(self):
        return (
            f"{BaseBBWrapper.BASE_SCHEMA}"
            f"oauth"
            f'{".sandbox" if self._is_sandbox else ""}'
            f"{BaseBBWrapper.BASE_DOMAIN}"
            f"/oauth/token"
        )

    def __authenticate(self):
        """
        https://forum.developers.bb.com.br/t/status-code-415-unsupported-media-type-somente-em-producao/1123

        O endpoint oauth recebe application/x-www-form-urlencoded!
        """
        url = self.__oauth_url()
        header = {"Authorization": f"Basic {self.__basic_token}"}

        data = {
            "grant_type": "client_credentials",
            "scope": self.SCOPE,
        }
        kwargs = dict(headers=header, verify=self._verify_https, data=data)

        if self.__should_authenticate():
            session = requests.Session()
            retry_strategy = Retry(
                total=self.AUTH_MAX_RETRY_ATTEMPTS,
                backoff_factor=0.1,
                status_forcelist=[401, 429, 500, 502, 503, 504],
                allowed_methods=frozenset(["POST"]),
                raise_on_status=False,
            )
            session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
            session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
            response = session.post(url, **kwargs)
            response = self._process_response(response)
            self._access_token = response.data["access_token"]
            self._token_type = response.data["token_type"]
            self._token_time = datetime.now()
            return True
        return False

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
