from freezegun import freeze_time
from datetime import timedelta
from py_bdd_context import BDDContextTestCase


from tests.utils import IsolatedEnvTestCase, MockedRequestsTestCase
from bb_wrapper.wrapper.bb import BaseBBWrapper
from bb_wrapper.wrapper.pix_cob import PIXCobBBWrapper

from requests import HTTPError


class BaseBBWrapperTestCase(
    BDDContextTestCase, IsolatedEnvTestCase, MockedRequestsTestCase
):
    def test_authentication(self):
        """
        - Teste para verificar a validação da autenticação.
        """
        with self.given(
            """
                - uma instância do BaseBBWrapper
            """
        ):
            bb_wrapper = BaseBBWrapper()

        with self.when(
            """
                - o service de autenticação do BaseBBWrapper for chamado
            """
        ):
            result = bb_wrapper._BaseBBWrapper__authenticate()

        with self.then(
            """
                - o resultado da autenticação deve ser bem sucedida
                - apenas uma requisição deve ser realizada
            """
        ):

            self.assertTrue(result)
            self.assertEqual(1, self.total_requests())

    def test_reauthentication(self):
        """
        - Teste para verificar a validação da reautenticação.
        """

        with self.given(
            """
                - uma autenticação já realizada peloBase BBWrapper
            """
        ):
            bb_wrapper = BaseBBWrapper()
            result = bb_wrapper._BaseBBWrapper__authenticate()

            self.assertTrue(result)
            self.assertEqual("token_1", bb_wrapper._access_token)

        with self.when(
            """
                -  o token de autenticação expirar
            """
        ):
            expire_time = timedelta(seconds=bb_wrapper.TOKEN_EXPIRE_TIME)
            time_travel = bb_wrapper._token_time + expire_time

        with self.then(
            """
                - uma nova autenticação deve ser realizada
                - o wrapper deve ter um novo token de autenticação
            """
        ):
            with freeze_time(time_travel):
                result = bb_wrapper._BaseBBWrapper__authenticate()

                self.assertTrue(result)
                self.assertEqual("token_2", bb_wrapper._access_token)

            self.assertEqual(2, self.total_requests())

    def test_authentication_for_multiple_instances(self):
        """
        - Teste para verificar se o token de autenticação é utilizado por instâncias diferentes. # noqa: E501
        """

        with self.given(
            """
                - duas instâncias BaseBBWrapper
            """
        ):
            bb_wrapper1 = BaseBBWrapper()
            bb_wrapper2 = BaseBBWrapper()

        with self.when(
            """
                - duas instâncias BaseBBWrapper realizarem requisições
            """
        ):
            result1 = bb_wrapper1._BaseBBWrapper__authenticate()

            self.assertTrue(result1)
            self.assertEqual("token_1", bb_wrapper1._access_token)

            result2 = bb_wrapper2._BaseBBWrapper__authenticate()

            self.assertFalse(result2)
            self.assertEqual("token_1", bb_wrapper2._access_token)

        with self.then(
            """
                - o dado de autenticação deve ser compartilhado
                - o tempo de expiração deve ser igual
            """
        ):
            self.assertEqual(bb_wrapper1._token_time, bb_wrapper2._token_time)
            self.assertEqual(1, self.total_requests())

    def test_authentication_multiple_wrappers(self):
        with self.given(
            """
                - dois wrapper BaseBBWrapper e PIXCobBBWrapper
            """
        ):
            wrapper1 = BaseBBWrapper()
            wrapper2 = PIXCobBBWrapper()
            self.assertNotEqual(wrapper1._data, wrapper2._data)

        with self.when(
            """
                - BaseBBWrapper e PIXCobBBWrapper fizem autenticação
            """
        ):
            wrapper1._BaseBBWrapper__authenticate()
            wrapper2._BaseBBWrapper__authenticate()

        with self.then(
            """
                - cada wrapper deve ter um token diferente
            """
        ):
            self.assertNotEqual(wrapper1._access_token, wrapper2._access_token)

            self.assertEqual("token_1", wrapper1._access_token)
            self.assertEqual("token_2", wrapper2._access_token)

            self.assertEqual(2, self.total_requests())

    def test_authentication_fail_and_reauthentication(self):
        """
        - Teste para verificar uma nova tentativa de autenticação após uma falha na autenticação. # noqa: E501
        """

        with self.given(
            """
                - uma instância do BaseBBWrapper
            """
        ):
            bb_wrapper = BaseBBWrapper()
            fail_attempts = 1
            total_requests = fail_attempts + 1

            self.set_auth(fail_attempts)

        with self.when(
            """
                - o service de autenticação do BaseBBWrapper for chamado
            """
        ):
            result = bb_wrapper._BaseBBWrapper__authenticate()

        with self.then(
            """
                - 2 tentativas de autenticação devem ser realizadas, uma falha e uma bem sucedida # noqa: E501
                - o resultado da autenticação deve ser True
            """
        ):
            self.assertTrue(result)
            self.assertEqual("token_2", bb_wrapper._access_token)
            self.assertEqual(total_requests, self.total_requests())

    def test_authentication_fail_and_reauthentication_fail_after_5_attempts(self):
        """
        - Teste para verificar falhas em todas as tentativas de autenticação.
        """

        with self.given(
            """
                - uma instância do BaseBBWrapper
            """
        ):
            self.set_auth(-1)
            bb_wrapper = BaseBBWrapper()

        with self.when(
            """
                - o service de autenticação do BaseBBWrapper for chamado
            """
        ):
            with self.assertRaises(HTTPError) as ctx:
                bb_wrapper._BaseBBWrapper__authenticate()
            response = ctx.exception.response

        with self.then(
            """
                - o máximo de tentativas de autenticação devem ser realizadas
                - a autenticação deve terminar em um lançamento de exceção HTTPError
            """
        ):
            self.assertEqual(401, response.status_code, msg=response.data)

            total_requests = bb_wrapper.AUTH_MAX_RETRY_ATTEMPTS + 1
            self.assertEqual(total_requests, self.total_requests())
