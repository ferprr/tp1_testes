from django.test import TestCase
from django.urls import reverse
from ..blog.views import Post
from ..blog.forms import PostForm
from django.utils import timezone
from django.contrib.auth.models import User

class BlogViewsTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_post_list_view(self):
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the content of the response

    def test_post_detail_view(self):
        post = Post.objects.create(title='Test Post', content='Test content', author=self.user, published_date=timezone.now())
        response = self.client.get(reverse('postDetail', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the content of the response

    def test_post_new_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postNew'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the content of the response

        data = {
            'title': 'New Post',
            'content': 'New post content',
        }

        response = self.client.post(reverse('postNew'), data)
        self.assertEqual(response.status_code, 302)  # Check for a redirect after submitting the form
        # Add more assertions to verify the new post is created and has the correct data

