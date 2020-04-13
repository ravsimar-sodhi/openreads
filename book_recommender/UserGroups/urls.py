<<<<<<< HEAD
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('create/', views.create, name = 'createGroup'),
    re_path(r'(?P<id>[0-9]+)/$', views.details, name = "groupDetails"),

    # path('logout/', LogoutView.as_view(next_page='/')),
    # path('register/', views.register, name="register"),
    # path('account/', views.view_profile, name = "view_profile"),
    # path('account/edit',views.edit_profile, name = "edit_profile")
]
=======
from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('create/', views.create, name = 'createGroup'),
    re_path(r'(?P<id>[0-9]+)/$', views.details, name = "groupDetails"),

    # path('logout/', LogoutView.as_view(next_page='/')),
    # path('register/', views.register, name="register"),
    # path('account/', views.view_profile, name = "view_profile"),
    # path('account/edit',views.edit_profile, name = "edit_profile")
]
>>>>>>> 7003b5a659b47ff10a98f9fa5808c8f11b231424
