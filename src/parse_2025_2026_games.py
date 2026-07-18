import time 
import pandas as pd 

from extract_boxscore import extract_wmt_game_id, extract_games
from parse_sample_game import parse_stats

schedulePath = "data/raw/penn_state_games_2025_2026.csv"
outputPath = "data/processed/penn_state_stats_2025_2026.csv"

def main():

    games = pd.read_csv(schedulePath)

    all_game_stats = []

    for index,row in games.iterrows():

        boxscore_url = row["Link"]

        if pd.isna(boxscore_url):
            print("Link not provided")
            continue

        try:

            game_id = extract_wmt_game_id(boxscore_url)
            game_json = extract_games(game_id)
            #print(game_json)

            
            stats = parse_stats(game_json)


            if stats is None:
                print("Skipped: no stats available")
                continue

            game_row = {
                "Date": row["Date"],
                "Opponent": row["Opponent"],
                "Location": row["Location"],
                "Result": row["Result"],
                "Box Score Link": boxscore_url,
                "WMT Game ID": game_id,
                **stats,
            }

            all_game_stats.append(game_row)
            print("Success")

        except Exception as error:
            print(f"\nFailed on {row['Opponent']} ({row['Date']})")
            print(type(error).__name__)
            print(error)

            import traceback
            traceback.print_exc()

        time.sleep(0.5)

    
    processed_df = pd.DataFrame(all_game_stats)

    processed_df.to_csv(outputPath, index = False)

if __name__ == "__main__":
    main()