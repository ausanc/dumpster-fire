from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views import View
from .sample_json import user_game_list_sample, user_stats_example, names
from .models import Hook
from django.http import JsonResponse
from django.core import serializers
from background_task import background
from .hook_functions import update_hook
from .vapour import game, profile, get_game_id_list

app_id_to_name = {}
for appinfo in names["applist"]["apps"]:
    app_id_to_name[appinfo["appid"]] = appinfo["name"]


# Create your views here.
def index(request):
    return render(request, 'dumpster/index.html')


class InputSteamURL(View):
    def get(self, request):
        return render(request, 'dumpster/input_user.html')

    def post(self, request):
        # get the input
        # trim the input
        inputURL = request.POST.get('profileInput')
        steam_id = '76561198015546177'
        if "/profiles/" in inputURL:
            steam_id = inputURL[36:]
        return redirect('select_game', steam_id=steam_id)


def select_game(request, steam_id):
    user = profile(steam_id)
    games = []
    for game in get_game_id_list(user):
        games.append({
            "appid": game,
            "name": app_id_to_name[game]
        })
    context = {
        "games": games,
        "steam_id": steam_id,
    }
    return render(request, 'dumpster/select_game.html', context)


def select_achieve(request, steam_id, app_id):
    game_object = game(app_id)
    achievements = game_object.get_all_achievements()
    context = {
        "achievements": achievements,
        "steam_id": steam_id,
        "app_id": app_id,
    }
    return render(request, 'dumpster/select_achievement.html', context)


def make_new_hook(request):
    if request.method == 'POST':
        print("MAKING NEW HOOK")
        steam_id = request.POST.get('steamID')
        app_id = request.POST.get('appID')
        achievement_name = request.POST.get('achievementName')
        print(steam_id, app_id, achievement_name)

        hook = Hook(account_url=steam_id, game_id=app_id, achievement_id=achievement_name)
        hook.save()

    return redirect('view_hooks')


def view_hooks(request):
    hooks = Hook.objects.all()
    context = {
        "hooks": hooks,
    }
    return render(request, 'dumpster/hooks.html', context)


def starttasks(request):
    print("Adding hook task")
    task_check_hooks(repeat=10)
    return JsonResponse({})


@background(schedule=10)
def task_check_hooks():
    print("HOOK CHECKS HERE")
    hooks = Hook.objects.filter(completed_on=None)
    for hook in hooks:
        update_hook(hook)
    print(hooks)


def delete_hook(request, hook_id):
    obj = get_object_or_404(Hook, pk=hook_id)
    obj.delete()
    return redirect('view_hooks')
