from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests


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

        self.requests_patcher = patch("bb_wrapper.wrapper.request.requests")
        self.auth_requests_patcher = patch("bb_wrapper.wrapper.bb.requests")

        self.mocked_requests = self.requests_patcher.start()
        self.mocked_auth_requests = self.auth_requests_patcher.start()

        self.addCleanup(self.requests_patcher.stop)
        self.addCleanup(self.auth_requests_patcher.stop)

        self.mocked_get = self.mocked_requests.get
        self.mocked_post = self.mocked_requests.post
        self.mocked_put = self.mocked_requests.put
        self.mocked_patch = self.mocked_requests.patch
        self.mocked_delete = self.mocked_requests.delete

    @staticmethod
    def build_response_mock(status_code=200, data=None, content=None):
        """
        Cria uma response mockada
        """
        response = MagicMock(
            status_code=status_code, data=data if data else {}, content=content
        )

        response.json.return_value = response.data

        def raise_for_status():
            # noinspection PyCallByClass
            requests.Response.raise_for_status(response)

        response.raise_for_status = raise_for_status
        return response


class MockedBBTestCase(MockedRequestsTestCase):
    def setUp(self):
        super().setUp()

        self.auth_requests_patcher = patch("bb_wrapper.wrapper.bb.requests")

        self.mocked_auth_requests = self.auth_requests_patcher.start()

        self.addCleanup(self.auth_requests_patcher.stop)

        self.set_auth()

    def set_auth(self):
        self.mocked_auth_requests.post.return_value = self.build_response_mock(
            200, data={"access_token": "access_token", "token_type": "token_type"}
        )

    def _get_headers(self):
        return {
            "Authorization": "token_type access_token",
            "Content-type": "application/json",
        }

    def get_request_complements(self, verify=False, cert=None):
        return dict(headers=self._get_headers(), verify=verify, cert=cert)
