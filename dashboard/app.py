import pandas as pd
import plotly.express as px
import streamlit as st

##page configuration
st.set_page_config(
    page_title = "Penn State Hockey analytics", 
    page_icon = "🏒",
    layout = "wide"
)

##styling and design of the dashboard
st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(49, 130, 206, 0.14),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #07111f 0%,
                    #0b1728 55%,
                    #0d1b2e 100%
                );
            color: #f8fafc;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #f8fafc !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                         sans-serif;
            letter-spacing: -0.02em;
        }

        h1 {
            font-weight: 800 !important;
        }

        h2, h3 {
            font-weight: 700 !important;
        }

        p, label, .stMarkdown {
            color: #dbeafe;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                #06101d 0%,
                #0a192b 100%
            );
            border-right: 1px solid rgba(147, 197, 253, 0.18);
        }

        section[data-testid="stSidebar"] * {
            color: #eaf4ff;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(
                145deg,
                rgba(18, 42, 70, 0.96),
                rgba(10, 27, 47, 0.96)
            );
            border: 1px solid rgba(125, 211, 252, 0.22);
            border-radius: 16px;
            padding: 1.1rem 1.2rem;
            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }

        div[data-testid="stMetric"]:hover {
            border-color: rgba(125, 211, 252, 0.55);
            transform: translateY(-2px);
            transition: 0.2s ease;
        }

        div[data-testid="stMetricLabel"] {
            color: #9ec5e8;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff;
            font-weight: 800;
        }

        hr {
            border-color: rgba(148, 163, 184, 0.18);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(125, 211, 252, 0.18);
            border-radius: 14px;
            overflow: hidden;
        }

        div[data-baseweb="select"] > div {
            background-color: #10233b;
            border-color: rgba(125, 211, 252, 0.25);
            color: white;
            border-radius: 10px;
        }

        div[role="radiogroup"] label {
            background-color: rgba(255, 255, 255, 0.025);
            border-radius: 10px;
            padding: 0.45rem 0.6rem;
            margin-bottom: 0.25rem;
        }

        div[role="radiogroup"] label:hover {
            background-color: rgba(56, 189, 248, 0.10);
        }

        .stButton > button {
            background: linear-gradient(
                90deg,
                #0ea5e9,
                #2563eb
            );
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.2rem;
            font-weight: 700;
        }

        .stButton > button:hover {
            box-shadow: 0 8px 22px rgba(14, 165, 233, 0.25);
            transform: translateY(-1px);
        }

        .hockey-accent {
            width: 72px;
            height: 5px;
            border-radius: 999px;
            background: linear-gradient(
                90deg,
                #ffffff,
                #7dd3fc,
                #2563eb
            );
            margin-bottom: 1.25rem;
        }

        .hero-card {
            background: linear-gradient(
                135deg,
                rgba(20, 47, 78, 0.96),
                rgba(8, 24, 43, 0.96)
            );
            border: 1px solid rgba(125, 211, 252, 0.22);
            border-radius: 22px;
            padding: 1.8rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
        }

        .hero-subtitle {
            color: #b9d8f2;
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 950px;
        }

        .section-card {
            background: rgba(11, 31, 52, 0.72);
            border: 1px solid rgba(125, 211, 252, 0.16);
            border-radius: 18px;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
        }

        .page-label {
            color: #7dd3fc;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


##loading the data
def load_data():

    filePath = "data/processed/penn_state_processed_combined_stats.csv"

    try:
        data = pd.read_csv(filePath)
        return data
    except FileNotFoundError:
        st.error(
            "The combined dataset could not be found. "
            "Run the app from the main project folder and confirm that "
            "`data/processed/penn_state_processed_combined_stats.csv` exists."
        )
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("The combined dataset exists, but it is empty.")
        st.stop()
    except Exception as error:
        st.error(f"An error occurred while loading the dataset: {error}")
        st.stop()

df = load_data()


##defining important columns  
required_columns = ["Win", "Opponent"]

missing_columns = [column for column in required_columns if column not in df.columns]

if missing_columns:
    st.error(
        "The dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


##making a sidebar 
st.sidebar.markdown("## 🏒 Hockey Analytics")

st.sidebar.caption(
    "Penn State Men's Hockey performance dashboard"
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Season Overview",
        "Performance Analysis",
        "Machine Learning",
        "Game Explorer"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    **Dashboard focus**

    Game-level performance, win-loss trends, feature importance,
    and predictive modeling.
    """
)


##helper functions 
def style_plotly_chart(fig):
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
        )
    )

    return fig


def display_hero(title, subtitle, page_label):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="page-label">{page_label}</div>
            <div class="hockey-accent"></div>
            <h1>{title}</h1>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


##season overview page
if page == "Season Overview":

    display_hero(
        title="🏒 Penn State Hockey Analytics",
        subtitle=(
            "A game-level analytics platform for exploring team performance, "
            "identifying the strongest drivers of winning, and presenting "
            "machine-learning insights through an efficient and interactive "
            "dashboard."
        ),
        page_label="Season Overview"
    )

    total_games = len(df)
    total_wins = int(df["Win"].sum())
    total_losses = total_games - total_wins

    win_percentage = (
        (total_wins / total_games) * 100
        if total_games > 0
        else 0
    )

    st.subheader("Team Snapshot")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Games",
        value=total_games
    )

    col2.metric(
        label="Wins",
        value=total_wins
    )

    col3.metric(
        label="Losses",
        value=total_losses
    )

    col4.metric(
        label="Win Percentage",
        value=f"{win_percentage:.1f}%"
    )

    st.divider()

    st.subheader("Game Dataset")

    st.write(
        "Preview the combined game-level dataset used throughout the "
        "analysis and machine-learning pipeline."
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


##performance analysis page
elif page == "Performance Analysis":

    display_hero(
        title="📊 Performance Analysis",
        subtitle=(
            "Compare Penn State's average game statistics in wins and losses "
            "to identify the metrics most closely associated with successful "
            "outcomes."
        ),
        page_label="Win-Loss Comparison"
    )

    possible_features = [
        "PSU Shots on Goal",
        "Opponent Shots on Goal",
        "Shot Differential",
        "PSU Faceoff %",
        "Opponent Faceoff %",
        "Faceoff Differential",
        "PSU Shooting %",
        "Opponent Shooting %",
        "PSU Save %",
        "Opponent Save %",
        "PSU Blocks",
        "Opponent Blocks",
        "PSU Penalty Minutes",
        "Opponent Penalty Minutes"
    ]

    comparison_features = [
        feature
        for feature in possible_features
        if feature in df.columns
    ]

    if not comparison_features:
        st.warning(
            "No supported comparison columns were found in the dataset."
        )

    else:
        selected_feature = st.selectbox(
            "Select a statistic to compare",
            comparison_features
        )

        comparison_df = (
            df.groupby("Win")[selected_feature]
            .mean()
            .reset_index()
        )

        comparison_df["Result"] = comparison_df["Win"].map({
            0: "Loss",
            1: "Win"
        })

        comparison_df = comparison_df.sort_values("Win")

        fig = px.bar(
            comparison_df,
            x="Result",
            y=selected_feature,
            text_auto=".2f",
            title=f"Average {selected_feature}: Wins vs Losses"
        )

        fig.update_traces(
            marker_color=["#64748b", "#38bdf8"],
            marker_line_color="#e0f2fe",
            marker_line_width=1
        )

        fig.update_layout(
            xaxis_title="Game Result",
            yaxis_title=f"Average {selected_feature}",
            showlegend=False
        )

        fig = style_plotly_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader("Comparison Table")

        display_comparison_df = comparison_df[
            ["Result", selected_feature]
        ].copy()

        display_comparison_df[selected_feature] = (
            display_comparison_df[selected_feature].round(2)
        )

        st.dataframe(
            display_comparison_df,
            use_container_width=True,
            hide_index=True
        )

##ml page
elif page == "Machine Learning":

    display_hero(
        title="🤖 Machine Learning",
        subtitle=(
            "Review model performance, evaluation metrics, and the game "
            "features that contribute most strongly to win prediction."
        ),
        page_label="Predictive Modeling"
    )

    st.info(
        "Machine-learning evaluation and feature-importance "
        "visualizations will be added next."
    )

    model_columns = st.columns(3)

    model_columns[0].metric(
        "Models Trained",
        "4"
    )

    model_columns[1].metric(
        "Target",
        "Win / Loss"
    )

    model_columns[2].metric(
        "Dataset Size",
        len(df)
    )

    st.divider()

    st.subheader("Planned Model Dashboard")

    st.write(
        """
        This page will contain:

        - model accuracy comparisons
        - precision, recall, and F1 scores
        - confusion matrix results
        - Random Forest feature importance
        - an interactive game outcome predictor
        """
    )


##game explorer page
elif page == "Game Explorer":

    display_hero(
        title="Game Explorer",
        subtitle=(
            "Filter Penn State games by opponent and outcome, then inspect "
            "individual game-level performance statistics."
        ),
        page_label="Interactive Game Search"
    )

    filter_col1, filter_col2 = st.columns(2)

    opponent_options = [
        "All Opponents"
    ] + sorted(
        df["Opponent"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_opponent = filter_col1.selectbox(
        "Opponent",
        opponent_options
    )

    selected_result = filter_col2.selectbox(
        "Result",
        [
            "All Games",
            "Wins",
            "Losses"
        ]
    )

    filtered_df = df.copy()

    if selected_opponent != "All Opponents":
        filtered_df = filtered_df[
            filtered_df["Opponent"].astype(str)
            == selected_opponent
        ]

    if selected_result == "Wins":
        filtered_df = filtered_df[
            filtered_df["Win"] == 1
        ]

    elif selected_result == "Losses":
        filtered_df = filtered_df[
            filtered_df["Win"] == 0
        ]

    st.divider()

    result_col1, result_col2 = st.columns(2)

    result_col1.metric(
        "Matching Games",
        len(filtered_df)
    )

    result_col2.metric(
        "Wins in Selection",
        int(filtered_df["Win"].sum())
        if len(filtered_df) > 0
        else 0
    )

    st.subheader("Filtered Games")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )