from django.shortcuts import render


def home(request):
    return render(request, 'templates/static_handler.html')
# Create your views here.
