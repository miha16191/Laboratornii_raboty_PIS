from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST


def archive(request):
    posts = Article.objects.all()
    return render(request, 'archive.html', {'posts': posts})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        raise Http404('Статья не найдена')

    return render(request, 'article.html', {'post': post})


def create_post(request):
    if not request.user.is_authenticated:
        raise Http404('Страница недоступна')

    form = {
        'title': '',
        'text': '',
        'errors': '',
    }

    if request.method == 'POST':
        form['title'] = request.POST.get('title', '').strip()
        form['text'] = request.POST.get('text', '').strip()

        if not form['title'] or not form['text']:
            form['errors'] = 'Не все поля заполнены.'

        elif len(form['title']) > 200:
            form['errors'] = 'Заголовок не должен превышать 200 символов.'

        elif Article.objects.filter(title=form['title']).exists():
            form['errors'] = 'Статья с таким заголовком уже существует.'

        else:
            article = Article.objects.create(
                title=form['title'],
                text=form['text'],
                author=request.user,
            )

            return redirect('get_article', article_id=article.id)

    return render(request, 'create_post.html', {'form': form})
    
def register(request):
    form = {
        'username': '',
        'email': '',
        'errors': '',
    }

    if request.method == 'POST':
        form['username'] = request.POST.get('username', '').strip()
        form['email'] = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not form['username'] or not form['email'] or not password.strip():
            form['errors'] = 'Заполните все поля.'

        elif len(form['username']) > 150:
            form['errors'] = 'Логин не должен превышать 150 символов.'

        elif User.objects.filter(username=form['username']).exists():
            form['errors'] = 'Пользователь с таким логином уже существует.'

        else:
            try:
                validate_email(form['email'])
            except ValidationError:
                form['errors'] = 'Введите корректный email.'
            else:
                User.objects.create_user(
                    username=form['username'],
                    email=form['email'],
                    password=password,
                )

                messages.success(
                    request,
                    'Регистрация прошла успешно. Учётная запись создана.'
                )

                return redirect('register')

    return render(request, 'registration.html', {'form': form})
    
def user_login(request):
    form = {
        'username': '',
        'errors': '',
    }

    if request.method == 'POST':
        form['username'] = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not form['username'] or not password.strip():
            form['errors'] = 'Введите логин и пароль.'
        else:
            user = authenticate(
                request,
                username=form['username'],
                password=password,
            )

            if user is not None:
                login(request, user)
                return redirect('archive')

            form['errors'] = 'Неверный логин или пароль.'

    return render(request, 'login.html', {'form': form})


@require_POST
def user_logout(request):
    logout(request)
    return redirect('archive')