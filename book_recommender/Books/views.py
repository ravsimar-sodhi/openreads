from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from Books.models import *
from Users.models import *
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


# Create your views here.
def details(request,id):
    request.session['book_id'] = id
    book = Book.objects.get(id=id)
    bookCategories = []
    if book.book_genre:
        for category in book.book_genre.all():
            bookCategories.append(category.name) 
    return render(request,"detail.html",
    {"book":book, "categories":bookCategories});

def search(request):
    text_search = request.GET.get("in")
    book_list = Book.objects.filter(book_title__icontains= text_search)
    # author=Book.objects.filter(Author_Name__icontains=text_search)
    return render(request,'search.html',
    {'book_list':book_list})

# AJAX
def userRateList(request):
    stars = request.GET.get('stars')
    bookID = request.GET.get('bookID')
    bookTitle= Book.objects.get(id=bookID).book_title
    print(bookTitle)
    checkExistedRatings= rateList.objects.filter(user= request.user, book_id = bookID)
    if len(checkExistedRatings)==0:
        rateList.objects.create(user= request.user, book_id = bookID, rate=stars)
        data = {
            'rateStatus': int(1),
            'bookTitle':bookTitle
        }
        return JsonResponse(data)
    else:
        rateList.objects.filter(user= request.user, book_id = bookID).update(rate=stars)
        data = {
            'rateStatus': int(0),
            'bookTitle':bookTitle
        }
        return JsonResponse(data)


def allBooks(request):
    books = Book.objects.all()
    booksList=[]
    for book in Book.objects.all():
        booksList.append(book)
    print(booksList)
    indexList = []
    for i in range(0, len(books), 5):
        indexList.append(i)

    return render(request, 'index.html', {'noOfBooks':len(booksList), 'books': booksList, "indexList" : indexList})

