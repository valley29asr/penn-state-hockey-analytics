import json

##creating a function to parse through the game stats and get team specific stats
def parse_stats(game):
    competitors = game["data"]["competitors"]
    penn_state_stats = None
    opponent_stats = None

    for team in competitors:
        is_penn_state =  team["nameTabular"] == "Penn St."

        for stat_entry in team["teamStats"]:
            if stat_entry["period"] == 0:
                stats = stat_entry["statistic"]

                team_game_stats = {
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

                if is_penn_state:
                    penn_state_stats = team_game_stats
                else:
                    opponent_stats = team_game_stats
                
    if penn_state_stats is None or opponent_stats is None:
        return None
    
    combined_stats = {}

    for key, value in penn_state_stats.items():
        combined_stats[f"PSU {key}"] = value
    
    for key, value in opponent_stats.items():
        combined_stats[f"Opponent {key}"] = value

    return combined_stats

if __name__ == "__main__":
    with open("sample_game.json", "r", encoding = "utf-8") as file:
        game = json.load(file)

    game_stats = parse_stats(game)

    print(game_stats)
