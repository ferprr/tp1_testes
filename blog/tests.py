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

    def test_login_form_valid(self):
        form = LoginForm(data = {'username': 'testUser', 'password': 'password'})
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form = LoginForm(data={'username': 'testuser'})
        self.assertFalse(form.is_valid())

    def test_post_form_valid(self):
        form_data = {
            'title': 'Test Title',
            'subtitle': 'Test Subtitle',
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
            'username': 'user789',
            'email': 'test@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123',
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

    def test_post_form_with_empty_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())

    def test_login_form_with_empty_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_view_url_exists_at_desired_location(self):
      response = self.client.get('/')
      self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
      response = self.client.get(reverse('postList'))
      self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_post_list(self):
      response = self.client.get(reverse('postList'))
      self.assertTemplateUsed(response, 'blog/postList.html')
     
    def test_view_uses_correct_template_post_publish(self):
      response = self.client.get(reverse('postPublish'))
      self.assertTemplateUsed(response, 'blog/postList.html')

    def test_view_uses_correct_template_post_remove(self):
      response = self.client.get(reverse('postRemove'))
      self.assertTemplateUsed(response, 'blog/postList.html')

    def test_view_uses_correct_template_register(self):
      response = self.client.get(reverse('register'))
      self.assertTemplateUsed(response, 'registration/register.html')
    
    def test_max_length_title(self):
        max_length = self.post._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_author_label(self):
        author_label = self.post._meta.get_field('author').verbose_name
        self.assertEquals(author_label, 'author')

    def test_title_label(self):
        title_label = self.post._meta.get_field('title').verbose_name
        self.assertEquals(title_label, 'title')

    def test_subtitle_label(self):
        subtitle_label = self.post._meta.get_field('subtitle').verbose_name
        self.assertEquals(subtitle_label, 'subtitle')

    def test_text_label(self):
        text_label = self.post._meta.get_field('text').verbose_name
        self.assertEquals(text_label, 'text')
    
    def test_created_at_label(self):
        created_at_label = self.post._meta.get_field('created_date').verbose_name
        self.assertEquals(created_at_label, 'created date')

    def test_published_date(self):
        published_date_label = self.post._meta.get_field('published_date').verbose_name
        self.assertEquals(published_date_label, 'published date')