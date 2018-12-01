from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('selectuser', views.InputSteamURL.as_view()),
    path('selectgame/<int:steam_id>', views.select_game, name='select_game'),
    path('selectachieve/<int:steam_id>/<int:app_id>',
         views.select_achieve, name='select_achieve'),
    path('makenewhook', views.make_new_hook, name='make_new_hook'),
    path('hooks', views.view_hooks)
]
