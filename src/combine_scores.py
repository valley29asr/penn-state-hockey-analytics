import pandas as pd

season2024_2025 = pd.read_csv("data/processed/penn_state_processed_stats_2025_2026.csv")
season2025_2026 = pd.read_csv("data/processed/penn_state_processed_stats_2025_2026.csv")

#checking if both of the seasons have the same columns just to make sure 
print("Columns match:", list(season2025_2026.columns) == list(season2024_2025.columns))

if list(season2024_2025.columns) != list(season2025_2026.columns):

    print("\nOnly in 2024-25:")
    print(
        set(season2024_2025.columns)
        - set(season2025_2026.columns)
    )

    print("\nOnly in 2025-26:")
    print(
        set(season2025_2026.columns)
        - set(season2024_2025.columns)
    )

    raise ValueError(
        "The two processed files do not have matching columns."
    )


season2024_2025["Season"] = "2024-2025"
season2025_2026["Season"] = "2025-2026"

combined_df = pd.concat([season2025_2026, season2024_2025], ignore_index=True)
combined_df.to_csv("data/processed/penn_state_processed_combined_stats.csv", index=False)