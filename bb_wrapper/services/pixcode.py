from .qrcode import QRCodeService


class PixCodeService:
    """
    Service para gerar QRCode PIX.

    https://forum.developers.bb.com.br/t/duvida-sobre-a-criacao-do-qrcode-da-cobranca-pix/4503

    seção 1.6.7 do II_ManualdePadroesparaIniciacaodoPix_versao2-3-0.pdf
    """

    def _get_len_zfilled(self, data, qt_zfill=2):
        return f"{data}".zfill(qt_zfill)

    def _create_field_string(self, _id, value):
        return f"{_id}{self._get_len_zfilled(value)}{value}"

    def create(self, location, nome_recebedor):
        """
        Função para criar o QRCode PIX!

        O QRCode PIX segue o padrão BRCode. O BRCode segue a implementação
        EMV QRCPS–MPM QRCodes for Payment Systems –Merchant Presented Mode.

        Referências:
            https://www.bcb.gov.br/content/estabilidadefinanceira/SiteAssets/Manual%20do%20BR%20Code.pdf
            https://www.emvco.com/terms-of-use/?u=/wp-content/uploads/documents/EMVCo-Merchant-Presented-QR-Specification-v1-1.pdf

        Args:
            location: url 'location' do PIX dinâmico
            nome_recebedor: nome do recebedor

        Returns:

        """
        # campo ID 00 Payload Format Indicator
        data = self._create_field_string(_id="00", value="01")

        # campo ID 01 Point of Initiation Method
        data += self._create_field_string(_id="01", value="12")
        """
        12 = não deve ser pago mais de uma vez
        """

        # campo ID 26 Merchant Account Information
        # subcampo ID 00 GUI
        merchant_account_information = self._create_field_string(_id="00", value="br.gov.bcb.pix")

        # subcampo ID 25 URL
        merchant_account_information += self._create_field_string(_id="25", value=location)

        data += self._create_field_string(_id="26", value=merchant_account_information)

        # campo ID 52 Merchant Category Code
        data += self._create_field_string(_id="52", value="0000")
        """
        0000 = não informado
        """

        # campo ID 53 Transaction Currency
        data += self._create_field_string(_id="53", value="986")
        """
        986 = R$
        """

        # campo ID 58 Country Code
        data += self._create_field_string(_id="58", value="BR")

        # campo ID 59 Merchant Name
        data += self._create_field_string(_id="59", value=nome_recebedor)

        # campo ID 60 Merchant City
        data += self._create_field_string(_id="60", value="BRASILIA")

        # campo ID 62 Aditional Data Field
        # subcampo ID 05 Reference Label
        aditional_data_field = self._create_field_string(_id="05", value="***")

        data += self._create_field_string(_id="62", value=aditional_data_field)

        # campo ID 63 CRC 16
        data += self._create_field_string(_id="63", value="????")

        return QRCodeService().generate_qrcode_b64image(data)
