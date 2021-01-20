import base64


class Base64Service:
    DEFAULT_DATA_URI_SCHEMA = "data:image/svg+xml;base64"

    def generate_b64image_from_buffer(
        self, buffer, data_uri_schema=DEFAULT_DATA_URI_SCHEMA
    ):
        """
        Método para gerar uma string base64 de imagem svg a partir de um buffer
        """
        base64_img = base64.b64encode(buffer.getvalue())
        base64_string = f"{data_uri_schema},{base64_img.decode('utf-8')}"
        return base64_string
