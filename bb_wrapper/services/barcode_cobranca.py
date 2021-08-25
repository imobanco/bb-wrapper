from .dac import DACService


class BarcodeCobrancaService:
    """
    Cálculos e métodos do código de barras e linha digitável dos boletos de cobrança!

    Foi utilizado o documento "docs/cobranca/especificações técnicas boleto de cobrança.pdf"

    Código de barras de cobrança possui 44 caracteres:

    Indices     Tamanho       Conteúdo
      0:3         03          Código do Banco na Câmara de Compensação
      3:4         01          Código da Moeda = 9 (Real)
      4:5         01          DV do código de Barras (calculado de acordo com o Módulo 11)  # noqa: E501
      5:9         04          Fator de Vencimento
      9:19        10          Valor
     19:44        25          Campo Livre


    Linha digitável de cobrança possui 47 caracteres:

    Indices     Tamanho       Conteúdo
      0:4         04          Slice 0:4 do código de barras (Código do Banco na Câmara de Compensação e Código da Moeda)  # noqa: E501
      4:9         05          Slice 19:24 do código de barras (Campo Livre pt1)
      9:10        01          DV do slice 0:9 da linha digitável (calculado de acordo com o Módulo 10)  # noqa: E501

     10:20        10          Slice 24:34 do código de barras (Campo Livre pt2)
     20:21        01          DV do slice 10:20 da linha digitável (calculado de acordo com o Módulo 10)  # noqa: E501

     21:31        10          Slice 34:44 do código de barras (Campo Livre pt3)
     31:32        01          DV do slice 21:31 da linha digitável (calculado de acordo com o Módulo 10)  # noqa: E501

     32:33        01          Slice 4:5 do código de barras (DV do código de Barras)

     33:37        04          Slice 5:9 do código de barras (Fator de Vencimento)
     37:47        10          Slice 9:19 do código de barras (Valor)
    """

    def calculate_barcode_dv(self, barcode: str) -> str:
        """
        Para calcular o DV considerar 43 posições do Código
        de Barras sendo os slices :4 e 5:

        O DV do Código de Barras deve ser calculado pelo módulo 11.

        Se o DV do módulo 11 for:
            DV 11 => DV 1
            DV 10 => DV 1
        """
        number = barcode[:4] + barcode[5:]

        return DACService().dac_11(number, dv_to_dv_mapping={"11": "1", "10": "1"})

    def calculate_code_line_dv(self, number: str) -> str:
        """
        O DV de uma parte da linha digitável deve ser
        calculado pelo módulo 10.

        Se o DV do módulo 10 for:
            DV 10 => DV 0
        """
        return DACService().dac_10(number, dv_to_dv_mapping={"10": "0"})

    def validate_barcode(self, barcode: str, raise_exception=True) -> bool:
        """
        Método para validar um código de barras.

        O digito no índice 4 é o DV do código de barras.
        """
        dv = barcode[4]

        calculated_dv = self.calculate_barcode_dv(barcode)

        is_dv_correct = dv == calculated_dv

        if raise_exception and not is_dv_correct:
            raise ValueError("Código de barras inválido!")
        return is_dv_correct

    def validate_code_line(self, code_line: str, raise_exception=True) -> bool:
        """
        Método para validar uma linha digitável.

        Os slices presentes nesse método estão documentados na docstring do service!
        """
        barcode = self.code_line_to_barcode(code_line, validate=False)

        try:
            self.validate_barcode(barcode)
        except ValueError as e:
            raise ValueError("Linha digitável inválida!") from e

        part_1 = code_line[0:9]
        dv_1 = code_line[9]
        calculated_dv_1 = self.calculate_code_line_dv(part_1)
        is_dv_1_correct = dv_1 == calculated_dv_1

        part_2 = code_line[10:20]
        dv_2 = code_line[20]
        calculated_dv_2 = self.calculate_code_line_dv(part_2)
        is_dv_2_correct = dv_2 == calculated_dv_2

        part_3 = code_line[21:31]
        dv_3 = code_line[31]
        calculated_dv_3 = self.calculate_code_line_dv(part_3)
        is_dv_3_correct = dv_3 == calculated_dv_3

        is_code_line_dvs_correct = (
            is_dv_1_correct and is_dv_2_correct and is_dv_3_correct
        )

        if raise_exception and not is_code_line_dvs_correct:
            raise ValueError("Linha digitável inválida!")
        return is_code_line_dvs_correct

    def barcode_to_code_line(self, barcode: str, validate=True) -> str:
        """
        Método para converter um código de barras em linha digitável.

        Os slices presentes nesse método estão documentados na docstring do service!
        """
        if validate:
            self.validate_barcode(barcode)

        part_1 = barcode[0:4] + barcode[19:24]
        dv_1 = self.calculate_code_line_dv(part_1)

        part_2 = barcode[24:34]
        dv_2 = self.calculate_code_line_dv(part_2)

        part_3 = barcode[34:44]
        dv_3 = self.calculate_code_line_dv(part_3)

        part_4 = barcode[4:5]

        part_5 = barcode[5:19]

        return part_1 + dv_1 + part_2 + dv_2 + part_3 + dv_3 + part_4 + part_5

    def code_line_to_barcode(self, code_line: str, validate=True) -> str:
        """
        Método para converter uma linha digitável em código de barras.

        Os slices presentes nesse método estão documentados na docstring do service!
        """
        if validate:
            self.validate_code_line(code_line)

        return (
            code_line[0:4]
            + code_line[32:47]
            + code_line[4:9]
            + code_line[10:20]
            + code_line[21:31]
        )
