from django.urls import path, re_path
from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html')),
    path('logout/', LogoutView.as_view(next_page='/')),
    path('register/', views.register, name="register"),
    path('account/', views.view_profile, name = "view_profile"),
    path('account/edit',views.edit_profile, name = "edit_profile")
]
