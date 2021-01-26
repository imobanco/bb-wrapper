import io

from barcode import generate as generate_barcode
from barcode.writer import SVGWriter

from .b64 import Base64Service
from .febrabran import FebrabranService


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

            Posição 0:3 (3) = Identificação do banco (exemplo: 001 = Banco do Brasil)
            Posição 3 (1) = Código de moeda (exemplo: 9 = Real)
            Posição 4:9 (5) = 5 primeiras posições do campo livre (posição 19:24 do código de barras)  # noqa
            Posição 9 (1) = Dígito verificador do primeiro campo
            Posição 10:20 (10) = 6ª a 15ª posições do campo livre (posição 24:34 do código de barras)  # noqa
            Posição 20 (1) = Dígito verificador do segundo campo
            Posição 21:31 (10) = 16ª a 25ª posições do campo livre (posição 34:44 do código de barras)  # noqa
            Posição 31 (1) = Dígito verificador do terceiro campo
            Posição 32 (1) = Dígito verificador geral (posição 4 do código de barras)
            Posição 33:37 (4) = Fator de vencimento (posição 5:9 do código de barras)
            Posição 37:47 (10) = Valor nominal do título (posição 9:19 do código de barras)  # noqa

            http://www.meusutilitarios.com.br/2015/05/boleto-bancario-validacao-do-codigo-de.html
        """

        barcode = ""
        barcode += codeline[0:3]  # banco
        barcode += codeline[3]  # modeda
        barcode += codeline[32]  # dígito verificador
        barcode += codeline[33:37]  # fator de vencimento
        barcode += codeline[37:47]  # valor do título
        barcode += codeline[4:9]  # 1ª parte campo livre
        barcode += codeline[10:20]  # 2ª parte campo livre
        barcode += codeline[21:31]  # 3ª parte campo livre
        return barcode

    def barcode_to_codeline(self, barcode):
        """
        Método para converter um código de barras em linha digitável!

        O código de barras segue a seguinte especificação:

            Posição 0:3 (3) = Número do banco
            Posição 3 (1) = Código da Moeda - 9 para Real
            Posição 4 (1) = Digito verificador do Código de Barras
            Posição 5:9 (4) = Data de vencimento em dias partir de 07/10/1997
            Posição 9:19 (10) = Valor do boleto (8 inteiros e 2 decimais)
            Posição 19:44 (25) = Campo Livre definido por cada banco

            https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L180  # noqa
        """
        codeline = ""

        first_number = ""
        first_number += barcode[0:3]  # banco
        first_number += barcode[3]  # moeda
        first_number += barcode[19:24]  # 5 primeiras posições do campo livre
        first_dv = self.calculate_codeline_dv(first_number)

        codeline += first_number + str(first_dv)

        second_number = barcode[24:34]  # 10 seguintes posições do campo livre
        second_dv = self.calculate_codeline_dv(second_number)

        codeline += second_number + str(second_dv)

        third_number = barcode[34:44]  # 10 seguintes posições do campo livre
        third_dv = self.calculate_codeline_dv(third_number)

        codeline += third_number + str(third_dv)

        codeline += barcode[4]  # dígito verificador do código de barras
        codeline += barcode[5:9]  # fator de vencimento
        codeline += barcode[9:19]  # valor do boleto

        return codeline

    def calculate_barcode_dv(self, number):
        """
        Método para calcular o DV geral do código de barras
        """
        return FebrabranService().dac_11(number)

    def calculate_codeline_dv(self, number):
        """
        Método para calcular o DV de um segmento da linha digitável

        .. note:
            Foi presumido que é utilizado o modulo 10 e deu
            certo para o cenário de teste.

            O que não significa que é uma regra universal!
        """
        return FebrabranService().dac_10(number)

    def validate_barcode(self, barcode):
        """
        Método para validar um código de barras

        O código de barras segue a seguinte especificação:

            Posição 0:2 (3) = Número do banco
            Posição 3 (1) = Código da Moeda - 9 para Real
            Posição 4 (1) = Digito verificador do Código de Barras
            Posição 5:9 (4) = Data de vencimento em dias partir de 07/10/1997
            Posição 9:19 (10) = Valor do boleto (8 inteiros e 2 decimais)
            Posição 19:44 (25) = Campo Livre definido por cada banco

            https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L180  # noqa
        """
        dv = int(barcode[4])

        number = barcode[:4] + barcode[5:]

        calculated_dv = self.calculate_barcode_dv(number)

        return dv == calculated_dv

    def validate_codeline(self, codeline):
        """
        Método para validar uma linha digitável

        A linha digitável segue a seguinte especificação:

            Posição 0:3 (3) = Identificação do banco (exemplo: 001 = Banco do Brasil)
            Posição 3 (1) = Código de moeda (exemplo: 9 = Real)
            Posição 4:9 (5) = 5 primeiras posições do campo livre (posições 20 a 24 do código de barras)  # noqa
            Posição 9 (1) = Dígito verificador do primeiro campo
            Posição 10:20 (10) = 6ª a 15ª posições do campo livre (posições 25 a 34 do código de barras)  # noqa
            Posição 20 (1) = Dígito verificador do segundo campo
            Posição 21:31 (10) = 16ª a 25ª posições do campo livre (posições 35 a 44 do código de barras)  # noqa
            Posição 31 (1) = Dígito verificador do terceiro campo
            Posição 32 (1) = Dígito verificador geral (posição 5 do código de barras)
            Posição 33:37 (4) = Fator de vencimento (posições 6 a 9 do código de barras)
            Posição 37:47 (10) = Valor nominal do título (posições 10 a 19 do código de barras)  # noqa

            http://www.meusutilitarios.com.br/2015/05/boleto-bancario-validacao-do-codigo-de.html  # noqa
        """
        valid_barcode = self.validate_barcode(self.codeline_to_barcode(codeline))

        first_number = codeline[:9]
        first_dv = int(codeline[9])
        first_calculated_dv = self.calculate_codeline_dv(first_number)
        first_bool = first_dv == first_calculated_dv

        second_number = codeline[10:20]
        second_dv = int(codeline[20])
        second_calculated_dv = self.calculate_codeline_dv(second_number)
        second_bool = second_dv == second_calculated_dv

        third_number = codeline[21:31]
        third_dv = int(codeline[31])
        third_calculated_dv = self.calculate_codeline_dv(third_number)
        third_bool = third_dv == third_calculated_dv

        return valid_barcode and first_bool and second_bool and third_bool
