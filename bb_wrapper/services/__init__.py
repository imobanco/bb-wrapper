from .b64 import Base64Service  # noqa: F401
from .unicode import UnicodeService
from .qrcode import QRCodeService
from .barcode import BarcodeService
from .mod import ModService  # noqa: F401
from .pixcode import PixCodeService  # noqa: F401


parse_unicode_to_alphanumeric = UnicodeService().parse_unicode_to_alphanumeric
generate_qrcode_b64image = QRCodeService().generate_qrcode_b64image
generate_barcode_b64image = BarcodeService().generate_barcode_b64image
