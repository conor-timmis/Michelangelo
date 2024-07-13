from django.urls import path
from . import views

urlpatterns = [
    path('create_booking/', views.create_booking, name="create_booking"),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name = 'edit_booking'),
    path('delete_booking/', views.delete_booking, name = 'delete_booking'),
    path('table_list/', views.booking_list, name = 'table_list'),
]
