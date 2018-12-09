from django.test import TestCase
from ..forms import RegistrationForm

class RegisterFormTest(TestCase):
    def test_form_has_fields(self):
        form = RegistrationForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)