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

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_chave_aleatoria_transferencia_pix(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando chave aleatória # noqa
        """

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "email": None,
                    "cnpj": None,
                    "cpf": 11122233300,
                    "dddTelefone": None,
                    "telefone": None,
                    "data": 19042023,
                    "valor": 11.0,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 4,
                    "identificacaoAleatoria": "d14d32de-b3b9-4c31-9f89-8df2cec92c50",
                }
            ],
        }

        response = PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=11,
            chave="d14d32de-b3b9-4c31-9f89-8df2cec92c50",
            descricao="Pagamento",
            tipo_pagamento=128,
            documento=11122233300,
        )

        self.assertEqual(expected_json, response)

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_chave_aleatoria_transferencia_pix_sem_documento(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando chave aleatória sem a chave de documento # noqa
        """

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "email": None,
                    "cnpj": None,
                    "cpf": None,
                    "dddTelefone": None,
                    "telefone": None,
                    "data": 19042023,
                    "valor": 11.0,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 4,
                    "identificacaoAleatoria": "d14d32de-b3b9-4c31-9f89-8df2cec92c50",
                }
            ],
        }

        response = PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=11,
            chave="d14d32de-b3b9-4c31-9f89-8df2cec92c50",
            descricao="Pagamento",
            tipo_pagamento=128,
            documento=None,
        )

        self.assertEqual(expected_json, response)

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_telefone_transferencia_pix(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando telefone como chave # noqa
        """

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "email": None,
                    "cnpj": None,
                    "cpf": 11122233300,
                    "dddTelefone": 11,
                    "telefone": 985732102,
                    "data": 19042023,
                    "valor": 11.0,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 1,
                    "identificacaoAleatoria": None,
                }
            ],
        }

        response = PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=11,
            chave="11985732102",
            descricao="Pagamento",
            tipo_pagamento=128,
            documento=11122233300,
        )

        self.assertEqual(expected_json, response)

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_email_transferencia_pix(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando email como chave # noqa
        """

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "email": "teste@imo.com",
                    "cnpj": None,
                    "cpf": 11122233300,
                    "dddTelefone": None,
                    "telefone": None,
                    "data": 19042023,
                    "valor": 11.0,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 2,
                    "identificacaoAleatoria": None,
                }
            ],
        }

        response = PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=11,
            chave="teste@imo.com",
            descricao="Pagamento",
            tipo_pagamento=128,
            documento=11122233300,
        )

        self.assertEqual(expected_json, response)

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_com_email_invalido(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando email como chave # noqa
        """

        with self.assertRaises(ValueError) as ctx:
            PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
                n_requisicao=123,
                agencia=345,
                conta=678,
                dv_conta="X",
                data_transferencia=19042023,
                valor_transferencia=11,
                chave="teste@...",
                descricao="Pagamento",
                tipo_pagamento=128,
                documento=11122233300,
            )

        self.assertEqual(
            ctx.exception.args[0][0].exc.args[0], "Email inválido!"
        )  # noqa

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_cpf_transferencia_pix(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando CPF como chave # noqa
        """

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "email": None,
                    "cnpj": None,
                    "cpf": 28779295827,
                    "dddTelefone": None,
                    "telefone": None,
                    "data": 19042023,
                    "valor": 11.0,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 3,
                    "identificacaoAleatoria": None,
                }
            ],
        }

        response = PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=11,
            chave="28779295827",
            descricao="Pagamento",
            tipo_pagamento=128,
            documento=None,
        )

        self.assertEqual(expected_json, response)

    @MockedRequestsTestCase.no_auth
    def test_criar_dados_cnpj_transferencia_pix(self):
        """
        Teste para verificar e montar os dados da transferência PIX usando CNPJ como chave # noqa
        """

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "email": None,
                    "cnpj": 95127446000198,
                    "cpf": None,
                    "dddTelefone": None,
                    "telefone": None,
                    "data": 19042023,
                    "valor": 11.0,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 3,
                    "identificacaoAleatoria": None,
                }
            ],
        }

        response = PagamentoLoteBBWrapper()._criar_dados_transferencia_chave_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=11,
            chave="95127446000198",
            descricao="Pagamento",
            tipo_pagamento=128,
            documento=None,
        )

        self.assertEqual(expected_json, response)

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
            "1", "2", "3", "4", "5", "6", "7", "8", "99391916180", "10", "11", "12"
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

    def test_criar_transferencia_pix_chave_aleatoria(self):
        """
        Teste para verificar a URL da requisição e dados de transferência PIX chave aleatória  # noqa
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )
        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "valor": 11,
                    "descricaoPagamento": "Pagamento",
                    "formaIdentificacao": 4,
                    "identificacaoAleatoria": "d14d32de-b3b9-4c31-9f89-8df2cec92c50",
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_chave_pix(
            123,
            345,
            678,
            "X",
            19042023,
            11,
            "d14d32de-b3b9-4c31-9f89-8df2cec92c50",
            "Pagamento",
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_criar_transferencia_pix_email(self):
        """
        Teste para verificar a URL da requisição e dados de transferência PIX email
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )
        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "valor": 12,
                    "descricaoPagamento": "Teste transfer",
                    "formaIdentificacao": 2,
                    "email": "testqrcode01@bb.com.br",
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_chave_pix(
            123,
            345,
            678,
            "X",
            19042023,
            12,
            "testqrcode01@bb.com.br",
            "Teste transfer",
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_criar_transferencia_pix_telefone(self):
        """
        Teste para verificar a URL da requisição e dados de transferência PIX telefone
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )
        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "ddd": 11,
                    "telefone": 985732102,
                    "valor": 12,
                    "descricaoPagamento": "Teste telefone",
                    "formaIdentificacao": 1,
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_chave_pix(
            123,
            345,
            678,
            "X",
            19042023,
            11,
            11985732102,
            "Teste telefone",
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_criar_transferencia_pix_cpf(self):
        """
        Teste para verificar a URL da requisição e dados de transferência PIX via CPF
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )
        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "cpf": 28779295827,
                    "valor": 12,
                    "descricaoPagamento": "Teste CPF",
                    "formaIdentificacao": 3,
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_chave_pix(
            123, 345, 678, "X", 19042023, 12, 28779295827, "Teste CPF"
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_criar_transferencia_pix_cnpj(self):
        """
        Teste para verificar a URL da requisição e dados de transferência PIX via CNPJ
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )
        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "cnpj": 95127446000198,
                    "valor": 12,
                    "descricaoPagamento": "Teste CNPJ",
                    "formaIdentificacao": 3,
                }
            ],
        }
        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_chave_pix(
            123, 345, 678, "X", 19042023, 11, 95127446000198, "Teste CNPJ"
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_criar_transferencia_pix_dados_bancarios(self):
        """
        Teste para verificar a URL da requisição e
        dados de transferência PIX por dados bancarios
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "valor": 50,
                    "descricaoPagamento": "Uma transferência via dados bancários",
                    "formaIdentificacao": 5,
                    "tipoConta": 1,
                    "agencia": 1234,
                    "conta": 12345,
                    "digitoVerificadorConta": "X",
                    "numeroISPB": 360305,
                    "cpf": 28779295827,
                }
            ],
        }

        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_dados_bancarios_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=12,
            tipo_conta_favorecido=1,
            agencia_favorecido=1234,
            conta_favorecido=12345,
            digito_verificador_conta="X",
            conta_pagamento=None,
            numero_ispb=360305,
            descricao="Uma transferência via dados bancários",
            documento=28779295827,
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_criar_transferencia_pix_dados_bancarios_2(self):
        """
        Teste para verificar a URL da requisição e
        dados de transferência PIX por dados bancarios
        """

        request_url = PagamentoLoteBBWrapper()._construct_url(
            "lotes-transferencias-pix"
        )

        expected_json = {
            "numeroRequisicao": 123,
            "agenciaDebito": 345,
            "contaCorrenteDebito": 678,
            "digitoVerificadorContaCorrente": "X",
            "tipoPagamento": 128,
            "listaTransferencias": [
                {
                    "data": 19042023,
                    "valor": 50,
                    "descricaoPagamento": "Uma transferência via dados bancários",
                    "formaIdentificacao": 5,
                    "tipoConta": 1,
                    "contaPagamento": 12345678,
                    "numeroISPB": 360305,
                    "cpf": 28779295827,
                }
            ],
        }

        self.mock_responses.add(
            responses.POST,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().criar_transferencia_por_dados_bancarios_pix(
            n_requisicao=123,
            agencia=345,
            conta=678,
            dv_conta="X",
            data_transferencia=19042023,
            valor_transferencia=12,
            tipo_conta_favorecido=1,
            conta_pagamento=12345678,
            numero_ispb=360305,
            descricao="Uma transferência via dados bancários",
            documento=28779295827,
        )

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())
        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)

    def test_consultar_pix(self):
        """
        - Teste para consultar um pix de um determinado lote
        """
        request_url = PagamentoLoteBBWrapper()._construct_url("pix", "1")
        expected_json = {}
        self.mock_responses.add(
            responses.GET,
            request_url,
            headers=self._build_authorization_header(1),
            json=expected_json,
        )

        response = PagamentoLoteBBWrapper().consultar_pix("1")

        self.assertEqual(request_url, response.url)
        self.assertEqual(self._get_headers(), response.headers)
        self.assertEqual(expected_json, response.json())

        self.assertEqual(2, self.total_requests())
        self.mock_responses.assert_call_count(request_url, 1)
