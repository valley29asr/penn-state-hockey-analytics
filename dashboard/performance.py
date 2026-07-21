import streamlit as st
import plotly.express as px

from config import (performanceFeatures, colors)
from utils import (display_hero, get_available_features, get_location_colors, style_plotly_chart)

def render(df):
    display_hero(
        title="📊 Performance Analysis",

        subtitle=(
            "Compare Penn State's performance in wins, losses, and different game locations to identify what contributes most to winning."
        ),

        page_label="Performance Analysis"
    )

    st.subheader("Wins vs Losses")

    comparison_features = get_available_features(
        df,
        performanceFeatures
    )

    if not comparison_features:

        st.warning("No supported statistics found.")

        return

    selected_feature = st.selectbox(
        "Statistic",
        comparison_features,
        key="comparison_feature"
    )

    comparison_df = (
        df.groupby("Win")[selected_feature]
        .mean()
        .reset_index()
    )

    comparison_df["Result"] = comparison_df["Win"].map(
        {
            0: "Loss",
            1: "Win"
        }
    )

    fig = px.bar(

        comparison_df,

        x="Result",

        y=selected_feature,

        text_auto=".2f",

        title=f"{selected_feature}: Wins vs Losses"

    )

    fig.update_traces(

        marker_color=[
            colors["loss"],
            colors["primary"]
        ],

        marker_line_color="white",

        marker_line_width=1

    )

    fig = style_plotly_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander(
        "View Comparison Table"
    ):

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("Performance by Location")

    if "Location" not in df.columns:

        st.warning("Location column not found.")

        return

    selected_location_feature = st.selectbox(

        "Statistic by Location",

        comparison_features,

        key="location_feature"

    )

    location_summary = (

        df.groupby("Location")[selected_location_feature]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        location_summary,

        x="Location",

        y=selected_location_feature,

        text_auto=".2f",

        title=f"{selected_location_feature} by Location"

    )

    fig.update_traces(

        marker_color=get_location_colors(
            location_summary["Location"]
        ),

        marker_line_color="white",

        marker_line_width=1

    )

    fig = style_plotly_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander(
        "View Location Statistics"
    ):

        st.dataframe(
            location_summary,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("Win Percentage by Location")

    location_results = (

        df.groupby("Location")["Win"]

        .agg(
            Games="count",
            Wins="sum",
            Win_Percentage="mean"
        )

        .reset_index()

    )

    location_results["Win Percentage"] = (

        location_results["Win_Percentage"]

        * 100

    )

    location_results["Label"] = (

        location_results["Win Percentage"]

        .round(1)

        .astype(str)

        + "%"

    )

    fig = px.bar(

        location_results,

        x="Location",

        y="Win Percentage",

        text="Label"

    )

    fig.update_traces(

        marker_color=get_location_colors(
            location_results["Location"]
        )

    )

    fig.update_layout(

        yaxis_range=[0,100],

        title="Win Percentage by Location"

    )

    fig = style_plotly_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander(
        "View Win Percentage Table"
    ):

        st.dataframe(

            location_results[
                [
                    "Location",
                    "Games",
                    "Wins",
                    "Win Percentage"
                ]
            ],

            hide_index=True,

            use_container_width=True

        )