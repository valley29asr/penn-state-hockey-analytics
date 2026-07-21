import pandas as pd 
import streamlit as st 

from config import dataPath, colors

@st.cache_data
def load_data():

    try:
        df = pd.read_csv(dataPath)

    except FileNotFoundError:

        st.error(
            "The combined dataset could not be found.\n\n Run the dashboard from the project root."
        )
        st.stop()

    except pd.errors.EmptyDataError:

        st.error("The dataset exists but is empty.")
        st.stop()

    except Exception as error:

        st.error(f"Error loading dataset:\n\n{error}")
        st.stop()

    df = df.reset_index(drop=True)

    df["Game Number"] = range(
        1,
        len(df) + 1
    )

    required_columns = [
        "Win",
        "Opponent"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        st.error(
            "Missing required columns:\n\n"
            + ", ".join(missing_columns)
        )

        st.stop()

    return df



def display_hero(title, subtitle, page_label):

    st.markdown(
        f"""
<div class="hero-card">

<div class="page-label">
{page_label}
</div>

<div class="hockey-accent"></div>

<h1>{title}</h1>

<p class="hero-subtitle">
{subtitle}
</p>

</div>
""",
        unsafe_allow_html=True,
    )


def get_available_features(
    dataframe,
    possible_features
):

    return [

        feature

        for feature in possible_features

        if feature in dataframe.columns

    ]


def get_location_colors(
    locations
):

    color_map = {

        "Home": colors["primary"],
        "Away": colors["secondary"],
        "Neutral": colors["muted"],

        "home": colors["primary"],
        "away": colors["secondary"],
        "neutral": colors["muted"]

    }

    return [

        color_map.get(
            str(location),
            colors["light"]
        )

        for location in locations

    ]


def style_plotly_chart(
    fig
):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#eaf4ff"
        ),

        title_font=dict(
            size=22,
            color="#ffffff"
        ),

        xaxis=dict(
            gridcolor="rgba(148,163,184,0.12)",
            zerolinecolor="rgba(148,163,184,0.12)"
        ),

        yaxis=dict(
            gridcolor="rgba(148,163,184,0.12)",
            zerolinecolor="rgba(148,163,184,0.12)"
        ),

        margin=dict(
            l=30,
            r=30,
            t=70,
            b=30
        ),

        hoverlabel=dict(
            bgcolor="#10233b",
            font_color="#ffffff",
            bordercolor=colors["primary"]
        )

    )

    return fig