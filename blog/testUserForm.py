from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from .models import Category, Post
from .forms import LoginForm, RegistrationForm

class UserFormTest(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(name="Technology")
        self.post = Post.objects.create(
            author=self.user,
            title="Post 1",
            subtitle="subtitle",
            text="content",
        )
        self.post.category.add(self.category)
    
    def test_login_form_valid(self):
        form = LoginForm(data = {'username': 'testuser', 'password': 'password'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={'username': 'testuser'})
        self.assertFalse(form.is_valid())

    def test_registration_form_user_valid(self):
        form_data = {
            'username': 'user789',
            'email': 'test@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_user_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_form_user_empty_username(self):
        form_data = {
            'username': '',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_form_user_empty_email(self):
        form_data = {
            'username': 'testuser',
            'email': '',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_form_user_empty_password1(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '',
            'password2': 'mismatchedpassword',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_registration_form_user_empty_password2(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'mismatchedpassword',
            'password2': '',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_form_existing_username(self):
        User.objects.create_user(username='existinguser', email='existing@example.com', password='testpassword')
        form_data = {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

if __name__ == '__main__':
    unittest.main()