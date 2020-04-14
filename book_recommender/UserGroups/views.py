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

def join_group(request, id):
    print("ok")
    if request.method == 'POST':
        print("yo")
        print(id)
        group = UserGroup.objects.filter(id=id).all()[0]
        group.group_members.add(request.user)

    return redirect('/')


def details(request, id):
    group = UserGroup.objects.filter(id=id).all()[0]
    # groupMember = GroupMember.objects.filter(user=request.user,group=group)
    groupMember= group.group_members.all()
    # print(groupMember)
    groupBooks = (UserGroup.objects.filter(id=id))[0].group_books.all()
    allBooks = Book.objects.all()
    otherBooks = set(allBooks).difference(set(groupBooks))
    groupMessages = Message.objects.filter(group_id=id)
    myGroups = request.user.my_groups.all()
    otherGroups = set(UserGroup.objects.all()).difference(set(myGroups))
    join = True
    if request.user in groupMember:
        join = False

    args = {'groupMembers':groupMember,
            'groupBooks':groupBooks,
                'otherBooks':otherBooks,
                'groupMessages':groupMessages,
                'myGroups':myGroups,
                'allGroups':otherGroups,
                'group':group,
                'join':join}
    return render(request, 'groups/groupInfo.html', args)

def addBookToGroup(request, bid, gid):
    book = Book.objects.get(id = bid)
    group = UserGroup.objects.get(id = gid)
    group.group_books.add(book)
    genres = group.group_genre.all()
    for genre in book.book_genre.all():
        if genre not in genres:
            group.group_genre.add(genre)
    return redirect("/group/"+str(gid))


