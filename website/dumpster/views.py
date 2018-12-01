from django.shortcuts import redirect, render
from django.views import View
from .sample_json import user_game_list_sample

# Create your views here.
def index(request):
    return render(request, 'dumpster/index.html')


class InputSteamURL(View):
    def get(self, request):
        return render(request, 'dumpster/input_user.html')

    def post(self, request):
        return redirect('select_game', steam_id='0123456789')


def select_game(request, steam_id):
    context = {
        "games_json": user_game_list_sample["response"]["games"],
        "steam_id": steam_id,
    }
    return render(request, 'dumpster/select_game.html', context)


def select_achieve(request, steam_id, app_id):
    return render(request, 'dumpster/index.html')
