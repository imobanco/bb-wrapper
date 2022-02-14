from unittest.mock import MagicMock

from pydantic import ValidationError

from bb_wrapper.wrapper.pagamento_lote import (
    PagamentoLoteBBWrapper,
    LoteData,
)
from tests.utils import (
    MockedBBTestCase,
    IsolatedEnvTestCase,
)


class PagamentoLoteBBWrapperTestCase(IsolatedEnvTestCase, MockedBBTestCase):
    maxDiff = None

    def test_construct_url_1(self):
        """
        Dado:
            -
        Quando:
            - for chamado PagamentoLoteBBWrapper()._construct_url(end_bar=True)
        Então:
            - o resultado deve ter pelo menos o texto
                'https://api.hm.bb.com.br/pagamentos-lote/v1/?gw-dev-app-key='
        """
        result = PagamentoLoteBBWrapper()._construct_url(end_bar=True)

        expected = (
            f"https://api.sandbox.bb.com.br/pagamentos-lote/v1/"
            f"?gw-dev-app-key={PagamentoLoteBBWrapper()._BaseBBWrapper__gw_app_key}"
        )

        self.assertEqual(expected, result)

    def test_valida_lote_0(self):
        """
        Teste para verificar a validação do model Pydantic
        """
        kwargs = {}

        with self.assertRaises(ValidationError):
            PagamentoLoteBBWrapper()._valida_lote_data(LoteData, **kwargs)

    def test_valida_lote_1(self):
        """
        Teste para verificar a validação do model Pydantic
        """
        kwargs = {"foo": "bar"}

        mocked_model = MagicMock()

        PagamentoLoteBBWrapper()._valida_lote_data(mocked_model, **kwargs)

        mocked_model.assert_called_with(**kwargs)

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
        PagamentoLoteBBWrapper().cancelar_pagamentos("1", "2", "3", "x")

        url = PagamentoLoteBBWrapper()._construct_url("cancelar-pagamentos")

        expected_json = {
            "agenciaDebito": "2",
            "contaCorrenteDebito": "3",
            "digitoVerificadorContaCorrente": "x",
            "listaPagamentos": [{"codigoPagamento": "1"}],
        }

        self.mocked_post.assert_called_with(
            url, **self.get_request_complements(), json=expected_json
        )

    def test_cancelar_pagamento_2(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().cancelar_pagamentos("1", "2", "3", "x", "4")

        url = PagamentoLoteBBWrapper()._construct_url("cancelar-pagamentos")

        expected_json = {
            "agenciaDebito": "2",
            "contaCorrenteDebito": "3",
            "digitoVerificadorContaCorrente": "x",
            "listaPagamentos": [{"codigoPagamento": "1"}],
            "numeroContratoPagamento": "4",
        }

        self.mocked_post.assert_called_with(
            url, **self.get_request_complements(), json=expected_json
        )

    def test_liberar_pagamentos_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().liberar_pagamentos("1")

        url = PagamentoLoteBBWrapper()._construct_url("liberar-pagamentos")

        expected_json = {"numeroRequisicao": "1", "indicadorFloat": "N"}

        self.mocked_post.assert_called_with(
            url, **self.get_request_complements(), json=expected_json
        )

    def test_resgatar_lote_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().resgatar_lote("1")

        url = PagamentoLoteBBWrapper()._construct_url("1")

        self.mocked_get.assert_called_with(url, **self.get_request_complements())

    def test_resgatar_lote_solicitacao_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().resgatar_lote_solicitacao("1")

        url = PagamentoLoteBBWrapper()._construct_url("1", "solicitacao")

        self.mocked_get.assert_called_with(url, **self.get_request_complements())

    def test_listar_pagamentos_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().listar_pagamentos("foo", "bar")

        url = PagamentoLoteBBWrapper()._construct_url(
            "pagamentos", search={"dataInicio": "foo", "dataFim": "bar", "indice": 0}
        )

        self.mocked_get.assert_called_with(url, **self.get_request_complements())

    def test_cadastrar_transferencia_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().cadastrar_transferencia(
            "1", "2", "3", "4", "5", "6", "7", "8", "99391916180", "10", "11", "12"
        )

        url = PagamentoLoteBBWrapper()._construct_url("lotes-transferencias")

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

        self.mocked_post.assert_called_with(
            url, **self.get_request_complements(), json=expected_json
        )

    def test_consultar_transferencia_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().consultar_transferencia("1")

        url = PagamentoLoteBBWrapper()._construct_url("transferencias", "1")

        self.mocked_get.assert_called_with(url, **self.get_request_complements())

    def test_cadastrar_pagamento_boleto_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().cadastrar_pagamento_boleto(
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

        url = PagamentoLoteBBWrapper()._construct_url("lotes-boletos")

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

        self.mocked_post.assert_called_with(
            url, **self.get_request_complements(), json=expected_json
        )

    def test_consultar_pagamento_boleto_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().consultar_pagamento_boleto("1")

        url = PagamentoLoteBBWrapper()._construct_url("boletos", "1")

        self.mocked_get.assert_called_with(url, **self.get_request_complements())

    def test_cadastrar_pagamento_tributo_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().cadastrar_pagamento_tributo(
            "1",
            "2",
            "3",
            "4",
            "85800000000600003282126307082112794112788193",
            "7",
            "8",
            "9",
        )

        url = PagamentoLoteBBWrapper()._construct_url("lotes-guias-codigo-barras")

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

        self.mocked_post.assert_called_with(
            url, **self.get_request_complements(), json=expected_json
        )

    def test_consultar_pagamento_tributo_1(self):
        """
        Teste para verificar a URL da requisição e dados
        """
        PagamentoLoteBBWrapper().consultar_pagamento_tributo("1")

        url = PagamentoLoteBBWrapper()._construct_url("guias-codigo-barras", "1")

        self.mocked_get.assert_called_with(url, **self.get_request_complements())
