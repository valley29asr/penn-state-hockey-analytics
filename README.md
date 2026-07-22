# 🏒 Penn State Hockey Analytics

> An end-to-end hockey analytics platform that collects, processes, analyzes, and visualizes Penn State Men's Hockey data to identify the key drivers behind winning games.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-green)

---

# 📖 Overview

This project is a complete hockey analytics platform built around **Penn State Men's Hockey**. It combines automated data collection, feature engineering, statistical analysis, machine learning, and interactive visualization into a single end-to-end workflow.

The project was inspired by the growing role of analytics in hockey and demonstrates how modern data science can be used to better understand team performance and the factors associated with winning games.

---

# 🏆 Project Highlights

- 🏒 Built a complete analytics platform for Penn State Men's Hockey
- 📅 Collected and processed **two full seasons** of game data (2024–25 and 2025–26)
- 🔄 Automated data collection using official Penn State Athletics data and the WMT Digital API
- 📊 Engineered advanced hockey performance metrics for game-level analysis
- 🤖 Trained and evaluated multiple machine learning models
- 📈 Created interactive dashboards for exploring team performance
- 💻 Designed a Streamlit application for coaches, analysts, and fans

---

# 📊 Dashboard Preview

> *(Replace these with screenshots after taking them.)*

## Home

![Home](assets/home.png)

---

## Season Overview

![Overview](assets/overview.png)

---

## Performance Analysis

![Performance](assets/performance.png)

---

## Machine Learning

![ML](assets/machine_learning.png)

---

## Hockey Insights

![Insights](assets/hockey_insights.png)

---

## Game Explorer

![Explorer](assets/game_explorer.png)

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

# 📈 Features

### Data Collection

- Automated schedule scraping
- Box score extraction
- API reverse engineering
- JSON parsing
- Error handling

### Feature Engineering

- Shot Differential
- Faceoff Differential
- Shooting Percentage
- Save Percentage
- Goal Differential
- Home / Away / Neutral classification

### Exploratory Data Analysis

- Win vs. Loss comparisons
- Home vs. Away performance
- Opponent analysis
- Season trends
- Performance summaries

### Machine Learning

Models evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Gradient Boosting

Evaluation techniques:

- Train/Test Split
- Stratified Cross Validation
- Hyperparameter Tuning
- Feature Importance
- Confusion Matrix
- Classification Report

### Dashboard

Interactive pages include:

- Home
- Season Overview
- Performance Analysis
- Machine Learning
- Hockey Insights
- Game Explorer

---

# 🏆 Key Findings

Some of the major insights from the analysis include:

- Positive shot differential is strongly associated with winning.
- Winning games generally feature stronger faceoff performance.
- Home games produce the highest win percentage.
- Random Forest achieved the strongest performance for post-game outcome classification.
- Interactive dashboards make it easy to compare seasons, opponents, and game-level performance.

---

# 🛠 Tech Stack

| Category | Technologies |
|-----------|--------------|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Data Collection | Requests, BeautifulSoup |
| Machine Learning | Scikit-Learn |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Version Control | Git & GitHub |

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
├── README.md
└── LICENSE
```

---

# 🚀 Future Improvements

- Player-level analytics
- Expected Goals (xG)
- Live game dashboards
- Automated season updates
- Pre-game predictive models
- Opponent scouting reports
- Interactive player comparisons

---

# 👤 Author

**Anshruta Rahar**

Computer Science & Applied Statistics

The Pennsylvania State University

Interested in Sports Analytics, Machine Learning, Data Science, and Software Engineering.

---
