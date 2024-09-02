from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Todo import views


urlpatterns = [
    path('',login,name="login"),
    path('register/',register,name="register"),
    path('show',show,name="show"),
    path('logout',logout,name="logout"),
    path('delete/<id>',delete,name="delete"),
    path('edit/<id>',edit,name="edit"),
]
