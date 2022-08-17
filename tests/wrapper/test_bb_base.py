from freezegun import freeze_time
from datetime import timedelta

from tests.utils import IsolatedEnvTestCase, MockedRequestsTestCase
from bb_wrapper.wrapper.bb import BaseBBWrapper
from bb_wrapper.wrapper.pix_cob import PIXCobBBWrapper

from requests import HTTPError


class BaseBBWrapperTestCase(IsolatedEnvTestCase, MockedRequestsTestCase):
    def test_authentication(self):
        """
        Teste para verificar a validação da autenticação.

        Dado:
            -
        Quando:
            - for chamado BaseBBWrapper()._BaseBBWrapper__authenticate()
        Então:
            - o resultado de uma autenticação bem sucedida deve ser True
            - apenas uma requisição deve ser realizada
        """
        result = BaseBBWrapper()._BaseBBWrapper__authenticate()

        self.assertTrue(result)
        self.mocked_getresponse.assert_called_once()

    def test_reauthentication(self):
        """
        Teste para verificar a validação da reautenticação.

        Dado:
            -
        Quando:
            - o token de autenticação expirar
        Então:
            - uma nova autenticação deve ser realizada
            - o wrapper deve ter um novo token de autenticação
        """
        total_requests = 2

        bb_wrapper = BaseBBWrapper()

        result = bb_wrapper._BaseBBWrapper__authenticate()

        self.assertTrue(result)
        self.assertEqual(bb_wrapper._access_token, "token_1")

        expire_time = timedelta(seconds=bb_wrapper.TOKEN_EXPIRE_TIME)
        time_travel = bb_wrapper._token_time + expire_time

        with freeze_time(time_travel):
            result = bb_wrapper._BaseBBWrapper__authenticate()

            self.assertTrue(result)
            self.assertEqual(bb_wrapper._access_token, "token_2")

        self.assertEqual(total_requests, self.mocked_getresponse.call_count)

    def test_authentication_for_multiple_instances(self):
        """
        Teste para verificar se o token de autenticação é utilizado
        por instâncias diferentes.

        Dado:
            -
        Quando:
            - 2 instâncias BaseBBWrapper realizarem requisições
        Então:
            - o dado de autenticação deve ser compartilhado
            - o tempo de expiração deve ser igual
        """
        bb_wrapper1 = BaseBBWrapper()
        result1 = bb_wrapper1._BaseBBWrapper__authenticate()

        self.assertEqual(result1, True)
        self.assertEqual(bb_wrapper1._access_token, "token_1")

        bb_wrapper2 = BaseBBWrapper()
        result2 = bb_wrapper2._BaseBBWrapper__authenticate()

        self.assertEqual(result2, False)
        self.assertEqual(bb_wrapper2._access_token, "token_1")

        self.assertEqual(bb_wrapper1._token_time, bb_wrapper2._token_time)

        self.mocked_getresponse.assert_called_once()

    def test_authentication_multiple_wrappers(self):
        """
        Dado:
            - um wrapper BaseBBWrapper
            - outro wrapper PIXCobBBWrapper
        Quando:
            - BaseBBWrapper se autenticar
            - PIXCobBBWrapper se autenticar
        Então:
            - cada wrapper deve ter um token diferente
        """
        total_requests = 2

        wrapper1 = BaseBBWrapper()
        wrapper2 = PIXCobBBWrapper()

        self.assertNotEqual(wrapper1._data, wrapper2._data)

        wrapper1._BaseBBWrapper__authenticate()
        wrapper2._BaseBBWrapper__authenticate()

        self.assertNotEqual(wrapper1._access_token, wrapper2._access_token)

        self.assertEqual(wrapper1._access_token, "token_1")
        self.assertEqual(wrapper2._access_token, "token_2")

        self.assertEqual(total_requests, self.mocked_getresponse.call_count)

    def test_authentication_fail_and_reauthentication(self):
        """
        Teste para verificar uma nova tentativa de autenticação
        após uma falha na autenticação.

        Dado:
            -
        Quando:
            - for chamado BaseBBWrapper()._BaseBBWrapper__authenticate()
        Então:
            - 2 tentativas de autenticação devem ser realizadas,
              uma falha e uma bem sucedida
            - o resultado da autenticação deve ser True
        """
        bb_wrapper = BaseBBWrapper()

        fail_attempts = 1
        total_attempts = fail_attempts + 1

        self.set_auth(fail_attempts)

        result = bb_wrapper._BaseBBWrapper__authenticate()

        self.assertTrue(result)
        self.assertEqual(bb_wrapper._access_token, "token_2")
        self.assertEqual(total_attempts, self.mocked_getresponse.call_count)

    def test_authentication_fail_and_reauthentication_fail_after_5_attempts(self):
        """
        Teste para verificar falhas em todas as tentativas de autenticação.

        Dado:
            -
        Quando:
            - for chamado BaseBBWrapper()._BaseBBWrapper__authenticate()
        Então:
            - o máximo de tentativas de autenticação devem ser realizadas
            - a autenticação deve terminar em um lançamento de exceção HTTPError
        """
        bb_wrapper = BaseBBWrapper()

        total_attempts = bb_wrapper.AUTH_MAX_RETRY_ATTEMPTS + 1

        self.set_auth(-1)

        with self.assertRaises(HTTPError) as ctx:
            bb_wrapper._BaseBBWrapper__authenticate()
        response = ctx.exception.response

        self.assertEqual(response.status_code, 401, msg=response.data)
        self.assertEqual(total_attempts, self.mocked_getresponse.call_count)
