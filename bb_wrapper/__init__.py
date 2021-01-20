from ._version import get_versions
from .services import (  # noqa
    generate_qrcode_b64image,
    generate_barcode_b64image,
    parse_unicode_to_alphanumeric,
)
from .wrapper import CobrancasBBWrapper  # noqa

__version__ = get_versions()["version"]
del get_versions
