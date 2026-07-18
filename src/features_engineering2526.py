import pandas as pd

df = pd.read_csv("data/processed/penn_state_stats_2025_2026.csv")

##Outcome features
df["Win"] = df["Result"].str.startswith("W").astype(int)
df["Goal Differential"] = df["PSU Goals"] - df["Opponent Goals"]


##Shot features
df["Shot Differential"] = df["PSU Shots on Goal"] - df["Opponent Shots on Goal"]
df["Total Shots on Goal"] = df["PSU Shots on Goal"] + df["Opponent Shots on Goal"]


##Faceoff features
df["Faceoff Differential"] = df["PSU Faceoff %"] - df["Opponent Faceoff %"]


##Goaltending features
df["PSU Save %"] = (df["PSU Saves"]/df["Opponent Shots on Goal"]).round(3)
df["Opponent Save %"] = (df["Opponent Saves"]/df["PSU Shots on Goal"]).round(3)


##Venue features
home_location = ("University Park, Pa. / Pegula Ice Arena")
home_location = ("University Park, Pa. / West Shore Home Field at Beaver Stadium")

neutral_locations = [
    "Washington, D.C. / Capital One Arena",
    "Chicago, Ill. / Wrigley Field",
    "Allentown, Pa. / PPL Center",
    "Allentown, Pa. / PLL Center",
    "St. Louis, Mo. / Enterprise Center"
] 

df["Home Game"] = (df["Location"] == home_location).astype(int)
df["Venue_Type"] = "Away"
df.loc[df["Location"] == "University Park, Pa. / Pegula Ice Arena", "Venue_Type"] = "Home"
df.loc[df["Location"].isin(neutral_locations), "Venue_Type"] = "Neutral"


##Game-total features
df["Total Goals"] = df["PSU Goals"] + df["Opponent Goals"]
df["Total Penalty Minutes"] = df["PSU Penalty Minutes"] + df["Opponent Penalty Minutes"]


##Shooting efficiency
df["PSU Shooting %"] = (df["PSU Goals"]/df["PSU Shots on Goal"]) * 100
df["Opponent Shooting %"] = (df["Opponent Goals"]/df["Opponent Shots on Goal"]) * 100


##Validating new features
print("\nVenue type counts:")
print(df["Venue_Type"].value_counts())

print("\nEngineered features:")
print(
    df[
        [
            "Result",
            "Win",
            "Goal Differential",
            "Shot Differential",
            "Faceoff Differential",
            "PSU Save %",
            "Opponent Save %",
            "Home Game",
            "Venue_Type",
            "PSU Shooting %",
            "Opponent Shooting %"
        ]
    ].head()
)



df.to_csv("data/processed/penn_state_processed_stats_2025_2026.csv", index = False)



