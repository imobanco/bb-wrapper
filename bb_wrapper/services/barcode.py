import io

from barcode import generate as generate_barcode
from barcode.writer import SVGWriter

from .b64 import Base64Service


class BarCodeService:
    def generate_barcode_b64image(self, barcode, text=""):
        """
        Método para gerar uma imagem base46 a partir de um código de barras numérico.
        """
        buffer = io.BytesIO()
        generate_barcode(
            name="itf",
            code=barcode,
            output=buffer,
            text=text,
            writer=SVGWriter(),
            writer_options={
                "quiet_zone": 0,  # margin esquerda e direita (sem margem pois nosso template tem espaço!)  # noqa
                # "module_width": 0.3,  # largura (0.3 mm => 817px)
                "module_width": 0.2,  # largura (0.2 mm => 545px)
                # "module_width": 0.1,  # largura (0.2 mm => 272px)
                # "module_height": 14  # altura (14 mm => 60px)
                # "module_height": 13  # altura (13 mm => 56px)
                "module_height": 12,  # altura (12 mm => 52px)
            },
        )
        return Base64Service().generate_b64image_from_buffer(buffer)

    def codeline_to_barcode(self, codeline: str):
        """
        Método para converter uma linha digitável em código de barras!

        A linha digitável segue a seguinte especificação:

            Posição 01-03 = Identificação do banco (exemplo: 001 = Banco do Brasil)
            Posição 04-04 = Código de moeda (exemplo: 9 = Real)
            Posição 05-09 = 5 primeiras posições do campo livre (posições 20 a 24 do código de barras)
            Posição 10-10 = Dígito verificador do primeiro campo
            Posição 11-20 = 6ª a 15ª posições do campo livre (posições 25 a 34 do código de barras)
            Posição 21-21 = Dígito verificador do segundo campo
            Posição 22-31 = 16ª a 25ª posições do campo livre (posições 35 a 44 do código de barras)
            Posição 32-32 = Dígito verificador do terceiro campo
            Posição 33-33 = Dígito verificador geral (posição 5 do código de barras)
            Posição 34-37 = Fator de vencimento (posições 6 a 9 do código de barras)
            Posição 38-47 = Valor nominal do título (posições 10 a 19 do código de barras)

            http://www.meusutilitarios.com.br/2015/05/boleto-bancario-validacao-do-codigo-de.html
        """

        barcode = ""
        barcode += codeline[0:4]  # banco + modeda
        barcode += codeline[33]  # dígito verificador
        barcode += codeline[33:37]  # fator de vencimento
        barcode += codeline[37:]  # valor do título
        barcode += codeline[5:9]  # 1ª parte campo livre
        barcode += codeline[11:20]  # 2ª parte campo livre
        barcode += codeline[22:31]  # 3ª parte campo livre
        return barcode

    def barcode_to_codeline(self, barcode):
        """
        Método para converter um código de barras em linha digitável!

        O código de barras segue a seguinte especificação:

            Posição 01-03 = Número do banco
            Posição 04-04 = Código da Moeda - 9 para Real
            Posição 05-05 = Digito verificador do Código de Barras
            Posição 06-09 = Data de vencimento em dias partir de 07/10/1997
            Posição 10-19 = Valor do boleto (8 inteiros e 2 decimais)
            Posição 20-44 = Campo Livre definido por cada banco

            https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L180  # noqa
        """

        return ""
