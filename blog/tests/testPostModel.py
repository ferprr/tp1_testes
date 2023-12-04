from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Post

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