
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('submit',views.registerSubmit,name='registerSubmit'),
    path('login',views.login,name='login'),
    path('loginUser',views.submitLogin,name='submitLogin'),
    path('logout',views.logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('home',views.dash_home,name='dashhome'),
    path('submitPost',views.submitPost,name='submitPost'),
    path('readPost',views.readPost,name='readPost'),
]
