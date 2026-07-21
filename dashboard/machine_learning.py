import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import confusion_matrix
from config import colors, modelFeatures
from ml_utils import trainModels, getBestModel, getFeatureImportance, predictGame, getModelSummary
from utils import display_hero, style_plotly_chart


def render(df):
    display_hero(
        title="🤖 Machine Learning",
        subtitle=(
            "Compare multiple classification models, evaluate their performance, identify the most influential statistics, and estimate Penn State's probability of winning."
        ),
        page_label="Machine Learning",
    )

    if "Win" not in df.columns:
        st.error("The database does not contain the required 'Win' target column.")
        return
    
    if df["Win"].nunique()<2:
        st.error("The Win column must contain both wins and losses before models can be trained.")
        return 
    
    try:
        (trainedModels, model_results, X_test, y_test, available_features) = trainModels(df=df, featureColumns=modelFeatures)
    except ValueError as error:
        st.error(str(error))
        return 
    except Exception as error:
        st.error("The machine learning models could not be trained.")
        st.exception(error)
        return 
    

    best_model_row = getModelSummary(model_results)
    best_model, best_model_name = getBestModel(trainedModels, model_results)

    st.subheader("Best Model")

    summary_col_1, summary_col_2, summary_col_3, summary_col_4 = st.columns(4)

    summary_col_1.metric(
        "Model",
        best_model_name,
    )

    summary_col_2.metric(
        "Accuracy",
        f"{best_model_row['Accuracy']:.1%}",
    )

    summary_col_3.metric(
        "Recall",
        f"{best_model_row['Recall']:.1%}",
    )

    summary_col_4.metric(
        "F1 Score",
        f"{best_model_row['F1 Score']:.1%}",
    )

    st.caption(
        "The best model is selected using the highest F1 score, which balances precision and recall."
    )

    st.divider()


    st.subheader("Model Comparison")

    display_results = model_results.copy()

    metric_columns = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
    ]

    for metric in metric_columns:

        display_results[metric] = (
            display_results[metric] * 100
        )

    comparison_long = display_results.melt(
        id_vars="Model",
        value_vars=metric_columns,
        var_name="Metric",
        value_name="Score",
    )

    comparison_chart = px.bar(
        comparison_long,
        x="Model",
        y="Score",
        color="Metric",
        barmode="group",
        text_auto=".1f",
        title="Classification Model Performance",
    )

    comparison_chart.update_layout(
        yaxis_title="Score (%)",
        xaxis_title="Model",
        yaxis_range=[0, 105],
        legend_title_text="Metric",
    )

    comparison_chart = style_plotly_chart(
        comparison_chart
    )

    st.plotly_chart(
        comparison_chart,
        use_container_width=True,
    )

    formatted_results = model_results.copy()

    for metric in metric_columns:

        formatted_results[metric] = (
            formatted_results[metric]
            .map(lambda value: f"{value:.1%}")
        )

    st.dataframe(
        formatted_results,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Confusion Matrix")

    selected_model_name = st.selectbox(
        "Choose a model",
        list(trainedModels.keys()),
        index=list(trainedModels.keys()).index(
            best_model_name
        ),
        key="confusion_matrix_model",
    )

    selected_model = trainedModels[
        selected_model_name
    ]

    test_predictions = selected_model.predict(
        X_test
    )

    matrix = confusion_matrix(
        y_test,
        test_predictions,
        labels=[0, 1],
    )

    matrix_chart = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=[
                "Predicted Loss",
                "Predicted Win",
            ],
            y=[
                "Actual Loss",
                "Actual Win",
            ],
            text=matrix,
            texttemplate="%{text}",
            textfont=dict(size=22),
            colorscale=[
                [0, "#0b1728"],
                [1, colors["primary"]],
            ],
            showscale=False,
            hovertemplate=(
                "%{y}<br>"
                "%{x}<br>"
                "Games: %{z}"
                "<extra></extra>"
            ),
        )
    )

    matrix_chart.update_layout(
        title=f"{selected_model_name} Confusion Matrix",
        xaxis_title="Predicted Result",
        yaxis_title="Actual Result",
    )

    matrix_chart = style_plotly_chart(
        matrix_chart
    )

    st.plotly_chart(
        matrix_chart,
        use_container_width=True,
    )

    true_losses = int(matrix[0][0])
    false_wins = int(matrix[0][1])
    false_losses = int(matrix[1][0])
    true_wins = int(matrix[1][1])

    matrix_col_1, matrix_col_2, matrix_col_3, matrix_col_4 = (
        st.columns(4)
    )

    matrix_col_1.metric(
        "Correct Losses",
        true_losses,
    )

    matrix_col_2.metric(
        "Correct Wins",
        true_wins,
    )

    matrix_col_3.metric(
        "Losses Predicted as Wins",
        false_wins,
    )

    matrix_col_4.metric(
        "Wins Predicted as Losses",
        false_losses,
    )

    st.divider()

    st.subheader("Random Forest Feature Importance")

    importance_df = getFeatureImportance(
        trainedModels,
        available_features,
    )

    if importance_df is None:

        st.warning(
            "Random Forest feature importance is unavailable."
        )

    else:

        importance_chart_data = (
            importance_df
            .sort_values(
                by="Importance",
                ascending=True,
            )
        )

        importance_chart = px.bar(
            importance_chart_data,
            x="Importance",
            y="Feature",
            orientation="h",
            text_auto=".3f",
            title=(
                "Statistics Used Most by the Random Forest Model"
            ),
        )

        importance_chart.update_traces(
            marker_color=colors["primary"],
        )

        importance_chart.update_layout(
            xaxis_title="Importance",
            yaxis_title="Statistic",
        )

        importance_chart = style_plotly_chart(
            importance_chart
        )

        st.plotly_chart(
            importance_chart,
            use_container_width=True,
        )

        with st.expander(
            "View Feature Importance Table"
        ):

            st.dataframe(
                importance_df,
                use_container_width=True,
                hide_index=True,
            )

    st.divider()

    st.subheader("Interactive Game Predictor")

    st.write(
        "Adjust the game statistics below to estimate Penn State's probability of winning."
    )

    prediction_model_name = st.selectbox(
        "Prediction Model",
        list(trainedModels.keys()),
        index=list(trainedModels.keys()).index(
            best_model_name
        ),
        key="prediction_model",
    )

    prediction_model = trainedModels[
        prediction_model_name
    ]

    input_values = {}

    input_columns = st.columns(2)

    for index, feature in enumerate(
        available_features
    ):

        feature_series = pd.to_numeric(
            df[feature],
            errors="coerce",
        )

        default_value = float(
            feature_series.median()
        )

        minimum_value = float(
            feature_series.min()
        )

        maximum_value = float(
            feature_series.max()
        )

        if pd.isna(default_value):

            default_value = 0.0

        if pd.isna(minimum_value):

            minimum_value = 0.0

        if pd.isna(maximum_value):

            maximum_value = 100.0

        value_range = maximum_value - minimum_value

        step = (
            0.01
            if value_range <= 10
            else 0.1
        )

        selected_column = input_columns[
            index % 2
        ]

        input_values[feature] = (
            selected_column.number_input(
                label=feature,
                min_value=minimum_value,
                max_value=maximum_value,
                value=default_value,
                step=step,
                key=f"prediction_{feature}",
            )
        )

    if st.button(
        "Predict Game Outcome",
        use_container_width=True,
    ):

        ordered_values = [
            input_values[feature]
            for feature in available_features
        ]

        try:

            prediction, win_probability = predictGame(
                trained_model=prediction_model,
                feature_names=available_features,
                values=ordered_values,
            )

        except Exception as error:

            st.error(
                "The prediction could not be generated."
            )

            st.exception(error)

            return

        loss_probability = 1 - win_probability

        result_label = (
            "Predicted Win"
            if prediction == 1
            else "Predicted Loss"
        )

        result_icon = (
            "🏆"
            if prediction == 1
            else "❌"
        )

        prediction_col_1, prediction_col_2 = (
            st.columns(2)
        )

        prediction_col_1.metric(
            "Predicted Outcome",
            f"{result_icon} {result_label}",
        )

        prediction_col_2.metric(
            "Win Probability",
            f"{win_probability:.1%}",
        )

        gauge_chart = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=win_probability * 100,
                number={
                    "suffix": "%",
                    "font": {
                        "size": 42,
                    },
                },
                title={
                    "text": (
                        f"{prediction_model_name} "
                        "Win Probability"
                    )
                },
                gauge={
                    "axis": {
                        "range": [0, 100],
                    },
                    "bar": {
                        "color": colors["primary"],
                    },
                    "bgcolor": "#10233b",
                    "borderwidth": 1,
                    "bordercolor": "#7dd3fc",
                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#1e293b",
                        },
                        {
                            "range": [40, 60],
                            "color": "#334155",
                        },
                        {
                            "range": [60, 100],
                            "color": "#0c4a6e",
                        },
                    ],
                    "threshold": {
                        "line": {
                            "color": "white",
                            "width": 4,
                        },
                        "thickness": 0.75,
                        "value": 50,
                    },
                },
            )
        )

        gauge_chart.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={
                "color": "#ffffff",
            },
            height=400,
            margin={
                "l": 40,
                "r": 40,
                "t": 80,
                "b": 20,
            },
        )

        st.plotly_chart(
            gauge_chart,
            use_container_width=True,
        )

        probability_df = pd.DataFrame(
            {
                "Outcome": [
                    "Win",
                    "Loss",
                ],
                "Probability": [
                    win_probability,
                    loss_probability,
                ],
            }
        )

        probability_df["Probability"] = (
            probability_df["Probability"]
            .map(lambda value: f"{value:.1%}")
        )

        st.dataframe(
            probability_df,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "This prediction describes patterns found in the available historical dataset. It should be treated as an analytical estimate rather than a guaranteed game result."
        )

    st.divider()


    with st.expander(
        "View Features Used for Model Training"
    ):

        feature_table = pd.DataFrame(
            {
                "Feature": available_features,
                "Dataset Average": [
                    df[feature].mean()
                    for feature in available_features
                ],
            }
        )

        st.dataframe(
            feature_table,
            use_container_width=True,
            hide_index=True,
        )






    