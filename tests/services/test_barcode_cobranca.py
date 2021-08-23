from unittest import TestCase

from bb_wrapper.services.barcode_cobranca import BarcodeCobranca


class BarcodeCobrancaTestCase(TestCase):
    maxDiff = None

    def test_validate_barcode_1(self):
        valid_barcodes = [
            "34191873400000614011092306628112938349558000",  # amil
            "23791872200000020043381260065904993200006330",  # nubank
            "00196846200000100000000003128557123123000917",  # bb
        ]

        for barcode in valid_barcodes:
            with self.subTest(barcode):
                self.assertTrue(
                    BarcodeCobranca().validate_barcode(barcode)
                )
