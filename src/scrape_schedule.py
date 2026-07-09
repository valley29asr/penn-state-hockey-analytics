import pandas as pd 
import requests
from bs4 import BeautifulSoup

URL = "https://gopsusports.com/sports/mens-ice-hockey/schedule/season/2024-25"

def main():
    response = requests.get(URL)
    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")

    games = soup.find_all("div", class_ = "schedule-event__content")

    print(f"Found {len(games)} games.")

    game_rows = []

    for game in games:
        date = game.find("time").get_text(" ", strip = True)
        opponent = game.find("strong", class_= "schedule-event-item-team__name").get_text(" ", strip = True)
        location = game.find("span", class_ = "schedule-event-location schedule-event__location-text").get_text(" ", strip = True)
        result_text = game.find("div", class_ = "schedule-event-item-result__label").get_text(" ", strip = True)

        game_rows.append({
            "Date" : date, 
            "Opponent" : opponent, 
            "Location" : location, 
            "Result" : result_text
        })
    
    df = pd.DataFrame(game_rows)
    print(df.head())
    print(f"Saved {len(df)} games.")

    df.to_csv("data/raw/penn_state_games_2024_2025.csv", index = False)
    print("CSV saved successfully!")

    

if __name__ == "__main__":
    main()


