#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add enhanced budgets and investments to WealthFlow"""
import sys
import io
import requests
from datetime import datetime, timedelta
from decimal import Decimal

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
API_BASE_URL = "http://72.61.233.12:8003"
USER_EMAIL = "shyamvijaybalaji@gmail.com"
USER_PASSWORD = "C@pital01"

def login():
    """Login and get JWT token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{API_BASE_URL}/api/v1/auth/login",
        data={"username": USER_EMAIL, "password": USER_PASSWORD}
    )
    if response.status_code == 200:
        print(f"✅ Logged in as {USER_EMAIL}\n")
        return response.json()["access_token"]
    print(f"❌ Login failed: {response.text}")
    return None

def get_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def get_categories(token):
    """Get all existing categories"""
    print("📋 Getting categories...")
    resp = requests.get(f"{API_BASE_URL}/api/v1/categories", headers=get_headers(token))
    if resp.status_code == 200:
        categories = resp.json()
        print(f"   ✅ Found {len(categories)} categories\n")
        return categories
    print(f"   ❌ Failed to get categories: {resp.text}\n")
    return []

def add_comprehensive_budgets(token, categories):
    """Add comprehensive monthly budgets"""
    print("💰 Adding comprehensive budgets...")

    # Get current month start date
    today = datetime.now()
    start_date = today.replace(day=1).isoformat()

    # Comprehensive budget amounts for all major categories
    budget_amounts = {
        # Food & Dining
        "Groceries": 500.00,
        "Restaurants": 250.00,
        "Coffee Shops": 100.00,
        "Fast Food": 75.00,

        # Housing
        "Rent": 1500.00,
        "Mortgage": 2000.00,
        "Property Tax": 300.00,
        "Home Maintenance": 200.00,

        # Utilities
        "Electricity": 120.00,
        "Water": 50.00,
        "Gas": 80.00,
        "Internet": 80.00,
        "Phone": 150.00,
        "Cable": 100.00,

        # Transportation
        "Gas": 200.00,
        "Car Payment": 350.00,
        "Car Insurance": 150.00,
        "Parking": 100.00,
        "Public Transit": 80.00,
        "Uber/Lyft": 120.00,

        # Entertainment
        "Streaming": 60.00,
        "Movies": 50.00,
        "Concerts": 100.00,
        "Gaming": 80.00,
        "Hobbies": 150.00,

        # Shopping
        "Shopping": 400.00,
        "Clothing": 200.00,
        "Electronics": 150.00,
        "Books": 50.00,

        # Health & Fitness
        "Gym": 80.00,
        "Healthcare": 200.00,
        "Pharmacy": 75.00,
        "Dental": 100.00,

        # Personal
        "Haircuts": 60.00,
        "Beauty": 100.00,
        "Personal Care": 80.00,

        # Subscriptions
        "Software": 50.00,
        "Memberships": 100.00,

        # Miscellaneous
        "Gifts": 150.00,
        "Donations": 100.00,
        "Pet Care": 120.00,
    }

    # Create category name to ID mapping
    category_map = {cat["name"]: cat["id"] for cat in categories}

    added = 0
    for cat_name, amount in budget_amounts.items():
        if cat_name not in category_map:
            continue

        payload = {
            "category_id": category_map[cat_name],
            "amount": amount,
            "period": "monthly",
            "alert_threshold": 0.80,
            "start_date": start_date
        }

        resp = requests.post(
            f"{API_BASE_URL}/api/v1/budgets",
            headers=get_headers(token),
            json=payload
        )

        if resp.status_code in [200, 201]:
            added += 1
            print(f"   ✅ {cat_name}: ${amount:,.2f}/month (80% alert)")
        elif resp.status_code == 409 or "already exists" in resp.text.lower():
            print(f"   ℹ️  {cat_name}: Already exists")
        else:
            print(f"   ⚠️  {cat_name}: {resp.status_code} - {resp.text}")

    print(f"\n✅ Added {added} new budgets\n")

def add_investment_portfolio(token):
    """Add diverse investment portfolio"""
    print("📈 Adding investment portfolio...")
    today = datetime.now()

    # Diverse investment portfolio with realistic data
    investments = [
        # Large Cap Tech Stocks
        {
            "asset_type": "stock",
            "symbol": "AAPL",
            "quantity": "25.5",
            "purchase_price": "145.50",
            "current_price": "178.25",
            "purchase_date": (today - timedelta(days=180)).isoformat()
        },
        {
            "asset_type": "stock",
            "symbol": "MSFT",
            "quantity": "15.0",
            "purchase_price": "310.00",
            "current_price": "375.50",
            "purchase_date": (today - timedelta(days=210)).isoformat()
        },
        {
            "asset_type": "stock",
            "symbol": "GOOGL",
            "quantity": "12.0",
            "purchase_price": "125.00",
            "current_price": "142.80",
            "purchase_date": (today - timedelta(days=150)).isoformat()
        },
        {
            "asset_type": "stock",
            "symbol": "NVDA",
            "quantity": "20.0",
            "purchase_price": "450.00",
            "current_price": "875.25",
            "purchase_date": (today - timedelta(days=240)).isoformat()
        },

        # Diversified Stocks
        {
            "asset_type": "stock",
            "symbol": "TSLA",
            "quantity": "8.5",
            "purchase_price": "210.00",
            "current_price": "245.50",
            "purchase_date": (today - timedelta(days=90)).isoformat()
        },
        {
            "asset_type": "stock",
            "symbol": "AMZN",
            "quantity": "18.0",
            "purchase_price": "140.00",
            "current_price": "175.30",
            "purchase_date": (today - timedelta(days=200)).isoformat()
        },
        {
            "asset_type": "stock",
            "symbol": "META",
            "quantity": "10.0",
            "purchase_price": "325.00",
            "current_price": "485.20",
            "purchase_date": (today - timedelta(days=165)).isoformat()
        },

        # ETFs for diversification
        {
            "asset_type": "etf",
            "symbol": "SPY",
            "quantity": "35.0",
            "purchase_price": "420.00",
            "current_price": "478.50",
            "purchase_date": (today - timedelta(days=300)).isoformat()
        },
        {
            "asset_type": "etf",
            "symbol": "QQQ",
            "quantity": "25.0",
            "purchase_price": "350.00",
            "current_price": "445.75",
            "purchase_date": (today - timedelta(days=270)).isoformat()
        },
        {
            "asset_type": "etf",
            "symbol": "VTI",
            "quantity": "40.0",
            "purchase_price": "210.00",
            "current_price": "258.90",
            "purchase_date": (today - timedelta(days=320)).isoformat()
        },
        {
            "asset_type": "etf",
            "symbol": "VOO",
            "quantity": "20.0",
            "purchase_price": "380.00",
            "current_price": "475.30",
            "purchase_date": (today - timedelta(days=280)).isoformat()
        },

        # Cryptocurrency
        {
            "asset_type": "crypto",
            "symbol": "BTC",
            "quantity": "0.25",
            "purchase_price": "42000.00",
            "current_price": "98500.00",
            "purchase_date": (today - timedelta(days=220)).isoformat()
        },
        {
            "asset_type": "crypto",
            "symbol": "ETH",
            "quantity": "2.5",
            "purchase_price": "2200.00",
            "current_price": "3800.00",
            "purchase_date": (today - timedelta(days=190)).isoformat()
        },
        {
            "asset_type": "crypto",
            "symbol": "SOL",
            "quantity": "15.0",
            "purchase_price": "85.00",
            "current_price": "195.00",
            "purchase_date": (today - timedelta(days=160)).isoformat()
        },

        # Bonds for stability
        {
            "asset_type": "bond",
            "symbol": "AGG",
            "quantity": "50.0",
            "purchase_price": "102.50",
            "current_price": "104.20",
            "purchase_date": (today - timedelta(days=365)).isoformat()
        },
        {
            "asset_type": "bond",
            "symbol": "BND",
            "quantity": "45.0",
            "purchase_price": "75.00",
            "current_price": "76.50",
            "purchase_date": (today - timedelta(days=340)).isoformat()
        },
    ]

    added = 0
    total_invested = Decimal("0")
    total_current = Decimal("0")

    for inv in investments:
        resp = requests.post(
            f"{API_BASE_URL}/api/v1/investments",
            headers=get_headers(token),
            json=inv
        )

        if resp.status_code in [200, 201]:
            added += 1
            qty = Decimal(inv["quantity"])
            purchase = Decimal(inv["purchase_price"])
            current = Decimal(inv["current_price"])

            invested = qty * purchase
            value = qty * current
            gain = value - invested
            roi = (gain / invested * 100) if invested else Decimal("0")

            total_invested += invested
            total_current += value

            emoji_map = {
                "stock": "📊",
                "etf": "📈",
                "crypto": "₿",
                "bond": "🔒"
            }
            emoji = emoji_map.get(inv["asset_type"], "💼")

            gain_emoji = "📈" if gain >= 0 else "📉"
            print(f"   {emoji} {inv['symbol']:6} | Qty: {float(qty):>10.4f} | "
                  f"${float(invested):>10,.2f} → ${float(value):>10,.2f} | "
                  f"{gain_emoji} {float(roi):>6.2f}%")
        else:
            print(f"   ⚠️  {inv['symbol']}: {resp.status_code}")

    if added > 0:
        total_gain = total_current - total_invested
        total_roi = (total_gain / total_invested * 100) if total_invested else Decimal("0")

        print(f"\n" + "="*80)
        print(f"   📊 Portfolio Summary:")
        print(f"   💰 Total Invested: ${float(total_invested):,.2f}")
        print(f"   💎 Current Value:  ${float(total_current):,.2f}")
        print(f"   {'📈' if total_gain >= 0 else '📉'} Total Gain/Loss: ${float(total_gain):,.2f} ({float(total_roi):.2f}%)")
        print(f"="*80)

    print(f"\n✅ Added {added} investments\n")

def add_more_savings_goals(token):
    """Add additional savings goals"""
    print("🎯 Adding more savings goals...")
    today = datetime.now()

    goals = [
        {
            "goal_name": "House Down Payment",
            "target_amount": 50000.00,
            "current_amount": 12000.00,
            "deadline": (today + timedelta(days=730)).isoformat(),
            "icon": "🏠"
        },
        {
            "goal_name": "Retirement Fund",
            "target_amount": 100000.00,
            "current_amount": 25000.00,
            "deadline": (today + timedelta(days=3650)).isoformat(),
            "icon": "🏖️"
        },
        {
            "goal_name": "Education Fund",
            "target_amount": 30000.00,
            "current_amount": 8000.00,
            "deadline": (today + timedelta(days=1460)).isoformat(),
            "icon": "🎓"
        },
        {
            "goal_name": "Business Startup",
            "target_amount": 20000.00,
            "current_amount": 5500.00,
            "deadline": (today + timedelta(days=545)).isoformat(),
            "icon": "🚀"
        },
    ]

    added = 0
    for goal in goals:
        resp = requests.post(
            f"{API_BASE_URL}/api/v1/savings-goals",
            headers=get_headers(token),
            json=goal
        )

        if resp.status_code in [200, 201]:
            added += 1
            progress = (goal["current_amount"] / goal["target_amount"]) * 100
            days_left = (datetime.fromisoformat(goal["deadline"]) - today).days
            print(f"   ✅ {goal['icon']} {goal['goal_name']:25} | "
                  f"${goal['current_amount']:>10,.2f} / ${goal['target_amount']:>10,.2f} | "
                  f"{progress:>5.1f}% | {days_left:>4} days")
        elif resp.status_code == 409 or "already exists" in resp.text.lower():
            print(f"   ℹ️  {goal['icon']} {goal['goal_name']}: Already exists")
        else:
            print(f"   ⚠️  {goal['goal_name']}: {resp.status_code}")

    print(f"\n✅ Added {added} new savings goals\n")

def main():
    print("\n" + "="*80)
    print("💰 WealthFlow - Enhanced Data Generator 💰".center(80))
    print("="*80 + "\n")

    token = login()
    if not token:
        return

    # Get categories for budgets
    categories = get_categories(token)

    # Add comprehensive budgets
    if categories:
        add_comprehensive_budgets(token, categories)
    else:
        print("⚠️  No categories found. Budgets require existing categories.\n")

    # Add investment portfolio
    add_investment_portfolio(token)

    # Add more savings goals
    add_more_savings_goals(token)

    print("="*80)
    print("✅ Enhanced data added successfully!".center(80))
    print("="*80)
    print(f"\n🌐 View at: http://wealthflow.fun")
    print(f"📧 Email: {USER_EMAIL}")
    print(f"🔑 Password: {USER_PASSWORD}\n")

if __name__ == "__main__":
    main()
