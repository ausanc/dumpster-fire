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

    def get_all_achievements(self):
        all_achievements = []
        for x in range(0, len(self.achievements)):
            achievement_to_add = achievement(self)
            achievement_to_add.manual_init(self, x)
            all_achievements.append(achievement_to_add)
        return all_achievements

class achievement:
    def __init__(self, igame, achievement_id=0):
        self.achievement_id = achievement_id
        self.achievements = igame.achievements
        self.achievement_name = ""
        self.achievement_description = ""
        self.achievement_hidden = 0
        self.achievement_icon = ""
        self.achievement_icon_grey = ""
        if not achievement_id == 0:
            x = 0
            for iachievement in self.achievements:
                if not iachievement["name"] == achievement_id:
                    x += 1
                else:
                    break
            self.manual_init(igame, x)

    
    def manual_init(self, game, pos):
        self.achievement_id = self.achievements[pos]["name"]
        self.achievement_name = self.achievements[pos]["displayName"]
        self.achievement_description = self.achievements[pos]["description"]
        self.achievement_hidden = self.achievements[pos]["hidden"]
        self.achievement_icon = self.achievements[pos]["icon"]
        self.achievement_icon_grey = self.achievements[pos]["icongray"]

