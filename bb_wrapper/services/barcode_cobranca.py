class BarcodeCobranca:
    """
    Cálculos e método do código de barras e linha digitável dos boletos de cobrança!

    Código de barras de cobrança possui 44 caracteres.

    Linha digitável de cobrança possui 47 caracteres.
    """

    def calculate_barcode_dv(self, barcode: str):
        """
        o “dígito verificador” (DV), do Código de Barras, deve ser
        calculado pelo módulo 11.

        Para calcular o DV considerar 43 posições do Código de Barras sendo da
        posição 1 a 4 e da posição 6 a 44;
        """
        number = barcode[:4] + barcode[5:]

        reversed_number = reversed(number)

        min_factor = 2
        max_factor = 9
        base = 11

        def shift_factor(factor):
            factor += 1
            if factor > max_factor:
                return min_factor
            return factor

        actual_factor = min_factor
        total = 0

        for num in reversed_number:
            result = actual_factor * int(num)
            total += result
            actual_factor = shift_factor(actual_factor)

        rest = total % base

        dv = base - rest

        if dv in [0, 10, 11]:
            dv = 1

        return dv

    def validate_barcode(self, barcode: str):
        """
        Método para validar um código de barras do boleto de cobrança.

        O digito na 5ª posição é o DV do código de barras.
        Por definição do BACEN, na 5ª posição do código de barras, deve ser indicado,
        obrigatoriamente,
        """
        dv = int(barcode[4])

        calculated_dv = self.calculate_barcode_dv(barcode)

        return dv == calculated_dv

    def barcode_to_codeline(self, barcode: str):
        """"""
        