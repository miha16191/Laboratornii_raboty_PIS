from django.shortcuts import render
from .models import Article


def archive(request):
    posts = Article.objects.all()
    return render(request, 'archive.html', {'posts': posts})

# Create your views here.
