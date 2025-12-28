from fastapi import APIRouter
from app.api.v1.endpoints import auth, dashboard, transactions, accounts, categories, budgets, savings_goals, investments, insights

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(savings_goals.router, prefix="/savings-goals", tags=["savings-goals"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])
api_router.include_router(insights.router, prefix="/insights", tags=["insights"])
