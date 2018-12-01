from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('selectuser', views.InputSteamURL.as_view()),
    path('selectgame/<int:steam_id>', views.select_game, name='select_game'),
]
