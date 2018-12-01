from steam_key import key
import json, urllib.request, time

def api_request(url):
    response = urllib.request.urlopen(url)
    contents = response.read()
    data = json.loads(contents)
    response.close()
    return data

def get_game_id_list(profile):
    game_list = []
    data = api_request("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&format=json" % (key, profile.steam_id))
    for game_json in data["response"]["games"]:
        game_list.append(game_json["appid"])
    return game_list

def get_game_list(profile):
    game_list = []
    data = api_request("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=%s&steamid=%s&include_appinfo=1&format=json" % (key, profile.steam_id))
    for game_json in data["response"]["games"]:
        working_game = game_info()
        try:
            working_game.set_game_id(game_json["appid"])
        except KeyError:
            pass
        try:
            working_game.set_game_name(game_json["name"])
        except KeyError:
            pass
        try:
            working_game.set_game_icon(game_json["img_icon_url"])
        except KeyError:
            pass
        try:
            working_game.set_game_logo(game_json["img_logo_url"])
        except KeyError:
            pass
        try:
            working_game.set_game_playtime(game_json["playtime_forever"])
        except KeyError:
            pass
        try:
            working_game.set_game_playtime_fortnight(game_json["playtime_2weeks"])
        except KeyError:
            pass
        try:
            working_game.set_game_has_achievements(game_json["has_community_visible_stats"])
        except KeyError:
            pass 
        game_list.append(working_game)
    return game_list


class profile:

    def __init__(self, steam_id):
        self.steam_id = steam_id
        self.data = api_request("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s" % (key, steam_id))
        self.player = self.data["response"]["players"][0]
        self.profile_name = self.player["personaname"]
        self.real_name = self.player["realname"]
        self.profile_url = self.player["profileurl"]
        self.avatar = self.player["avatarfull"]

class game_info:
    def __init__(self):
        self.game_id = ""
        self.game_name = ""
        self.game_icon = ""
        self.game_logo = ""
        self.game_playtime = ""
        self.game_playtime_fortnight = ""
        self.game_has_achievements = ""

    def set_game_id(self, game_id):
        self.game_id = game_id
    def set_game_name(self, game_name):
        self.game_name = game_name
    def set_game_icon(self, game_icon):
        self.game_icon = game_icon
    def set_game_logo(self, game_logo):
        self.game_logo = game_logo
    def set_game_playtime(self, game_playtime):
        self.game_playtime = game_playtime
    def set_game_playtime_fortnight(self, game_playtime_fortnight):
        self.game_playtime_fortnight = game_playtime_fortnight
    def set_game_has_achievements(self, game_has_achievements):
        self.game_has_achievements = game_has_achievements

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

