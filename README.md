# 🏒 Penn State Hockey Analytics

> An end-to-end hockey analytics platform that collects, processes, analyzes, and visualizes **Penn State Men's Hockey** data to identify the performance factors most strongly associated with winning games.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-green)

---

# 🌐 Live Dashboard

🚀 **Explore the interactive dashboard here:**

### https://penn-state-hockey-analytics.streamlit.app

---

# 📸 Dashboard Preview
<img width="1352" height="674" alt="Screenshot 2026-07-23 at 2 40 09 PM" src="https://github.com/user-attachments/assets/7cf3b00c-9e30-4cc5-b54f-330781468650" />


```markdown
![Dashboard](assets/dashboard_home.png)
```

---

# 📖 Overview

This project is a complete hockey analytics platform built around **Penn State Men's Hockey**. It combines automated data collection, feature engineering, statistical analysis, machine learning, and interactive visualization into a single end-to-end workflow.

Inspired by the growing role of analytics in hockey, the project demonstrates how modern data science techniques can be applied to understand team performance, evaluate game-level metrics, and explore the factors most strongly associated with winning.

---

# 🏆 Project Highlights

- Built a complete analytics platform for Penn State Men's Hockey
- Collected and processed **two full NCAA seasons** (2024–25 and 2025–26)
- Automated data collection using Penn State Athletics and the WMT Digital API
- Engineered advanced hockey performance metrics for game-level analysis
- Trained and evaluated multiple machine learning models
- Developed an interactive Streamlit dashboard for exploring performance trends
- Deployed the dashboard publicly using Streamlit Community Cloud

---

# ⚙️ Data Pipeline

```text
Official Penn State Schedule
            │
            ▼
Schedule Scraper
            │
            ▼
Box Score Links
            │
            ▼
WMT Digital API
            │
            ▼
JSON Parsing
            │
            ▼
Raw Game Statistics
            │
            ▼
Feature Engineering
            │
            ▼
Exploratory Data Analysis
            │
            ▼
Machine Learning
            │
            ▼
Interactive Dashboard
```

---

# 📊 Results

- ✅ Two NCAA seasons analyzed
- ✅ Automated end-to-end data collection pipeline
- ✅ Advanced hockey performance metrics engineered
- ✅ Four machine learning models evaluated
- ✅ Random Forest achieved the strongest post-game classification performance
- ✅ Interactive Streamlit dashboard deployed publicly

---

# 📈 Features

## Data Collection

- Automated schedule scraping
- Box score extraction
- API reverse engineering
- JSON parsing
- Robust error handling

## Feature Engineering

- Shot Differential
- Faceoff Differential
- Shooting Percentage
- Save Percentage
- Goal Differential
- Home / Away / Neutral classification

## Exploratory Data Analysis

- Win vs. Loss comparisons
- Home vs. Away performance
- Opponent analysis
- Season trends
- Performance summaries

## Machine Learning

### Models

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

### Evaluation

- Train/Test Split
- Stratified Cross Validation
- Hyperparameter Tuning
- Feature Importance
- Confusion Matrix
- Classification Report

## Interactive Dashboard

The Streamlit dashboard includes:

- Home
- Season Overview
- Performance Analysis
- Machine Learning
- Hockey Insights
- Game Explorer

---

# 🏆 Key Findings

Some of the primary insights from the analysis include:

- Positive shot differential is strongly associated with winning.
- Teams generally perform better when winning the faceoff battle.
- Home games produce the highest win percentage.
- Random Forest achieved the strongest performance for post-game outcome classification.
- Interactive visualizations make it easy to compare seasons, opponents, and individual game performance.

> **Note:** The machine learning models classify completed game outcomes using game-level statistics collected during the game. As a result, this project demonstrates post-game outcome classification rather than true pre-game prediction.

---

# 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Requests
- BeautifulSoup
- JSON APIs
- Scikit-learn
- Plotly
- Streamlit
- Matplotlib
- Joblib
- Git & GitHub

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/valley29asr/penn-state-hockey-analytics.git
```

Move into the project directory

```bash
cd penn-state-hockey-analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📂 Repository Structure

```text
penn-state-hockey-analytics/

├── dashboard/
│   ├── app.py
│   ├── home.py
│   ├── overview.py
│   ├── performance.py
│   ├── hockey_insights.py
│   ├── machine_learning.py
│   ├── game_explorer.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
├── notebooks/
├── reports/
├── src/
├── assets/
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🚀 Future Improvements

- Expected Goals (xG) model
- Player-level analytics
- Pre-game win probability prediction
- Live season updates
- Opponent scouting reports
- Interactive player comparisons
- Advanced shot-location analysis

---

# 👤 Author

## **Anshruta Rahar**

Computer Science & Applied Statistics

The Pennsylvania State University

GitHub: https://github.com/valley29asr
