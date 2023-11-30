import responses

from unittest.mock import MagicMock

from pydantic import ValidationError

from bb_wrapper.wrapper.pagamento_lote import (
    PagamentoLoteBBWrapper,
    LoteData,
)
from tests.utils import (
    MockedRequestsTestCase,
    IsolatedEnvTestCase,
)


class PagamentoLoteBBWrapperTestCase(IsolatedEnvTestCase, MockedRequestsTestCase):
    maxDiff = None

    @MockedRequestsTestCase.no_auth
    def test_construct_url_1(self):
        """
        Dado:
            -
        Quando:
            - for chamado PagamentoLoteBBWrapper()._construct_url(end_bar=True)
        Então:
            - o resultado deve ter pelo menos o texto
                'https://api.sandbox.bb.com.br/pagamentos-lote/v1/?gw-dev-app-key='
        """
        result = PagamentoLoteBBWrapper()._construct_url(end_bar=True)

        expected = (
            f"https://api.sandbox.bb.com.br/pagamentos-lote/v1/"
            f"?gw-dev-app-key={PagamentoLoteBBWrapper()._BaseBBWrapper__gw_app_key}"
        )

        self.assertEqual(expected, result)

    @MockedRequestsTestCase.no_auth
    def test_construct_url_prod(self):
        """
        Dado:
            -
        Quando:
            - for chamado PagamentoLoteBBWrapper(is_sandbox=False)._construct_url(end_bar=True)  # noqa
        Então:
            - o resultado deve ter pelo menos o texto
                'https://api-ip.bb.com.br/pagamentos-lote/v1/?gw-dev-app-key='
        """

        result = PagamentoLoteBBWrapper(is_sandbox=False)._construct_url(end_bar=True)

        expected = (
            f"https://api-ip.bb.com.br/pagamentos-lote/v1/"
            f"?gw-dev-app-key={PagamentoLoteBBWrapper()._BaseBBWrapper__gw_app_key}"
        )

        self.assertEqual(expected, result)

    @MockedRequestsTestCase.no_auth
    def test_valida_lote_0(self):
        """
        Teste para verificar a validação do model Pydantic
        """
        kwargs = {}

        with self.assertRaises(ValidationError):
            PagamentoLoteBBWrapper()._valida_lote_data(LoteData, **kwargs)

    @MockedRequestsTestCase.no_auth
    def test_valida_lote_1(self):
        """
        Teste para verificar a validação do model Pydantic
        """
        kwargs = {"foo": "bar"}

        mocked_model = MagicMock()

        PagamentoLoteBBWrapper()._valida_lote_data(mocked_model, **kwargs)

        mocked_model.assert_called_with(**kwargs)

    @MockedRequestsTestCase.no_auth
    def test_valida_lote_2_remocao_convenio(self):
        """
        Teste para garantir a remoção do argumento convenio quando None
        """
        kwargs = {"foo": "bar", "convenio": None, "barz": None}

        mocked_model = MagicMock()

        PagamentoLoteBBWrapper()._valida_lote_data(mocked_model, **kwargs)

        expected_kwargs_call = {"foo": "bar", "barz": None}

        mocked_model.assert_called_with(**expected_kwargs_call)

    def test_cancelar_pagamento_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("cancelar-pagamentos")
        expected_json = {
            "agenciaDebito": "2",
            "contaCorrenteDebito": "3",
            "digitoVerificadorContaCorrente": "x",
            "listaPagamentos": [{"codigoPagamento": "1"}],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().cancelar_pagamentos("1", "2", "3", "x")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_cancelar_pagamento_2(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("cancelar-pagamentos")
        expected_json = {
            "agenciaDebito": "2",
            "contaCorrenteDebito": "3",
            "digitoVerificadorContaCorrente": "x",
            "listaPagamentos": [{"codigoPagamento": "1"}],
            "numeroContratoPagamento": "4",
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().cancelar_pagamentos("1", "2", "3", "x", "4")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_liberar_pagamentos_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("liberar-pagamentos")
        expected_json = {"numeroRequisicao": "1", "indicadorFloat": "N"}
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().liberar_pagamentos("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_resgatar_lote_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("1")
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().resgatar_lote("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_resgatar_lote_solicitacao_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("1", "solicitacao")
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().resgatar_lote_solicitacao("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_listar_pagamentos_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url(
            "pagamentos", search={"dataInicio": "foo", "dataFim": "bar", "indice": 0}
        )
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().listar_pagamentos("foo", "bar")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_cadastrar_transferencia_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("lotes-transferencias")
        expected_json = {
            "numeroRequisicao": "1",
            "agenciaDebito": "2",
            "contaCorrenteDebito": "3",
            "digitoVerificadorContaCorrente": "4",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "numeroCOMPE": "5",
                    "agenciaCredito": "6",
                    "contaCorrenteCredito": "7",
                    "digitoVerificadorContaCorrente": "8",
                    "dataTransferencia": "10",
                    "valorTransferencia": "11",
                    "descricaoTransferencia": "12",
                    "cpfBeneficiario": "99391916180",
                    "codigoFinalidadeTED": 1,
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().cadastrar_transferencia(
            "1",
            "2",
            "3",
            "4",
            "5",
            "99391916180",
            "6",
            "7",
            "8",
            agencia_destino="10",
            conta_destino="11",
            dv_conta_destino="12",
            finalidade_ted=1,
            tipo_pagamento=128,
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_cadastrar_transferencia_2_conta_pagamento(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("lotes-transferencias")
        expected_json = {
            "numeroRequisicao": "1",
            "agenciaDebito": "2",
            "contaCorrenteDebito": "3",
            "digitoVerificadorContaCorrente": "4",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "numeroCOMPE": "5",
                    "dataTransferencia": "6",
                    "valorTransferencia": "7",
                    "descricaoTransferencia": "8",
                    "contaPagamentoCredito": "9",
                    "cpfBeneficiario": "99391916180",
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().cadastrar_transferencia(
            "1",
            "2",
            "3",
            "4",
            "5",
            "99391916180",
            "6",
            "7",
            "8",
            conta_pagamento_destino="9",
            tipo_pagamento=128,
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_consultar_transferencia_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("transferencias", "1")
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().consultar_transferencia("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_cadastrar_pagamento_boleto_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("lotes-boletos")
        expected_json = {
            "numeroRequisicao": "1",
            "numeroAgenciaDebito": "2",
            "numeroContaCorrenteDebito": "3",
            "digitoVerificadorContaCorrenteDebito": "4",
            "lancamentos": [
                {
                    "numeroCodigoBarras": "34191873400000614011092306628112938349558000",  # noqa: E501
                    "codigoTipoBeneficiario": 1,
                    "documentoBeneficiario": "99391916180",
                    "dataPagamento": "7",
                    "valorPagamento": "8",
                    "valorNominal": "9",
                    "descricaoPagamento": "10",
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().cadastrar_pagamento_boleto(
            "1",
            "2",
            "3",
            "4",
            "34191873400000614011092306628112938349558000",
            "99391916180",
            "7",
            "8",
            "9",
            "10",
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_consultar_pagamento_boleto_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("boletos", "1")
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().consultar_pagamento_boleto("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_cadastrar_pagamento_tributo_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-guias-codigo-barras"
        )
        expected_json = {
            "numeroRequisicao": "1",
            "numeroAgenciaDebito": "2",
            "numeroContaCorrenteDebito": "3",
            "digitoVerificadorContaCorrenteDebito": "4",
            "lancamentos": [
                {
                    "codigoBarras": "85800000000600003282126307082112794112788193",
                    "dataPagamento": "7",
                    "valorPagamento": "8",
                    "descricaoPagamento": "9",
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().cadastrar_pagamento_tributo(
            "1",
            "2",
            "3",
            "4",
            "85800000000600003282126307082112794112788193",
            "7",
            "8",
            "9",
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_consultar_pagamento_tributo_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        request_url = PagamentoLoteBBWrapper()._construct_url(
            "guias-codigo-barras", "1"
        )
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().consultar_pagamento_tributo("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)
