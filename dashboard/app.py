import streamlit as st

from config import navigationPages
from styles import apply_styles
from utils import load_data

import home
import overview
import performance
import machine_learning
import game_explorer
import insight


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Penn State Hockey Analytics",
    page_icon="🏒",
    layout="wide",
)

# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------

apply_styles()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = load_data()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🏒 Navigation")

page = st.sidebar.radio(
    "Choose a page",
    navigationPages,
    key = "selected_page"
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
**Penn State Hockey Analytics**

Interactive dashboard built using:

- Python
- Streamlit
- Plotly
- Scikit-Learn
- Pandas

Designed to identify the biggest
drivers of winning hockey games.
"""
)

# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

if page == "Home":

    home.render(df)

elif page == "Season Overview":

    overview.render(df)

elif page == "Performance Analysis":

    performance.render(df)

elif page == "Machine Learning":

    machine_learning.render(df)
elif page == "Hockey Insights":
    insight.render(df)

elif page == "Game Explorer":

    game_explorer.render(df)