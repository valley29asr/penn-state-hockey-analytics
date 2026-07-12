# 🏒 Penn State Hockey Analytics

An end-to-end hockey analytics project that collects, processes, and analyzes Penn State Men's Hockey data to identify the key factors behind winning games.

This project builds a complete data pipeline—from web scraping to machine learning and interactive dashboards—using modern Python tools.

---

## 🚀 Project Goals

- Build a complete game-level hockey dataset
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

### ✔️ Day 1 — Project Setup

- Created project structure
- Initialized Git repository
- Created GitHub repository
- Set up Python environment

### ✔️ Day 2 — Schedule Scraper

- Scraped the complete 2024–25 Penn State Men's Hockey schedule
- Extracted:
  - Date
  - Opponent
  - Location
  - Result
  - Box score links
- Saved schedule as a CSV dataset

### ✔️ Day 3 — Box Score Discovery

- Investigated Penn State box score pages
- Determined that statistics are loaded dynamically
- Reverse-engineered the website's data source
- Identified the underlying WMT statistics API

### ✔️ Day 4 — Game Statistics Extraction

- Connected directly to the WMT API
- Parsed JSON game data
- Successfully extracted team statistics including:
  - Goals
  - Shots
  - Faceoffs
  - Penalties
  - Blocks
  - Power-play opportunities
- Built the foundation for automated data collection across the full season

---

## 📅 Next Steps

- Extract statistics for every game in the season
- Build the master game dataset
- Engineer advanced hockey metrics
- Perform exploratory data analysis
- Train predictive machine learning models
- Develop an interactive Streamlit dashboard

---

## 🎯 Planned Analytics

- Win/Loss prediction
- Home vs. Away analysis
- Faceoff impact
- Special teams analysis
- Shot efficiency
- Possession metrics
- Team performance trends
- Player contribution analysis

---

## 📈 Current Status

🟢 Successfully collecting structured game statistics directly from the WMT API.

The project has progressed from web scraping to building an automated hockey analytics data pipeline.
