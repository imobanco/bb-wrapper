from crc import CrcCalculator, Configuration


class BRCodeService:
    """
    BR Code é a padronização brasileira de pagamentos via QR Code.

    O BR Code implementa a padronização mundial
    EMV QRCPS–MPM QRCodes for Payment Systems –Merchant Presented Mode.

    References:
        https://www.bcb.gov.br/content/estabilidadefinanceira/SiteAssets/Manual%20do%20BR%20Code.pdf
        https://www.emvco.com/terms-of-use/?u=/wp-content/uploads/documents/EMVCo-Merchant-Presented-QR-Specification-v1-1.pdf
    """

    def _get_len_zfilled(self, data, qt_zfill=2):
        """
        Método para retornar o tamanho de uma informação com
        um zfill de 2.

        Examples:
            >>> len_value = BRCodeService()._get_len_zfilled('123')
            >>> print(len_value)
            "03"
        """

        return f"{len(data)}".zfill(qt_zfill)

    def create_field_string(self, _id, value):
        """
        Qualquer campo do BRCode segue o seguinte padrão:
            ID + LEN VALOR + VALOR

        Onde LEN VALOR é a quantidade de caracteres do valor com zfill de 2.
        Ou seja, LEN VALOR de '123' é '03'
        """
        return f"{_id}{self._get_len_zfilled(value)}{value}"

    def crc_16_ccitt_ffff(self, data: str):
        """
        Método para calcular o CRC-16-CCIT-FFFF de um valor.

        Retorna os dois valores hexadecimais do resultado como string.

        Configurações:
            CRC - algorítmo de verificação
            16 - width
            ccitt - polinômio 0x1021
            ffff - valor inicial 0xFFFF
        """
        crc_configuration = Configuration(
            width=16,
            polynomial=0x1021,
            init_value=0xFFFF,
            final_xor_value=0x0000,
            reverse_input=False,
            reverse_output=False,
        )
        crc_calculator = CrcCalculator(crc_configuration)
        data_to_encode = bytes(data, encoding="utf-8")
        crc_value = crc_calculator.calculate_checksum(data_to_encode)
        crc_value = str(hex(crc_value))[2:].upper()
        return crc_value
