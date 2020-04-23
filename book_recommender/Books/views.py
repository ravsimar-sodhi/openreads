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
from UserGroups.models import Groupshelf


# Create your views here.
def details(request,id):
    request.session['book_id'] = id
    book = Book.objects.get(id=id)
    bookCategories = []
    if book.book_genre:
        for category in book.book_genre.all():
            bookCategories.append(category.name)
    if not request.user.is_authenticated:
        return render(request,"detail.html", {"book":book, "categories":bookCategories})
    user = User.objects.get(id=request.user.id)
    shelves = Bookshelf.objects.filter(user = request.user)
    groups = user.my_groups.all()
    groupshelves = Groupshelf.objects.filter(group__in=groups)
    return render(request,"detail.html", {"book":book, "categories":bookCategories, 'shelves' : shelves, 'groupshelves': groupshelves})

def search(request):
    text_search = request.GET.get("in")
    book_list = Book.objects.filter(book_title__icontains= text_search) | Book.objects.filter(book_author__icontains = text_search)
    # author=Book.objects.filter(Author_Name__icontains=text_search)k
    return render(request,'search.html',
    {'book_list':book_list})

# AJAX
def userRateList(request):
    stars = request.GET.get('stars')
    bookID = request.GET.get('bookID')
    bookTitle= Book.objects.get(id=bookID).book_title
    print(bookTitle)
    book = Book.objects.get(id=bookID)
    num_of_ratings = book.book_num_of_ratings
    avg_rating = book.book_avg_rating

    checkExistedRatings= rateList.objects.filter(user= request.user, book_id = bookID)
    if len(checkExistedRatings)==0:
        rateList.objects.create(user= request.user, book_id = bookID, rate=stars)
        data = {
            'rateStatus': int(1),
            'bookTitle':bookTitle
        }
        avg_rating = ((avg_rating*num_of_ratings)+int(stars))/(num_of_ratings + 1)
        num_of_ratings += 1
        Book.objects.filter(id=bookID).update(book_num_of_ratings = num_of_ratings, book_avg_rating = avg_rating)
        return JsonResponse(data)
    else:
        old_rate = rateList.objects.filter(user= request.user, book_id = bookID)[0].rate
        rateList.objects.filter(user= request.user, book_id = bookID).update(rate=stars)
        data = {
            'rateStatus': int(0),
            'bookTitle':bookTitle
        }
        avg_rating = ((avg_rating*num_of_ratings)-old_rate+int(stars))/(num_of_ratings)
        Book.objects.filter(id=bookID).update(book_avg_rating = avg_rating)

        return JsonResponse(data)


def allBooks(request):

    booksPerGenre=6
    finalBooksDict = {}
    for genre in Genre.objects.all():
        cnt=0
        bookList=genre.book_set.all()
        bookList = bookList[:min(booksPerGenre,len(bookList))]
        # bookList = Book.objects.filter(book_genre__icontains=genre.name)
        # for book in Book.objects.all():
        #     if genre in book.book_genre.all():
        #         bookList.append(book)
        #         cnt=cnt+1
        #         if (cnt>=booksPerGenre):
        #             break
        finalBooksDict[genre]=bookList



    return render(request, 'index.html', {'finalBooksDict':finalBooksDict})
