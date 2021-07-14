from json.decoder import JSONDecodeError

import requests

from ..utils import _get_logger


logger = _get_logger("requests")


class RequestsWrapper:
    """
    wrapper da lib requests

    Attributes:
        __base_url: Url base para construir os requests
    """

    VERIFY_HTTPS = False

    def __init__(self, base_url):
        self.__base_url = base_url

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
            response.data = response.json()
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
    def _base_url(self):
        return self.__base_url

    @property
    def _authorization_header_data(self):
        return {"Authorization": self._auth}

    def _delete(self, url, headers=None) -> requests.Response:
        """
        http delete

        Args:
            url: url de requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.delete(
            url,
            headers=headers if headers else self._authorization_header_data,
            verify=self.VERIFY_HTTPS,
        )
        response = self._process_response(response)
        return response

    def _get(self, url, headers=None) -> requests.Response:
        """
        http get

        Args:
            url: url de requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.get(
            url,
            headers=headers if headers else self._authorization_header_data,
            verify=self.VERIFY_HTTPS,
        )
        response = self._process_response(response)
        return response

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
        kwargs = dict(
            headers=headers if headers else self._authorization_header_data,
            verify=self.VERIFY_HTTPS,
        )
        if use_json:
            kwargs["json"] = data
        else:
            kwargs["data"] = data

        response = requests.post(url, **kwargs)
        response = self._process_response(response)
        return response

    def _put(self, url, data, headers=None) -> requests.Response:
        """
        http put

        Args:
            url: url de requisição
            data (dict): dados da requisição

        Returns:
            (:class:`.requests.Response`)
        """
        response = requests.put(
            url,
            json=data,
            headers=headers if headers else self._authorization_header_data,
            verify=self.VERIFY_HTTPS,
        )
        response = self._process_response(response)
        return response

    def _patch(self, url, data, headers=None) -> requests.Response:
        response = requests.patch(
            url,
            json=data,
            headers=headers if headers else self._authorization_header_data,
            verify=self.VERIFY_HTTPS,
        )
        response = self._process_response(response)
        return response
