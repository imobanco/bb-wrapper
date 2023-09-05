from bb_wrapper.services.barcode_cobranca import BarcodeCobrancaService
from ..utils import BarcodeAndCodeLineTestCase
from datetime import datetime
from freezegun import freeze_time


class BarcodeCobrancaTestCase(BarcodeAndCodeLineTestCase):
    def test_calculate_barcode_dv(self):
        numbers_to_dvs = {
            "1": "9",
            "4": "3",
            "7": "8",
            "14": "1",
            "25": "6",
            "123456": "3",
        }

        for number, dv in numbers_to_dvs.items():
            with self.subTest(number):
                calculated_dv = BarcodeCobrancaService().calculate_barcode_dv(number)

                self.assertEqual(dv, calculated_dv)

    def test_calculate_code_line_dv(self):
        numbers_to_dvs = {
            "1": "8",
            "4": "2",
            "7": "5",
            "14": "1",
            "25": "7",
            "123456": "6",
        }

        for number, dv in numbers_to_dvs.items():
            with self.subTest(number):
                calculated_dv = BarcodeCobrancaService().calculate_code_line_dv(number)

                self.assertEqual(dv, calculated_dv)

    def test_validate_barcode_1(self):
        for barcode in self.cobrancas_barcodes_to_code_lines.keys():
            with self.subTest(barcode):
                self.assertTrue(BarcodeCobrancaService().validate_barcode(barcode))

    def test_validate_code_line(self):
        for code_line in self.cobrancas_barcodes_to_code_lines.values():
            with self.subTest(code_line):
                self.assertTrue(BarcodeCobrancaService().validate_code_line(code_line))

    def test_barcode_to_code_line(self):
        for barcode, code_line in self.cobrancas_barcodes_to_code_lines.items():
            with self.subTest(barcode):
                result = BarcodeCobrancaService().barcode_to_code_line(barcode)

                self.assertEqual(result, code_line)

    def test_code_line_to_barcode(self):
        for barcode, code_line in self.cobrancas_barcodes_to_code_lines.items():
            with self.subTest(code_line):
                result = BarcodeCobrancaService().code_line_to_barcode(code_line)

                self.assertEqual(result, barcode)

    def test_calculate_due_date_1(self):
        """
        Dado:
            - Um Fator de Vencimento fv = 1009
        Quando:
            - É dia 12/02/2025
            - BarcodeCobrancaService().calculate_due_date(fv)
        Então:
            - Deve ser retonado 03/03/2025
        """

        fv = "1009"

        date = datetime.strptime("2025-02-12", "%Y-%m-%d")

        with freeze_time(date):
            result = BarcodeCobrancaService().calculate_due_date(fv)

        self.assertEqual(str(result), "2025-03-03")

    def test_calculate_due_date_2(self):
        """
        Dado:
            - Um Fator de Vencimento fv = 1000
        Quando:
            - É dia 22/02/2025
            - BarcodeCobrancaService().calculate_due_date(fv)
        Então:
            - Deve ser retonado 22/02/2025
        """
        fv = "1000"

        date = datetime.strptime("2025-02-22", "%Y-%m-%d")

        with freeze_time(date):
            result = BarcodeCobrancaService().calculate_due_date(fv)

        self.assertEqual(str(result), "2025-02-22 00:00:00")

    def test_calculate_due_date_3(self):
        """
        Dado:
            - Um Fator de Vencimento fv = 1000
        Quando:
            - É dia 19/02/2025
            - BarcodeCobrancaService().calculate_due_date(fv)
        Então:
            - Deve ser retonado 22/02/2025
        """
        fv = "1000"

        date = datetime.strptime("2025-02-19", "%Y-%m-%d")

        with freeze_time(date):
            result = BarcodeCobrancaService().calculate_due_date(fv)

        self.assertEqual(str(result), "2025-02-22 00:00:00")

    def test_calculate_due_date_4(self):
        """
        Dado:
            - Um Fator de Vencimento fv = 9999
        Quando:
            - É dia 22/02/2025
            - BarcodeCobrancaService().calculate_due_date(fv)
        Então:
            - Deve ser retonado 21/02/2025
        """

        fv = "9999"

        date = datetime.strptime("2025-02-22", "%Y-%m-%d")

        with freeze_time(date):
            result = BarcodeCobrancaService().calculate_due_date(fv)

        self.assertEqual(str(result), "2025-02-21 00:00:00")
