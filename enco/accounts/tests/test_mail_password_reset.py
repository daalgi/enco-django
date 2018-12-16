from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        username = 'enco'
        email = 'admin@enco.com'
        password = 'abecedario'
        User.objects.create_user(username=username, email=email, password=password)
        args = {'email': email}
        self.response = self.client.post(reverse('accounts:password_reset'), args)
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual(self.email.subject, '[ENCO] Reset your password')

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('enco', self.email.body)
        self.assertIn('admin@enco.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['admin@enco.com',], self.email.to)