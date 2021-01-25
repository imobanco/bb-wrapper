from .mod import ModService


class FebrabranService:
    def dac_10(self, number):
        """
        Método para calcular o dac modulo 10 de um número.

        Referência:
            - página 14 https://github.com/imobanco/bb-wrapper/blob/7643255ac3d6f4ed1d6086cc2ad37c281659ea95/docs/Layout%20-%20C%C3%B3digo%20de%20Barras%20ATUALIZADO.pdf  # noqa
        """
        dv = ModService().modulo10(number)
        if dv == 10:
            dv = 0
        return dv

    def dac_11(self, number):
        """
        Método para calcular o dac modulo 11 de um número.

        Referências:
            - página 16 https://github.com/imobanco/bb-wrapper/blob/7643255ac3d6f4ed1d6086cc2ad37c281659ea95/docs/Layout%20-%20C%C3%B3digo%20de%20Barras%20ATUALIZADO.pdf  # noqa
        """
        dv = ModService().modulo11(number, multiply_by_10_flag=False)
        if dv in [11, 10]:
            dv = 0
        return dv
