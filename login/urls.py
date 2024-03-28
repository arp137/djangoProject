from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=''),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-logout/', views.user_logout, name='user_logout')
]