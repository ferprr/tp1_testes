from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Post
from ..forms import LoginForm, PostForm
from django.urls import reverse
    
class PostFormTest(TestCase):
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

    def test_post_form_post_valid(self):
        form_data = {
            'title': 'Test Title',
            'subtitle': 'Test Subtitle',
            'category': [self.category.pk],
            'text': 'Test Text',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_post_empty_title(self):
        form_data = {
            'title': '',
            'subtitle': 'Test Subtitle',
            'category': [self.category.pk],
            'text': 'Test Text',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_form_post_empty_subtitle(self):
        form_data = {
            'title': 'Post Test',
            'subtitle': '',
            'category': [self.category.pk],
            'text': 'Test Text',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_form_post_empty_text(self):
        form_data = {
            'title': 'Post Test',
            'subtitle': 'Subtitle Test',
            'category': 'Test Category',
            'text': '',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_form_with_empty_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_form_with_empty_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_view_uses_correct_template_register(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'registration/register.html')