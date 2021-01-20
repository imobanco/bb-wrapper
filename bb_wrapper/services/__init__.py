from .b64 import Base64Service  # noqa
from .unicode import UnicodeService
from .qrcode import QRCodeService
from .barcode import BarCodeService
from .mod import ModService  # noqa


parse_unicode_to_alphanumeric = UnicodeService().parse_unicode_to_alphanumeric
generate_qrcode_b64image = QRCodeService().generate_qrcode_b64image
generate_barcode_b64image = BarCodeService().generate_barcode_b64image
