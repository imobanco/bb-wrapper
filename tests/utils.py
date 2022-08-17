from unittest import TestCase
from unittest.mock import patch, MagicMock
import io
import json


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

        self.get_conn_patcher = patch(
            "urllib3.connectionpool.HTTPConnectionPool._get_conn"
        )
        self.mocked_get_conn = self.get_conn_patcher.start()
        self.mocked_conn = self.mocked_get_conn.return_value
        self.mocked_getresponse = self.mocked_conn.getresponse
        self.addCleanup(self.get_conn_patcher.stop)

        self.set_auth()

    def tearDown(self):
        super().tearDown()
        self.clear_data()

    def clear_data(self):
        from bb_wrapper.wrapper.bb import BaseBBWrapper
        from bb_wrapper.wrapper.pagamento_lote import PagamentoLoteBBWrapper
        from bb_wrapper.wrapper.pix_cob import PIXCobBBWrapper
        from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

        BaseBBWrapper().reset_data()
        PagamentoLoteBBWrapper().reset_data()
        PIXCobBBWrapper().reset_data()
        CobrancasBBWrapper().reset_data()

    def build_auth_success_response(self, call_count):
        data = {
            "access_token": f"token_{call_count}",
            "token_type": "token_type",
            "expires_in": 600,
        }

        resp = self.build_mocked_response(201, data)

        return resp

    def build_auth_fail_response_401(self, call_count):
        data = {
            "error": f"invalid_client{call_count}",
            "error_description": "Identificador ou credencial inválidos",
        }

        resp = self.build_mocked_response(401, data)

        return resp

    @staticmethod
    def build_mocked_response(status_code=200, data=None):
        if data is None:
            data = {}
        data = json.dumps(data).encode()
        raw_io = io.BytesIO(data)
        resp = MagicMock(
            code=status_code,
            status=status_code,
            reason="foo??",
            strict=0,
            fp=io.BufferedReader(raw_io),  # noqa
            closed=False,
        )

        def read(*args, **kwargs):
            return raw_io.read()

        def close(*args, **kwargs):
            resp.closed = True

        def isclosed(*args, **kwargs):
            return resp.closed

        resp.read.side_effect = read
        resp.close.side_effect = close
        resp.isclosed.side_effect = isclosed

        return resp

    def set_auth(self, number_of_retries_to_success: int = 0):
        """
        Se `number_of_retries_to_success` for 0, não haverá falhas!
        Se `number_of_retries_to_success` for negativo, sempre haverá falhas!
        Se `number_of_retries_to_success` for positivo, vai definir o número de falhas!
        """
        self.mocked_getresponse.reset_mock()

        def get_response(*args, **kwargs):
            call_count = self.mocked_getresponse.call_count

            never_fail = number_of_retries_to_success == 0
            always_fail = number_of_retries_to_success < 0
            retry_again = number_of_retries_to_success >= call_count and not never_fail

            if always_fail or retry_again:
                return self.build_auth_fail_response_401(call_count)
            return self.build_auth_success_response(call_count)

        self.mocked_getresponse.side_effect = get_response

    def _get_headers(self):
        return {
            "Authorization": f"token_type token_"
            f"{self.mocked_getresponse.call_count}",
            "Content-type": "application/json",
        }

    def get_request_complements(self, verify=False, cert=None):
        return dict(headers=self._get_headers(), verify=verify, cert=cert)
