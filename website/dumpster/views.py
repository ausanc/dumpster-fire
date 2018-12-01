from django.shortcuts import redirect, render
from django.views import View

# Create your views here.
def index(request):
    return render(request, 'dumpster/index.html')


def select_game(request, steam_id):
    return render(request, 'dumpster/index.html')


class InputSteamURL(View):
    def get(self, request):
        print("GETTING HERE")
        return render(request, 'dumpster/input_user.html')

    def post(self, request):
        print("POSTING HERE")
        return redirect('select_game', steam_id='0123456789')
