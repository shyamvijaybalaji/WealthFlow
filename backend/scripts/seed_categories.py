"""Script to seed default system categories."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.database import SessionLocal
from app.crud.category import category
from app.schemas.category import CategoryCreate


def seed_categories():
    """Create default system categories."""
    db = SessionLocal()

    # Default expense categories
    expense_categories = [
        {"name": "Food & Dining", "category_type": "expense", "icon": "🍔", "color": "#FF6B6B"},
        {"name": "Transportation", "category_type": "expense", "icon": "🚗", "color": "#4ECDC4"},
        {"name": "Shopping", "category_type": "expense", "icon": "🛍️", "color": "#95E1D3"},
        {"name": "Entertainment", "category_type": "expense", "icon": "🎬", "color": "#F38181"},
        {"name": "Bills & Utilities", "category_type": "expense", "icon": "📱", "color": "#AA96DA"},
        {"name": "Healthcare", "category_type": "expense", "icon": "🏥", "color": "#FCBAD3"},
        {"name": "Education", "category_type": "expense", "icon": "📚", "color": "#A8D8EA"},
        {"name": "Travel", "category_type": "expense", "icon": "✈️", "color": "#FFD93D"},
        {"name": "Housing", "category_type": "expense", "icon": "🏠", "color": "#6BCB77"},
        {"name": "Other Expenses", "category_type": "expense", "icon": "💸", "color": "#C4C4C4"},
    ]

    # Default income categories
    income_categories = [
        {"name": "Salary", "category_type": "income", "icon": "💰", "color": "#00D9A3"},
        {"name": "Freelance", "category_type": "income", "icon": "💼", "color": "#00B4D8"},
        {"name": "Investments", "category_type": "income", "icon": "📈", "color": "#FFD700"},
        {"name": "Bonus", "category_type": "income", "icon": "🎁", "color": "#90EE90"},
        {"name": "Other Income", "category_type": "income", "icon": "💵", "color": "#98D8C8"},
    ]

    all_categories = expense_categories + income_categories

    try:
        for cat_data in all_categories:
            # Check if category already exists
            existing = db.query(category.model).filter(
                category.model.name == cat_data["name"],
                category.model.is_system == True
            ).first()

            if not existing:
                cat_in = CategoryCreate(**cat_data)
                category.create_system_category(db, obj_in=cat_in)
                print(f"[OK] Created: {cat_data['name']}")
            else:
                print(f"[SKIP] Skipped: {cat_data['name']} (already exists)")

        print(f"\n[SUCCESS] Seeding complete! Created {len(all_categories)} default categories.")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_categories()
