<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from django.contrib.auth.models import User,Book, Author
from django.shortcuts import render,redirect
from UserGroups.forms import *
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from UserGroups.models import *
from Users.models import *
from Books.models import *

def create(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect('/books')
    else:
        form = GroupCreationForm()
    args = {'form': form}
    return render(request, 'groups/group_creation.html', args)
def details(request, id):
    groupMember = GroupMember.objects.filter(user=request.user,group=UserGroup.objects.filter(id=id))
    groupBooks = (UserGroup.objects.filter(id=id))[0].group_books.all()
    allBooks = Book.objects.all()
    for book in groupBooks:
        allBooks.remove(book)
    groupMessages = Message.objects.filter(group_id=id)
    myGroups = GroupMember.objects.filter(user=request.user)
    allGroups = GroupMember.objects.all()
    group = UserGroup.objects.filter(id=id)
    args = {'groupMember':groupMember,
            'groupBooks':groupBooks,
                'otherBooks':allBooks,
                'groupMessages':groupMessages,
                'myGroups':myGroups,
                'allGroups':allGroups,
                'group':group}
    return render(request, 'groups/groupInfo.html', args)

=======
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from django.contrib.auth.models import User,Book, Author
from django.shortcuts import render,redirect
from UserGroups.forms import *
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from UserGroups.models import *
from Users.models import *
from Books.models import *

def create(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            return redirect('/books')
    else:
        form = GroupCreationForm()
    args = {'form': form}
    return render(request, 'groups/group_creation.html', args)
def details(request, id):
    groupMember = GroupMember.objects.filter(user=request.user,group=UserGroup.objects.filter(id=id))
    groupBooks = (UserGroup.objects.filter(id=id))[0].group_books.all()
    allBooks = Book.objects.all()
    for book in groupBooks:
        allBooks.remove(book)
    groupMessages = Message.objects.filter(group_id=id)
    myGroups = GroupMember.objects.filter(user=request.user)
    allGroups = GroupMember.objects.all()
    group = UserGroup.objects.filter(id=id)
    args = {'groupMember':groupMember,
            'groupBooks':groupBooks,
                'otherBooks':allBooks,
                'groupMessages':groupMessages,
                'myGroups':myGroups,
                'allGroups':allGroups,
                'group':group}
    return render(request, 'groups/groupInfo.html', args)

>>>>>>> 7003b5a659b47ff10a98f9fa5808c8f11b231424
