from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboardClass.as_view(), name='dashboard'),
    path('make-comp/', views.make_comparative, name="make-comp"),
    path('make-comp/<int:user_id>/<int:season_id>/<int:equip1_id>/<int:equip2_id>/', views.retrieve_comparison, name="get-comp"),
    path('edit-comp/<int:comp_id>/', views.edit_comparison, name="edit-comp")
]