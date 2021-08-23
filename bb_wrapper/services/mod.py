class ModService:
    def mod_10(self, num):
        """
        Método para calcular o DV módulo 10.

        O DAC (Dígito de Auto-Conferência) módulo 10, de um número é calculado multiplicando
        cada algarismo, pela seqüência de multiplicadores 2, 1, 2, 1, ...
        posicionados da direita para a esquerda.

        A soma dos algarismos do produto é dividida por 10 e o DAC será a diferença entre o
        divisor (10) e o resto da divisão.

        Referências:
            - https://pt.wikipedia.org/wiki/D%C3%ADgito_verificador
            - https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L453  # noqa
        """
        if isinstance(num, int):
            num = str(num)

        if not isinstance(num, str):
            raise TypeError("O número deve estar no formato de str!")

        total = 0

        """
        O fator começa com 2
        """
        factor = 2

        """
        O produto é feito da direita para esquerda!
        """
        reversed_num = reversed(num)

        for digit in reversed_num:
            result = int(digit) * factor

            """
            A soma dos algarismos do produto será dividida por 10...
            """
            total += sum([int(d) for d in str(result)])

            """
            O fator alterna entre 2 e 1...
            """
            factor = (factor % 2) + 1

        """
        o DAC será a diferença entre o
        divisor (10) e o resto da divisão.
        """
        rest = total % 10
        dv = 10 - rest
        return dv

    def mod_11(self, num, multiply_by_10_flag=True, base=9):
        """
        Método para calcular o DV módulo 11.

        Referências:
            - https://pt.wikipedia.org/wiki/D%C3%ADgito_verificador
            - https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L478  # noqa
        """
        if isinstance(num, int):
            num = str(num)

        if not isinstance(num, str):
            raise TypeError("O número deve estar no formato de str!")

        total = 0
        factor = 2
        for digit in reversed(num):
            total += int(digit) * factor
            factor = (factor % base) + 1 + (factor // base) * 1

        if multiply_by_10_flag:
            total = total * 10

        rest = total % 11
        dv = 11 - rest
        return dv
