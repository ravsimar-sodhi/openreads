from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('create/', views.create, name = 'createGroup'),
    path('join/<int:id>/', views.join_group, name = 'join_group'),
    path('leave/<int:id>/', views.leave_group, name = 'leave_group'),
    url(r'chat/(?P<id>[0-9]+)/$', views.display_msgs, name = 'display_msgs'),
    path('<int:id>/new_msg/', views.write_message, name = 'write_messages'),
    path('get_msgs/', views.get_msgs, name = 'get_messages'),
    url(r'(?P<id>[0-9]+)/$', views.details, name = "groupDetails"),
    # url(r'(?P<bid>[0-9]+)/(?P<gid>[0-9]+)$', views.addBookToGroup, name = "addBookToGroup"),
    path('createShelf/', views.addShelf, name="createShelf"),
    path('removeShelf/<int:sid>/<int:gid>', views.removeShelf, name="removeShelf"),
    url(r'shelves/(?P<gid>[0-9]+)$', views.groupShelves, name="groupShelves"),
    url(r'shelf/(?P<sid>[0-9]+)$', views.myShelf, name="groupShelf"),
    url(r'addBookToShelf/(?P<sid>[0-9]+)/(?P<bid>[0-9]+)$', views.addBookToShelf, name = "addBookToGroupShelf"),
    url(r'removeBookFromShelf/(?P<sid>[0-9]+)/(?P<bid>[0-9]+)$', views.removeBookFromShelf, name = "removeBookFromGroupShelf"),
]
