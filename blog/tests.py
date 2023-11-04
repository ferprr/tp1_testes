from django.test import TestCase
from django.contrib.auth.models import User  
from .models import Category, Post

class BlogViewDetailTest(TestCase):
  def setUp(self):
    user = User.objects.create_user(username='testuser', password='test123')
    category = Category.objects.create(name='Categoria de Teste')
    self.post = Post.objects.create(author = user, title='Título de Teste', subtitle='Subtítulo de Teste',
                        text='Texto de Teste')
    self.post.category.add(category)

  def testViewUrlExistsAtDesiredLocation(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)

  def testViewUrlAccessibleByName(self):
    response = self.client.get(reverse('postList'))
    self.assertEqual(response.status_code, 200)

  def testViewUsesCorrectTemplate(self):
    response = self.client.get(reverse('postList'))
    self.assertTemplateUsed(response, 'blog/postList.html')

  def testViewDisplaysPosts(self):
    response = self.client.get(reverse('postList'))
    self.assertContains(response, 'Título de Teste')