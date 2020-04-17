from django.shortcuts import render
from django.shortcuts import render,redirect
from Books.models import *
from django.views.generic import View
from django.contrib.auth.views import LoginView

def index(request):
    return render(request,'login.html', {})

# def home(request):
# def custom_login(request):
#     if request.user.is_authenticated:
#         return redirect('/books/')
#     else:
#         return LoginView.as_view(template_name='./users/login.html')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/user/account')
    else:
        return LoginView.as_view(template_name='./users/login.html')(request)
