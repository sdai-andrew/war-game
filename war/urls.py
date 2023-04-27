from django.contrib import admin
from django.urls import path
from wargame import views

urlpatterns = [
    path('', views.home_action, name="home"),
    path('game', views.go_game, name="go_game"),
    path('get-wins/<str:name>', views.get_wins_json),
    
]
