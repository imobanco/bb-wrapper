import re

import unidecode


class UnicodeService:
    def parse_unicode_to_alphanumeric(self, string):
        """
        Método para transliterar um texto com caracteres especiais
        em um texto maiúsculo sem caracteres especiais.
        """
        ascii_string = unidecode.unidecode(string)
        alphanumeric_string = re.sub(r"[^A-Za-z0-9]", "", ascii_string)
        return alphanumeric_string.upper()
