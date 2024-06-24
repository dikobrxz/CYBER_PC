from django.test import TestCase, Client  # Импорт базовых классов тестирования и клиента для запросов
from django.urls import reverse  # Для генерации URL из имен URL-адресов
from django.contrib.auth.models import User  # Модель пользователя Django
from app.models import Blog, Comment  # Импорт моделей данных из приложения
from app.forms import FeedbackForm, CommentForm, BootstrapAuthenticationForm, BlogForm  # Импорт форм из приложения
from datetime import datetime  # Импорт модуля для работы с датами и временем

class FeedbackFormTest(TestCase):
    """
    Тесты формы обратной связи.
    """
    
    def test_feedback_form_valid(self):
        """
        Проверка валидации формы с корректными данными.
        """
        form = FeedbackForm(data={
            'name': "Test User",
            'like': "Sample text 1234567890_",
            'pcconfig' : 'Sample text 1234567890_',
            'recommend' : '1',
            'level' : '1',
            'notice' : True,
            'email': "test@example.com",
            'message': "Test message"
        })
        self.assertTrue(form.is_valid())  # Утверждение, что форма проходит валидацию

    def test_feedback_form_invalid(self):
        """
        Проверка валидации формы с некорректными данными.
        """
        form = FeedbackForm(data={})
        self.assertFalse(form.is_valid())  # Утверждение, что форма не проходит валидацию
        self.assertEqual(len(form.errors), 7)  # Проверка, что все поля заполнены

class CommentFormTest(TestCase):
    """
    Тесты формы комментария.
    """
    
    def setUp(self):
        """
        Подготовка данных для теста формы комментария.
        """
        self.user = User.objects.create(username="commentuser", password="12345")  # Создание пользователя
        self.blog = Blog.objects.create(
            title="Comment Blog",
            description="Short description",
            content="Full content",
            posted=datetime.now(),
            author=self.user,
            image="comment.jpg"
        )  # Создание блога для пользователя

    def test_comment_form_valid(self):
        """
        Проверка валидации формы комментария с корректными данными.
        """
        form = CommentForm(data={'text': "Test comment"})
        self.assertTrue(form.is_valid())  # Утверждение, что форма проходит валидацию

    def test_comment_form_invalid(self):
        """
        Проверка валидации формы комментария с некорректными данными.
        """
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())  # Утверждение, что форма не проходит валидацию
        self.assertEqual(len(form.errors), 1)  # Проверка, что есть одна ошибка (поле `text` обязательно)

class BootstrapAuthenticationFormTest(TestCase):
    """
    Тесты формы аутентификации Bootstrap.
    """
    
    def test_authentication_form_valid(self):
        """
        Проверка валидации формы аутентификации с корректными данными.
        """
        form = BootstrapAuthenticationForm(data={
            'username': "Testing_User",
            'password': "G6Hdj+zfh!"
        })
        self.assertFalse(form.is_valid())  # Утверждение, что форма не проходит валидацию

    def test_authentication_form_invalid(self):
        """
        Проверка валидации формы аутентификации с некорректными данными.
        """
        form = BootstrapAuthenticationForm(data={})
        self.assertFalse(form.is_valid())  # Утверждение, что форма не проходит валидацию
        self.assertEqual(len(form.errors), 2)  # Проверка, что есть две ошибки (поля `username` и `password` обязательны)

class BlogFormTest(TestCase):
    """
    Тесты формы блога.
    """
    
    def test_blog_form_valid(self):
        """
        Проверка валидации формы блога с корректными данными.
        """
        form = BlogForm(data={
            'title': "Test Blog",
            'description': "Short description",
            'content': "Full content",
            'image': "test.jpg"
        })
        self.assertTrue(form.is_valid())  # Утверждение, что форма проходит валидацию

    def test_blog_form_invalid(self):
        """
        Проверка валидации формы блога с некорректными данными.
        """
        form = BlogForm(data={})
        self.assertFalse(form.is_valid())  # Утверждение, что форма не проходит валидацию
        self.assertEqual(len(form.errors), 3)  # Проверка, что есть три ошибки (поля `title`, `description` и `content` обязательны)
