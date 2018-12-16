from django.shortcuts import reverse
from django.urls import resolve
from django.test import TestCase
from ..forms import RegistrationForm
from ..views import register

class RegisterFormTest(TestCase):
    def test_form_has_fields(self):
        form = RegistrationForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_register_url_resolves_register_view(self):
        view = resolve('/accounts/register/')
        self.assertEquals(view.func, register)