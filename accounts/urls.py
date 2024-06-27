from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.user_login, name="login"),
    path('user_logout/', views.user_login, name = 'logout'),
    path('registration', views.registration, name = 'registration'),
]