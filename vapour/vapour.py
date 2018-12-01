from steam_key import key
import json, urllib.request

def api_request(url):
    response = urllib.request.urlopen(url)
    contents = response.read()
    data = json.loads(contents)
    response.close()
    return data


class profile:

    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.data = api_request("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s" % (key, steam_id))
        self.player = self.data["response"]["players"][0]
        self.profile_name = self.player["personaname"]
        self.real_name = self.player["realname"]
        self.profile_url = self.player["profileurl"]
        self.avatar = self.player["avatarfull"]

class game:
    def __init__(self, game_id):
        self.game_id = game_id
        self.data = api_request("http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key=%s&appid=%s" % (key, game_id))
        self.game = self.data["game"]
        self.game_name = self.game["gameName"]
        self.achievements = self.game["availableGameStats"]["achievements"]

class achievement:
    def __init__(self, game, achievement_id):
        self.achievement_id = achievement_id
        self.achievements = game.achievements
        x = 0
        for iachievement in self.achievements:
            if not iachievement["name"] == achievement_id:
                x += 1
            else:
                break
        print("Achievement Position: " + str(x))
        self.achievement_id_json = self.achievements[x]["name"]
        self.achievement_name = self.achievements[x]["displayName"]
        self.achievement_description = self.achievements[x]["description"]
        self.achievement_hidden = self.achievements[x]["hidden"]
        self.achievement_icon = self.achievements[x]["icon"]
        self.achievement_icon_grey = self.achievements[x]["icongray"]