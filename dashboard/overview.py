import streamlit as st
import plotly.express as px

from config import (
    trendFeatures,
    colors
)

from utils import (
    display_hero,
    get_available_features,
    style_plotly_chart
)

def render(df):

    display_hero(
        title="🏒 Penn State Hockey Analytics",

        subtitle=(
            "A game-level analytics platform for exploring team performance, identifying the strongest drivers of winning, and presenting machine learning insights through an interactive dashboard."
        ),

        page_label="Season Overview"
    )

    total_games = len(df)

    total_wins = int(df["Win"].sum())

    total_losses = total_games - total_wins

    win_percentage = (
        total_wins /
        total_games *
        100
        if total_games > 0
        else 0
    )

    st.subheader("Team Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Games", total_games)

    col2.metric("Wins", total_wins)

    col3.metric("Losses", total_losses)

    col4.metric(
        "Win Percentage",
        f"{win_percentage:.1f}%"
    )

    metrics = []

    if "PSU Goals" in df.columns:

        metrics.append(
            (
                "Goals / Game",
                f"{df['PSU Goals'].mean():.2f}"
            )
        )

    if "PSU Shots on Goal" in df.columns:

        metrics.append(
            (
                "Shots / Game",
                f"{df['PSU Shots on Goal'].mean():.2f}"
            )
        )

    if "PSU Shooting %" in df.columns:

        metrics.append(
            (
                "Shooting %",
                f"{df['PSU Shooting %'].mean():.2f}%"
            )
        )

    if "PSU Save %" in df.columns:

        metrics.append(
            (
                "Save %",
                f"{df['PSU Save %'].mean():.3f}"
            )
        )

    if metrics:

        st.subheader("Season Averages")

        cols = st.columns(len(metrics))

        for column, metric in zip(cols, metrics):

            name, value = metric

            column.metric(name, value)

    st.divider()

    st.subheader("Season Trends")

    st.write(
        "Explore how Penn State's performance changed throughout the season."
    )

    trend_features = get_available_features(
        df,
        trendFeatures
    )

    if not trend_features:

        st.warning(
            "No supported statistics were found."
        )

    else:

        selected_trend = st.selectbox(
            "Statistic",
            trend_features
        )

        trend_columns = [
            "Game Number",
            "Opponent",
            "Win",
            selected_trend
        ]

        if "Season" in df.columns:

            trend_columns.append("Season")

        trend_df = df[
            trend_columns
        ].copy()

        trend_df["Result"] = trend_df["Win"].map(
            {
                1: "Win",
                0: "Loss"
            }
        )

        hover_columns = [
            "Opponent",
            "Result"
        ]

        if "Season" in trend_df.columns:

            hover_columns.append("Season")

        fig = px.line(

            trend_df,

            x="Game Number",

            y=selected_trend,

            markers=True,

            custom_data=hover_columns,

            title=f"{selected_trend} Throughout the Season"

        )

        fig.update_traces(

            line=dict(
                color=colors["primary"],
                width=3
            ),

            marker=dict(

                size=8,

                color="white",

                line=dict(
                    color=colors["primary"],
                    width=2
                )

            )

        )

        fig.update_layout(

            hovermode="x unified",

            xaxis_title="Game",

            yaxis_title=selected_trend

        )

        if selected_trend in [

            "Goal Differential",

            "Shot Differential",

            "Faceoff Differential"

        ]:

            fig.add_hline(

                y=0,

                line_dash="dash",

                line_color=colors["muted"]

            )

        fig = style_plotly_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("Game Dataset")

    st.write(
        "Complete combined dataset used throughout the dashboard."
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

