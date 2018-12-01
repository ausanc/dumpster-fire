from vapour import profile, game, achievement

test_profile = profile("76561198015546177")
print("Name: " + test_profile.profile_name)
print("Real Name: " + test_profile.real_name)

my_game = game("440")
achievements = my_game.get_all_achievements()
my_achievement = achievement(my_game, "TF_TEAM_PYROVISION")
