﻿"""
Definition of views.
"""

from datetime import datetime
import imp
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.forms import FeedbackForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'CYBER_PC',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Список контактов нашей компании',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Общие сведения о нашем проекте',
            'year':datetime.now().year,
        }
    )

def builder(request):
    assert isinstance(request, HttpRequest)
    """Renders the builder page."""
    return render(
        request,
        'app/builder.html',
        {
            'title':'Конфигуратор',
            'message':'Переход на страницу конфиругуратора ПК',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    data = None
    recommend = {'1': 'Да', '2': 'Нет'}
    level = {'1': 'Крайне удовлетворён', '2': 'Удовлетворён', 
                '3': 'Неудовлетворён', '4': 'Крайне неудовлетворён'}
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['like'] = form.cleaned_data['like']
            data['pcconfig'] = form.cleaned_data['pcconfig']
            data['recommend'] = recommend[ form.cleaned_data['recommend'] ]
            data['level'] = level[ form.cleaned_data['level'] ]
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = FeedbackForm()
    return render(
        request,
        'app/feedback.html',
        {
            'form':form,
            'data':data,
            'title':'Обратная связь',
            'message':'Вы можете оставить обратную связь здесь.',
            'year':datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm (request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
        return redirect('home')
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(

        request,
        'app/registration.html',
        {
            'title': 'Регистрация',
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
        return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'title':'Пост блога',
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
        }
    )
def newpost(request):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки данных формы на сервер методом POST
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.author = request.user
            blog_f.posted = datetime.now() 
            blog_f.save() # сохраняем изменения после добавления полей
        return redirect('blog') # переадресация на ту же страницу статьи после отправки комментария
    else:
        blogform = BlogForm() # создание формы для ввода комментария
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform, # передача формы добавления комментария в шаблон веб-страницы
            'title': 'Добавить статью блога',
            
            'year':datetime.now().year,
        }
    )
def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Общие сведения о нашем проекте',
            'year':datetime.now().year,
        }
    )