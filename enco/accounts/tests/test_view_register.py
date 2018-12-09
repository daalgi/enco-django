from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from ..views import register
from ..forms import RegistrationForm

class RegisterTests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_register_url_resolves_register_view(self):
        view = resolve('/accounts/register/')
        self.assertEquals(view.func, register)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegistrationForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulRegisterTests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        data = {'username': 'pierre', 'email':'ab@cd.com', 'password1':'abecedario', 'password2':'abecedario'}
        self.response = self.client.post(url, data)
        self.redirect_url = reverse('home:home')

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())
         

    def test_redirection(self):
        self.assertRedirects(self.response, self.redirect_url)

    def test_user_authentication(self):
        response = self.client.get(self.redirect_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidRegisterTests(TestCase):
    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
