from django.contrib import admin
from django.urls import path
from wargame import views

urlpatterns = [
    path('', views.home_action, name="home"),
]
