from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name=''),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('user-logout/', views.user_logout, name='user_logout')
]