from py_bdd_context import BDDContextTestCase

from bb_wrapper.services.document import DocumentoService


class DocumentServiceTestCase(BDDContextTestCase):
    maxDiff = None

    def test_identifica_tipo_pessoa_fisica(self):
        with self.given(
            """
            - Uma string '77855240098'
            """
        ):
            cpf = "77855240098"
        with self.when(
            """
            - DocumentoService().identifica_tipo('77855240098')
            """
        ):
            result = DocumentoService().identifica_tipo(cpf)
        with self.then(
            """
            - O resultado deve ser 1
            """
        ):
            expected = 1
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_fisica_com_pontuacao(self):
        with self.given(
            """
            - Uma string '778.552.400-98'
            """
        ):
            cpf = "778.552.400-98"
        with self.when(
            """
            - DocumentoService().identifica_tipo('778.552.400-98')
            """
        ):
            result = DocumentoService().identifica_tipo(cpf)
        with self.then(
            """
            - O resultado deve ser 1
            """
        ):
            expected = 1

            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_juridica(self):
        with self.given(
            """
            - Uma string '55468100000139'
            """
        ):
            cnpj = "55468100000139"
        with self.when(
            """
            - DocumentoService().identifica_tipo('55468100000139')
            """
        ):
            result = DocumentoService().identifica_tipo(cnpj)
        with self.then(
            """
            - O resultado deve ser 1
            """
        ):
            expected = 2
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_juridica_com_pontuacao(self):
        with self.given(
            """
            - Uma string '18.853.097/0001-40'
            """
        ):
            cnpj = "18.853.097/0001-40"

        with self.when(
            """
            - DocumentoService().identifica_tipo('18.853.097/0001-40')
            """
        ):
            result = DocumentoService().identifica_tipo(cnpj)
        with self.then(
            """
            - O  resultado deve ser 1
            """
        ):
            expected = 2
            self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_document_invalid(self):
        with self.given(
            """
            - Uma string '554681000001'
            """
        ):
            invalid_document = "554681000001"
        with self.when(
            """
            - DocumentoService().identifica_tipo('554681000001')
            """
        ):
            with self.assertRaises(ValueError) as ctx:
                DocumentoService().identifica_tipo(invalid_document)
        with self.then(
            """
            - CPF/CNPJ '554681000001' é inválido!
            """
        ):
            self.assertEqual(
                ctx.exception.args[0], f"CPF/CNPJ '{invalid_document}' é inválido!"
            )  # noqa
