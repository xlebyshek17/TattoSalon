import pytest
import unittest
from unittest import TestCase
from parameterized import parameterized
from TattooSalon.salon.validator import Validator

class TestValidator(TestCase):
    @parameterized.expand([
        ["MT is the best!", True],
        ["A", True],
        ["", False],
        [None, False]
    ])
    def test_check_str_is_not_none_and_not_empty(self, input_string, expected):

        actual = Validator.check_str_is_not_none_and_not_empty(input_string)

        self.assertEqual(actual, expected)

    @parameterized.expand([
        ["Belarus", 3, 20, True],
        ["Belarus", 7, 20, True],
        ["Belarus", 3, 7, True],
        ["Belarus", 8, 20, False],
        ["Belarus", 1, 3, False],
    ])
    def test_check_length(self, input_string, min, max, expected):

        actual = Validator.check_length(input_string, min, max)

        self.assertEqual(actual, expected)

    @parameterized.expand([
        ["kristina_mironenko@mail.ru", True],
        ["kris2334@gmail.com", True],
        ["12356@mail.ru", True],
        ["kristina_mironenko@mail.", False],
        ["kristina_mironenko@mailru", False],
        ["kristina_mironenkomail.ru", False],
        ["kristina_mironenko@.com", False],
    ])
    def test_check_email(self, input_string, expected):

        actual = Validator.check_email(input_string)

        self.assertEqual(actual, expected)


    @parameterized.expand([
        ["80291234567",  True],
        ["80331234567",  True],
        ["80441234567", True],
        ["80251234567", True],
        ["+375291234567",  True],
        ["+375331234567",  True],
        ["+375441234567", True],
        ["+375251234567", True],
        ["qwerty", False],
        ["80881234567", False],
        ["+375881234567", False],
        ["1234567", False],
        ["80291234567qwerty", False],
    ])
    def test_check_phone_number(self, input_string, expected):

        actual = Validator.check_phone_number(input_string)

        self.assertEqual(actual, expected)

    @parameterized.expand([
        ["qwerty", True],
        ["q", True],
        ["12345йцукен", False],
        ["34567", False],
        ["", False],
        [None, False]
    ])
    def test_check_for_Latin_letters(self, input_string, expected):

        actual = Validator.check_for_Latin_letters(input_string)

        self.assertEqual(actual, expected)

    @parameterized.expand([
        ["12345qwerty", True],
        ["qwerty", False],
        ["34567", True],
        ["q", False],
        ["", False],
    ])
    def test_check_on_figures(self, input_string, expected):

        actual = Validator.check_on_figures(input_string)

        self.assertEqual(actual, expected)

    @parameterized.expand([
        ["Кристина123", True],
        ["kristina@gmail.com", True],
        ["+34567567kris", True],
        ["main_admin", True],
        ["super-admin", True],
        ["#Admin123", False],
        ["Костя%1%1%", False],
        ["1*2*3*4", False],
        ["kristina/mironenko", False],
        ["", False],
    ])
    def test_check_login(self, input_string, expected):

        actual = Validator.check_login(input_string)

        self.assertEqual(actual, expected)