from py_bdd_context import BDDContextTestCase
from bb_wrapper.models.perfis import TipoInscricaoEnum

from bb_wrapper.services.document import DocumentoService


class DocumentServiceTestCase(BDDContextTestCase):
    maxDiff = None

    def test_identifica_tipo_pessoa_fisica(self):
        with self.given(
            """
                - um CPF '77855240098'
            """
        ):
            cpf = "77855240098"

        with self.when(
            """
                - utilizar o service de Documento para identificar o tipo de pessoa
            """
        ):
            result = DocumentoService().identifica_tipo(cpf)

        with self.then(
            """
                - o tipo de pessoa deve ser física
            """
        ):
            expected = TipoInscricaoEnum.cpf
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_fisica_com_pontuacao(self):
        with self.given(
            """
                - um CPF com pontuação '778.552.400-98'
            """
        ):
            cpf = "778.552.400-98"

        with self.when(
            """
                - utilizar o service de Documento para identificar o tipo de pessoa
            """
        ):
            result = DocumentoService().identifica_tipo(cpf)

        with self.then(
            """
                - o tipo de pessoa deve ser física
            """
        ):
            expected = TipoInscricaoEnum.cpf
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_juridica(self):
        with self.given(
            """
                - um CNPJ sem pontuação '55468100000139'
            """
        ):
            cnpj = "55468100000139"

        with self.when(
            """
                - utilizar o service de Documento para identificar o tipo de pessoa
            """
        ):
            result = DocumentoService().identifica_tipo(cnpj)

        with self.then(
            """
                - o tipo de pessoa deve ser jurídica
            """
        ):
            expected = TipoInscricaoEnum.cnpj
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_juridica_com_pontuacao(self):
        with self.given(
            """
                - um CNPJ sem pontuação '18.853.097/0001-40'
            """
        ):
            cnpj = "18.853.097/0001-40"

        with self.when(
            """
                - utilizar o service de Documento para identificar o tipo de pessoa
            """
        ):
            result = DocumentoService().identifica_tipo(cnpj)

        with self.then(
            """
                - o tipo de pessoa deve ser jurídica
            """
        ):
            expected = TipoInscricaoEnum.cnpj
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_document_invalid(self):
        with self.given(
            """
                - um valor que não corresponde a um CPF e nem CPNJ sem pontuação: '554681000001' # noqa E501
            """
        ):
            invalid_document = "554681000001"

        with self.when(
            """
                - utilizar o service de Documento para identificar o tipo de pessoa
            """
        ):
            with self.assertRaises(ValueError) as ctx:
                DocumentoService().identifica_tipo(invalid_document)

        with self.then(
            """
                - deverá ser levantada uma exceção informando que o CPF/CNPJ é inválido!
            """
        ):
            self.assertEqual(
                ctx.exception.args[0], f"CPF/CNPJ '{invalid_document}' é inválido!"
            )  # noqa
