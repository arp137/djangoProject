from django.urls import path
from . import views

urlpatterns = [
    path("teams/", views.equips, name="teams"),
    path('teams/<int:equip_id>/', views.equip, name="info"),
    path('make-comp/', views.make_comparative, name="make-comp")
]