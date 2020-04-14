from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from django.contrib.auth.models import User,Book, Author
from django.shortcuts import render,redirect
from Users.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from Users.models import *
from UserGroups.models import *

def register(request):
    print("222")
    if request.method == 'POST':
        print("333")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("111")
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    args = {'form': form}
    return render(request, 'users/reg_form.html', args)

@login_required
def view_profile(request):
    userName = {'user':request.user}
    UserRateList=rateList.objects.filter(user=request.user)
    print (UserRateList)
    # myGroups = None
    # otherGroups = None
    myGroups = request.user.my_groups.all()
    otherGroups = set(UserGroup.objects.all()).difference(set(myGroups))
    return render(request, 'users/account.html', {'UserRateList':UserRateList, 'myGroups':myGroups, 'otherGroups':otherGroups})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance= request.user)

        if form.is_valid():
            form.save()
            return redirect("/users/account")
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, '/users/account_edit', args)


def logout(request):
    logout(request)
    return redirect('/users/login')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('/books/')
    else:
        return LoginView.as_view(template_name='./users/login.html')(request)
