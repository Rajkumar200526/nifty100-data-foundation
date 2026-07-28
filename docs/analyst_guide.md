# N100 Financial Intelligence Platform - Analyst Guide

## Project Overview

The N100 Financial Intelligence Platform is an AI-powered financial analytics system that evaluates companies using financial ratios, clustering, stock trends, and portfolio recommendations.

---

## Features

- User Authentication (JWT)
- Company Dashboard
- Company Search
- Financial Ratio Analysis
- Financial Summary
- Sector Analytics
- Company Comparison
- Portfolio Recommendation
- K-Means Company Clustering
- Stock Price Trends
- Correlation Heatmap
- Outlier Detection
- Portfolio Statistics
- REST APIs with FastAPI
- Swagger Documentation
- Automated API Testing

---

## Technology Stack

Backend
- Python
- FastAPI

Database
- SQLite

Machine Learning
- Scikit-learn
- Pandas
- NumPy

Visualization
- Matplotlib
- Chart.js

Frontend
- HTML
- Bootstrap
- JavaScript

---

## Running the Project

### Activate Virtual Environment

```powershell
venv\Scripts\activate
```

### Start the API

```powershell
uvicorn src.api.main:app --reload
```

### Open Swagger

```
http://127.0.0.1:8000/docs
```

---

## API Modules

- Authentication
- Dashboard
- Companies
- Financial Ratios
- Financial Trends
- Portfolio
- Analytics
- Sector Analysis
- Company Comparison
- Stock Trends
- Health Check

---

## Machine Learning

- K-Means Clustering
- Correlation Matrix
- Outlier Detection
- Portfolio Statistics

---

## Testing

Run:

```powershell
python -m pytest tests/api -v
```

Generate HTML Report:

```powershell
python -m pytest tests/api --html=reports/pytest_report.html --self-contained-html
```

---

## Output Files

- company_scores.csv
- cluster_labels.csv
- cluster_profile.csv
- recommended_portfolio.csv
- portfolio_summary.csv
- portfolio_statistics.csv
- outlier_report.csv

---

## Author

Rajkumar Ampolu

Final Year B.Tech CSE (AI & ML)

SRGEC