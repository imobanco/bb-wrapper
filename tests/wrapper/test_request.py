from unittest.mock import patch
import responses
from time import sleep
from requests import Timeout
from py_bdd_context import BDDContextTestCase

from bb_wrapper.wrapper.request import RequestsWrapper

from tests.utils import MockedRequestsTestCase, IsolatedEnvTestCase


class RequestsWrapperTestCase(
    BDDContextTestCase, MockedRequestsTestCase, IsolatedEnvTestCase
):
    maxDiff = None

    @MockedRequestsTestCase.no_auth
    def test_contruct_url_1(self):
        with self.given(
            """
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
            """
        ):
            base_url = "http://foo.bar"
            wrapper = RequestsWrapper(base_url=base_url)

        with self.when(
            """
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2')
            """
        ):
            result = wrapper._construct_url("acao1", "id1", "subacao2", "id2")

        with self.then(
            """
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2"
            """
        ):
            expected = "http://foo.bar/acao1/id1/subacao2/id2"

            self.assertEqual(result, expected)

    @MockedRequestsTestCase.no_auth
    def test_contruct_url_2(self):
        with self.given(
            """
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
            """
        ):
            base_url = "http://foo.bar"
            wrapper = RequestsWrapper(base_url=base_url)
        with self.when(
            """
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search='query1=1&query2=2')  # noqa
            """
        ):
            result = wrapper._construct_url(
                "acao1", "id1", "subacao2", "id2", search="query1=1&query2=2"
            )

        with self.then(
            """
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"  # noqa
            """
        ):
            expected = "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"

            self.assertEqual(result, expected)

    @MockedRequestsTestCase.no_auth
    def test_contruct_url_3(self):
        with self.given(
            """
            - uma base_url 'http://foo.bar'
            - um wrapper RequestsWrapper(self.base_url)
            """
        ):
            base_url = "http://foo.bar"
            wrapper = RequestsWrapper(base_url=base_url)

        with self.when(
            """
            - self.wrapper._construct_url('acao1', 'id1', 'subacao2', 'id2', search=dict(query1=1, query2=2))  # noqa
            """
        ):
            result = wrapper._construct_url(
                "acao1", "id1", "subacao2", "id2", search=dict(query1=1, query2=2)
            )

        with self.then(
            """
            - o resultado deve ser "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"  # noqa
            """
        ):
            expected = "http://foo.bar/acao1/id1/subacao2/id2?query1=1&query2=2"

            self.assertEqual(result, expected)

    @MockedRequestsTestCase.no_auth
    def test_request_timeout_1(self):
        with self.given(
            """
            - uma requisição qualquer
            """
        ):
            self.mock_responses.stop()
            self.headers_patcher = patch(
                "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
            )
            self.mocked_headers = self.headers_patcher.start()

            self.mocked_headers.return_value = {}
            wrapper = RequestsWrapper(base_url="", timeout=2)

        with self.when(
            """
            - o servidor demorar X segundos para responder
            """
        ):
            url = "https://httpstat.us/200?sleep=5000"
            with self.assertRaises(Timeout):
                wrapper._get(url)

        with self.then(
            """
            - um erro de timeout deve ser lançado
            """
        ):
            self.headers_patcher.stop()

    @MockedRequestsTestCase.no_auth
    def test_request_timeout_2(self):
        with self.given(
            """
            - uma requisição qualquer
            """
        ):
            url = "http://foo.com"

            self.headers_patcher = patch(
                "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
            )
            self.mocked_headers = self.headers_patcher.start()

            def raise_timeout(request):
                sleep(3)
                return self.raise_timeout()

            self.mocked_headers.return_value = {}
            self.mock_responses.add_callback(
                responses.GET,
                url,
                callback=raise_timeout,
            )
            wrapper = RequestsWrapper(base_url="", timeout=1)

        with self.when(
            """
            - o servidor demorar X segundos para responder
            """
        ):
            with self.assertRaises(Timeout):
                wrapper._get(url)

        with self.then(
            """
            - um erro de timeout deve ser lançado
            """
        ):
            self.headers_patcher.stop()

    @MockedRequestsTestCase.no_auth
    def test_retry_request(self):
        with self.given(
            """
            - uma requisição qualquer
            """
        ):
            self.headers_patcher = patch(
                "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
            )
            url = "http://foo"

            self.mocked_headers = self.headers_patcher.start()
            self.mock_responses.add(
                responses.GET,
                url,
                "OK",
                headers=self._build_authorization_header(1),
                status=200,
            )
            max_retries = 3

            def raise_connection_reset_error(headers=None):
                call_count = self.mocked_headers.call_count
                if call_count <= max_retries:
                    raise ConnectionResetError
                else:
                    return dict()

            self.mocked_headers.side_effect = raise_connection_reset_error

            wrapper = RequestsWrapper(base_url="")

        with self.when(
            """
            - a requisição é realizada
            - o ConnectionResetError é lançado
            """
        ):
            wrapper._get(url)

        with self.then(
            """
            - a requisição deve ocorrer com sucesso
            - devem ter sido realizadas 4 requisições
              (3 tentativas falhas e 1 bem sucedida)
            """
        ):
            self.assertEqual(self.mocked_headers.call_count, 4)

            self.headers_patcher.stop()

    @MockedRequestsTestCase.no_auth
    def test_fail_retry_request(self):
        with self.given(
            """
            - uma requisição qualquer
            """
        ):
            self.headers_patcher = patch(
                "bb_wrapper.wrapper.request.RequestsWrapper._get_request_info"
            )
            self.mocked_headers = self.headers_patcher.start()

            def raise_connection_reset_error(headers=None):
                raise ConnectionResetError

            self.mocked_headers.side_effect = raise_connection_reset_error

            wrapper = RequestsWrapper(base_url="")
            url = "https://httpstat.us/200?sleep=1"

        with self.when(
            """
            - a requisição é realizada
            - o ConnectionResetError é lançado
            """
        ):
            with self.assertRaises(ConnectionResetError):
                wrapper._get(url)

        with self.then(
            """
            - o erro de conexão deve ser lançado
              (4 tentativas falhas)
            """
        ):
            self.assertEqual(self.mocked_headers.call_count, 4)

            self.headers_patcher.stop()
