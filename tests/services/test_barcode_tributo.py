from bb_wrapper.services.barcode_tributo import BarcodeTributoService
from ..utils import BarcodeAndCodeLineTestCase


class BarcodeTributoTestCase(BarcodeAndCodeLineTestCase):
    def test_calculate_barcode_dv_10(self):
        numbers_to_dvs = {
            "1": "8",
            "4": "2",
            "7": "5",
            "14": "1",
            "25": "7",
            "123456": "2",
        }

        for number, dv in numbers_to_dvs.items():
            with self.subTest(number):
                calculated_dv = BarcodeTributoService()._calculate_dv_10(number)

                self.assertEqual(dv, calculated_dv)

    def test_calculate_barcode_dv_11(self):
        numbers_to_dvs = {
            "1": "9",
            "4": "3",
            "7": "8",
            "14": "0",
            "25": "6",
            "123456": "0",
        }

        for number, dv in numbers_to_dvs.items():
            with self.subTest(number):
                calculated_dv = BarcodeTributoService()._calculate_dv_11(number)

                self.assertEqual(dv, calculated_dv)

    def test_validate_barcode_1(self):
        for barcode in self.tributos_barcodes_to_code_lines.keys():
            with self.subTest(barcode):
                self.assertTrue(BarcodeTributoService().validate_barcode(barcode))

    #
    # def test_validate_code_line(self):
    #     for code_line in self.cobrancas_barcodes_to_code_lines.values():
    #         with self.subTest(code_line):
    #             self.assertTrue(BarcodeCobrancaService().validate_code_line(code_line))
    #
    def test_barcode_to_code_line(self):
        for barcode, code_line in self.tributos_barcodes_to_code_lines.items():
            with self.subTest(barcode):
                result = BarcodeTributoService().barcode_to_code_line(barcode)

                self.assertEqual(result, code_line)

    def test_code_line_to_barcode(self):
        for barcode, code_line in self.tributos_barcodes_to_code_lines.items():
            with self.subTest(code_line):
                result = BarcodeTributoService().code_line_to_barcode(code_line)

                self.assertEqual(result, barcode)
