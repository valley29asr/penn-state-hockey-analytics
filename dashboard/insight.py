import streamlit as st 
import pandas as pd
import plotly.express as px 

def render(df):
    st.markdown(
        """
        <div class="hero-card">
            <div class="hockey-accent"></div>
            <h1 class="hero-title">🏒 Hockey Insights</h1>
            <p class="hero-subtitle">
                Explore season trends, opponent performance,
                location-based success, and the key drivers behind
                Penn State victories.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    #season comparison
    st.header("📈 Season Comparison")
    seasonSummary = df.groupby("Season").agg({"Win":"mean", "PSU Goals":"mean", "Shot Differential":"mean", "PSU Faceoff %":"mean"}).reset_index()

    seasonSummary["Win %"] = seasonSummary["Win"] * 100

    fig = px.bar(
        seasonSummary,
        x="Season",
        y="Win %",
        color="Season",
        title="Win Percentage by Season",
        text_auto=".1f",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.dataframe(
        seasonSummary.round(2),
        use_container_width=True,
    )

    st.markdown("---")

    #Location effect on performance
    st.header("🏟 Home vs Away")

    location = df.groupby("Venue_Type").agg(Games = ("Win", "count"), Wins=("Win", "sum"), WinPercentage=("Win", "mean"), GoalDifferential=("Goal Differential", "mean")).reset_index()

    location["WinPercentage"] *= 100

    fig = px.bar(
        location,
        x="Venue_Type",
        y="WinPercentage",
        color="Venue_Type",
        title="Win Percentage by Location",
        text_auto=".1f",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.dataframe(
        location.round(2),
        use_container_width=True,
    )

    st.markdown("---")

#toughest opponents
    
    st.header("💪 Toughest Opponents")

    opponents = (
        df.groupby("Opponent")
        .agg(
            Games=("Win", "count"),
            WinPercentage=("Win", "mean"),
            GoalDifferential=("Goal Differential", "mean"),
        )
        .reset_index()
    )

    opponents["WinPercentage"] *= 100

    opponents = opponents.sort_values(
        "WinPercentage"
    )

    st.dataframe(
        opponents.round(2),
        use_container_width=True,
    )

    fig = px.bar(
        opponents,
        x="Opponent",
        y="WinPercentage",
        color="GoalDifferential",
        title="Win % Against Each Opponent",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.markdown("---")

#winning formula
    
    st.header("🎯 Winning Formula")

    comparison = df.groupby("Win").mean(numeric_only=True).T

    comparison["Difference"] = comparison[1]-comparison[0]

    comparison = comparison.sort_values("Difference", ascending = False).head(10)

    fig = px.bar(comparison, x="Difference", y=comparison.index, orientation="h", title="Top Metrics That separate Wins from Losses")

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.dataframe(
        comparison.round(2),
        use_container_width=True,
    )