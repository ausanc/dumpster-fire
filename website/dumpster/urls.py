from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('select', views.InputSteamURL.as_view()),
    path('select/<int:steam_id>', views.select_game, name='select_game'),
    path('select/<int:steam_id>/<int:app_id>',
         views.select_achieve, name='select_achieve'),
    path('makenewhook', views.make_new_hook, name='make_new_hook'),
    path('hooks', views.view_hooks, name='view_hooks'),
    path('starttaskrunner', views.starttasks),
    path('deletehook/<int:hook_id>', views.delete_hook, name="delete_hook")
]
