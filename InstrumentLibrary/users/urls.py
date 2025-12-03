from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('success/', views.success, name='success'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]

