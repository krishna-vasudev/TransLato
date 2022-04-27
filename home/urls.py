from tkinter import N
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns =[
    path('',views.dashboard,name='dashboard'),
    path('createproject',views.createproject,name='createproject'),
    path('translateproject/<str:pk>',views.translateproject,name='translateproject'),
    path("login", views.loginUser, name='login'),
    path("logout", views.logoutuser, name='logout'),
    path("assignannotator/<str:pk>",views.assignannotator, name='assignannotator'),
]
