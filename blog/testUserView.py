from django.test import TestCase
import unittest
from django.contrib.auth.models import User
from .models import Category, Post
from django.urls import reverse

class UserViewTest(unittest.TestCase):
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

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_valid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'Test123password'})
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'invalidpassword'})
        self.assertContains(response, 'Your username and password didn\'t match. Please try again.')

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_valid_registration(self):
        response = self.client.post(reverse('register'), {'username': 'newuser', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_invalid_registration(self):
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password1': 'testpassword', 'password2': 'testpassword'})
        self.assertContains(response, 'A user with that username already exists.')

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('postList'))

    def test_create_user(self):
        user = User.objects.all()
        self.assertEqual(1, user.count())

        payload = {
            'username': 'user1',
            'email': 'user1@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
    
        response = self.client.post(reverse('register'), payload)

        user = User.objects.all()
        self.assertEqual(2, user.count())
        self.assertRedirects(response, reverse('postList'))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('postList'))
        self.assertEqual(response.context['user']._wrapped.username, 'user1')

        response = self.client.post('/accounts/login/', {'username':'user1', 'password': 'testpassword123'})
        self.assertRedirects(response, reverse('postList'))
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()