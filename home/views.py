from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'pages/index.html')


def get_login(request):
    return render(request, 'pages/login.html')
