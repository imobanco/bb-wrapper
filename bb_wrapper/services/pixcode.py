from .brcode import BRCodeService
from .qrcode import QRCodeService
from .unicode import UnicodeService


class PixCodeService:
    """
    Service para gerar QR Code PIX.

    O QRCode PIX segue a implementação do BR Code

    https://forum.developers.bb.com.br/t/duvida-sobre-a-criacao-do-qrcode-da-cobranca-pix/4503

    seção 1.6.7 do II_ManualdePadroesparaIniciacaodoPix_versao2-3-0.pdf
    """

    def create(self, location: str, nome_recebedor: str):
        """
        Função para criar o QRCode PIX!

        Args:
            location: url 'location' do PIX dinâmico
            nome_recebedor: nome do recebedor
        """
        # campo ID 00 Payload Format Indicator
        data = BRCodeService().create_field_string(_id="00", value="01")

        # campo ID 01 Point of Initiation Method
        data += BRCodeService().create_field_string(_id="01", value="12")
        """
        12 = não deve ser pago mais de uma vez
        """

        # campo ID 26 Merchant Account Information
        # subcampo ID 00 GUI
        merchant_account_information = BRCodeService().create_field_string(
            _id="00", value="br.gov.bcb.pix"
        )

        # subcampo ID 25 URL
        merchant_account_information += BRCodeService().create_field_string(
            _id="25", value=location
        )

        data += BRCodeService().create_field_string(
            _id="26", value=merchant_account_information
        )

        # campo ID 52 Merchant Category Code
        data += BRCodeService().create_field_string(_id="52", value="0000")
        """
        0000 = não informado
        """

        # campo ID 53 Transaction Currency
        data += BRCodeService().create_field_string(_id="53", value="986")
        """
        986 = R$
        """

        # campo ID 58 Country Code
        data += BRCodeService().create_field_string(_id="58", value="BR")

        # campo ID 59 Merchant Name
        nome_recebedor = nome_recebedor[:13]
        nome_recebedor = UnicodeService().parse_unicode_to_alphanumeric(nome_recebedor)
        data += BRCodeService().create_field_string(_id="59", value=nome_recebedor)

        # campo ID 60 Merchant City
        data += BRCodeService().create_field_string(_id="60", value="NATAL")

        # campo ID 62 Aditional Data Field
        # subcampo ID 05 Reference Label
        aditional_data_field = BRCodeService().create_field_string(
            _id="05", value="***"
        )

        data += BRCodeService().create_field_string(
            _id="62", value=aditional_data_field
        )

        # campo ID 63 CRC 16
        data_to_encode = data + "6304"
        crc_value = BRCodeService().crc_16_ccitt_ffff(data_to_encode)
        crc_value = crc_value.zfill(4)
        data += BRCodeService().create_field_string(_id="63", value=crc_value)

        return data, QRCodeService().generate_qrcode_b64image(data)
