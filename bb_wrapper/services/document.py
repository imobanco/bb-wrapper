from pycpfcnpj import cpfcnpj


class DocumentoService:
    def identifica_tipo(self, documento):
        """
        1 - Pessoa Física
        2 - Pessoa Jurídica

        Args:
            documento: CPF/CNPJ a ser validado
        """
        documento = self.valida(documento)
        if len(documento) == 11:
            return 1
        else:
            return 2

    def valida(self, documento):
        """
        Valida e limpa pontuação de um documento CPF ou CNPJ

        Args:
            documento: documento a ser validado

        Returns:
            Documento validado e sem máscara
        """
        documento = cpfcnpj.clear_punctuation(documento)
        if not cpfcnpj.validate(documento):
            raise ValueError(f"CPF/CNPJ '{documento}' é inválido!")
        return documento
