from fastapi import FastAPI, HTTPException
import time
import pandas as pd
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from src.auth.routes import router as auth_router
from fastapi import Depends
from src.auth.dependencies import get_current_user
from src.api.routers import company_compare

from src.api.routers.companies import router as companies_router
from src.api.routers.clusters import router as clusters_router
from src.api.routers.dashboard import router as dashboard_router
from src.api.routers.top_performers import router as top_performers_router
from src.api.routers.cluster_details import router as cluster_details_router
from src.api.routers.company_ratios import router as company_ratios_router
from src.api.routers.financial_summary import router as financial_summary_router
from src.api.routers.search import router as search_router
from src.api.routers.sector_analysis import router as sector_analysis_router
from src.api.routers.compare import router as compare_router
from src.api.routers.financial_trends import router as financial_trends_router
from src.api.routers.recommendation import router as recommendation_router
from src.api.routers.portfolio import router as portfolio_router
from src.api.routers.analytics import router as analytics_router
from src.api.stock_trends import router as stock_trends_router
from src.api.routers.health import router as health_router

app = FastAPI(
    title="N100 Financial Intelligence Platform",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "output"

app.include_router(companies_router)
app.include_router(clusters_router)
app.include_router(dashboard_router)
app.include_router(top_performers_router)
app.include_router(cluster_details_router)
app.include_router(company_ratios_router)
app.include_router(financial_summary_router)
app.include_router(search_router)
app.include_router(sector_analysis_router)
app.include_router(compare_router)
app.include_router(financial_trends_router)
app.include_router(recommendation_router)
app.include_router(portfolio_router)
app.include_router(analytics_router)
app.include_router(auth_router)
app.include_router(company_compare.router)
app.include_router(stock_trends_router)
app.include_router(health_router)
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = round((time.time() - start_time) * 1000, 2)

    print(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {process_time} ms"
    )

    return response

@app.get("/")
def home():
    return {
        "project": "N100 Financial Intelligence Platform",
        "status": "Running"
    }
# ----------------------------------------------------
# Company Scores
# ----------------------------------------------------

@app.get("/company-scores")
def company_scores(current_user: str = Depends(get_current_user)):
    file = OUTPUT_DIR / "company_scores.csv"
    df = pd.read_csv(file)

    df.rename(columns={
        "Investment Score": "investment_score"
    }, inplace=True)

    return df.to_dict(orient="records")


# ----------------------------------------------------
# Recommended Portfolio
# ----------------------------------------------------

@app.get("/recommended-portfolio")
def recommended_portfolio(current_user: str = Depends(get_current_user)):
    file = OUTPUT_DIR / "recommended_portfolio.csv"
    df = pd.read_csv(file)
    return df.to_dict(orient="records")


# ----------------------------------------------------
# Portfolio Summary
# ----------------------------------------------------

@app.get("/portfolio-summary")
def portfolio_summary(current_user: str = Depends(get_current_user)):
    file = OUTPUT_DIR / "portfolio_summary.csv"
    df = pd.read_csv(file)
    return df.to_dict(orient="records")


# ----------------------------------------------------
# Cluster Labels
# ----------------------------------------------------

@app.get("/cluster-labels")
def cluster_labels(current_user: str = Depends(get_current_user)):
    file = OUTPUT_DIR / "cluster_labels.csv"
    df = pd.read_csv(file)
    return df.to_dict(orient="records")


# ----------------------------------------------------
# Cluster Profile
# ----------------------------------------------------

@app.get("/cluster-profile")
def cluster_profile(current_user: str = Depends(get_current_user)):
    file = OUTPUT_DIR / "cluster_profile.csv"
    df = pd.read_csv(file)
    return df.to_dict(orient="records")
@app.get("/dashboard")
def dashboard(current_user: str = Depends(get_current_user)):
    file = OUTPUT_DIR / "company_scores.csv"
    df = pd.read_csv(file)

    return {
        "total_companies": len(df),
        "average_score": round(df["Investment Score"].mean(), 2),
        "highest_score": round(df["Investment Score"].max(), 2),
        "strong_buy": len(df[df["Recommendation"] == "Strong Buy"]),
        "buy": len(df[df["Recommendation"] == "Buy"]),
        "hold": len(df[df["Recommendation"] == "Hold"]),
        "sell": len(df[df["Recommendation"] == "Sell"])
    }
@app.get("/company/{company_id}")
def get_company(company_id: int, current_user: str = Depends(get_current_user)):

    file = OUTPUT_DIR / "company_scores.csv"

    df = pd.read_csv(file)

    # Rename column to match frontend
    df.rename(columns={
        "Investment Score": "investment_score"
    }, inplace=True)

    # Find the company
    company = df[df["company_id"] == company_id]

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return company.iloc[0].to_dict()