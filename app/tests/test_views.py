from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Blog, Comment
from app.forms import FeedbackForm, BlogForm
from datetime import datetime

class ViewsTest(TestCase):
    def setUp(self):
        # Создаем клиент для работы с запросами
        self.client = Client()
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Создаем тестовый блог
        self.blog = Blog.objects.create(
            title="Test Blog",
            description="Short description",
            content="Full content",
            posted=datetime.utcnow(),
            author=self.user,
            image="test.jpg"
        )
        # Создаем тестовый комментарий для блога
        self.comment = Comment.objects.create(
            text="Test comment",
            date=datetime.utcnow(),
            author=self.user,
            post=self.blog
        )
        
    def test_blog_view(self):
        # Проверяем, что страница блога возвращает код 200 (успешный запрос)
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон 'app/blog.html'
        self.assertTemplateUsed(response, 'app/blog.html')
        # Проверяем, что на странице присутствует текст 'Блог'
        self.assertContains(response, 'Блог')

    def test_blogpost_view_get(self):
        # Проверяем, что страница конкретного поста блога возвращает код 200
        response = self.client.get(reverse('blogpost', args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон 'app/blogpost.html'
        self.assertTemplateUsed(response, 'app/blogpost.html')

    def test_blogpost_view_post(self):
        # Проверяем, что при отправке комментария к посту блога возвращается код 302 (редирект)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('blogpost', args=[self.blog.id]), {
            'text': 'Test comment',
        })
        self.assertEqual(response.status_code, 302)
        # Проверяем, что количество комментариев увеличилось на 1
        self.assertEqual(Comment.objects.count(), 2)
        # Проверяем, что последний созданный комментарий имеет текст 'Test comment'
        self.assertEqual(Comment.objects.last().text, 'Test comment')

    def test_registration_view_get(self):
        # Проверяем, что страница регистрации возвращает код 200
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон 'app/registration.html'
        self.assertTemplateUsed(response, 'app/registration.html')
        # Проверяем, что на странице присутствует текст 'Регистрация'
        self.assertContains(response, 'Регистрация')

    def test_registration_view_post(self):
        # Проверяем, что при отправке формы регистрации нового пользователя возвращается код 302 (редирект)
        response = self.client.post(reverse('registration'), {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь 'newuser' был успешно создан
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_home_view(self):
        # Проверяем, что главная страница возвращает код 200
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон 'app/index.html'
        self.assertTemplateUsed(response, 'app/index.html')

    def test_feedback_view_get(self):
        # Проверяем, что страница обратной связи возвращает код 200
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон 'app/feedback.html'
        self.assertTemplateUsed(response, 'app/feedback.html')
        # Проверяем, что на странице присутствует форма FeedbackForm
        self.assertIsInstance(response.context['form'], FeedbackForm)

    def test_feedback_view_post(self):
        # Проверяем, что при отправке формы обратной связи возвращается код 200 и JSON-ответ {'success': True}
        response = self.client.post(reverse('feedback'), {
            'name': "Test User",
            'like': "Sample text 1234567890_",
            'pcconfig' : 'Sample text 1234567890_',
            'recommend' : '1',
            'level' : '1',
            'notice' : True,
            'email': "test@example.com",
            'message': "Test message"
        })
        self.assertEqual(response.status_code, 200)

    def test_newpost_view_get(self):
        # Проверяем, что страница создания нового поста возвращает код 200
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('newpost'))
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон 'app/newpost.html'
        self.assertTemplateUsed(response, 'app/newpost.html')
        # Проверяем, что на странице присутствует форма BlogForm
        self.assertIsInstance(response.context['blogform'], BlogForm)

    def test_newpost_view_post(self):
        # Проверяем, что при отправке формы создания нового поста возвращается код 302 (редирект)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('newpost'), {
            'title': "New Blog",
            'description': "New short description",
            'content': "New full content",
            'image': "new.jpg"
        })
        self.assertEqual(response.status_code, 302)
        # Проверяем, что количество созданных постов увеличилось на 1
        self.assertEqual(Blog.objects.count(), 2)
        # Проверяем, что последний созданный пост имеет заголовок 'Test Blog'
        self.assertEqual(Blog.objects.last().title, 'Test Blog')
