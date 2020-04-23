
from django.urls import path,re_path
from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
     path('', views.allBooks,name="books"),
     re_path(r'(?P<id>[0-9]+)/$', views.details, name = "details"),
#      re_path(r'(?P<id>[0-9]+)/wishList/$', views.userWishList, name='wishList'),
#      re_path(r'(?P<id>[0-9]+)/readList/$', views.userReadList, name='readList'),
     re_path(r'^search/$',views.search, name='search'),
#      # re_path(r'^rate/(?P<rate_value>[0-5]+)/(?P<book_id>[0-9]+)$', views.rate_book, name='rate_book'),
# #      re_path(r'^rate/(?P<rate_value>[0-5]+)/(?P<book_id>[0-9]+)$',
     url(r'^rateList', views.userRateList, name='rateList'),
#      url(r'(?P<id>[0-9]+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
