from .constants import CONVENIO_NUMBER


def build_our_number(number, convenio=None):
    """
    Método para construir o 'Nosso Número'.

    20 dígitos, que deverá ser formatado da seguinte forma:
        “000” + (número do convênio com 7 dígitos) + (10 algarismos)
    """
    if convenio is None:
        convenio = CONVENIO_NUMBER

    assert len(convenio) == 7, "O número do convênio não tem 7 dígitos!"
    assert len(number) == 10, "O número não tem 10 dígitos!"

    return f"000{convenio}{number}"
