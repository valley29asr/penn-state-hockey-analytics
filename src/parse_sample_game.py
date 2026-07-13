import json

with open("sample_game.json", "r", encoding = "utf-8") as file:
    game = json.load(file)

competitors = game["data"]["competitors"]

for team in competitors:
    if team["nameTabular"] == "Penn St.":
        print("Found Penn State!")

        for stat_entry in team["teamStats"]:
            if stat_entry["period"] == 0:
                print("Found full-game totals!")
                stats = stat_entry["statistic"]

                print("Goals:", stats["sGoals"])
                print("Shots on goal:", stats["sShotAttempts"])
                print("Total shot attempts:", stats["sTotalShotAttempts"])
                print("Faceoffs won:", stats["sFaceoffsWon"])
                print("Faceoffs lost:", stats["sFaceoffsLost"])
                print("Faceoff percentage:", stats["sFaceoffPercentage"]*100)
                print("Penalty minutes:", stats["sPenaltyMinutes"])
                print("Blocks:", stats["sBlocks"])
                print("Saves:", stats["sSaves"])