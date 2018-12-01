from .vapour import api_request
from .steam_key import key
from .models import Hook

url = "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=%s&key=%s&steamid=%s"

def update_hook(hook: Hook):
    steam_api_url = url % (hook.game_id, key, hook.account_url)
    print(steam_api_url)
    try:
        data = api_request(steam_api_url)
        achieves = data["playerstats"]["achievements"]
        for achievement in achieves:
            if achievement["name"] == hook.achievement_id:
                if achievement["achieved"] == 1:
                    print("USER %s HAS UNLOCKED %s IN GAME %s" %
                        (hook.account_url, hook.achievement_id, hook.game_id))
                    hook.completed = True
                    hook.save()
    except:
        pass
    
    print("Check hook: %s" % hook)
