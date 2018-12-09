from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import resolve, reverse
from django.test import TestCase, Client


class ChangePasswordTests(TestCase):
    def setUp(self):
        username = 'enco'
        password = 'abecedario'
        User.objects.create_user(username=username, email='admin@enco.com', password=password)
        self.client.login(username=username, password=password)
        url = reverse('accounts:password_change')
        self.response = self.client.get(url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    def test_register_url_resolves_register_view(self):
        view = resolve('/accounts/password_change/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)
        
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, old_password, password1, password2
        '''
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)

class SuccessfullChangePasswordTests(TestCase):
    pass
    