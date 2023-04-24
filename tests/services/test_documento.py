from unittest import TestCase

from bb_wrapper.services.document import DocumentoService


class DocumentServiceTestCase(TestCase):
    maxDiff = None

    def test_identifica_tipo_pessoa_fisica(self):
        """
        Dado:
            - Dado uma string '77855240098'
        Quando:
            - for chamado DocumentoService().identifica_tipo('77855240098')
        Então:
            - o resultado deve ser 1
        """
        cpf = "77855240098"

        result = DocumentoService().identifica_tipo(cpf)

        expected = 1

        self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_fisica_com_pontuacao(self):
        """
        Dado:
            - Dado uma string '778.552.400-98'
        Quando:
            - for chamado DocumentoService().identifica_tipo('778.552.400-98')
        Então:
            - o resultado deve ser 1
        """
        cpf = "778.552.400-98"

        result = DocumentoService().identifica_tipo(cpf)

        expected = 1

        self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_juridica(self):
        """
        Dado:
            - Dado uma string '55468100000139'
        Quando:
            - for chamado DocumentoService().identifica_tipo('55468100000139')
        Então:
            - o resultado deve ser 1
        """
        cnpj = "55468100000139"

        result = DocumentoService().identifica_tipo(cnpj)

        expected = 2

        self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_juridica_com_pontuacao(self):
        """
        Dado:
            - Dado uma string '18.853.097/0001-40'
        Quando:
            - for chamado DocumentoService().identifica_tipo('18.853.097/0001-40')
        Então:
            - o resultado deve ser 1
        """
        cnpj = "18.853.097/0001-40"

        result = DocumentoService().identifica_tipo(cnpj)

        expected = 2

        self.assertEqual(result, expected)

    def test_identifica_tipo_pessoa_document_invalid(self):
        """
        Dado:
            - Dado uma string '554681000001'
        Quando:
            - for chamado DocumentoService().identifica_tipo('554681000001')
        Então:
            - o resultado deve ser 1
        """
        invalid_document = "554681000001"

        with self.assertRaises(ValueError) as ctx:
            DocumentoService().identifica_tipo(invalid_document)

        self.assertEqual(
            ctx.exception.args[0], f"CPF/CNPJ '{invalid_document}' é inválido!"
        )  # noqa
