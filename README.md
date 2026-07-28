# 📈 N100 Financial Intelligence Platform

## Overview

The **N100 Financial Intelligence Platform** is an AI-powered financial analytics platform that helps investors analyze companies using financial statements, stock trends, machine learning, and portfolio recommendations.

It provides a modern REST API built with FastAPI and includes interactive dashboards, clustering analysis, and financial insights.

---

# Features

### Authentication
- JWT Login
- Secure API Access

### Company Analytics
- Company Dashboard
- Company Search
- Company Details
- Financial Ratios
- Financial Summary
- Financial Trends

### Portfolio Analytics
- Portfolio Recommendation
- Portfolio Summary
- Portfolio Statistics

### Machine Learning
- K-Means Company Clustering
- Cluster Profiling
- Correlation Heatmap
- Outlier Detection

### Stock Analysis
- Stock Trend API
- Historical Price Visualization

### REST APIs
- FastAPI
- Swagger UI
- OpenAPI Documentation
- Health Check API

### Testing
- Pytest
- HTML Test Report

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLite

## Machine Learning

- Scikit-learn
- Pandas
- NumPy

## Visualization

- Matplotlib
- Chart.js

## Frontend

- HTML
- Bootstrap
- JavaScript

---

# Project Structure

```
nifty100-data-foundation
│
├── db
├── docs
├── output
├── reports
├── src
│   ├── api
│   ├── auth
│   └── analytics
├── static
├── templates
├── tests
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nifty100-data-foundation.git
```

Move into the project

```bash
cd nifty100-data-foundation
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
uvicorn src.api.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

# API Modules

- Authentication
- Dashboard
- Companies
- Search
- Financial Ratios
- Financial Trends
- Sector Analytics
- Company Comparison
- Portfolio
- Analytics
- Stock Trends
- Health

---

# Machine Learning

- K-Means Clustering
- Correlation Analysis
- Outlier Detection
- Portfolio Statistics

---

# Testing

Run

```bash
python -m pytest tests/api -v
```

Generate HTML Report

```bash
python -m pytest tests/api --html=reports/pytest_report.html --self-contained-html
```

---

# Project Outputs

- company_scores.csv
- cluster_labels.csv
- cluster_profile.csv
- recommended_portfolio.csv
- portfolio_summary.csv
- portfolio_statistics.csv
- outlier_report.csv
- correlation_heatmap.png
- elbow_plot.png

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

Health API

```
GET /health
```

---

# Future Enhancements

- AI Investment Advisor
- Stock Price Prediction using LSTM
- News Sentiment Analysis
- Real-time NSE/BSE Data Integration
- Risk Analysis Dashboard
- Mobile Application
- Cloud Deployment (AWS/Azure)

---

# Author

**Rajkumar Ampolu**

B.Tech Computer Science & Engineering (AI & ML)

SRGEC

---

# License

This project is developed for academic and learning purposes.