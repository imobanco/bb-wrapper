from .mod import ModService


class DACService:
    def dac_10(self, number, dv_to_dv_mapping=None):
        """
        Método para calcular DAC módulo 10.
        """
        dv = ModService().mod_10(number)

        try:
            dv = dv_to_dv_mapping[dv]
        except (TypeError, KeyError):
            pass

        return dv

    def dac_11(self, number, dv_to_dv_mapping=None):
        """
        Método para calcular o DAC módulo 11.
        """
        dv = ModService().mod_11(number)

        try:
            dv = dv_to_dv_mapping[dv]
        except (TypeError, KeyError):
            pass

        return str(dv)
