from unittest import TestCase

from unittest.mock import patch
from requests import Timeout

from bb_wrapper.wrapper.request import RequestsWrapper


class RequestsWrapperTestCase(TestCase):
    maxDiff = None

    def test_contruct_url_1(self):
        """
        Dado:
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2')
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2"
        """
        base_url = "http://foo.bar"
        wrapper = RequestsWrapper(base_url=base_url)

        result = wrapper._construct_url("acao1", "id1", "subacao2", "id2")

        expected = "http://foo.bar/acao1/id1/subacao2/id2"

        self.assertEqual(result, expected)

    def test_contruct_url_2(self):
        """
        Dado:
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search='query1=1&query2=2')  # noqa
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"  # noqa
        """
        base_url = "http://foo.bar"
        wrapper = RequestsWrapper(base_url=base_url)

        result = wrapper._construct_url(
            "acao1", "id1", "subacao2", "id2", search="query1=1&query2=2"
        )

        expected = "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"

        self.assertEqual(result, expected)

    def test_contruct_url_3(self):
        """
        Dado:
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
        Quando:
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search=dict(query1=1, query2=2))  # noqa
        Então:
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"  # noqa
        """
        base_url = "http://foo.bar"
        wrapper = RequestsWrapper(base_url=base_url)

        result = wrapper._construct_url(
            "acao1", "id1", "subacao2", "id2", search=dict(query1=1, query2=2)
        )

        expected = "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"

        self.assertEqual(result, expected)

    def test_request_timeout(self):
        """
        Dado:
            - uma requisição qualquer
        Quando:
            - o servidor demorar X segundos para responder
        Então:
            - um erro de timeout deve ser lançado
        """
        self.headers_patcher = patch(
            "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
        )
        self.mocked_headers = self.headers_patcher.start()

        self.mocked_headers.return_value = {}

        wrapper = RequestsWrapper(base_url="", timeout=2)
        url = "https://httpstat.us/200?sleep=5000"
        with self.assertRaises(Timeout):
            wrapper._get(url)

        self.headers_patcher.stop()

    def test_retry_request(self):
        """
        Dado:
            - uma requisição qualquer
        Quando:
            - o ConnectionResetError é lançado
        Então:
            - a requisição deve ocorrer com sucesso
            - devem ter sido realizadas 4 requisições
              (3 tentativas falhas e 1 bem sucedida)
        """
        self.headers_patcher = patch(
            "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
        )
        self.mocked_headers = self.headers_patcher.start()

        max_retries = 3

        def raise_connection_reset_error(headers=None):
            call_count = self.mocked_headers.call_count
            if call_count <= max_retries:
                raise ConnectionResetError
            else:
                return dict()

        self.mocked_headers.side_effect = raise_connection_reset_error

        wrapper = RequestsWrapper(base_url="")
        url = "https://httpstat.us/200?sleep=1"
        wrapper._get(url)
        
        self.assertEqual(self.mocked_headers.call_count, 4)

        self.headers_patcher.stop()

    def test_fail_retry_request(self):
        """
        Dado:
            - uma requisição qualquer
        Quando:
            - o ConnectionResetError é lançado
        Então:
            - o erro de conexão deve ser lançado
              (4 tentativas falhas)
        """
        self.headers_patcher = patch(
            "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
        )
        self.mocked_headers = self.headers_patcher.start()

        def raise_connection_reset_error(headers=None):
            raise ConnectionResetError

        self.mocked_headers.side_effect = raise_connection_reset_error

        wrapper = RequestsWrapper(base_url="")
        url = "https://httpstat.us/200?sleep=1"
        with self.assertRaises(ConnectionResetError):
            wrapper._get(url)

        self.assertEqual(self.mocked_headers.call_count, 4)

        self.headers_patcher.stop()
