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

    _fields_to_barcode_and_code_line_mapping = [
        {
            "field": "Código do Banco na Câmara de Compensação e Código da Moeda",
            "barcode_slice_indexes": [0, 4],
            "barcode_order": 1,
            "code_line_slice_indexes": [0, 4],
            "code_line_order": 1.0,
        },
        {
            "field": "Campo Livre pt1",
            "barcode_slice_indexes": [19, 24],
            "barcode_order": 5,
            "code_line_slice_indexes": [4, 9],
            "code_line_order": 1.1,
        },
        {
            "field": "Campo Livre pt2",
            "barcode_slice_indexes": [24, 34],
            "barcode_order": 6,
            "code_line_slice_indexes": [10, 20],
            "code_line_order": 2.0,
        },
        {
            "field": "Campo Livre pt3",
            "barcode_slice_indexes": [34, 44],
            "barcode_order": 7,
            "code_line_slice_indexes": [21, 31],
            "code_line_order": 3.0,
        },
        {
            "field": "DV do código de Barras",
            "barcode_slice_indexes": [4, 5],
            "barcode_order": 2,
            "code_line_slice_indexes": [32, 33],
            "code_line_order": 4.0,
        },
        {
            "field": "Fator de Vencimento",
            "barcode_slice_indexes": [5, 9],
            "barcode_order": 3,
            "code_line_slice_indexes": [33, 37],
            "code_line_order": 5.0,
        },
        {
            "field": "Valor",
            "barcode_slice_indexes": [9, 19],
            "barcode_order": 4,
            "code_line_slice_indexes": [37, 47],
            "code_line_order": 5.1,
        },
    ]

    def calculate_barcode_dv(self, barcode: str) -> str:
        """
        O DV do Código de Barras deve ser calculado pelo módulo 11.

        Para calcular o DV considerar 43 posições do Código
        de Barras sendo os slices :4 e 5:
        """
        number = barcode[:4] + barcode[5:]

        reversed_number = reversed(number)

        factor = 2
        total = 0
        for num in reversed_number:
            result = factor * int(num)
            total += result
            factor = (factor % 9) + 1 + (factor // 9) * 1

        base = 11
        rest = total % base
        dv = base - rest
        if dv in [0, 10, 11]:
            dv = 1

        return str(dv)

    def calculate_code_line_dv(self, number: str) -> str:
        """
        O DV de uma parte da linha digitável deve ser
        calculado pelo módulo 10.
        """
        reversed_number = reversed(number)

        factor = 2
        total = 0
        for num in reversed_number:
            result = factor * int(num)
            result = sum([int(d) for d in str(result)])
            total += result
            factor = (factor % 2) + 1

        base = 10
        rest = total % base
        dv = base - rest
        if dv in [10]:
            dv = 0

        return str(dv)

    def validate_barcode(self, barcode: str, raise_exception=True) -> bool:
        """
        Método para validar um código de barras do boleto de cobrança.

        O digito no índice 4 é o DV do código de barras.
        """
        dv = barcode[4]

        calculated_dv = self.calculate_barcode_dv(barcode)

        is_dv_correct = dv == calculated_dv

        if raise_exception and not is_dv_correct:
            raise ValueError("Código de barras inválido!")
        return is_dv_correct

    def validate_code_line(self, code_line: str, raise_exception=True) -> bool:
        """ """
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
        """"""
        if validate:
            self.validate_barcode(barcode)

        code_line = ""
        parts = {}

        mapping_for_code_line = sorted(
            self._fields_to_barcode_and_code_line_mapping,
            key=lambda k: k["code_line_order"],
        )

        for item in mapping_for_code_line:
            barcode_part_start = item["barcode_slice_indexes"][0]
            barcode_part_end = item["barcode_slice_indexes"][1]
            part_index = int(item["code_line_order"])
            barcode_part = barcode[barcode_part_start:barcode_part_end]
            try:
                parts[part_index] += barcode_part
            except KeyError:
                parts[part_index] = barcode_part

        for part_index in range(1, 6):
            part = parts[part_index]
            code_line += part
            if part_index < 4:
                code_line += self.calculate_code_line_dv(part)

        return code_line

    def code_line_to_barcode(self, code_line: str, validate=True) -> str:
        """"""
        if validate:
            self.validate_code_line(code_line)

        barcode = ""

        mapping_for_barcode = sorted(
            self._fields_to_barcode_and_code_line_mapping,
            key=lambda k: k["barcode_order"],
        )

        for item in mapping_for_barcode:
            code_line_part_start = item["code_line_slice_indexes"][0]
            code_line_part_end = item["code_line_slice_indexes"][1]
            barcode += code_line[code_line_part_start:code_line_part_end]
        return barcode
