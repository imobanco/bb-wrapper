from unittest import TestCase

from bb_wrapper.services.barcode_cobranca import BarcodeCobrancaService


class BarcodeCobrancaTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()
        self.barcodes_to_code_lines = {
            "34191873400000614011092306628112938349558000": "34191092300662811293783495580009187340000061401",  # amil  # noqa: E501
            "23791872200000020043381260065904993200006330": "23793381286006590499132000063308187220000002004",  # nubank  # noqa: E501
            "00196846200000100000000003128557123123000917": "00190000090312855712531230009172684620000010000",  # bb  # noqa: E501
            "00191851500000003100000003128557999999999917": "00190000090312855799299999999172185150000000310",  # bb  # noqa: E501
            "10497848400003240007946015202101347639700002": "10497946031520210134976397000027784840000324000",  # caixa  # noqa: E501
            "00192849800000003000000003128557999999999417": "00190000090312855799299999994173284980000000300",  # bb  # noqa: E501
            "75691872100000215251419401015749004599691001": "75691419430101574900345996910019187210000021525",  # bancoob  # noqa: E501
        }

    def test_calculate_barcode_dv(self):
        numbers_to_dvs = {"1": "9", "2": "7", "12": "4", "21": "3", "1235": "1"}

        for number, dv in numbers_to_dvs.items():
            with self.subTest(number):
                calculated_dv = BarcodeCobrancaService().calculate_barcode_dv(number)

                self.assertEqual(dv, calculated_dv)

    def test_calculate_code_line_dv(self):
        numbers_to_dvs = {"1": "8", "2": "6", "12": "5", "21": "6", "1235": "1"}

        for number, dv in numbers_to_dvs.items():
            with self.subTest(number):
                calculated_dv = BarcodeCobrancaService().calculate_code_line_dv(number)

                self.assertEqual(dv, calculated_dv)

    def test_validate_barcode_1(self):
        for barcode in self.barcodes_to_code_lines.keys():
            with self.subTest(barcode):
                self.assertTrue(BarcodeCobrancaService().validate_barcode(barcode))

    def test_validate_code_line(self):
        for code_line in self.barcodes_to_code_lines.values():
            with self.subTest(code_line):
                self.assertTrue(BarcodeCobrancaService().validate_code_line(code_line))

    def test_barcode_to_code_line(self):
        for barcode, code_line in self.barcodes_to_code_lines.items():
            with self.subTest(barcode):
                result = BarcodeCobrancaService().barcode_to_code_line(barcode)

                self.assertEqual(result, code_line)

    def test_code_line_to_barcode(self):
        for barcode, code_line in self.barcodes_to_code_lines.items():
            with self.subTest(code_line):
                result = BarcodeCobrancaService().code_line_to_barcode(code_line)

                self.assertEqual(result, barcode)
