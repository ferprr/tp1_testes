from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Post
from .forms import LoginForm, RegistrationForm, PostForm
from django.urls import reverse

class PostModelTest(TestCase):
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

    def test_category_creation(self):
        category = Category.objects.get(name="Technology")
        self.assertEqual(category.name, "Technology")

    def test_post_creation(self):
        post = Post.objects.get(title="Post 1")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, "Post 1")
        self.assertEqual(post.subtitle, "subtitle")
        self.assertEqual(post.text, "content")

    def test_add_category_to_post(self):
        post = Post.objects.get(title="Post 1")
        self.assertEqual(post.category.count(), 1)
        self.assertEqual(post.category.first(), self.category)

    def test_publish_post(self):
        post = Post.objects.get(title="Post 1")
        post.publish()
        self.assertIsNotNone(post.published_date)

    def test_filter_posts_by_category(self):
        posts_in_technology_category = Post.objects.filter(category__name="Technology")
        self.assertEqual(posts_in_technology_category.count(), 1)

    def test_filter_posts_by_author(self):
        user_posts = Post.objects.filter(author=self.user)
        self.assertEqual(user_posts.count(), 1)

    def test_update_post(self):
        post = Post.objects.get(title="Post 1")
        post.title = "Post atualizado"
        post.save()
        updated_post = Post.objects.get(pk=post.pk)
        self.assertEqual(updated_post.title, "Post atualizado")

    def test_delete_category(self):
        category = Category.objects.get(name="Technology")
        category.delete()
        self.assertFalse(Category.objects.filter(name="Technology").exists())

    def test_delete_post(self):
        post = Post.objects.get(title="Post 1")
        post.delete()
        self.assertFalse(Post.objects.filter(title="Post 1").exists())

    def test_check_if_post_is_published(self):
        post = Post.objects.get(title="Post 1")
        self.assertFalse(post.published_date)

    def test_check_if_post_is_published_after_publishing(self):
        post = Post.objects.get(title="Post 1")
        post.publish()
        self.assertTrue(post.published_date)

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

    def test_postList_view(self):
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)

    def test_postDetail_view_valid_post(self):
        response = self.client.get(reverse('postDetail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_postDetail_view_invalid_post(self):
        response = self.client.get(reverse('postDetail', args=[999]))  # Assuming 999 is an invalid post ID
        self.assertEqual(response.status_code, 404)

    def test_postNew_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postNew'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('postList'))
    
    def test_postPublish_view_valid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postPublish', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_postPublish_view_invalid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postPublish', args=[999]))  # Assuming 999 is an invalid post ID
        self.assertEqual(response.status_code, 302)

    def test_postRemove_view_valid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postRemove', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_postRemove_view_invalid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postRemove', args=[999]))  # Assuming 999 is an invalid post ID
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('postList'))

    def test_login_form_valid(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'Test123password'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={'username': 'testuser'})
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        form_data = {
            'title': 'Test Title',
            'subtitle': 'Test Subtitle',
            'category': 'Test Category',
            'text': 'Test Text',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_form_invalid(self):
        form_data = {
            'title': '',
            'subtitle': 'Test Subtitle',
            'category': 'Test Category',
            'text': 'Test Text',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
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

    def test_registration_form_existing_email(self):
        User.objects.create_user(username='testuser', email='existing@example.com', password='testpassword')
        form_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_post_form_with_empty_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_form_with_empty_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

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
      self.assertContains(response.title, 'Título de Teste')
    
    def testCreatedAtLabel(self):
      createdAtLabel = self.post._meta.get_field('created_date').verbose_name
      self.assertEquals(createdAtLabel, 'created date')

    def testPublishedDate(self):
      publishedDateLabel = self.post._meta.get_field('published_date').verbose_name
      self.assertEquals(publishedDateLabel, 'published date')