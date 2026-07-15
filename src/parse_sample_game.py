import json

##creating a function to parse through the game stats and get team specific stats
def parse_stats(game):
    competitors = game["data"]["competitors"]

    for team in competitors:
        if team["nameTabular"] == "Penn St.":

            for stat_entry in team["teamStats"]:
                if stat_entry["period"] == 0:
                    stats = stat_entry["statistic"]

                    game_stats = {
                        "Goals": stats.get("sGoals", team.get("score", 0)),
                        "Shots on Goal": stats.get("sShotAttempts", 0),
                        "Total Shot Attempts": stats.get("sTotalShotAttempts", 0),
                        "Faceoffs Won": stats.get("sFaceoffsWon", 0),
                        "Faceoffs Lost": stats.get("sFaceoffsLost", 0),
                        "Faceoff %": round(
                            stats.get("sFaceoffPercentage", 0) * 100,
                            2
                        ),
                        "Penalty Minutes": stats.get("sPenaltyMinutes", 0),
                        "Blocks": stats.get("sBlocks", 0),
                        "Saves": stats.get("sSaves", 0),
                    }

                    return game_stats
                
    return None

if __name__ == "__main__":
    with open("sample_game.json", "r", encoding = "utf-8") as file:
        game = json.load(file)

    game_stats = parse_stats(game)

    print(game_stats)
