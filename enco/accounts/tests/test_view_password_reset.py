from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import render, redirect, reverse
from django.urls import resolve
from django.test import TestCase

class ResetPasswordTests(TestCase):
    def setUp(self):
        username = 'enco'
        email = 'admin@enco.com'
        password = 'abecedario'
        User.objects.create_user(username=username, email=email, password=password)
        self.client.login(username=username, password=password)
        url = reverse('accounts:password_reset')
        self.response = self.client.get(url)

    def test_user_exist(self):
        self.assertEqual(1, len(User.objects.all()))

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_form_inputs(self):
        """The view must contain two inputs: csrf and email"""
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        username = 'enco'
        email = 'admin@enco.com'
        password = 'abecedario'
        User.objects.create_user(username=username, email=email, password=password)
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_redirection(self):
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@mail.com'})

    def test_redirection(self):
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)
    
    def test_no_reset_mail_sent(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/accounts/password_reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        # TODO: verify all the tests!
        username = 'enco'
        email = 'admin@enco.com'
        password = 'abecedario'
        user = User.objects.create_user(username=username, email=email, password=password)

        self.uid = (force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url)#, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_view_function(self):
        view = resolve('/accounts/password_reset/confirm/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    def est_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def est_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def est_form_inputs(self):
        '''
        The view must contain two inputs: csrf and two password fields
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        username = 'enco'
        email = 'admin@enco.com'
        password = 'abecedario'
        user = User.objects.create_user(username=username, email=email, password=password)

        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        '''
        invalidate the token by changing the password
        '''
        user.set_password('abcdef123')
        user.save()

        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('accounts:password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))
