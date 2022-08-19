from unittest import TestCase
from unittest.mock import patch
import json
import responses
from responses import registries


class BarcodeAndCodeLineTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()
        self.cobrancas_barcodes_to_code_lines = {
            "34191873400000614011092306628112938349558000": "34191092300662811293783495580009187340000061401",  # amil  # noqa: E501
            "23791872200000020043381260065904993200006330": "23793381286006590499132000063308187220000002004",  # nubank  # noqa: E501
            "00196846200000100000000003128557123123000917": "00190000090312855712531230009172684620000010000",  # bb  # noqa: E501
            "00191851500000003100000003128557999999999917": "00190000090312855799299999999172185150000000310",  # bb  # noqa: E501
            "10497848400003240007946015202101347639700002": "10497946031520210134976397000027784840000324000",  # caixa  # noqa: E501
            "00192849800000003000000003128557999999999417": "00190000090312855799299999994173284980000000300",  # bb  # noqa: E501
            "75691872100000215251419401015749004599691001": "75691419430101574900345996910019187210000021525",  # bancoob  # noqa: E501
        }
        self.tributos_barcodes_to_code_lines = {
            "85800000000600003282126307082112794112788193": "858000000003600003282129630708211275941127881934",  # DAS  # noqa: E501
            "85820000008833201802108166242038105540980001": "858200000082833201802101816624203813055409800012",  # convênio  # noqa: E501
        }


class IsolatedEnvTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.sandbox_patcher = patch("bb_wrapper.wrapper.bb.IS_SANDBOX", True)
        self.token_patcher = patch("bb_wrapper.wrapper.bb.BASIC_TOKEN", "TOKEN")
        self.key_patcher = patch("bb_wrapper.wrapper.bb.GW_APP_KEY", "KEY")

        self.mocked_sandbox = self.sandbox_patcher.start()
        self.mocked_token = self.token_patcher.start()
        self.mocked_key = self.key_patcher.start()

        self.addCleanup(self.sandbox_patcher.stop)
        self.addCleanup(self.token_patcher.stop)
        self.addCleanup(self.key_patcher.stop)


class MockedRequestsTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.mock_responses = responses.RequestsMock(
            registry=registries.OrderedRegistry
        )
        self.mock_responses.start()
        self.addCleanup(self.mock_responses.stop)

        self.addCleanup(self.clear_data)

        self.set_auth()

    @staticmethod
    def clear_data():
        from bb_wrapper.wrapper.bb import BaseBBWrapper
        from bb_wrapper.wrapper.pagamento_lote import PagamentoLoteBBWrapper
        from bb_wrapper.wrapper.pix_cob import PIXCobBBWrapper
        from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

        BaseBBWrapper().reset_data()
        PagamentoLoteBBWrapper().reset_data()
        PIXCobBBWrapper().reset_data()
        CobrancasBBWrapper().reset_data()

    @staticmethod
    def __auth_success_201_data(call_count):
        return {
            "access_token": f"token_{call_count}",
            "token_type": "token_type",
            "expires_in": 600,
        }

    def build_auth_success_response(self, call_count):
        status = 201
        headers = self._get_headers()
        data = json.dumps(self.__auth_success_201_data(call_count))
        return status, headers, data

    @staticmethod
    def __auth_fail_401_data(call_count):
        return {
            "error": f"invalid_client{call_count}",
            "error_description": "Identificador ou credencial inválidos",
        }

    def build_auth_fail_response_401(self, call_count):
        status = 401
        headers = self._get_headers()
        data = json.dumps(self.__auth_fail_401_data(call_count))
        return status, headers, data

    def __get_auth_request(self):
        """
        Retorna a primeira requisição cadastrada, ou seja, a
        requisição de autenticação.
        """
        return self.mock_responses.registered()[0]

    def total_requests(self):
        return len(self.mock_responses.calls)

    @staticmethod
    def __get_auth_url():
        from bb_wrapper.wrapper.bb import BaseBBWrapper

        return BaseBBWrapper()._BaseBBWrapper__oauth_url()

    def set_auth(self, number_of_retries_to_success: int = 0):
        self.mock_responses.reset()

        def auth_request(request):
            call_count = self.__get_auth_request().call_count + 1

            never_fail = number_of_retries_to_success == 0
            always_fail = number_of_retries_to_success < 0
            retry_again = number_of_retries_to_success >= call_count and not never_fail

            if always_fail or retry_again:
                return self.build_auth_fail_response_401(call_count)
            return self.build_auth_success_response(call_count)

        self.mock_responses.add_callback(
            responses.POST,
            self.__get_auth_url(),
            callback=auth_request,
        )

    def no_auth(func):
        """
        Nem todos os testes de uma classe realizaram requisições,
        nesse caso, é necessário utilizar este decorator para
        desativar o mock de responses.
        """

        def inner(self):
            self.mock_responses.remove(responses.POST, self.__get_auth_url())
            func(self)

        return inner

    @staticmethod
    def _build_authorization_header(token):
        return {"Authorization": "token_type token_" f"{token}"}

    def _get_headers(self):
        return {
            "Authorization": "token_type token_"
            f"{self.__get_auth_request().call_count}",
            "Content-type": "application/json",
        }
