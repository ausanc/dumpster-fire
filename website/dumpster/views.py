from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views import View
from .sample_json import user_game_list_sample, user_stats_example, names
from .models import Hook
from django.http import JsonResponse
from django.core import serializers
from background_task import background
from .hook_functions import update_hook
from .vapour import game, profile, get_game_id_list, api_request, get_game_list
from .steam_key import key

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
    game_list = get_game_list(user)
    games = []
    for game in get_game_id_list(user):
        games.append({
            "appid": game,
            "name": app_id_to_name[game]
        })
    context = {
        "games": game_list,
        "steam_id": steam_id,
    }
    return render(request, 'dumpster/select_game.html', context)


def select_achieve(request, steam_id, app_id):
    game_object = game(app_id)
    achievements = game_object.get_all_achievements()

    url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=%s&key=%s&steamid=%s"
    steam_api_url = url % (app_id, key, steam_id)
    unlocked_ids = []
    try:
        data = api_request(steam_api_url)
        unlocked = data["playerstats"]["achievements"]
        for item in unlocked:
            unlocked_ids.append(item["name"])
    except:
        pass

    for item in achievements:
        item.unlocked = item.achievement_id in unlocked_ids

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

        user = profile(steam_id)
        game_object = game(app_id)
        achievements = game_object.get_all_achievements()
        ach_name = ""
        icon_url = ""
        for achievement in achievements:
            if achievement.achievement_id == achievement_name:
                ach_name = achievement.achievement_name
                icon_url = achievement.achievement_icon

        hook = Hook(account_url=steam_id, game_id=app_id, achievement_id=achievement_name, ach_name=ach_name, icon_url=icon_url, game_name=game_object.game_name, profile_name=user.profile_name)
        hook.save()

    return redirect('view_hooks')


def view_hooks(request):
    hooks = Hook.objects.all().order_by("-created_on")
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
    hooks = Hook.objects.filter(completed=False)
    for hook in hooks:
        update_hook(hook)
    print(hooks)


def delete_hook(request, hook_id):
    obj = get_object_or_404(Hook, pk=hook_id)
    obj.delete()
    return redirect('view_hooks')
