# 🏒 Penn State Hockey Analytics

An end-to-end hockey analytics project that collects, processes, and analyzes **Penn State Men's Hockey** data to identify the factors that contribute most to winning hockey games.

This project builds a complete analytics pipeline—from web scraping and API reverse engineering to feature engineering, machine learning, and interactive dashboards—using modern Python tools.

---

## 🚀 Project Goals

- Build a complete game-level hockey dataset
- Automate data collection from official Penn State sources
- Engineer advanced hockey performance metrics
- Analyze the biggest drivers of winning
- Build predictive machine learning models
- Create an interactive dashboard for coaches and analysts
---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Requests
- BeautifulSoup
- JSON APIs
- Scikit-learn *(planned)*
- Plotly *(planned)*
- Streamlit *(planned)*
- Git & GitHub

---

## 📂 Project Structure

```
penn-state-hockey-analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dashboard/
├── notebooks/
├── reports/
├── src/
├── tests/
│
├── README.md
└── LICENSE
```

---

## ✅ Progress

## ✔️ Day 1 — Project Setup

- Created project structure
- Initialized Git repository
- Created GitHub repository
- Set up Python virtual environment

---

## ✔️ Day 2 — Schedule Scraper

Built a scraper for the official Penn State Athletics website that collected the complete **2024–25 schedule**.

Extracted:

- Date
- Opponent
- Location
- Game Result
- Box Score Link

Saved the results as a structured CSV dataset.

---

## ✔️ Day 3 — Reverse Engineering Box Scores

Investigated the Penn State Athletics box score pages.

Discovered that:

- Statistics are **not contained in the HTML**
- The website loads data dynamically
- Game statistics come from a hidden **WMT Digital JSON API**

Successfully identified the API powering every official box score.

---

## ✔️ Day 4 — API Connection

Connected directly to the WMT Digital API.

Successfully:

- Retrieved JSON game data
- Parsed nested API responses
- Extracted Penn State team statistics
- Verified data against official box scores

---

## ✔️ Day 5 — Automated Team Stat Extraction

Built an automated extraction pipeline that:

- Loops through every game in the season
- Downloads statistics directly from the API
- Extracts Penn State team statistics
- Stores structured results for further analysis

Extracted statistics include:

- Goals
- Shots
- Faceoff Wins
- Faceoff Losses
- Faceoff Percentage
- Power Play Goals
- Power Play Opportunities
- Penalties
- Penalty Minutes
- Saves
- Goals Against
- Blocks
- Additional team metrics available through the API

---

## ✔️ Day 6 — Robust Data Collection

Improved the scraping pipeline by handling edge cases across the season.

Added:

- Automatic error handling
- Missing-stat detection
- Support for games with inconsistent API responses
- Progress reporting while scraping

Successfully generated a clean season dataset containing Penn State team statistics for nearly every game.

---

## ✔️ Day 7 — Dataset Completion

Completed the full-season data collection pipeline.

Current pipeline:

```
Official Schedule
        ↓
   Box Score Links
        ↓
 WMT Digital API
        ↓
    JSON Parsing
        ↓
 Team Statistics
        ↓
 Structured Dataset (CSV)
```

The project can now automatically build a structured season dataset from official Penn State data.

---
# 📊 Current Dataset

Each game currently includes information such as:

- Date
- Opponent
- Location
- Result
- Goals
- Shots
- Faceoff Wins
- Faceoff Losses
- Faceoff Percentage
- Saves
- Goals Against
- Power Play Goals
- Power Play Opportunities
- Penalties
- Penalty Minutes
- Blocks

---

## 📅 Next Steps

- Build the master cleaned dataset
- Engineer advanced hockey metrics
- Create visualizations
- Perform exploratory data analysis (EDA)
- Train machine learning models
- Evaluate feature importance
- Build an interactive Streamlit dashboard

---

## 🎯 Planned Analytics

- Win/Loss prediction
- Home vs. Away performance
- Shot efficiency
- Faceoff impact
- Special teams analysis
- Defensive performance
- Team performance trends
- Feature importance analysis
- Interactive visual dashboards

---
