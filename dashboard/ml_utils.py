import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, f1_score, recall_score

def trainModels(df, featureColumns):
    available_features = [feature for feature in featureColumns if feature in df.columns]

    if len(available_features) == 0:
        raise ValueError("No valid model features found.")
    
    X = df[available_features]
    y = df["Win"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

    models = {
        "Logistic Regression" : LogisticRegression(max_iter=1000), 
        "Decision Tree" : DecisionTreeClassifier(max_depth=4, random_state=42),
        "Random Forest" : RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42), 
        "Gradient Boosting" : GradientBoostingClassifier(random_state=42)
    }

    trained_models = {}
    evaluation_results = []

    for model_name, model in models.items():
        pipeline = Pipeline([("scaler", StandardScaler()), ("model", model)])
        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        trained_models[model_name] = pipeline

        evaluation_results.append(
            {
                "Model":model_name,
                "Accuracy":accuracy_score(y_test, predictions),
                "Precision":precision_score(y_test, predictions, zero_division=0),
                "Recall":recall_score(y_test, predictions, zero_division=0),
                "F1 Score":f1_score(y_test, predictions, zero_division=0)
            }
        )
    
    results_df = pd.DataFrame(evaluation_results).sort_values(by="F1 Score", ascending=False)

    return trained_models, results_df, X_test, y_test, available_features


def getBestModel(trained_models, results_df):
    bestModelName = results_df.iloc[0]["Model"]

    return trained_models[bestModelName], bestModelName


def getFeatureImportance(trained_models, feature_names):
    if "Random Forest" not in trained_models:
        return None
    
    pipeline = trained_models["Random Forest"]
    model = pipeline.named_steps["model"]

    importance_df = pd.DataFrame({"Feature":feature_names, "Importance": model.feature_importances_})
    importance_df = importance_df.sort_values(by="Importance", ascending=False)

    return importance_df


def predictGame(trained_model, feature_names, values):
    input_df = pd.DataFrame([values], columns=feature_names)

    prediction = trained_model.predict(input_df)[0]
    probablity = trained_model.predict_proba(input_df)[0][1]

    return prediction, probablity


def getModelSummary(results_df):
    bestModelRow = results_df.loc[results_df["F1 Score"].idxmax()]

    return bestModelRow
