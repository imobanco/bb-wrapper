from .dac import DACService


class BarcodeTributoService:
    """
    Cálculos e métodos do código de barras e linha digitável dos boletos de tributos!

    Foi utilizado o documento "docs/tributos/Layout - Código de Barras ATUALIZADO.pdf"

    Segimentos:
        1. Prefeituras;
        2. Saneamento;
        3. Energia Elétrica e Gás;
        4. Telecomunicações;
        5. Órgãos Governamentais;
        6. Carnes e Assemelhados ou demais Empresas / Órgãos que serão identificadas através do CNPJ.  # noqa: E501
        7. Multas de trânsito
        9. Uso exclusivo do banco

    valor real ou referência:
        "6" - Valor a ser cobrado efetivamente em reais e DV módulo 10
        "7" - Quantidade de moeda e DV módulo 10
        "8" - Valor a ser cobrado efetivamente em reais e DV módulo 11
        "9" - Quantidade de moeda e DV módulo 11


    Código de barras de tributos possui 44 caracteres:

    Indices     Tamanho       Conteúdo
      0:1         01          Identificação do Produto (Constante “8” para identificar arrecadação)  # noqa: E501
      1:2         01          Identificação do Segmento
      2:3         01          Identificação do valor real ou referência
      3:4         01          Dígito verificador geral (módulo 10 ou 11)
      4:15        11          Valor
    ------------------------------  OU    --------------------------------
     15:18        04          Identificação da Empresa/Órgão
     18:44        25          Campo livre de utilização da Empresa/Órgão
    ------------------------------  OU    --------------------------------
     15:23        08          CNPJ / Ministério da Fazenda
     24:44        21          Campo livre de utilização da Empresa/Órgão


    Linha digitável de tributos possui 48 caracteres:

    Indices     Tamanho       Conteúdo
      0:11        11          Slice 0:11 do código de barras
     11:12        01          DV do slice 0:11 da linha digitável

     12:23        11          Slice 11:22 do código de barras
     23:24        01          DV do slice 12:23 da linha digitável

     24:35        11          Slice 22:33 do código de barras (Campo Livre pt3)
     35:36        01          DV do slice 24:35 da linha digitável

     36:47        11          Slice 33:44 do código de barras
     47:48        01          DV do slice 36:47 da linha digitável
    """

    def _get_number_from_barcode(self, barcode: str) -> str:
        """
        Para calcular o DV considerar 43 posições do Código
        de Barras sendo os slices :3 e 4:
        """
        return barcode[:3] + barcode[4:]

    def _calculate_dv_10(self, barcode_or_code_line: str) -> str:
        """
        O DV do Código de Barras pode ser calculado pelo módulo 10.

        Se o DV no módulo 10 for:
            DV 10 => DV 0
        """
        if len(barcode_or_code_line) == 44:
            number = self._get_number_from_barcode(barcode_or_code_line)
        else:
            number = barcode_or_code_line

        return DACService().dac_10(number, dv_to_dv_mapping={"10": "0"})

    def _calculate_dv_11(self, barcode_or_code_line: str) -> str:
        """
        O DV do Código de Barras pode ser calculado pelo módulo 11.

        Se o DV no módulo 11 for:
            DV 11 => DV 0
            DV 10 => DV 0
        """
        if len(barcode_or_code_line) == 44:
            number = self._get_number_from_barcode(barcode_or_code_line)
        else:
            number = barcode_or_code_line

        return DACService().dac_11(number, dv_to_dv_mapping={"10": "0", "11": "0"})

    def _get_dv_method_for_barcode_or_code_line(
        self, barcode_or_code_line: str
    ) -> callable:
        valor_real_ou_referencia = barcode_or_code_line[2]
        mapping_to_dv_method = {
            "6": self._calculate_dv_10,
            "7": self._calculate_dv_10,
            "8": self._calculate_dv_11,
            "9": self._calculate_dv_11,
        }
        try:
            method_to_calculate_dv = mapping_to_dv_method[valor_real_ou_referencia]
        except KeyError as e:
            raise ValueError("Valor real ou referência invalida!") from e
        return method_to_calculate_dv

    def validate_barcode(self, barcode: str, raise_exception=True) -> bool:
        """
        Método para validar um código de barras.

        O DV do código de barras está no índice 3.
        """
        dv = barcode[3]

        method_to_calculate_dv = self._get_dv_method_for_barcode_or_code_line(barcode)

        # noinspection PyArgumentList
        calculated_dv = method_to_calculate_dv(barcode)

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

        method_to_calculate_dv = self._get_dv_method_for_barcode_or_code_line(barcode)

        part_1 = code_line[0:11]
        dv_1 = code_line[11]
        # noinspection PyArgumentList
        calculated_dv_1 = method_to_calculate_dv(part_1)
        is_dv_1_correct = dv_1 == calculated_dv_1

        part_2 = code_line[12:23]
        dv_2 = code_line[23]
        # noinspection PyArgumentList
        calculated_dv_2 = method_to_calculate_dv(part_2)
        is_dv_2_correct = dv_2 == calculated_dv_2

        part_3 = code_line[24:35]
        dv_3 = code_line[35]
        # noinspection PyArgumentList
        calculated_dv_3 = method_to_calculate_dv(part_3)
        is_dv_3_correct = dv_3 == calculated_dv_3

        part_4 = code_line[36:47]
        dv_4 = code_line[47]
        # noinspection PyArgumentList
        calculated_dv_4 = method_to_calculate_dv(part_4)
        is_dv_4_correct = dv_4 == calculated_dv_4

        is_code_line_dvs_correct = (
            is_dv_1_correct and is_dv_2_correct and is_dv_3_correct and is_dv_4_correct
        )

        if raise_exception and not is_code_line_dvs_correct:
            raise ValueError("Linha digitável inválida!")
        return is_code_line_dvs_correct

    def barcode_to_code_line(self, barcode: str, validate=True) -> str:
        """
        Método para converter o códigoa linha digitável em código de barras.

        Os slices presentes nesse método estão documentados na docstring do service!
        """
        if validate:
            self.validate_barcode(barcode)

        method_to_calculate_dv = self._get_dv_method_for_barcode_or_code_line(barcode)

        part_1 = barcode[0:11]
        # noinspection PyArgumentList
        dv_1 = method_to_calculate_dv(part_1)

        part_2 = barcode[11:22]
        # noinspection PyArgumentList
        dv_2 = method_to_calculate_dv(part_2)

        part_3 = barcode[22:33]
        # noinspection PyArgumentList
        dv_3 = method_to_calculate_dv(part_3)

        part_4 = barcode[33:44]
        # noinspection PyArgumentList
        dv_4 = method_to_calculate_dv(part_4)

        return part_1 + dv_1 + part_2 + dv_2 + part_3 + dv_3 + part_4 + dv_4

    def code_line_to_barcode(self, code_line: str, validate=True) -> str:
        """
        Método para converter a linha digitável em código de barras.

        Os slices presentes nesse método estão documentados na docstring do service!
        """
        if validate:
            self.validate_code_line(code_line)

        return code_line[0:11] + code_line[12:23] + code_line[24:35] + code_line[36:47]
