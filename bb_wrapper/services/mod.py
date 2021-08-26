from typing import Union


class ModService:
    def mod_10(self, number: Union[int, str]) -> str:
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
        if isinstance(number, int):
            number = str(number)

        if not isinstance(number, str):
            raise TypeError("O número deve estar no formato de str!")

        """
        a multiplicação é feita da direita para esquerda
        """
        reversed_number = reversed(number)

        """
        O fator começa em 2
        """
        factor = 2
        total = 0
        for num in reversed_number:
            result = factor * int(num)

            """
            É realizado a soma dos algarismos do produto
            """
            result = sum([int(d) for d in str(result)])

            total += result

            """
            O fator alterna entre 2 e 1
            """
            factor = (factor % 2) + 1

        base = 10
        rest = total % base
        dv = base - rest
        return str(dv)

    def mod_11(self, number: Union[int, str]) -> str:
        """
        Método para calcular o DV módulo 11.

        Referências:
            - https://pt.wikipedia.org/wiki/D%C3%ADgito_verificador
            - https://github.com/eduardocereto/pyboleto/blob/1fed215eac2c974efc6f03a16b94406c2bb55cc2/pyboleto/data.py#L478  # noqa
        """
        if isinstance(number, int):
            number = str(number)

        if not isinstance(number, str):
            raise TypeError("O número deve estar no formato de str!")

        """
        a multiplicação é feita da direita para esquerda
        """
        reversed_number = reversed(number)

        """
        O fator começa em 2
        """
        factor = 2
        total = 0
        for num in reversed_number:
            result = factor * int(num)
            total += result

            """
            O fator alterna entre 2,3,4,5,6,7,8,9 sequencialmente
            """
            factor = (factor % 9) + 1 + (factor // 9) * 1

        base = 11
        rest = total % base
        dv = base - rest
        return str(dv)
