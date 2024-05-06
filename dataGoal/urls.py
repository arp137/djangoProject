from django.urls import path
from . import views

urlpatterns = [
    path("teams/", views.equips, name="teams"),
    path('teams/<int:equip_id>/', views.equip, name="info"),
    path('make-comp/', views.make_comparative, name="make-comp"),
    path('make-comp/<str:season>/<str:equip1_name>/<str:equip2_name>/', views.make_comparative_selection, name="get_comp")
]