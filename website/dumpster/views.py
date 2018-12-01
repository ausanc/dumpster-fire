from django.shortcuts import redirect, render
from django.views import View
from .sample_json import user_game_list_sample, user_stats_example, names

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
