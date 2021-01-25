class ModService:
    def modulo10(self, num):
        """
        Método para calcular o DV módulo 10.

        Referências:
            - https://pt.wikipedia.org/wiki/D%C3%ADgito_verificador
            - https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L453  # noqa
        """
        if not isinstance(num, str):
            raise TypeError
        soma = 0

        peso = 2
        for c in reversed(num):
            result = str(int(c) * peso)

            try:
                soma += int(result[0]) + int(result[1])
            except IndexError:
                soma += int(result)

            peso = (peso % 2)+1

        resto = soma % 10
        dv = 10 - resto
        return dv

    def modulo11(self, num, base=9, multiply_by_10_flag=True):
        """
        Método para calcular o DV módulo 11.

        Referências:
            - https://pt.wikipedia.org/wiki/D%C3%ADgito_verificador
            - página 16 https://github.com/imobanco/bb-wrapper/blob/7643255ac3d6f4ed1d6086cc2ad37c281659ea95/docs/Layout%20-%20C%C3%B3digo%20de%20Barras%20ATUALIZADO.pdf  # noqa
            - https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L478  # noqa
        """

        if not isinstance(num, str):
            raise TypeError

        soma = 0
        fator = 2
        for c in reversed(num):
            soma += int(c) * fator
            if fator == base:
                fator = 1
            fator += 1

        if multiply_by_10_flag:
            soma = soma * 10

        resto = soma % 11
        dv = 11 - resto
        return dv
