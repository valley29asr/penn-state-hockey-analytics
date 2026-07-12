'''
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://wmt.games/gopsusports/stats/match/full/5722151"

response = requests.get(url)

print("Status code:", response.status_code)
print("Page length:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")

print("Page title:", soup.title.text if soup.title else "No title")


tables = soup.find_all("table")
print("Tables found:", len(tables))


scripts = soup.find_all("script")
print("Scripts found:", len(scripts))

for i, script in enumerate(scripts):
    source = script.get('src')

    if source and "_nuxt" in source:
        full_url = urljoin(url, source)

        print("Downloading:", full_url)

        js_response = requests.get(full_url)
        filename = f"wmt_script_{i}.js"

        with open(filename, "w", encoding = "utf-8") as f:
            f.write(js_response.text)

        print("Saved:" ,  filename)
        print("Length:", len(js_response.text))
        print()


'''
###the above code is for getting the url for the data related to the boxscores for one game and loading it in js files like wmt_script_5.js and so on in the main folder. 
'''
import requests
import json

url = "https://api.wmt.games/api/statistics/games/5722151"

response = requests.get(url)
data = response.json()

with open("sample_game.json", "w") as f:
    json.dump(data, f, indent = 4)


print("Status Code:", response.status_code)
print("Content type:", response.headers.get("content-type"))
print("Response length:", len(response.text))
print()
print(response.text[:2000])

'''
###############################################################################################################################

###Got the json file with the boxscore data. Inspecting the top-level structure and both teams 

import requests 
import json

url = "https://api.wmt.games/api/statistics/games/5722151"

response = requests.get(url)
response.raise_for_status()

game_data = response.json()["data"]
competitors = game_data["competitors"]

penn_state = None

for competitor in competitors:
    if competitor["nameTabular"] == "Penn St.":
        penn_state = competitor
        break


if penn_state is None:
    raise ValueError("Penn State was not found in this game")

full_game_stats = None

for stat_section in penn_state["teamStats"]:
    if stat_section["period"] == 0:
        full_game_stats = stat_section["statistic"]
        break

if full_game_stats is None:
    raise ValueError("Full-game statistics were not found")

print("Opponent:", [team["nameTabular"] for team in competitors if team["nameTabular"] != "Penn St."][0])

print("Penn State score:", penn_state["score"])
print("Goals:", full_game_stats.get("sGoals", 0))
print("Shots on Goal:", full_game_stats.get("sShotAttempts", 0))
print("Total Shot Attempts:", full_game_stats.get("sTotalShotAttempts",0))
print("Faceoffs Won:", full_game_stats.get("sFaceoffsWon",0))
print("Faceoffs Lost:", full_game_stats.get("sFaceoffsLost", 0))
print("Faceoff Percentage:", full_game_stats.get("sFaceoffPercentage", 0))
print("Penalties:", full_game_stats.get("sPenalties",0))
print("Penalty minutes:", full_game_stats.get("sPenaltyMinutes",0))
print("Blocks:", full_game_stats.get("sBlocks", 0))
print("Power-play opportunities:", full_game_stats.get("sTeamPowerPlayGoalAtt", 0))
print("Power-play goals:", full_game_stats.get("sPowerPlayGoals", 0))


