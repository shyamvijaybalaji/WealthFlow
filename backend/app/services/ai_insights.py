"""AI-powered financial insights using OpenAI."""
from typing import List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.transaction import Transaction
from app.models.category import Category
from app.models.budget import Budget
from app.core.config import settings


class AIInsightsService:
    """Generate AI-powered financial insights."""

    @staticmethod
    def analyze_spending_patterns(db: Session, user_id: int) -> dict:
        """Analyze user's spending patterns and generate insights."""

        # Get spending by category (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        category_spending = (
            db.query(
                Category.name,
                func.sum(Transaction.amount).label("total")
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= thirty_days_ago
            )
            .group_by(Category.name)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(5)
            .all()
        )

        # Get total income and expenses
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "income",
            Transaction.transaction_date >= thirty_days_ago
        ).scalar() or Decimal("0.00")

        expenses = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "expense",
            Transaction.transaction_date >= thirty_days_ago
        ).scalar() or Decimal("0.00")

        # Get budget adherence
        budgets = db.query(Budget).filter(Budget.user_id == user_id).all()
        budget_alerts = []

        for budget in budgets:
            if budget.period == "monthly":
                end_date = budget.start_date + timedelta(days=30)
            else:
                end_date = budget.start_date + timedelta(days=365)

            spent = db.query(func.sum(Transaction.amount)).filter(
                Transaction.user_id == user_id,
                Transaction.category_id == budget.category_id,
                Transaction.transaction_type == "expense",
                Transaction.transaction_date >= budget.start_date,
                Transaction.transaction_date <= end_date,
            ).scalar() or Decimal("0.00")

            percentage = float((spent / budget.amount) * 100) if budget.amount > 0 else 0
            if percentage >= budget.alert_threshold * 100:
                category = db.query(Category).filter(Category.id == budget.category_id).first()
                budget_alerts.append({
                    "category": category.name if category else "Unknown",
                    "percentage": percentage,
                    "spent": float(spent),
                    "limit": float(budget.amount)
                })

        return {
            "top_spending_categories": [
                {"category": row.name, "amount": float(row.total)}
                for row in category_spending
            ],
            "monthly_income": float(income),
            "monthly_expenses": float(expenses),
            "savings_rate": float(((income - expenses) / income * 100)) if income > 0 else 0,
            "budget_alerts": budget_alerts,
        }

    @staticmethod
    def generate_insights(financial_data: dict) -> List[dict]:
        """Generate AI insights based on financial data."""
        insights = []

        # Insight 1: Savings Rate
        savings_rate = financial_data.get("savings_rate", 0)
        if savings_rate < 10:
            insights.append({
                "type": "warning",
                "title": "Low Savings Rate",
                "message": f"Your current savings rate is {savings_rate:.1f}%. Financial experts recommend saving at least 20% of your income. Consider reducing discretionary spending to increase your savings.",
                "icon": "⚠️"
            })
        elif savings_rate >= 20:
            insights.append({
                "type": "success",
                "title": "Excellent Savings!",
                "message": f"Great job! You're saving {savings_rate:.1f}% of your income, which exceeds the recommended 20%. Keep up the good work!",
                "icon": "🎉"
            })
        else:
            insights.append({
                "type": "info",
                "title": "Good Savings Progress",
                "message": f"You're saving {savings_rate:.1f}% of your income. Try to reach the 20% goal for optimal financial health.",
                "icon": "💡"
            })

        # Insight 2: Top Spending Category
        top_categories = financial_data.get("top_spending_categories", [])
        if top_categories:
            top_cat = top_categories[0]
            insights.append({
                "type": "info",
                "title": "Highest Spending Category",
                "message": f"Your biggest expense is {top_cat['category']} at ${top_cat['amount']:.2f} this month. Review if this aligns with your priorities.",
                "icon": "📊"
            })

        # Insight 3: Budget Alerts
        budget_alerts = financial_data.get("budget_alerts", [])
        if budget_alerts:
            for alert in budget_alerts[:2]:  # Show top 2 alerts
                insights.append({
                    "type": "warning",
                    "title": f"{alert['category']} Budget Alert",
                    "message": f"You've used {alert['percentage']:.1f}% of your {alert['category']} budget (${alert['spent']:.2f} / ${alert['limit']:.2f}). Consider reducing spending in this category.",
                    "icon": "🚨"
                })

        # Insight 4: Income vs Expenses
        monthly_income = financial_data.get("monthly_income", 0)
        monthly_expenses = financial_data.get("monthly_expenses", 0)

        if monthly_expenses > monthly_income:
            deficit = monthly_expenses - monthly_income
            insights.append({
                "type": "warning",
                "title": "Spending Exceeds Income",
                "message": f"You're spending ${deficit:.2f} more than you earn this month. This is unsustainable. Review your expenses and create a budget to get back on track.",
                "icon": "⚠️"
            })

        # Insight 5: Diversification Recommendation
        if len(top_categories) > 0:
            insights.append({
                "type": "tip",
                "title": "Expense Diversification",
                "message": "Track all your expenses to get a complete picture of your spending habits. The more detailed your tracking, the better insights you'll receive.",
                "icon": "💼"
            })

        return insights
