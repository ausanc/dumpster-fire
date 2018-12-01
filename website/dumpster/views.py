from django.shortcuts import redirect, render
from django.views import View
from .sample_json import user_game_list_sample, user_stats_example, names
from .models import Hook
from django.http import JsonResponse
from django.core import serializers
from background_task import background

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
        return redirect('select_game', steam_id='0123456789')


def select_game(request, steam_id):
    games = []
    for game in user_game_list_sample["response"]["games"]:
        games.append({
            "appid": game["appid"],
            "name": app_id_to_name[game["appid"]]
        })
    context = {
        "games": games,
        "steam_id": steam_id,
    }
    return render(request, 'dumpster/select_game.html', context)


def select_achieve(request, steam_id, app_id):
    context = {
        "achievements": user_stats_example["playerstats"]["achievements"],
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

    return render(request, 'dumpster/index.html')


def view_hooks(request):
    qs = Hook.objects.all()
    qs_json = serializers.serialize('json', qs)
    return JsonResponse(qs_json, safe=False)


def starttasks(request):
    print("Adding hook task")
    task_check_hooks(repeat=10)
    return JsonResponse({})


@background(schedule=10)
def task_check_hooks():
    print("HOOK CHECKS HERE")
