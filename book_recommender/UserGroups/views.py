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
from Predictor.recom import *

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
        group = UserGroup.objects.get(id=id)
        group.group_members.add(request.user)

    return redirect('/')

def write_message(request, id):
    if request.method == 'POST':
        message_content = request.POST['content']
        group = UserGroup.objects.get(id=id)
        message = Message(message_text=message_content, sender_id=request.user, group_id=group)
        message.save()
        groupMessages = Message.objects.filter(group_id=group)
        shelves = Groupshelf.objects.filter(group=group).all()
        args = {
                'group': group,
                'messages': groupMessages,
               }
        # display_msgs(request, args)
        return render(request, 'groups/groupChat.html', args)

def display_msgs(request, id):
    if request.method == 'POST':
        group = UserGroup.objects.get(id=id)
        groupMessages = Message.objects.filter(group_id=group)
        args = {
                'group': group,
                'messages': groupMessages,
               }
        return render(request, 'groups/groupChat.html', args)

def details(request, id, argsDict = None):
    group = UserGroup.objects.get(id=id)
    # groupMember = GroupMember.objects.filter(user=request.user,group=group)
    groupMember= group.group_members.all()
    # print(groupMember)
    shelves = Groupshelf.objects.filter(group=group).all()
    # groupMessages = Message.objects.filter(group=group)
    myGroups = request.user.my_groups.all()
    otherGroups = set(UserGroup.objects.all()).difference(set(myGroups))
    join = True
    if request.user in groupMember:
        join = False
    if argsDict is not None:
        form = argsDict['form']
    else:
        form = AddGroupShelfForm()
    args = {
            'groupMembers':groupMember,
            'shelves':shelves,
            'myGroups':myGroups,
            'allGroups':otherGroups,
            'group':group,
            'join':join,
            'form':form
            }
    return render(request, 'groups/groupInfo.html', args)

# def addBookToGroup(request, bid, gid):
#     book = Book.objects.get(id = bid)
#     group = UserGroup.objects.get(id = gid)
#     group.group_books.add(book)
#     genres = group.group_genre.all()
#     for genre in book.book_genre.all():
#         if genre not in genres:
#             group.group_genre.add(genre)
#     return redirect("/group/"+str(gid))

@login_required
def addShelf(request):
    if request.method == 'POST':
        form = AddGroupShelfForm(request.POST,request.POST.get('group'))
        if form.is_valid():
            form.save()
            return redirect('/group/'+str(request.POST.get('group')))
    else:
        form = AddGroupShelfForm()
    args = {'form': form}
    print("111",args)
    return details(request,request.POST.get('group'), args)

@login_required
def groupShelves(request, gid):
    group = UserGroup.objects.filter(id = gid)[0]
    shelves = Groupshelf.objects.filter(group=group).all()
    return render(request, './groups/shelves.html',{'shelves':shelves,'group':group})


@login_required
def myShelf(request, sid):
    shelf = Groupshelf.objects.filter(id = sid)[0]
    group = shelf.group
    member = False
    group_members = group.group_members.all()
    if request.user in group_members:
        member = True

    shelfBooks = shelf.book.all()
    otherBooks = list()
    books = Book.objects.all()
    for book in shelfBooks:
        recomBooks = recommendations(book.book_title)
        for book1 in books:
            if book1.book_title in recomBooks:
                otherBooks.append(book1)
                recomBooks.remove(book1.book_title)
    otherBooks = list(set(otherBooks))  
    if len(otherBooks) == 0:
        otherBooks=list(set(books).difference(set(shelfBooks)))
        otherBooks = otherBooks[0:min(10,len(otherBooks))]

    # shelfBooks = shelf.book.all()
    # books = Book.objects.all()
    
    return render(request, './groups/shelf.html',{'shelf':shelf, 'otherBooks':otherBooks,'member':member})

@login_required
def addBookToShelf(request, sid, bid):
    userid = request.user.id
    shelf = Groupshelf.objects.filter(id = sid)[0]
    book = Book.objects.filter(id = bid)[0]
    shelf.book.add(book)
    return redirect("/group/shelf/"+str(shelf.id))

@login_required
def removeBookFromShelf(request, sid, bid):
    userid = request.user.id
    shelf = Groupshelf.objects.get(id = sid)
    book = Book.objects.get(id = bid)
    if shelf.book.remove(book):
        print("Book in shelf, removing...")
    else:
        print("Book not in shelf!")
        # TODO: give alert/message
    return redirect("/group/shelf/"+str(shelf.id))
