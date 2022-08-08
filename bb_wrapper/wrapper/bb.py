from .request import RequestsWrapper, requests
from ..constants import IS_SANDBOX, BASIC_TOKEN, GW_APP_KEY
from requests import HTTPError


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

    UNAUTHORIZED = [401, 403]

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

    def __authenticate(self, force_auth=False):
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

        if self.__access_token is None or force_auth is True:
            response = requests.post(url, **kwargs)
            response = self._process_response(response)
            self.__access_token = response.data["access_token"]
            self.__token_type = response.data["token_type"]

        return True

    def __do_request(self, request_method, *args, **kwargs) -> requests.Response:
        try:
            self.__authenticate()
            response = request_method(*args, **kwargs)

        except HTTPError as err:
            if err.response.status_code in self.UNAUTHORIZED:
                self.__authenticate(force_auth=True)
                return request_method(*args, **kwargs)

            raise err

        return response

    def _delete(self, url, headers=None) -> requests.Response:
        return self.__do_request(super()._delete, url, headers)

    def _get(self, url, headers=None) -> requests.Response:
        return self.__do_request(super()._get, url, headers)

    def _post(self, url, data, headers=None, use_json=True) -> requests.Response:
        return self.__do_request(super()._post, url, data, headers, use_json)

    def _put(self, url, data, headers=None, use_json=True) -> requests.Response:
        return self.__do_request(super()._put, url, data, headers, use_json)

    def _patch(self, url, data, headers=None, use_json=True) -> requests.Response:
        return self.__do_request(super()._patch, url, data, headers, use_json)
