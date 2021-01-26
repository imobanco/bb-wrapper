class ModService:
    def mod_10(self, num):
        """
        Método para calcular o DV módulo 10.

        Referências:
            - https://pt.wikipedia.org/wiki/D%C3%ADgito_verificador
            - https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L453  # noqa
        """
        if isinstance(num, int):
            num = str(num)

        if not isinstance(num, str):
            raise TypeError("O número deve estar no formato de str!")

        total = 0
        factor = 2
        for digit in reversed(num):
            result = int(digit) * factor
            total += sum([int(d) for d in str(result)])
            factor = (factor % 2) + 1

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
