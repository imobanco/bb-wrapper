import uuid
import re

from pycpfcnpj import cpfcnpj

from ..models.pagamentos import TipoChavePIX


class PixService:
    def identify_key_type(self, key: str):
        """
        Identifica o tipo de chave PIX.

        Existem diversas validações/verificações nesse método.

        1. '@' presente (para email)
        2. CPF/CNPJ válido
        3. tamanho 11 e inicia com '9' (para telefone)
        4. UUID válido

        Args:
            key: Chave a ser identificada

        Returns:
            Tipo de chave PIX
        """
        key_len = len(key)

        # 1
        is_email = "@" in key

        # 2
        is_document = cpfcnpj.validate(key)

        # 3
        is_phone = key_len == 11 and key[2] == "9"

        # 4
        try:
            is_uuid = bool(uuid.UUID(key))
        except ValueError:
            is_uuid = False

        if (is_email + is_phone + is_uuid + is_document) > 1:
            raise ValueError("A chave utilizada pode ser mais de um tipo!")
        elif is_email:
            return TipoChavePIX.email
        elif is_document:
            return TipoChavePIX.documento
        elif is_phone:
            return TipoChavePIX.telefone
        elif is_uuid:
            return TipoChavePIX.uuid
        else:
            raise ValueError("Tipo de chave não identificado")

    def verify_email(self, email: str, raise_exception=True):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        is_email_valid = re.fullmatch(regex, email)

        if raise_exception and not is_email_valid:
            raise ValueError("Email inválido!")
        return is_email_valid
