import uuid

from pycpfcnpj import cpfcnpj

from ..models.pagamentos import TipoChavePIX


class PixService:
    def identify_key_type(self, key: str):
        key_len = len(key)
        try:
            is_uuid = uuid.UUID(key)
        except ValueError:
            is_uuid = False
        is_document = cpfcnpj.validate(key)

        if '@' in key:
            return TipoChavePIX.email
        elif is_document:
            return TipoChavePIX.documento
        elif key_len == 11 and key[2] == '9':
            return TipoChavePIX.telefone
        elif is_uuid:
            return TipoChavePIX.uuid
        else:
            raise ValueError("Tipo de chave não identificado")
