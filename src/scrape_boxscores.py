import pandas as pd
import requests
from bs4 import BeautifulSoup

def main():

    '''reading the games from the csv file'''
    games = pd.read_csv("data/raw/penn_state_games_2024_2025.csv")

    first_game_link = games.loc[0, "Link"]

    print("testing box score:")
    print(first_game_link)

    response = requests.get(first_game_link)
    print("Status Code:",  response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    print("Page title:")
    print(soup.title.get_text(" ", strip = True))

    tables = soup.find_all("table")
    print(f"Found {len(tables)} tables.")

    scripts = soup.find_all("script")
    
    boxscore_data = scripts[4].get_text(" ", strip = True)

    print("Length of script 5:", len(boxscore_data))

    keywords = [
        "16818",
        "boxscore",
        "score",
        "goal",
        "period",
        "home",
        "away",
        "player",
        "team",
        "stat"
    ]

    for keyword in keywords:
        position = boxscore_data.lower().find(keyword.lower())

        print(f"\n{keyword} position:", position)

        if position != -1:
            start = max(0, position - 200)
            end = position + 500

            print(boxscore_data[start:end])

if __name__ == "__main__":
    main()




