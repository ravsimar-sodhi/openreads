from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from django.contrib.auth.models import User,Book, Author
from django.shortcuts import render,redirect
from UserGroups.forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from UserGroups.models import *
from Users.models import *
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from Books.models import *
from Predictor.recom import *

def create(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            messages.success(request, "Group creation successful!")
            return redirect('/books')
    else:
        form = GroupCreationForm()
    args = {'form': form}
    return render(request, 'groups/group_creation.html', args)

def join_group(request, id):
    group = UserGroup.objects.get(id=id)
    if request.method == 'POST':
        group.group_members.add(request.user)
        messages.success(request, "Successfully joined group \"%s\" !"%(group))
    return redirect('/group/'+ str(group.id))

def leave_group(request, id):
    group = UserGroup.objects.get(id = id)
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        if user in group.group_members.all():
            group.group_members.remove(user)
            messages.success(request, "Successfully left group \"%s\" !" %(group))
        else:
            messages.error(request, "Error leaving group")
    return redirect('/group/' + str(group.id))

def write_message(request, id):
    group = UserGroup.objects.get(id=id)
    if request.user not in group.group_members.all():
        messages.error(request, "You are not a member of this group!")
        return redirect('/group/' + str(group.id))
    if request.method == 'POST':
        message_content = request.POST['content']
        if message_content == "" or message_content.isspace():
        	messages.error(request, 'Message can not be empty')
        	return redirect(display_msgs, id=id)
        message = Message(message_text=message_content, sender_id=request.user, group_id=group)
        message.save()
        groupMessages = Message.objects.filter(group_id=group)
        shelves = Groupshelf.objects.filter(group=group).all()
        args = {
                'group': group,
                'Messages': groupMessages,
               }
        # display_msgs(request, args)
        return redirect(display_msgs, id = id)

def display_msgs(request, id):
    group = UserGroup.objects.get(id=id)
    if request.user not in group.group_members.all():
        messages.error(request, "You are not a member of this group!")
        return redirect('/group/' + str(group.id))
    groupMessages = Message.objects.filter(group_id=group)
    args = {
            'gid':id,
            'group': group,
            'chat': groupMessages,
            }
    return render(request, 'groups/groupChat.html', args)

@csrf_exempt
def get_msgs(request):
    if request.method == 'POST':
        print(request)
        gid = request.POST['gid']
        print(gid)
        group = UserGroup.objects.get(id=gid)
        groupMessages = Message.objects.filter(group_id=group)
        messages = []
        for message in groupMessages:
            messages.append(
                {
                    'message_text' : message.message_text,
                    'sender':message.sender_id.username,
                    'time':message.sent_on.strftime("%I:%M, %a, %d %b")
                }
            )
        args = {
                'status': 'true',
                'chat': messages,
               }
        return JsonResponse(args)

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
        gid = request.POST.get('group')
        uid = request.user.id
        form = AddGroupShelfForm(request.POST, gid)
        try:
            group = UserGroup.objects.get(id=gid)
        except ObjectDoesNotExist:
            messages.error(request, "Group does not exist")
            return details(request, gid)

        user = User.objects.get(id = uid)
        if user not in group.group_members.all():
            messages.error(request, "You are not a member of this group")
            return details(request, gid)

        if form.is_valid():
            form.save()
            return redirect('/group/'+str(request.POST.get('group')))
    else:
        form = AddGroupShelfForm()
    args = {'form': form}
    print("111",args)
    return details(request,request.POST.get('group'), args)

def removeShelf(request, sid, gid):
    user = request.user
    group = UserGroup.objects.get(id=gid)
    if user not in group.group_members:
        messages.error(request, "You are not a member of this group")
        return redirect('/group/' + str(gid))
    try:
        shelf = Groupshelf.objects.get(id = sid, group=gid)
        shelf.delete()
        messages.success(request, "Shelf Deleted successfully!")
    except ObjectDoesNotExist:
        messages.error(request, "Error removing shelf")
    return redirect('/group/' + str(gid))

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

    if member is False:
        return render(request, './groups/shelf.html',{'shelf':shelf, 'member':member})

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


    return render(request, './groups/shelf.html',{'group': group,'shelf':shelf, 'otherBooks':otherBooks,'member':member})

@login_required
def addBookToShelf(request, sid, bid):
    user = User.objects.get(id = request.user.id)
    shelf = Groupshelf.objects.filter(id = sid)[0]
    group = shelf.group
    book = Book.objects.filter(id = bid)[0]
    if user in group.group_members.all():
        shelf.book.add(book)
        messages.success(request, 'Book \"%s\" added to shelf \"%s\" ' %(book.book_title,shelf.name))
    else:
        messages.error(request, "You do not have permission to perform this action!")
    return redirect("/group/shelf/"+str(shelf.id))

@login_required
def removeBookFromShelf(request, sid, bid):
    user = User.objects.get(id = request.user.id)
    shelf = Groupshelf.objects.get(id = sid)
    group = shelf.group

    book = Book.objects.get(id = bid)
    if book in shelf.book.all() and user in group.group_members.all():
        shelf.book.remove(book)
        messages.success(request, 'Book \"%s\" removed from shelf \"%s\" ' %(book.book_title,shelf.name))
    else:
        messages.error(request,"You do not have permission to perform this action!")
    return redirect("/group/shelf/"+str(shelf.id))
