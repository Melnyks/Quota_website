from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

class UserLoginTestCase(TestCase):
    
    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        response = self.client.post(reverse('login_user'), {
            'username': self.username,
            'password': self.password
        })
        
        self.assertRedirects(response, '/subject_list')

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_fail(self):
        response = self.client.post(reverse('login_user'), {
            'username': self.username,
            'password': 'wrongpassword'
        })

        self.assertRedirects(response, reverse('login_user'))

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "There was an errror logging in, Try again")

class UserRegisterTestCase(TestCase):

    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })

        self.assertRedirects(response, '/users/login_user')

        self.assertTrue(User.objects.filter(username='newuser').exists())

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Registration successful! You can now login.")

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'password1': 'newpassword',
            'password2': 'differentpassword',
        })

        self.assertRedirects(response, reverse('register'))

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Passwords do not match!")



    def test_register_existing_username(self):
        response = self.client.post(reverse('register'), {
            'username': self.username,  
            'password1': 'newpassword',
            'password2': 'newpassword',
        })

        self.assertRedirects(response, reverse('register'))

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "Username already exists!")