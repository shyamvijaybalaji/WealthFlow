# WealthFlow Development Guidelines

This document contains critical development patterns, coding standards, and best practices for working on the WealthFlow financial planner application using Claude Code.

## Project Context

**WealthFlow** is a premium AI-driven personal finance and budget planning application with:
- Real-time financial dashboard with glassmorphism UI
- Budget tracking with category-based limits and visual alerts
- Savings goals with progress tracking
- Investment portfolio management
- AI-powered financial insights using OpenAI
- Subscription tiers (Free/Pro/Elite)

**Tech Stack:**
- Backend: FastAPI + Python + SQLAlchemy + PostgreSQL
- Frontend: SvelteKit + TypeScript + TailwindCSS + Chart.js
- AI: OpenAI API (GPT-4)

---

## Code Style & Standards

### Python (Backend)

**Follow PEP 8 with these specifics:**

- Use type hints for all function signatures
- Use async/await for all database operations
- Use docstrings for all public functions
- Maximum line length: 100 characters
- Use f-strings for string formatting

**Example:**

```python
async def get_user_transactions(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[Transaction]:
    """
    Retrieve transactions for a specific user with pagination.

    Args:
        db: Database session
        user_id: ID of the user
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of Transaction objects owned by the user
    """
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()
```

### TypeScript/Svelte (Frontend)

**Standards:**

- Use TypeScript strict mode
- Functional components (avoid class components)
- Type all props and component exports
- Use `$:` for reactive statements
- Follow SvelteKit file-based routing conventions

**Example:**

```typescript
// src/lib/types/transaction.ts
export interface Transaction {
    id: number;
    amount: number;  // In cents for precision
    description: string;
    category: string;
    transaction_date: string;
}

// src/lib/components/TransactionCard.svelte
<script lang="ts">
    import type { Transaction } from '$lib/types/transaction';

    export let transaction: Transaction;

    $: formattedAmount = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(transaction.amount / 100);
</script>
```

---

## Architecture Patterns

### Backend Structure

```
backend/app/
├── core/
│   ├── config.py      # Pydantic Settings for configuration
│   ├── database.py    # SQLAlchemy session management
│   └── security.py    # JWT, password hashing, authentication
├── models/            # SQLAlchemy ORM models
├── schemas/           # Pydantic request/response schemas
├── crud/              # Database operations (Create, Read, Update, Delete)
├── services/          # Business logic (financial calculations, AI insights)
├── api/v1/endpoints/  # FastAPI route handlers
└── main.py           # FastAPI app initialization
```

**Pattern:**
1. **Models** define database tables (SQLAlchemy)
2. **Schemas** define API contracts (Pydantic)
3. **CRUD** handles database operations
4. **Services** contain business logic
5. **API endpoints** orchestrate CRUD and services

### Frontend Structure

```
frontend/src/
├── lib/
│   ├── components/    # Reusable Svelte components
│   ├── stores/        # Svelte stores for state management
│   ├── api/          # API client and request functions
│   └── types/        # TypeScript type definitions
└── routes/           # File-based routing (SvelteKit)
```

**Pattern:**
1. **Components** are reusable UI elements
2. **Stores** manage global state (auth, user data)
3. **API layer** handles all backend communication
4. **Routes** are pages mapped to URLs

---

## Database Guidelines

### Critical: Always Use Alembic for Migrations

**Never** modify the database schema manually. Always create migrations:

```bash
# Create migration
alembic revision --autogenerate -m "Add investment_portfolio table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### ⚠️ CRITICAL: Use Decimal for Currency

**NEVER use float for money.** Always use `Decimal` or `Numeric`:

```python
# CORRECT ✅
from decimal import Decimal
from sqlalchemy import Numeric

class Transaction(Base):
    amount = Column(Numeric(12, 2), nullable=False)  # Max 9999999999.99

# In application code
amount = Decimal("19.99")
total = sum(Decimal(str(item.amount)) for item in items)

# WRONG ❌
amount = 19.99  # Float causes precision errors!
price = float(user_input)  # Never convert currency to float
```

**Why:** Floats have precision errors (e.g., 0.1 + 0.2 = 0.30000000000000004)

### Foreign Keys and Relationships

**Always use foreign keys with proper indexing:**

```python
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)

    # Relationships
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
```

**Index on:**
- Foreign keys (user_id, category_id)
- Date fields used in filtering
- Fields used in WHERE clauses

### Cascade Deletes

**Use cascade deletes to maintain data integrity:**

```python
class User(Base):
    transactions = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"  # Delete transactions when user is deleted
    )
```

---

## Security Best Practices

### JWT Authentication

**Pattern:**

```python
# In api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    # Decode JWT, verify, return user
    ...
```

### User Ownership Verification

**CRITICAL:** Always verify user owns the resource:

```python
# CORRECT ✅
@router.get("/transactions/{transaction_id}")
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id  # ✅ Ownership check
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

# WRONG ❌
transaction = db.query(Transaction).filter(
    Transaction.id == transaction_id  # Missing ownership check!
).first()
```

### Input Validation

**Use Pydantic for validation:**

```python
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class TransactionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2)
    description: str = Field(..., min_length=1, max_length=200)
    category_id: int = Field(..., gt=0)

    @validator('description')
    def description_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty')
        return v.strip()
```

### Never Commit Secrets

**NEVER commit .env files or API keys to Git.**

Use `.env.example` instead:

```env
# .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=change-this-in-production
OPENAI_API_KEY=your-api-key-here
```

---

## Financial-Specific Patterns

### ⚠️ Server-Side Calculations

**NEVER trust client-provided totals.** Always calculate on server:

```python
# CORRECT ✅
def create_budget_summary(db: Session, user_id: int, budget_id: int) -> dict:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()

    # Calculate spent amount on server
    spent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.category_id == budget.category_id,
        Transaction.transaction_date >= budget.start_date,
        Transaction.transaction_date <= budget.end_date
    ).scalar() or Decimal("0")

    usage_percentage = (spent / budget.amount) * 100 if budget.amount else 0

    return {
        "budget_limit": budget.amount,
        "spent": spent,
        "remaining": budget.amount - spent,
        "usage_percentage": usage_percentage
    }

# WRONG ❌
# Accepting client-provided totals
def create_budget_summary(total_from_client: Decimal):  # Never do this!
    ...
```

### Budget Alert Thresholds

**Pattern for budget warnings:**

```python
def get_budget_status(usage_percentage: Decimal) -> str:
    """
    Return budget status based on usage percentage.

    - Green: < 80%
    - Amber: 80-99%
    - Red: >= 100%
    """
    if usage_percentage >= 100:
        return "over_budget"  # Red alert
    elif usage_percentage >= 80:
        return "warning"  # Amber warning
    else:
        return "on_track"  # Green
```

### Investment ROI Calculations

**Use high precision for investment quantities:**

```python
from decimal import Decimal, getcontext

# Set precision for financial calculations
getcontext().prec = 28

class Investment(Base):
    quantity = Column(Numeric(15, 8), nullable=False)  # High precision for crypto
    purchase_price = Column(Numeric(12, 2), nullable=False)
    current_price = Column(Numeric(12, 2), nullable=False)

def calculate_roi(investment: Investment) -> Decimal:
    """Calculate Return on Investment percentage."""
    cost_basis = investment.quantity * investment.purchase_price
    current_value = investment.quantity * investment.current_price
    gain_loss = current_value - cost_basis
    roi_percentage = (gain_loss / cost_basis) * 100 if cost_basis else Decimal("0")
    return roi_percentage
```

### User Ownership on All Financial Data

**Every financial entity MUST have user_id:**

```python
class Account(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

class Transaction(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

class Budget(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

class SavingsGoal(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

class Investment(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
```

---

## Glassmorphism UI Patterns

### Consistent Glass Card Styling

**TailwindCSS configuration:**

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'midnight-blue': '#1A1A2E',
        'charcoal': '#2C2C34',
        'emerald': '#00D9A3',
        'cyan': '#00B4D8',
        'gold': '#FFD700',
      }
    }
  }
}
```

**Component pattern:**

```svelte
<div class="glass-card glass-card-hover p-6 rounded-2xl">
  <!-- Content -->
</div>

<style>
.glass-card {
  background: rgba(44, 44, 52, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-card-hover:hover {
  background: rgba(44, 44, 52, 0.6);
  border-color: rgba(0, 217, 163, 0.3);
  transition: all 0.3s ease;
}
</style>
```

### Dark Mode Color Palette

**Always use the defined palette:**

- Primary: Deep Midnight Blue (#1A1A2E), Charcoal (#2C2C34)
- Success/Growth: Electric Emerald Green (#00D9A3)
- Technology/Trust: Cyan Blue (#00B4D8)
- Premium: Metallic Gold (#FFD700)

### Gradient Text Effects

```svelte
<h1 class="gradient-text">WealthFlow</h1>

<style>
.gradient-text {
  background: linear-gradient(135deg, #00D9A3 0%, #00B4D8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
```

---

## Testing Requirements

### Backend Tests (pytest)

**Target: 80% code coverage**

```python
# tests/test_transactions.py
import pytest
from decimal import Decimal
from app.models import Transaction

def test_create_transaction(db_session, test_user):
    """Test transaction creation with Decimal precision."""
    transaction = Transaction(
        user_id=test_user.id,
        amount=Decimal("19.99"),
        description="Test transaction"
    )
    db_session.add(transaction)
    db_session.commit()

    assert transaction.id is not None
    assert transaction.amount == Decimal("19.99")
    assert isinstance(transaction.amount, Decimal)

def test_user_ownership_verification(client, test_user, other_user_transaction):
    """Test that users cannot access other users' transactions."""
    response = client.get(
        f"/api/v1/transactions/{other_user_transaction.id}",
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 404
```

### Frontend Tests (Vitest)

```typescript
// src/lib/utils/currency.test.ts
import { describe, it, expect } from 'vitest';
import { formatCurrency } from './currency';

describe('formatCurrency', () => {
  it('formats cents to dollars correctly', () => {
    expect(formatCurrency(1999)).toBe('$19.99');
    expect(formatCurrency(100)).toBe('$1.00');
  });

  it('handles zero correctly', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });
});
```

---

## Performance Considerations

### Database Indexes

**Always index:**

```python
# On foreign keys
user_id = Column(Integer, ForeignKey("users.id"), index=True)

# On date fields used in filtering
transaction_date = Column(Date, index=True)

# On frequently queried fields
category_id = Column(Integer, ForeignKey("categories.id"), index=True)
```

### Pagination for Transaction Lists

**Always paginate large datasets:**

```python
@router.get("/transactions")
async def list_transactions(
    skip: int = 0,
    limit: int = 100,  # Max 100 per request
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).offset(skip).limit(min(limit, 100)).all()

    return transactions
```

### Chart Data Optimization

**Aggregate data before sending to frontend:**

```python
@router.get("/dashboard/monthly-summary")
async def monthly_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Aggregate in database, not in Python
    summary = db.query(
        func.date_trunc('month', Transaction.transaction_date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == current_user.id
    ).group_by('month').all()

    return [{"month": str(row.month), "total": float(row.total)} for row in summary]
```

---

## PRPs (Product Requirement Prompts)

### Follow Template Structure

Use `PRPs/templates/prp_base.md` as the foundation for all PRPs.

**Key sections:**
- Purpose
- Core Principles
- Goal & Why
- Success Criteria
- Context (documentation, codebase references)
- Implementation (data models, tasks, pseudocode)
- Validation Loop (tests, checks)
- Anti-Patterns

### Include Validation Criteria

**Every PRP must have executable validation:**

```bash
# Backend validation
mypy app/
pytest tests/ -v

# Frontend validation
npm run check
npm run lint
```

### Document Anti-Patterns

**Example:**

```markdown
## Anti-Patterns to Avoid

❌ **Don't** use float for currency (use Decimal)
❌ **Don't** trust client-provided totals (calculate on server)
❌ **Don't** skip user ownership checks
❌ **Don't** forget cascade deletes on relationships
```

---

## Common Gotchas

### 1. Currency Precision (Decimal vs Float)

**Problem:** Using float causes rounding errors.

**Solution:** Always use Decimal:

```python
from decimal import Decimal

# ✅ CORRECT
amount = Decimal("19.99")

# ❌ WRONG
amount = 19.99
```

### 2. SQLAlchemy Relationships

**Problem:** Missing cascade deletes causes orphaned records.

**Solution:**

```python
user = relationship("User", back_populates="transactions", cascade="all, delete-orphan")
```

### 3. Environment Variables with Pydantic

**Problem:** Environment variables not loading.

**Solution:**

```python
# core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## Critical Reminders

⚠️ **ALWAYS use Decimal for currency**
⚠️ **ALWAYS verify user ownership**
⚠️ **NEVER trust client-side calculations**
⚠️ **Use server-side validations**
⚠️ **Follow glassmorphism design consistently**
⚠️ **Index foreign keys and date fields**
⚠️ **Paginate large datasets**
⚠️ **Use Alembic for all schema changes**

---

## Resources

- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy docs: https://docs.sqlalchemy.org
- SvelteKit docs: https://kit.svelte.dev
- TailwindCSS docs: https://tailwindcss.com
- Chart.js docs: https://www.chartjs.org
- OpenAI API docs: https://platform.openai.com/docs

---

**Happy coding! Build WealthFlow with precision and elegance.**
