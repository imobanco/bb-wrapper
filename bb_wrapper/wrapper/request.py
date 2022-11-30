import random
from time import sleep
from json.decoder import JSONDecodeError

import requests

from requests import ConnectionError
from urllib3.exceptions import ProtocolError

from bb_wrapper.utils import _get_logger


logger = _get_logger("requests")


def retry_request(max_retries=5):
    def wrapper(func):
        def inner(*args, counter=None, **kwargs):
            counter = counter if counter is not None else max_retries
            try:
                sleep_time = random.randint(1, 90) / 100
                sleep(sleep_time)
                return func(*args, **kwargs)
            except (ConnectionResetError, ConnectionError, ProtocolError):
                if counter > 0:
                    counter -= 1
                    return inner(*args, counter=counter, **kwargs)
                raise

        return inner

    return wrapper


class RequestsWrapper:
    """
    wrapper da lib requests

    Attributes:
        __base_url: Url base para construir os requests
        __timeout: Tempo máximo de espera de requests
        __verity_https: flag que ativa verificação https
        __cert: certificado http
    """

    def __init__(self, *args, base_url, verify_https=True, cert=None, **kwargs):
        self.__base_url = base_url
        self._verify_https = verify_https
        self.__cert = cert
        self.__timeout = kwargs.get("timeout", None)

    @staticmethod
    def _process_response(response) -> requests.Response:
        """
        Processa a resposta.

        Adiciona o :attr:`.data` carregado do :meth:`requests.Response.json`.

        Args:
            response (:class:`requests.Response`): resposta a ser processada

        Raises:
            HttpError: quando a resposta não foi ok (200 <= status <= 299)!

        Returns:
            'objeto' (:class:`.requests.Response`) de resposta http
        """
        try:
            response.data = response.json(strict=False)
        except JSONDecodeError:
            response.data = {}
        response.reason = response.data
        response.raise_for_status()
        return response

    def _construct_url(self, *args, **kwargs):
        # noinspection PyProtectedMember
        """
        Constrói a url para o request.

        Args:
            args: lista de argumentos
            search: atributo de busca (dict ou string)

        Examples:
            >>> rw = RequestsWrapper()
            >>> rw._construct_url('acao', '1', 'subacao', search='algum_atributo=1')  # noqa:
            'rw.__base_url/acao/1/subacao?algum_atributo=1'

        Returns:
            url completa para o request
        """
        url = f"{self._base_url}"

        for arg in args:
            url += f"/{arg}"

        end_bar = kwargs.get("end_bar")
        if end_bar:
            url = f"{url}/"

        search = kwargs.get("search")
        if search:
            url += "?"
            if isinstance(search, dict):
                for index, (key, value) in enumerate(search.items()):
                    url += f"{key}={value}"
                    if index < len(search) - 1:
                        url += "&"
            else:
                url += f"{search}"
        return url

    @property
    def _auth(self):
        """
        Propriedade de autenticação

        Raises:
            NotImplementedError: É um método abstrato!
        """
        raise NotImplementedError("Must implement auth function!")

    @property
    def _authorization_header_data(self):
        return {"Authorization": self._auth}

    @property
    def _base_url(self):
        return self.__base_url

    def _get_request_info(self, headers=None):
        if not headers:
            headers = self._authorization_header_data

        headers["Content-type"] = "application/json"

        return dict(
            headers=headers,
            verify=self._verify_https,
            cert=self.__cert,
        )

    @retry_request(max_retries=3)
    def _delete(self, url, headers=None) -> requests.Response:
        """
        http delete

        Args:
            url: url de requisição

        Returns:
            (:class:`.requests.Response`)
        """
        request_info = self._get_request_info(headers)
        response = requests.delete(url, timeout=self.__timeout, **request_info)
        response = self._process_response(response)
        return response

    @retry_request(max_retries=3)
    def _get(self, url, headers=None) -> requests.Response:
        """
        http get

        Args:
            url: url de requisição

        Returns:
            (:class:`.requests.Response`)
        """
        request_info = self._get_request_info(headers)
        response = requests.get(url, timeout=self.__timeout, **request_info)
        response = self._process_response(response)
        return response

    @retry_request(max_retries=3)
    def _post(self, url, data, headers=None, use_json=True) -> requests.Response:
        """
        http post

        Args:
            url: url de requisição
            data (dict): dados da requisição
            headers: headers
            use_json: Flag

        Returns:
            (:class:`.requests.Response`)
        """
        request_info = self._get_request_info(headers)
        if use_json:
            request_info["json"] = data
        else:
            request_info["data"] = data
        response = requests.post(url, timeout=self.__timeout, **request_info)
        response = self._process_response(response)
        return response

    @retry_request(max_retries=3)
    def _put(self, url, data, headers=None, use_json=True) -> requests.Response:
        """
        http put

        Args:
            url: url de requisição
            data (dict): dados da requisição

        Returns:
            (:class:`.requests.Response`)
        """
        request_info = self._get_request_info(headers)
        if use_json:
            request_info["json"] = data
        else:
            request_info["data"] = data
        response = requests.put(url, timeout=self.__timeout, **request_info)
        response = self._process_response(response)
        return response

    @retry_request(max_retries=3)
    def _patch(self, url, data, headers=None, use_json=True) -> requests.Response:
        request_info = self._get_request_info(headers)
        if use_json:
            request_info["json"] = data
        else:
            request_info["data"] = data
        response = requests.patch(url, timeout=self.__timeout, **request_info)
        response = self._process_response(response)
        return response
