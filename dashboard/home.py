from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# =========================================================
# Navigation
# =========================================================

def go_to_page(page_name):
    st.session_state["selected_page"] = page_name


# =========================================================
# Column helpers
# =========================================================

def find_venue_column(df):
    possible_columns = [
        "Venue_Type",
        "Venue",
        "Location Type",
        "Game Location",
        "Home/Away",
        "Home Away",
        "Site",
    ]

    for column in possible_columns:
        if column in df.columns:
            return column

    return None


# =========================================================
# Insight helpers
# =========================================================

def get_top_winning_factor(df):
    """
    Compare wins and losses using standardized effect size.

    Standardization makes metrics with different units—such as
    shots, percentages, blocks, and penalty minutes—comparable.
    """

    insight_features = [
        "Shot Differential",
        "Faceoff Differential",
        "PSU Faceoff %",
        "PSU Shots on Goal",
        "Opponent Shots on Goal",
        "PSU Blocks",
        "Opponent Blocks",
        "PSU Penalty Minutes",
        "Opponent Penalty Minutes",
    ]

    available_features = [
        feature
        for feature in insight_features
        if feature in df.columns
    ]

    if (
        "Win" not in df.columns
        or not available_features
        or df["Win"].nunique() < 2
    ):
        return {
            "metric": "Not available",
            "difference": None,
            "effect_size": None,
            "wins_mean": None,
            "losses_mean": None,
        }

    results = []

    wins = df[df["Win"] == 1]
    losses = df[df["Win"] == 0]

    for feature in available_features:
        win_values = pd.to_numeric(
            wins[feature],
            errors="coerce",
        ).dropna()

        loss_values = pd.to_numeric(
            losses[feature],
            errors="coerce",
        ).dropna()

        if len(win_values) < 2 or len(loss_values) < 2:
            continue

        win_mean = win_values.mean()
        loss_mean = loss_values.mean()

        pooled_variance_numerator = (
            (len(win_values) - 1) * win_values.var(ddof=1)
            + (len(loss_values) - 1) * loss_values.var(ddof=1)
        )

        pooled_variance_denominator = (
            len(win_values)
            + len(loss_values)
            - 2
        )

        if pooled_variance_denominator <= 0:
            continue

        pooled_std = np.sqrt(
            pooled_variance_numerator
            / pooled_variance_denominator
        )

        if pooled_std == 0 or pd.isna(pooled_std):
            continue

        effect_size = (
            win_mean - loss_mean
        ) / pooled_std

        results.append(
            {
                "metric": feature,
                "difference": win_mean - loss_mean,
                "effect_size": effect_size,
                "wins_mean": win_mean,
                "losses_mean": loss_mean,
            }
        )

    if not results:
        return {
            "metric": "Not available",
            "difference": None,
            "effect_size": None,
            "wins_mean": None,
            "losses_mean": None,
        }

    result_df = pd.DataFrame(results)

    result_df["Absolute Effect"] = (
        result_df["effect_size"].abs()
    )

    strongest = result_df.sort_values(
        "Absolute Effect",
        ascending=False,
    ).iloc[0]

    return {
        "metric": strongest["metric"],
        "difference": strongest["difference"],
        "effect_size": strongest["effect_size"],
        "wins_mean": strongest["wins_mean"],
        "losses_mean": strongest["losses_mean"],
    }


def describe_metric_difference(metric, difference):
    if difference is None or pd.isna(difference):
        return "Win-loss comparison unavailable"

    absolute_difference = abs(difference)

    if "%" in metric or "Percentage" in metric:
        unit = "percentage points"

    elif "Goal" in metric:
        unit = "goals per game"

    elif "Shot" in metric:
        unit = "shots per game"

    elif "Block" in metric:
        unit = "blocks per game"

    elif "Penalty" in metric:
        unit = "penalty minutes per game"

    elif "Faceoff" in metric:
        unit = "percentage points"

    else:
        unit = "units per game"

    direction = (
        "higher"
        if difference >= 0
        else "lower"
    )

    return (
        f"{absolute_difference:.2f} {unit} "
        f"{direction} in wins"
    )


def get_best_venue(df):
    venue_column = find_venue_column(df)

    if venue_column is None or "Win" not in df.columns:
        return {
            "venue": "Not available",
            "win_rate": None,
            "games": None,
            "wins": None,
        }

    venue_summary = (
        df.groupby(venue_column)
        .agg(
            Games=("Win", "count"),
            Wins=("Win", "sum"),
            WinRate=("Win", "mean"),
        )
        .reset_index()
    )

    if venue_summary.empty:
        return {
            "venue": "Not available",
            "win_rate": None,
            "games": None,
            "wins": None,
        }

    best_row = venue_summary.sort_values(
        by=[
            "WinRate",
            "Games",
        ],
        ascending=[
            False,
            False,
        ],
    ).iloc[0]

    return {
        "venue": str(best_row[venue_column]),
        "win_rate": float(best_row["WinRate"]) * 100,
        "games": int(best_row["Games"]),
        "wins": int(best_row["Wins"]),
    }


def get_toughest_opponent(df):
    if not {
        "Opponent",
        "Win",
    }.issubset(df.columns):
        return {
            "opponent": "Not available",
            "win_rate": None,
            "games": None,
            "wins": None,
            "losses": None,
        }

    opponent_summary = (
        df.groupby("Opponent")
        .agg(
            Games=("Win", "count"),
            Wins=("Win", "sum"),
            WinRate=("Win", "mean"),
        )
        .reset_index()
    )

    # Require at least two meetings to reduce one-game noise.
    repeated_opponents = opponent_summary[
        opponent_summary["Games"] >= 2
    ]

    if not repeated_opponents.empty:
        opponent_summary = repeated_opponents

    if opponent_summary.empty:
        return {
            "opponent": "Not available",
            "win_rate": None,
            "games": None,
            "wins": None,
            "losses": None,
        }

    toughest_row = opponent_summary.sort_values(
        by=[
            "WinRate",
            "Games",
        ],
        ascending=[
            True,
            False,
        ],
    ).iloc[0]

    games = int(toughest_row["Games"])
    wins = int(toughest_row["Wins"])

    return {
        "opponent": str(toughest_row["Opponent"]),
        "win_rate": float(toughest_row["WinRate"]) * 100,
        "games": games,
        "wins": wins,
        "losses": games - wins,
    }


# =========================================================
# Model-results helper
# =========================================================

def load_best_model():
    possible_paths = [
        Path("reports/cross_validation_results.csv"),
        Path("../reports/cross_validation_results.csv"),
        Path("reports/model_results.csv"),
        Path("../reports/model_results.csv"),
        Path("reports/model_comparison.csv"),
        Path("../reports/model_comparison.csv"),
    ]

    results_path = next(
        (
            path
            for path in possible_paths
            if path.exists()
        ),
        None,
    )

    if results_path is None:
        return {
            "model": "Results unavailable",
            "f1": None,
        }

    try:
        results = pd.read_csv(results_path)

    except (OSError, pd.errors.ParserError):
        return {
            "model": "Results unavailable",
            "f1": None,
        }

    model_columns = [
        "Model",
        "Model Name",
        "model",
    ]

    f1_columns = [
        "Mean F1",
        "Mean F1 Score",
        "CV F1",
        "CV F1 Score",
        "F1 Score",
        "F1",
    ]

    model_column = next(
        (
            column
            for column in model_columns
            if column in results.columns
        ),
        None,
    )

    f1_column = next(
        (
            column
            for column in f1_columns
            if column in results.columns
        ),
        None,
    )

    if model_column is None:
        return {
            "model": "Results available",
            "f1": None,
        }

    if f1_column is None:
        return {
            "model": str(results.iloc[0][model_column]),
            "f1": None,
        }

    results[f1_column] = pd.to_numeric(
        results[f1_column],
        errors="coerce",
    )

    valid_results = results.dropna(
        subset=[f1_column]
    )

    if valid_results.empty:
        return {
            "model": "Results unavailable",
            "f1": None,
        }

    best_row = valid_results.loc[
        valid_results[f1_column].idxmax()
    ]

    return {
        "model": str(best_row[model_column]),
        "f1": float(best_row[f1_column]),
    }


# =========================================================
# Main page
# =========================================================

def render(df):
    total_games = len(df)

    total_seasons = (
        df["Season"].nunique()
        if "Season" in df.columns
        else 1
    )

    wins = (
        int(df["Win"].sum())
        if "Win" in df.columns
        else 0
    )

    win_pct = (
        df["Win"].mean() * 100
        if "Win" in df.columns
        else 0
    )

    winning_factor = get_top_winning_factor(df)
    best_venue = get_best_venue(df)
    toughest_opponent = get_toughest_opponent(df)
    best_model = load_best_model()

    # -----------------------------------------------------
    # Hero
    # -----------------------------------------------------

    hero_html = (
        '<div class="hero-card">'
        '<div class="hockey-accent"></div>'
        '<h1>🏒 Penn State Hockey Analytics</h1>'
        '<p class="hero-subtitle">'
        "An end-to-end sports analytics platform that transforms "
        "Penn State Men's Hockey game data into performance insights, "
        "machine-learning evaluation, and interactive visualizations."
        "</p>"
        "</div>"
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )

    st.markdown("")

    # -----------------------------------------------------
    # KPIs
    # -----------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🏒 Games",
            total_games,
        )

    with c2:
        st.metric(
            "📅 Seasons",
            total_seasons,
        )

    with c3:
        st.metric(
            "🏆 Wins",
            wins,
        )

    with c4:
        st.metric(
            "📈 Win Rate",
            f"{win_pct:.1f}%",
        )

    st.markdown("---")

    # -----------------------------------------------------
    # Executive summary
    # -----------------------------------------------------

    st.header("🏆 Executive Summary")

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        winning_factor_caption = describe_metric_difference(
            winning_factor["metric"],
            winning_factor["difference"],
        )

        st.success(
            f"""
### 🥅 Strongest Win–Loss Separator

**{winning_factor["metric"]}**

{winning_factor_caption}

Standardized effect size: \
{winning_factor["effect_size"]:.2f}
"""
            if winning_factor["effect_size"] is not None
            else
            """
### 🥅 Strongest Win–Loss Separator

**Not available**

Insufficient data for comparison.
"""
        )

        venue_caption = (
            f'{best_venue["wins"]} wins in '
            f'{best_venue["games"]} games'
            if best_venue["games"] is not None
            else "Venue information unavailable"
        )

        st.success(
            f"""
### 🏠 Best Venue Type

**{best_venue["venue"]}**

{best_venue["win_rate"]:.1f}% win rate

{venue_caption}
"""
            if best_venue["win_rate"] is not None
            else
            """
### 🏠 Best Venue Type

**Not available**

Venue information unavailable.
"""
        )

    with summary_col2:
        model_caption = (
            f'Cross-validation F1: {best_model["f1"]:.3f}'
            if best_model["f1"] is not None
            else "Evaluation score unavailable"
        )

        st.info(
            f"""
### 🤖 Best Classification Model

**{best_model["model"]}**

{model_caption}

Post-game outcome classification
"""
        )

        opponent_caption = (
            f'{toughest_opponent["wins"]}-'
            f'{toughest_opponent["losses"]} record across '
            f'{toughest_opponent["games"]} games'
            if toughest_opponent["games"] is not None
            else "Opponent information unavailable"
        )

        st.info(
            f"""
### 💪 Toughest Opponent

**{toughest_opponent["opponent"]}**

Penn State win rate: \
{toughest_opponent["win_rate"]:.1f}%

{opponent_caption}
"""
            if toughest_opponent["win_rate"] is not None
            else
            """
### 💪 Toughest Opponent

**Not available**

Opponent information unavailable.
"""
        )

    st.caption(
        """
Executive-summary findings describe associations in the collected
game data. They should not be interpreted as proof that one metric
independently causes wins.
"""
    )

    st.markdown("---")

    # -----------------------------------------------------
    # Project overview
    # -----------------------------------------------------

    overview_col, status_col = st.columns(
        [2, 1]
    )

    with overview_col:
        st.subheader("🏆 Project Overview")

        st.write(
            """
This project automatically collects Penn State Men's Hockey
schedule and box-score data, engineers team-performance
metrics, compares wins and losses, evaluates machine-learning
classifiers, and presents the results through a multi-page
Streamlit dashboard.
"""
        )

        st.markdown("### 🔄 Analytics Pipeline")

        st.markdown(
            """
📅 **Schedule Scraping**

⬇️

🥅 **Box-Score API Extraction**

⬇️

🧹 **Data Cleaning and Feature Engineering**

⬇️

📊 **Exploratory and Hockey-Specific Analysis**

⬇️

🤖 **Cross-Validated Model Evaluation**

⬇️

🏒 **Interactive Streamlit Application**
"""
        )

    with status_col:
        st.subheader("Project Status")

        st.success("✓ Two seasons collected")
        st.success(f"✓ {total_games} games analyzed")
        st.success("✓ Hockey metrics engineered")
        st.success("✓ Four classifiers evaluated")
        st.success("✓ Interactive dashboard completed")

    st.markdown("---")

    # -----------------------------------------------------
    # Clickable navigation
    # -----------------------------------------------------

    st.subheader("📌 Explore the Dashboard")

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        st.button(
            "📈 Season Overview",
            width="stretch",
            on_click=go_to_page,
            args=("Season Overview",),
        )

        st.button(
            "📊 Performance Analysis",
            width="stretch",
            on_click=go_to_page,
            args=("Performance Analysis",),
        )

        st.button(
            "🤖 Machine Learning",
            width="stretch",
            on_click=go_to_page,
            args=("Machine Learning",),
        )

    with nav_col2:
        st.button(
            "🏒 Hockey Insights",
            width="stretch",
            on_click=go_to_page,
            args=("Hockey Insights",),
        )

        st.button(
            "🔍 Game Explorer",
            width="stretch",
            on_click=go_to_page,
            args=("Game Explorer",),
        )

    st.markdown("---")

    # -----------------------------------------------------
    # Project goal
    # -----------------------------------------------------

    st.subheader("🎯 Project Goal")

    st.write(
        """
Identify the game-level performance statistics most strongly
associated with Penn State victories while demonstrating a
complete sports-analytics workflow—from raw data collection
through analysis, machine learning, and interactive deployment.
"""
    )

    st.warning(
        """
Warning: The models classify completed game outcomes using game-level
performance statistics. Because those statistics are recorded
during the game, this is a post-game classification task rather
than a true pre-game prediction model.
"""
    )

    # -----------------------------------------------------
    # Footer
    # -----------------------------------------------------

    st.markdown("---")

    footer_html = (
        '<div style="text-align:center; padding:24px 0 12px 0;">'
        '<p style="font-size:1.05rem; font-weight:700; margin-bottom:6px;">'
        "Built by Anshruta Rahar"
        "</p>"
        '<p style="opacity:0.80; margin:4px 0;">'
        "Penn State University · Computer Science & Applied Statistics"
        "</p>"
        '<p style="opacity:0.65; margin:4px 0;">'
        "Python · Pandas · Scikit-learn · Plotly · Streamlit"
        "</p>"
        "</div>"
    )

    st.markdown(
        footer_html,
        unsafe_allow_html=True,
    )