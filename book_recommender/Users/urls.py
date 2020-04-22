from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', views.custom_login),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('register/', views.register, name="register"),
    path('account/', views.view_profile, name = "view_profile"),
    path('account/edit',views.edit_profile, name = "edit_profile"),
    path('createShelf/', views.addShelf, name="createShelf"),
    path('removeShelf/<int:sid>', views.removeShelf, name="removeShelf"),
    path('shelves/', views.myShelves, name="shelves"),
    re_path(r'(?P<sid>[0-9]+)/shelf/$', views.myShelf, name="shelf"),
    url(r'addBookToShelf/(?P<sid>[0-9]+)/(?P<bid>[0-9]+)$', views.addBookToShelf, name = "addBookToShelf"),
    url(r'removeBookFromShelf/(?P<sid>[0-9]+)/(?P<bid>[0-9]+)$', views.removeBookFromShelf, name = "removeBookFromShelf"),

]
