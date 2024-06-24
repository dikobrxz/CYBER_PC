from email import message
from django.test import TestCase, Client  # Импорт базовых классов тестирования и клиента для запросов
from django.urls import reverse  # Для генерации URL из имен URL-адресов
from django.contrib.auth.models import User  # Модель пользователя Django
from app.models import Blog, Comment  # Импорт моделей данных из приложения
from app.forms import FeedbackForm, CommentForm, BootstrapAuthenticationForm, BlogForm  # Импорт форм из приложения
from datetime import datetime  # Импорт модуля для работы с датами и временем

class BlogModelTest(TestCase):
    """
    Тесты модели Blog.
    """
    
    def setUp(self):
        """
        Подготовка данных для теста модели Blog.
        """
        self.user = User.objects.create(username="Testing_User", password="12345nfo23i@#f3")  # Создание пользователя
        self.blog = Blog.objects.create(
            title="Тестовый заголовок",
            description="краткий текст поста",
            content="тут текст всего поста, текст текст тут текст",
            posted=datetime.now(),
            author=self.user,
            image="test.jpg"
        )  # Создание объекта Blog для тестирования

    def test_blog_meta(self):
        """
        Проверка метаданных модели Blog.
        """
        self.assertEqual(self.blog._meta.db_table, "Posts")  # Проверка имени таблицы в базе данных
        self.assertEqual(self.blog._meta.verbose_name, "статья блога")  # Проверка единственного числа имени модели
        self.assertEqual(self.blog._meta.verbose_name_plural, "статьи блога")  # Проверка множественного числа имени модели

class CommentModelTest(TestCase):
    """
    Тесты модели Comment.
    """
    
    def setUp(self):
        """
        Подготовка данных для теста модели Comment.
        """
        self.user = User.objects.create(username="commentuser", password="12345")  # Создание пользователя
        self.blog = Blog.objects.create(
            title="Комментарий для статьи блога",
            description="Сокращенный текст",
            content="Весь текст комментария тут",
            posted=datetime.now(),
            author=self.user,
            image="comment.jpg"
        )  # Создание объекта Blog для пользователя
        self.comment = Comment.objects.create(
            text="Test comment",
            date=datetime.now(),
            author=self.user,
            post=self.blog
        )  # Создание объекта Comment для тестирования

    def test_comment_creation(self):
        """
        Проверка создания объекта Comment.
        """
        self.assertTrue(isinstance(self.comment, Comment))  # Утверждение, что объект является экземпляром модели Comment
        self.assertEqual(self.comment.__str__(), f'Комментарий {self.comment.id} {self.comment.author} к {self.comment.post}')  # Проверка метода __str__ модели Comment

    def test_comment_meta(self):
        """
        Проверка метаданных модели Comment.
        """
        self.assertEqual(self.comment._meta.db_table, "Comment")  # Проверка имени таблицы в базе данных
        self.assertEqual(self.comment._meta.verbose_name, "Комментарии к статье блога")  # Проверка единственного числа имени модели
        self.assertEqual(self.comment._meta.verbose_name_plural, "Комментарии к статьям блога")  # Проверка множественного числа имени модели