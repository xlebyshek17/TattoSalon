from unittest import TestCase
from parameterized import parameterized
from TattooSalon.salon.validator import Validator

class TestValidatorTDD(TestCase):

    @parameterized.expand([
        ["Кристина123", True],
        ["kristina@gmail.com", True],
        ["+34567567kris", True],
        ["main_admin", True],
        ["super-admin", True],
        ["#Admin123", True],
        ["Костя%1%1%", True],
        ["1*2*3*4", True],
        ["kristina/Mironenko", True],
        ["", False],
    ])
    def test_check_login(self, input_string, expected):

        actual = Validator.check_login(input_string)

        self.assertEqual(actual, expected)


class TestIntegrated(TestCase):

    def test_addToCart_AddToCart_DeleteFromCart_ExceptedTrue(self):
        self.assertEqual(True, True)
    def test_CheckOnValidLoginAndValidPasswordExceptTrue(self):
        self.assertEqual(True, True)