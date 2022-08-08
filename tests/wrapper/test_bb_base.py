from freezegun import freeze_time
from datetime import timedelta

from tests.utils import IsolatedEnvTestCase, MockedBBTestCase
from bb_wrapper.wrapper.bb import BaseBBWrapper


class BaseBBWrapperTestCase(IsolatedEnvTestCase, MockedBBTestCase):
    def test_authenticate(self):
        """
        Teste para verificar a validação da autenticação.

        Dado:
            -
        Quando:
            - for chamado BaseBBWrapper()._BaseBBWrapper__authenticate()
        Então:
            - o resultado da autenticação deve ser True
        """
        result = BaseBBWrapper()._BaseBBWrapper__authenticate()
        self.assertTrue(result)

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
        bb_wrapper = BaseBBWrapper()

        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            200, data={"access_token": "access_token1", "token_type": "token_type"}
        )
        result = bb_wrapper._BaseBBWrapper__authenticate()

        self.assertTrue(result)
        self.assertEqual(bb_wrapper._BaseBBWrapper__data.access_token, "access_token1")

        expire_time = timedelta(seconds=bb_wrapper.TOKEN_EXPIRE_TIME)
        time_travel = bb_wrapper._BaseBBWrapper__data.token_time + expire_time

        with freeze_time(time_travel):
            self.mocked_auth_requests.post.return_value = self.build_response_mock(
                200, data={"access_token": "access_token2", "token_type": "token_type"}
            )
            result = bb_wrapper._BaseBBWrapper__authenticate()

            self.assertTrue(result)
            self.assertEqual(
                bb_wrapper._BaseBBWrapper__data.access_token, "access_token2"
            )

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
        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            200, data={"access_token": "access_token", "token_type": "token_type"}
        )

        bb_wrapper1 = BaseBBWrapper()
        bb_wrapper2 = BaseBBWrapper()

        result1 = bb_wrapper1._BaseBBWrapper__authenticate()
        result2 = bb_wrapper2._BaseBBWrapper__authenticate()

        self.assertTrue(result1)
        self.assertTrue(result2)

        self.assertEqual(bb_wrapper1._BaseBBWrapper__data.access_token, "access_token")
        self.assertEqual(bb_wrapper2._BaseBBWrapper__data.access_token, "access_token")

        self.assertEqual(
            bb_wrapper1._BaseBBWrapper__data.token_time,
            bb_wrapper2._BaseBBWrapper__data.token_time,
        )
