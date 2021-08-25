from unittest import TestCase

from bb_wrapper.services import ModService


class ModServiceTestCase(TestCase):
    def test_mod_10(self):
        """"""
        number_to_mod = {
            "1": "8",
            "2": "6",
            "32": "3",
            "21": "6",
            "46": "3",
            "79": "4",
            "51234": "3",
        }

        for number, mod in number_to_mod.items():
            with self.subTest(number):
                result = ModService().mod_10(number)

                self.assertEqual(result, mod)

    def test_mod_11(self):
        """"""
        number_to_mod = {
            "1": "9",
            "2": "7",
            "21": "3",
            "32": "9",
            "46": "9",
            "79": "5",
            "51234": "6",
        }
        for number, mod in number_to_mod.items():
            with self.subTest(number):
                result = ModService().mod_11(number)

                self.assertEqual(result, mod)
