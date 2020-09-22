from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from .models import Post
 
 
class BlogTests(TestCase):
 
    # Настройка тестов
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
 
        self.post = Post.objects.create(
            name='Some Title here',
            text='Nice text content',
            author=self.user,
            is_published=True,
        )
    # Корректный возврат строки
    def test_string_representation(self):
        post = Post(name='A sample title')
        self.assertEqual(str(post), post.name)
 
    # Проверка содержимого
    def test_post_content(self):
        self.assertEqual(f'{self.post.name}', 'Some Title here')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.text}', 'Nice text content')
 
    # Проверка списка постов, ответ и содержимое
    def test_post_list_view(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice text content')
        self.assertTemplateUsed(response, 'post/post_list.html')
 
    # Проверка одного поста, ответ и содержимое
    def test_post_detail_view(self):
        response = self.client.get('/post/2/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Some Title here')
        self.assertTemplateUsed(response, 'post/post_detail.html')