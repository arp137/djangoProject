from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboardClass.as_view(), name='dashboard'),
    path('make-comp/', views.make_comparativeClass.as_view(), name="make-comp"),
    #path('make-comp/<int:user_id>/<str:season>/<str:equip1_name>/<str:equip2_name>/', views.make_comparative_selection, name="get-comp")
]