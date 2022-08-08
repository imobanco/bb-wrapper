from unittest.mock import patch

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
        self.assertEqual(bb_wrapper.data.access_token, "access_token1")

        with patch("bb_wrapper.wrapper.bb.time.time") as mocked_time:
            mocked_time.return_value = (
                bb_wrapper.data.token_time + bb_wrapper.TOKEN_TIME
            )

        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            200, data={"access_token": "access_token2", "token_type": "token_type"}
        )
        result = bb_wrapper._BaseBBWrapper__authenticate(force_auth=True)

        self.assertTrue(result)
        self.assertEqual(bb_wrapper.data.access_token, "access_token2")
