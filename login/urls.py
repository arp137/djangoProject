from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard')
]