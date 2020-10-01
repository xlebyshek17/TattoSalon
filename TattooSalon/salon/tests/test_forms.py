from django.test import TestCase
from django.forms import ValidationError
from django.contrib.auth.models import User
from shop.forms import LoginForm, RegistrationForm


class TestForms(TestCase):

    def setUp(self):
        User.objects.create_user('ira', email='ira@mail.ru', password='12345qwerty')


    def test_login_form_valid_data_expected_True(self):
        form = LoginForm(data = {
            'username': 'ira',
            'password': '12345qwerty'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_username_expected_False_and_ValidationError(self):
        form = LoginForm(data = {
            'username': 'iraj',
            'password': '12345qwerty'
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError) as e:form.clean()
        self.assertEquals(e.exception.message, 'Пользователь с данным логином не зарегистрирован в системе!')

    def test_login_form_invalid_password_expected_False_and_ValidationError(self):
        form = LoginForm(data = {
            'username': 'ira',
            'password': '123456789qwerty'
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError) as e:form.clean()
        self.assertEquals(e.exception.code, 'false_password')

    def test_registration_form_valid_data_expected_True(self):
        form = RegistrationForm(data={
            'username':'irina',
            'password':'123',
            'password_check':'123'
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_length_login_expected_False_and_ValidationError(self):
        form = RegistrationForm(data={
            'username':'ir',
            'password':'123',
            'password_check':'123'
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError) as e:form.clean()
        self.assertEquals(e.exception.message, 'Неверная длина логина!')

    def test_registration_form_invalid_login_expected_False_and_ValidationError(self):
        form = RegistrationForm(data={
            'username':'ira',
            'password':'123',
            'password_check':'123'
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError) as e:form.clean()
        self.assertEquals(e.exception.message, 'Пользователь с данным логином уже зарегистрирован в системе!')

    def test_registration_form_invalid_passwords_length_expected_False_and_ValidationError(self):
        form = RegistrationForm(data={
            'username':'irina',
            'password':'12',
            'password_check':'12'
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError) as e:form.clean()
        self.assertEquals(e.exception.message, 'Неверная длина пароля!')

    def test_registration_form_invalid_password_check_expected_False_and_ValidationError(self):
        form = RegistrationForm(data={
            'username':'irina',
            'password':'123',
            'password_check':'124'
        })
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError) as e:form.clean()
        self.assertEquals(e.exception.message, 'Ваши пароли не совпадают! Попробуйте снова.')
