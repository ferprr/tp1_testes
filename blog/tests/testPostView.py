from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Post
from django.urls import reverse

class PostViewTest(TestCase):
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
    
    def test_postPublish_view_valid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postPublish', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_postPublish_view_invalid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postPublish', args=[999])) 
        self.assertEqual(response.status_code, 302)

    def test_postRemove_view_valid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postRemove', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)

    def test_postRemove_view_invalid_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postRemove', args=[999])) 
        self.assertEqual(response.status_code, 302)

    def test_postList_view(self):
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)

    def test_postDetail_view_valid_post(self):
        response = self.client.get(reverse('postDetail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_postDetail_view_invalid_post(self):
        response = self.client.get(reverse('postDetail', args=[999]))  
        self.assertEqual(response.status_code, 404)

    def test_postNew_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('postNew'))
        self.assertEqual(response.status_code, 302)
    
    def test_view_url_exists_at_desired_location(self):
      response = self.client.get('/')
      self.assertEqual(response.status_code, 200)
    
    def test_view_url_inexistent(self):
      response = self.client.get('/remove')
      self.assertEqual(response.status_code, 404)

    def test_view_url_accessible_by_name(self):
      response = self.client.get(reverse('postList'))
      self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template_post_list(self):
      response = self.client.get(reverse('postList'))
      self.assertTemplateUsed(response, 'blog/postList.html')

    def test_view_uses_correct_template_post_detail(self):
      response = self.client.get(reverse('postDetail', kwargs={'pk': 1}))
      self.assertTemplateUsed(response, 'blog/postDetail.html')

    def test_create_new_post(self):
        self.client.login(username='testuser', password='password')

        post = Post.objects.all()
        self.assertEqual(1, post.count())

        payload = {
        "title": "Test Post",
        "subtitle": "Test Subtitle",
        "category": [self.category.pk],
        "text": "Test Text",
        }
    
        response = self.client.post(reverse('postNew'), payload)
        response = self.client.post(f"/post/2/publish/")

        self.assertRedirects(response, reverse('postList'))
        self.assertEqual(response.status_code, 302)

        post = Post.objects.all()
        self.assertEqual(2, post.count())

        post = Post.objects.get(title="Test Post")
        self.assertEqual("Test Text", post.text)

    def test_list_and_filter_post(self):
        self.client.login(username='testuser', password='password')
        category2 = Category.objects.create(name="Algorithms")

        payload1 = {
        "title": "Post 1 Algorithmns",
        "subtitle": "Test Subtitle",
        "category": [category2.pk],
        "text": "Test Text",
        }

        payload2 = {
        "title": "Post 2 Algorithmns",
        "subtitle": "Test Subtitle",
        "category": [category2.pk],
        "text": "Test Text",
        }

        self.client.post(f"/post/1/publish/")
        self.client.post(reverse('postNew'), payload1)
        self.client.post(f"/post/2/publish/")
        self.client.post(reverse('postNew'), payload2)
        self.client.post(f"/post/3/publish/")

        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'].count(), 3)

        response = self.client.get(f"/post/category/{category2.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'].count(), 2)

    def test_search_post(self):
        self.client.login(username='testuser', password='password')
        category2 = Category.objects.create(name="Algorithms")

        payload1 = {
        "title": "Post 1 Algorithmns",
        "subtitle": "Test Subtitle",
        "category": [category2.pk],
        "text": "Test Text",
        }

        payload2 = {
        "title": "Post 2 Algorithmns",
        "subtitle": "Test Subtitle",
        "category": [category2.pk],
        "text": "Test Text",
        }

        self.client.post(f"/post/1/publish/")
        self.client.post(reverse('postNew'), payload1)
        self.client.post(f"/post/2/publish/")
        self.client.post(reverse('postNew'), payload2)
        self.client.post(f"/post/3/publish/")

        response = self.client.get(reverse('postList'), {"search":"Algorithmns"})    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'].count(), 2)

    def test_edit_delete_post(self):
        self.client.login(username='testuser', password='password')
        category2 = Category.objects.create(name="Algorithms")

        payload1 = {
        "title": "Post 1 Algorithmns",
        "subtitle": "Test Subtitle",
        "category": [category2.pk],
        "text": "Test Text",
        }

        payload2 = {
        "title": "Post 2 Algorithmns",
        "subtitle": "Test Subtitle",
        "category": [category2.pk],
        "text": "Test Text",
        }

        self.client.post(f"/post/1/publish/")
        self.client.post(reverse('postNew'), payload1)
        self.client.post(f"/post/2/publish/")
        self.client.post(reverse('postNew'), payload2)
        self.client.post(f"/post/3/publish/")

        response = self.client.post("/post/2/edit/",
            {
            "title": "Post 1 Algorithmns",
            "subtitle": "subtitle of an article about algorithms",
            "category": [category2.pk],
            "text": "Test Text",
            })
        self.assertRedirects(response, reverse('postDetail', kwargs={'pk': 2}))

        response = self.client.get("/post/2/")
        self.assertEqual(response.context['post'].subtitle, "subtitle of an article about algorithms")

        self.client.post("/post/2/remove/")
        response = self.client.get(reverse('postList'))
        post = Post.objects.all()
        self.assertEqual(2, post.count())
        self.assertEqual(response.context['posts'].count(), 2)

        response = self.client.get(reverse('postList'), {"search":"Post 1 Algorithmns"})    
        self.assertEqual(response.context['posts'].count(), 0)