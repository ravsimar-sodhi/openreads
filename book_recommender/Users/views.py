from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
#from django.contrib.auth.models import User,Book, Author
from django.shortcuts import render,redirect
from Users.forms import *
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from Users.models import *
from UserGroups.models import *
from django.contrib import messages
from Predictor.recom import *

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
def view_profile(request, args = None, error = None):
    userName = {'user':request.user}
    UserRateList=rateList.objects.filter(user=request.user)
    print (UserRateList)
    if len(UserRateList)>5:
        UserRateList=UserRateList[len(UserRateList)-5:]
    # myGroups = None
    # otherGroups = None
    myGroups = request.user.my_groups.all()
    otherGroups = set(UserGroup.objects.all()).difference(set(myGroups))
    if args is not None:
        form = args['form']
    else:
        form = AddShelfForm()
    shelves = Bookshelf.objects.filter(user=request.user)
    print(form)

    return render(request, 'users/account.html', {'UserRateList':UserRateList, 'myGroups':myGroups, 'otherGroups':otherGroups, 'form': form, 'shelves':shelves,'error':error})

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

@login_required
def addShelf(request):
    if request.method == 'POST':
        form = AddShelfForm(request.POST, user=request.user)
        print("555")
        if form.is_valid():
            print("345")
            form.save()
            return redirect('/user/account/')
    else:
        form = AddShelfForm()
    args = {'form': form}
    print("111",args)
    return view_profile(request, args)

@login_required
def myShelves(request):
    user = request.user
    shelves = Bookshelf.objects.filter(user=user).all()
    return render(request, './users/shelves.html',{'shelves':shelves})


@login_required
def myShelf(request, sid):
    user = request.user
    shelf = Bookshelf.objects.filter(user=user, id = sid)
    if len(shelf) == 0:
        messages.warning(request, 'It is not your bookshelf!')
        return view_profile(request, error = "Not your shelf")
    else:
        shelf = shelf[0]
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
    

    # books = Book.objects.all()
    # otherBooks=list(set(books).difference(set(shelfBooks)))
    # otherBooks = otherBooks[0:min(5,len(otherBooks))]
    return render(request, './users/shelf.html',{'shelf':shelf, 'otherBooks':otherBooks})

@login_required
def addBookToShelf(request, sid, bid):
    userid = request.user.id
    shelf = Bookshelf.objects.filter(id = sid)[0]
    book = Book.objects.filter(id = bid)[0]
    shelf.book.add(book)
    return redirect("/user/"+str(sid)+"/shelf/")

@login_required
def removeBookFromShelf(request, sid, bid):
    userid = request.user.id
    shelf = Bookshelf.objects.get(id = sid)
    book = Book.objects.get(id = bid)
    print("111")
    print(sid)
    if shelf.book.remove(book):
        print("Book in shelf, removing...")
    else:
        print("Book not in shelf!")
        # TODO: give alert/message
    return redirect("/user/"+str(sid)+"/shelf/")
