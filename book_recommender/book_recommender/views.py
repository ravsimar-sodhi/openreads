from django.shortcuts import render
from django.shortcuts import render,redirect
from Books.models import *
from django.views.generic import View


def index(request):
    return render(request,'login.html', {})