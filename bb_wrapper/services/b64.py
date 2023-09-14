import base64


class Base64Service:
    SVG_DATA_URI_SCHEMA = "data:image/svg+xml;base64"
    PNG_DATA_URI_SCHEMA = "data:image/png;base64"
    URI_MAPPING = {"png": PNG_DATA_URI_SCHEMA, "svg": SVG_DATA_URI_SCHEMA}

    def _generate_b64image_bytes(self, bytes_content, return_as_string=False):
        """
        Método auxiliar para codificar como base 64 os bytes da imagem
        """
        base64_image_bytes = base64.b64encode(bytes_content)
        if return_as_string:
            return base64_image_bytes.decode("utf-8")
        return base64_image_bytes

    def generate_b64image_string(self, bytes_content, image_type="png", add_uri=True):
        """
        Método para gerar uma string base64 de imagem a partir de bytes.

        Note:
            É possível gerar SVG e PNG de acordo com o image_type
        """
        uri = self.URI_MAPPING[image_type]
        base64_string = self._generate_b64image_bytes(
            bytes_content, return_as_string=True
        )
        if add_uri:
            return f"{uri},{base64_string}"
        return base64_string

    def generate_b64image_string_from_buffer(
        self, buffer, image_type="png", add_uri=True
    ):
        """
        Método para gerar uma string base64 de imagem a partir de um buffer.

        Note:
            É possível gerar SVG e PNG de acordo com o image_type
        """
        return self.generate_b64image_string(
            buffer.getvalue(), image_type=image_type, add_uri=add_uri
        )
