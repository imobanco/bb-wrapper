from ._version import get_versions
from .services import generate_qrcode_b64image, generate_barcode_b64image, parse_unicode_to_alphanumeric

__version__ = get_versions()["version"]
del get_versions
