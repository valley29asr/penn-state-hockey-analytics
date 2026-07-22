import pandas as pd 
import plotly.express as px
import streamlit as st
from config import colors
from utils import display_hero, style_plotly_chart


def render(df):
    display_hero(
        title="🔎 Game Explorer",
        subtitle=("Filter the combined game dataset by opponent, result, location, and season to inspect individual performances and compare selected games."
        ),
        page_label="Game Explorer",
    )

    filtered_df = df.copy()

    st.subheader("Game Filters")

    filter_columns = st.columns(4)

    # Opponent filter
    if "Opponent" in filtered_df.columns:

        opponent_options = sorted(
            filtered_df["Opponent"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_opponents = filter_columns[0].multiselect(
            "Opponent",
            options=opponent_options,
            placeholder="All opponents",
        )

        if selected_opponents:

            filtered_df = filtered_df[
                filtered_df["Opponent"]
                .astype(str)
                .isin(selected_opponents)
            ]

    # Result filter
    result_options = [
        "Win",
        "Loss",
    ]

    selected_results = filter_columns[1].multiselect(
        "Result",
        options=result_options,
        placeholder="Wins and losses",
    )

    if selected_results:

        result_values = []

        if "Win" in selected_results:
            result_values.append(1)

        if "Loss" in selected_results:
            result_values.append(0)

        filtered_df = filtered_df[
            filtered_df["Win"].isin(result_values)
        ]

    # Location filter
    if "Location" in filtered_df.columns:

        location_options = sorted(
            filtered_df["Location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_locations = filter_columns[2].multiselect(
            "Location",
            options=location_options,
            placeholder="All locations",
        )

        if selected_locations:

            filtered_df = filtered_df[
                filtered_df["Location"]
                .astype(str)
                .isin(selected_locations)
            ]

    # Season filter
    if "Season" in filtered_df.columns:

        season_options = sorted(
            filtered_df["Season"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_seasons = filter_columns[3].multiselect(
            "Season",
            options=season_options,
            placeholder="All seasons",
        )

        if selected_seasons:

            filtered_df = filtered_df[
                filtered_df["Season"]
                .astype(str)
                .isin(selected_seasons)
            ]

    else:

        filter_columns[3].caption(
            "Season filtering is unavailable."
        )

    st.divider()

    # ---------------------------------------------------------
    # FILTERED SUMMARY
    # ---------------------------------------------------------

    st.subheader("Filtered Summary")

    total_games = len(filtered_df)
    total_wins = int(filtered_df["Win"].sum())
    total_losses = total_games - total_wins

    win_percentage = (
        total_wins / total_games * 100
        if total_games > 0
        else 0
    )

    summary_col_1, summary_col_2, summary_col_3, summary_col_4 = (
        st.columns(4)
    )

    summary_col_1.metric(
        "Games",
        total_games,
    )

    summary_col_2.metric(
        "Wins",
        total_wins,
    )

    summary_col_3.metric(
        "Losses",
        total_losses,
    )

    summary_col_4.metric(
        "Win Percentage",
        f"{win_percentage:.1f}%",
    )

    if filtered_df.empty:

        st.warning(
            "No games match the selected filters."
        )

        return

    st.divider()

    # ---------------------------------------------------------
    # RESULT DISTRIBUTION
    # ---------------------------------------------------------

    st.subheader("Result Distribution")

    result_summary = (
        filtered_df["Win"]
        .value_counts()
        .rename_axis("Win")
        .reset_index(name="Games")
    )

    result_summary["Result"] = result_summary["Win"].map(
        {
            1: "Win",
            0: "Loss",
        }
    )

    result_summary["Result"] = pd.Categorical(
        result_summary["Result"],
        categories=[
            "Win",
            "Loss",
        ],
        ordered=True,
    )

    result_summary = result_summary.sort_values(
        "Result"
    )

    result_chart = px.bar(
        result_summary,
        x="Result",
        y="Games",
        text="Games",
        title="Filtered Wins and Losses",
    )

    result_chart.update_traces(
        marker_color=[
            (
                colors["primary"]
                if result == "Win"
                else colors["loss"]
            )
            for result in result_summary["Result"]
        ],
        marker_line_color="white",
        marker_line_width=1,
    )

    result_chart = style_plotly_chart(
        result_chart
    )

    st.plotly_chart(
        result_chart,
        use_container_width=True,
    )

    st.divider()

    # ---------------------------------------------------------
    # GAME COMPARISON CHART
    # ---------------------------------------------------------

    st.subheader("Compare Games")

    numeric_columns = (
        filtered_df
        .select_dtypes(include="number")
        .columns
        .tolist()
    )

    excluded_columns = [
        "Win",
        "Game Number",
        "WMT Game ID"
    ]

    chart_options = [
        column
        for column in numeric_columns
        if column not in excluded_columns
    ]

    if chart_options:

        selected_statistic = st.selectbox(
            "Statistic to compare",
            options=chart_options,
        )

        chart_df = filtered_df.copy()

        if "Game Number" not in chart_df.columns:

            chart_df = chart_df.reset_index(
                drop=True
            )

            chart_df["Game Number"] = range(
                1,
                len(chart_df) + 1,
            )

        chart_df["Result"] = chart_df["Win"].map(
            {
                1: "Win",
                0: "Loss",
            }
        )

        hover_data = {
            "Game Number": True,
            selected_statistic: ":.2f",
            "Result": True,
        }

        if "Opponent" in chart_df.columns:
            hover_data["Opponent"] = True

        if "Season" in chart_df.columns:
            hover_data["Season"] = True

        game_chart = px.scatter(
            chart_df,
            x="Game Number",
            y=selected_statistic,
            color="Result",
            hover_data=hover_data,
            color_discrete_map={
                "Win": colors["primary"],
                "Loss": colors["loss"],
            },
            title=(
                f"{selected_statistic} Across "
                "Filtered Games"
            ),
        )

        game_chart.update_traces(
            marker={
                "size": 11,
                "line": {
                    "width": 1,
                    "color": "white",
                },
            }
        )

        game_chart = style_plotly_chart(
            game_chart
        )

        st.plotly_chart(
            game_chart,
            use_container_width=True,
        )

    else:

        st.warning(
            "No numeric statistics are available for game comparison."
        )

    st.divider()

    # ---------------------------------------------------------
    # FILTERED DATA TABLE
    # ---------------------------------------------------------

    st.subheader("Filtered Games")

    preferred_columns = [
        "Season",
        "Game Number",
        "Date",
        "Opponent",
        "Location",
        "Result",
        "PSU Goals",
        "Opponent Goals",
        "Goal Differential",
        "PSU Shots on Goal",
        "Opponent Shots on Goal",
        "Shot Differential",
        "PSU Faceoff %",
        "Opponent Faceoff %",
        "PSU Shooting %",
        "Opponent Shooting %",
        "PSU Save %",
        "Opponent Save %",
        "PSU Blocks",
        "Opponent Blocks",
        "PSU Penalty Minutes",
        "Opponent Penalty Minutes",
        "Win",
    ]

    table_columns = [
        column
        for column in preferred_columns
        if column in filtered_df.columns
    ]

    remaining_columns = [
        column
        for column in filtered_df.columns
        if column not in table_columns
    ]

    display_df = filtered_df[
        table_columns + remaining_columns
    ].copy()

    if "Win" in display_df.columns:

        display_df["Game Result"] = (
            display_df["Win"].map(
                {
                    1: "Win",
                    0: "Loss",
                }
            )
        )

        if "Win" in display_df.columns:
            display_df = display_df.drop(
                columns=["Win"]
            )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"Showing {len(display_df)} of {len(df)} total games."
    )

    # ---------------------------------------------------------
    # DOWNLOAD
    # ---------------------------------------------------------

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Games as CSV",
        data=csv_data,
        file_name="filtered_penn_state_hockey_games.csv",
        mime="text/csv",
        use_container_width=True,
    )