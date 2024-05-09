from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboardClass.as_view(), name='dashboard'),
    path('make-comp/', views.make_comparative, name="make-comp"),
    path('make-comp/<int:user_id>/<str:season>/<str:equip1_name>/<str:equip2_name>/', views.retrieve_comparison, name="get-comp"),
    path('make-comp/<str:season>/<str:equip1_name>/<str:equip2_name>/', views.make_comparative_selection,
         name="get-comp")
]