from django.urls import path
from wargame import views

urlpatterns = [
    path('', views.home_action, name="home"),
    path('game', views.go_game, name="go_game"),
    path('get-wins/<str:name>', views.get_wins_json),
    path('login', views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('play-game/<str:p1name>/<str:p2name>', views.play_game),
]
