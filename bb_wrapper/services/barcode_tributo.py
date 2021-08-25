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
        6. Carnes e Assemelhados ou demais Empresas / Órgãos que serão identificadas através do CNPJ.
        7. Multas de trânsito
        9. Uso exclusivo do banco

    valor real ou referência:
        “6”- Valor a ser cobrado efetivamente em reais e DV módulo 10
        “7”- Quantidade de moeda e DV módulo 10
        “8” – Valor a ser cobrado efetivamente em reais e DV módulo 11
        “9” – Quantidade de moeda e DV módulo 11


    Código de barras de tributos possui 44 caracteres:

    Indices     Tamanho       Conteúdo
      0:1         01          Identificação do Produto (Constante “8” para identificar arrecadação)
      1:2         01          Identificação do Segmento
      2:3         01          Identificação do valor real ou referência
      3:4         01          Dígito verificador geral (módulo 10 ou 11)
      4:15        11          Valor
    ------------------------------  OU    --------------------------------
     15:18        04          Identificação da Empresa/Órgão
     18:44        25          Campo livre de utilização da Empresa/Órgão
    ------------------------------  OU    --------------------------------
     15:23        08          CNPJ / MF
     24:44        21          Campo livre de utilização da Empresa/Órgão


    Linha digitável de cobrança possui 48 caracteres:

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

    def _get_number_from_barcode(self, barcode: str) -> str:
        """
        Para calcular o DV considerar 43 posições do Código
        de Barras sendo os slices :3 e 4:
        """
        return barcode[:3] + barcode[4:]

    def _calculate_dv_10(self, barcode: str) -> str:
        """
        O DV do Código de Barras pode ser calculado pelo módulo 10.

        Se o DV no módulo 10 for:
            DV 10 => DV 0
        """
        number = self._get_number_from_barcode(barcode)

        return DACService().dac_10(number, dv_to_dv_mapping={"10": "0"})

    def _calculate_dv_11(self, barcode: str) -> str:
        """
        O DV do Código de Barras pode ser calculado pelo módulo 11.

        Se o DV no módulo 11 for:
            DV 11 => DV 0
            DV 10 => DV 0
        """
        number = self._get_number_from_barcode(barcode)

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
        """ """
        dv = barcode[3]

        method_to_calculate_dv = self._get_dv_method_for_barcode_or_code_line(barcode)

        # noinspection PyArgumentList
        calculated_dv = method_to_calculate_dv(barcode)

        is_dv_correct = dv == calculated_dv

        if raise_exception and not is_dv_correct:
            raise ValueError("Código de barras inválido!")
        return is_dv_correct

    def validate_code_line(self, code_line: str, raise_exception=True) -> bool:
        pass

    def barcode_to_code_line(self, barcode: str, validate=True) -> str:
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
        if validate:
            self.validate_code_line(code_line)

        return code_line[0:11] + code_line[12:23] + code_line[24:35] + code_line[36: 47]
