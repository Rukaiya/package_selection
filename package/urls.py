from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

]