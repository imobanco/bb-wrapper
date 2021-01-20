class ModService:
    def modulo10(self, num):
        """
        Método para calcular módulo 10.

        https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L453  # noqa
        """
        if not isinstance(num, str):
            raise TypeError
        soma = 0
        peso = 2
        for c in reversed(num):
            parcial = int(c) * peso
            if parcial > 9:
                s = str(parcial)
                parcial = int(s[0]) + int(s[1])
            soma += parcial
            if peso == 2:
                peso = 1
            else:
                peso = 2

        resto10 = soma % 10

        if resto10 == 0:
            modulo10 = 0
        else:
            modulo10 = 10 - resto10

        return modulo10

    def modulo11(self, num, base=9, r_base=0):
        """
        Método para calcular módulo 11.

        https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L478  # noqa
        """
        if not isinstance(num, str):
            raise TypeError

        if r_base != 0 and r_base != 1:
            raise ValueError("O r_base precisa ser 1 ou 0")

        soma = 0
        fator = 2
        for c in reversed(num):
            soma += int(c) * fator
            if fator == base:
                fator = 1
            fator += 1
        if r_base == 0:
            soma = soma * 10
            digito = soma % 11
            if digito == 10:
                digito = 0
            return digito
        if r_base == 1:
            resto = soma % 11
            return resto
