import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Penn State Hockey Analytics",
    page_icon="🏒",
    layout="wide"
)


# ---------------------------------------------------------
# DASHBOARD STYLING
# ---------------------------------------------------------

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

            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
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


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    file_path = (
        "data/processed/"
        "penn_state_processed_combined_stats.csv"
    )

    try:
        data = pd.read_csv(file_path)

        return data

    except FileNotFoundError:

        st.error(
            "The combined dataset could not be found. "
            "Run the app from the main project folder and confirm that "
            "`data/processed/"
            "penn_state_processed_combined_stats.csv` exists."
        )

        st.stop()

    except pd.errors.EmptyDataError:

        st.error(
            "The combined dataset exists, but it is empty."
        )

        st.stop()

    except Exception as error:

        st.error(
            f"An error occurred while loading the dataset: {error}"
        )

        st.stop()


df = load_data()


# Create a sequential game number for trend visualizations

df = df.reset_index(drop=True)

df["Game Number"] = range(
    1,
    len(df) + 1
)


# ---------------------------------------------------------
# VALIDATE DATASET
# ---------------------------------------------------------

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
        "The dataset is missing these required columns: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.markdown(
    "## 🏒 Hockey Analytics"
)

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

    Game-level performance, win-loss trends, location analysis,
    feature importance, and predictive modeling.
    """
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

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
        ),

        hoverlabel=dict(
            bgcolor="#10233b",
            font_color="#ffffff",
            bordercolor="#38bdf8"
        )
    )

    return fig


def display_hero(
    title,
    subtitle,
    page_label
):

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="page-label">
                {page_label}
            </div>

            <div class="hockey-accent"></div>

            <h1>
                {title}
            </h1>

            <p class="hero-subtitle">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
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


def get_location_colors(locations):

    location_color_map = {
        "Home": "#38bdf8",
        "Away": "#2563eb",
        "Neutral": "#94a3b8",

        "home": "#38bdf8",
        "away": "#2563eb",
        "neutral": "#94a3b8"
    }

    return [
        location_color_map.get(
            str(location),
            "#7dd3fc"
        )
        for location in locations
    ]


# ---------------------------------------------------------
# SEASON OVERVIEW PAGE
# ---------------------------------------------------------

if page == "Season Overview":

    display_hero(
        title="🏒 Penn State Hockey Analytics",

        subtitle=(
            "A game-level analytics platform for exploring team "
            "performance, identifying the strongest drivers of winning, "
            "and presenting machine-learning insights through an "
            "efficient and interactive dashboard."
        ),

        page_label="Season Overview"
    )


    # -----------------------------------------------------
    # TEAM SNAPSHOT
    # -----------------------------------------------------

    total_games = len(df)

    total_wins = int(
        df["Win"].sum()
    )

    total_losses = (
        total_games
        - total_wins
    )

    win_percentage = (
        total_wins
        / total_games
        * 100
        if total_games > 0
        else 0
    )


    st.subheader(
        "Team Snapshot"
    )

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


    # -----------------------------------------------------
    # ADDITIONAL TEAM METRICS
    # -----------------------------------------------------

    snapshot_metrics = []

    if "PSU Goals" in df.columns:

        snapshot_metrics.append(
            (
                "Goals Per Game",
                f"{df['PSU Goals'].mean():.2f}"
            )
        )

    if "PSU Shots on Goal" in df.columns:

        snapshot_metrics.append(
            (
                "Shots Per Game",
                f"{df['PSU Shots on Goal'].mean():.2f}"
            )
        )

    if "PSU Shooting %" in df.columns:

        snapshot_metrics.append(
            (
                "Average Shooting %",
                f"{df['PSU Shooting %'].mean():.2f}%"
            )
        )

    if "PSU Save %" in df.columns:

        snapshot_metrics.append(
            (
                "Average Save %",
                f"{df['PSU Save %'].mean():.3f}"
            )
        )


    if snapshot_metrics:

        st.subheader(
            "Season Averages"
        )

        average_columns = st.columns(
            len(snapshot_metrics)
        )

        for column, metric in zip(
            average_columns,
            snapshot_metrics
        ):

            metric_name, metric_value = metric

            column.metric(
                label=metric_name,
                value=metric_value
            )


    st.divider()


    # -----------------------------------------------------
    # SEASON TRENDS
    # -----------------------------------------------------

    st.subheader(
        "Season Trends"
    )

    st.write(
        "Select a game statistic to examine how Penn State's "
        "performance changed throughout the season."
    )


    possible_trend_features = [
        "PSU Goals",
        "Opponent Goals",
        "Goal Differential",

        "PSU Shots on Goal",
        "Opponent Shots on Goal",
        "Shot Differential",

        "PSU Total Shot Attempts",
        "Opponent Total Shot Attempts",

        "PSU Faceoffs Won",
        "Opponent Faceoffs Won",

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


    trend_features = get_available_features(
        df,
        possible_trend_features
    )


    if not trend_features:

        st.warning(
            "No supported numeric statistics were found "
            "for the season trend chart."
        )

    else:

        selected_trend = st.selectbox(
            "Select a statistic",
            trend_features,
            key="season_trend_selector"
        )


        trend_columns = [
            "Game Number",
            "Opponent",
            "Win",
            selected_trend
        ]


        if "Season" in df.columns:

            trend_columns.append(
                "Season"
            )


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

            hover_columns.append(
                "Season"
            )


        fig = px.line(
            trend_df,

            x="Game Number",
            y=selected_trend,

            markers=True,

            custom_data=hover_columns,

            title=(
                f"{selected_trend} "
                "Throughout the Combined Seasons"
            )
        )


        if "Season" in trend_df.columns:

            hover_template = (
                "<b>Game %{x}</b><br>"
                "Opponent: %{customdata[0]}<br>"
                "Result: %{customdata[1]}<br>"
                "Season: %{customdata[2]}<br>"
                f"{selected_trend}: %{{y:.2f}}"
                "<extra></extra>"
            )

        else:

            hover_template = (
                "<b>Game %{x}</b><br>"
                "Opponent: %{customdata[0]}<br>"
                "Result: %{customdata[1]}<br>"
                f"{selected_trend}: %{{y:.2f}}"
                "<extra></extra>"
            )


        fig.update_traces(
            line=dict(
                width=3,
                color="#38bdf8"
            ),

            marker=dict(
                size=8,
                color="#ffffff",

                line=dict(
                    width=2,
                    color="#38bdf8"
                )
            ),

            hovertemplate=hover_template
        )


        fig.update_layout(
            xaxis_title="Game Number",
            yaxis_title=selected_trend,
            hovermode="x unified"
        )


        differential_features = [
            "Goal Differential",
            "Shot Differential",
            "Faceoff Differential"
        ]


        if selected_trend in differential_features:

            fig.add_hline(
                y=0,

                line_dash="dash",
                line_color="#94a3b8",

                annotation_text="Even",
                annotation_position="top left"
            )


        fig = style_plotly_chart(
            fig
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.divider()


    # -----------------------------------------------------
    # GAME DATASET
    # -----------------------------------------------------

    st.subheader(
        "Game Dataset"
    )

    st.write(
        "Preview the combined game-level dataset used throughout "
        "the analysis and machine-learning pipeline."
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# PERFORMANCE ANALYSIS PAGE
# ---------------------------------------------------------

elif page == "Performance Analysis":

    display_hero(
        title="📊 Performance Analysis",

        subtitle=(
            "Compare Penn State's statistics across game outcomes "
            "and locations to identify performance patterns associated "
            "with successful results."
        ),

        page_label="Team Performance"
    )


    possible_features = [
        "PSU Goals",
        "Opponent Goals",
        "Goal Differential",

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


    comparison_features = get_available_features(
        df,
        possible_features
    )


    # -----------------------------------------------------
    # WIN VS LOSS COMPARISON
    # -----------------------------------------------------

    st.subheader(
        "Wins vs Losses"
    )

    st.write(
        "Compare average game statistics between Penn State wins "
        "and losses."
    )


    if not comparison_features:

        st.warning(
            "No supported comparison columns were found "
            "in the dataset."
        )

    else:

        selected_feature = st.selectbox(
            "Select a statistic to compare",
            comparison_features,
            key="win_loss_feature"
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


        comparison_df = comparison_df.sort_values(
            "Win"
        )


        fig = px.bar(
            comparison_df,

            x="Result",
            y=selected_feature,

            text_auto=".2f",

            title=(
                f"Average {selected_feature}: "
                "Wins vs Losses"
            )
        )


        fig.update_traces(
            marker_color=[
                "#64748b",
                "#38bdf8"
            ],

            marker_line_color="#e0f2fe",
            marker_line_width=1
        )


        fig.update_layout(
            xaxis_title="Game Result",
            yaxis_title=f"Average {selected_feature}",
            showlegend=False
        )


        fig = style_plotly_chart(
            fig
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        display_comparison_df = comparison_df[
            [
                "Result",
                selected_feature
            ]
        ].copy()


        display_comparison_df[selected_feature] = (
            display_comparison_df[selected_feature]
            .round(2)
        )


        with st.expander(
            "View win-loss comparison table"
        ):

            st.dataframe(
                display_comparison_df,
                use_container_width=True,
                hide_index=True
            )


    st.divider()


    # -----------------------------------------------------
    # LOCATION ANALYSIS
    # -----------------------------------------------------

    st.subheader(
        "Performance by Game Location"
    )

    st.write(
        "Compare Penn State's performance across home, away, "
        "and neutral-site games."
    )


    if "Location" not in df.columns:

        st.warning(
            "The dataset does not contain a Location column."
        )

    else:

        possible_location_features = [
            "PSU Goals",
            "Opponent Goals",
            "Goal Differential",

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


        location_features = get_available_features(
            df,
            possible_location_features
        )


        if not location_features:

            st.warning(
                "No supported statistics were found "
                "for location analysis."
            )

        else:

            selected_location_feature = st.selectbox(
                "Select a location statistic",
                location_features,
                key="location_feature"
            )


            location_summary = (
                df.groupby(
                    "Location",
                    dropna=False
                )[selected_location_feature]
                .mean()
                .reset_index()
            )


            location_summary[
                selected_location_feature
            ] = (
                location_summary[
                    selected_location_feature
                ]
                .round(2)
            )


            location_colors = get_location_colors(
                location_summary["Location"]
            )


            fig = px.bar(
                location_summary,

                x="Location",
                y=selected_location_feature,

                text_auto=".2f",

                title=(
                    f"Average {selected_location_feature} "
                    "by Game Location"
                )
            )


            fig.update_traces(
                marker_color=location_colors,

                marker_line_color="#e0f2fe",
                marker_line_width=1
            )


            fig.update_layout(
                xaxis_title="Game Location",
                yaxis_title=selected_location_feature,
                showlegend=False
            )


            fig = style_plotly_chart(
                fig
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


            with st.expander(
                "View location comparison table"
            ):

                st.dataframe(
                    location_summary,
                    use_container_width=True,
                    hide_index=True
                )


        st.divider()


        # -------------------------------------------------
        # WIN PERCENTAGE BY LOCATION
        # -------------------------------------------------

        st.subheader(
            "Win Percentage by Location"
        )


        win_location = (
            df.groupby(
                "Location",
                dropna=False
            )["Win"]
            .agg(
                Games="count",
                Wins="sum",
                Win_Percentage="mean"
            )
            .reset_index()
        )


        win_location["Win Percentage"] = (
            win_location["Win_Percentage"]
            * 100
        ).round(1)


        win_location["Label"] = (
            win_location["Win Percentage"]
            .astype(str)
            + "%"
        )


        win_location_colors = get_location_colors(
            win_location["Location"]
        )


        fig = px.bar(
            win_location,

            x="Location",
            y="Win Percentage",

            text="Label",

            custom_data=[
                "Games",
                "Wins"
            ],

            title="Penn State Win Percentage by Game Location"
        )


        fig.update_traces(
            marker_color=win_location_colors,

            marker_line_color="#e0f2fe",
            marker_line_width=1,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Games: %{customdata[0]}<br>"
                "Wins: %{customdata[1]}<br>"
                "Win Percentage: %{y:.1f}%"
                "<extra></extra>"
            )
        )


        fig.update_layout(
            xaxis_title="Game Location",
            yaxis_title="Win Percentage (%)",
            yaxis_range=[
                0,
                100
            ],
            showlegend=False
        )


        fig = style_plotly_chart(
            fig
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        display_win_location = win_location[
            [
                "Location",
                "Games",
                "Wins",
                "Win Percentage"
            ]
        ].copy()


        with st.expander(
            "View location win-percentage table"
        ):

            st.dataframe(
                display_win_location,
                use_container_width=True,
                hide_index=True
            )


# ---------------------------------------------------------
# MACHINE LEARNING PAGE
# ---------------------------------------------------------

elif page == "Machine Learning":

    display_hero(
        title="🤖 Machine Learning",

        subtitle=(
            "Review the predictive modeling pipeline, model performance, "
            "evaluation metrics, and the features used to estimate "
            "Penn State game outcomes."
        ),

        page_label="Predictive Modeling"
    )


    model_columns = st.columns(3)

    model_columns[0].metric(
        label="Models Trained",
        value="4"
    )

    model_columns[1].metric(
        label="Prediction Target",
        value="Win / Loss"
    )

    model_columns[2].metric(
        label="Dataset Size",
        value=len(df)
    )


    st.divider()


    st.subheader(
        "Models Included"
    )


    model_names = [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Gradient Boosting"
    ]


    model_display_columns = st.columns(4)


    for column, model_name in zip(
        model_display_columns,
        model_names
    ):

        column.markdown(
            f"""
            <div class="section-card">
                <strong>{model_name}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    st.subheader(
        "Model Evaluation"
    )


    st.info(
        "The machine-learning evaluation charts will be connected "
        "to the saved model results and trained model files in the "
        "next dashboard step."
    )


    st.write(
        """
        This section will include:

        - model accuracy comparisons
        - precision, recall, and F1 scores
        - confusion matrix results
        - Random Forest feature importance
        - an interactive game outcome predictor
        """
    )


# ---------------------------------------------------------
# GAME EXPLORER PAGE
# ---------------------------------------------------------

elif page == "Game Explorer":

    display_hero(
        title="🔎 Game Explorer",

        subtitle=(
            "Filter Penn State games by opponent, outcome, and location, "
            "then inspect individual game-level performance statistics."
        ),

        page_label="Interactive Game Search"
    )


    filter_col1, filter_col2, filter_col3 = st.columns(3)


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


    if "Location" in df.columns:

        location_options = [
            "All Locations"
        ] + sorted(
            df["Location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    else:

        location_options = [
            "All Locations"
        ]


    selected_location = filter_col3.selectbox(
        "Location",
        location_options
    )


    filtered_df = df.copy()


    if selected_opponent != "All Opponents":

        filtered_df = filtered_df[
            filtered_df["Opponent"]
            .astype(str)
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


    if (
        selected_location != "All Locations"
        and "Location" in filtered_df.columns
    ):

        filtered_df = filtered_df[
            filtered_df["Location"]
            .astype(str)
            == selected_location
        ]


    st.divider()


    result_col1, result_col2, result_col3 = st.columns(3)


    result_col1.metric(
        label="Matching Games",
        value=len(filtered_df)
    )


    selected_wins = (
        int(filtered_df["Win"].sum())
        if len(filtered_df) > 0
        else 0
    )


    result_col2.metric(
        label="Wins in Selection",
        value=selected_wins
    )


    selected_win_percentage = (
        selected_wins
        / len(filtered_df)
        * 100
        if len(filtered_df) > 0
        else 0
    )


    result_col3.metric(
        label="Selection Win Percentage",
        value=f"{selected_win_percentage:.1f}%"
    )


    st.subheader(
        "Filtered Games"
    )


    if filtered_df.empty:

        st.warning(
            "No games match the selected filters."
        )

    else:

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )