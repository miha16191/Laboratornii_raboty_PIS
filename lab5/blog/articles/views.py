from django.http import Http404
from django.shortcuts import render, redirect
from .models import Article


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