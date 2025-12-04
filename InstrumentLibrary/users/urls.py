from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('success/', views.success, name='success'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password_change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name='password_change_done'),
]

