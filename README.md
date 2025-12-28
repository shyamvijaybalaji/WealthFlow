# WealthFlow - AI-Driven Financial Planner

A premium, full-stack personal finance and budget planning application with AI-powered insights, investment tracking, and beautiful glassmorphism UI built for individuals and small businesses.

## Tech Stack

- **Frontend:** SvelteKit + TypeScript + TailwindCSS
- **Backend:** FastAPI + Python
- **Database:** PostgreSQL
- **Charts:** Chart.js
- **AI Insights:** OpenAI API (GPT-4)
- **Design:** Dark Mode + Glassmorphism

## Features

- **Dashboard:** Real-time financial overview with balance tracking
- **Budget Management:** Category-based budgets with visual alerts
- **Savings Goals:** Track financial goals with progress visualization
- **Investment Portfolio:** Stocks, crypto, and asset allocation tracking
- **Transaction Management:** Complete income/expense tracking
- **AI Insights:** Personalized financial recommendations
- **Subscription Tiers:** Free, Pro, and Elite plans
- **User Authentication:** Secure JWT-based authentication

## Quick Start

See [INITIAL.md](./INITIAL.md) for detailed setup instructions.

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Git
- OpenAI API Key (for AI insights)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Financial_Planner
   ```

2. **Start the database**
   ```bash
   docker-compose up -d postgres
   ```

3. **Setup backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   alembic upgrade head
   uvicorn app.main:app --reload --port 8001
   ```

4. **Setup frontend**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   npm run dev
   ```

## Access Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8001
- **API Documentation:** http://localhost:8001/docs
- **PgAdmin:** http://localhost:5050

## Default Test Account

- **Email:** demo@example.com
- **Password:** demo123

## Features in Detail

- **Financial Dashboard:** Total balance, income/expense summary, 30-day trend chart
- **Smart Budgeting:** Category-based budgets with 80%/100% alerts (green/amber/red)
- **Goal Tracking:** Visual progress with circular indicators and estimated completion dates
- **Investment Portfolio:** Asset allocation donut chart with ROI calculations
- **AI Financial Insights:** Spending analysis, budget recommendations, future predictions
- **Transaction Management:** Filterable lists with date ranges, categories, and search
- **Subscription Management:** Tiered pricing (Free/Pro/Elite) with feature gating
- **Glassmorphism UI:** Premium dark mode design with frosted glass effects

## Project Structure

This project follows the AI_FullStack_Development_Kit pattern:

- `.claude/` - Claude Code configuration and commands
- `PRPs/` - Product Requirement Prompts (feature specifications)
- `backend/` - FastAPI backend application
  - `app/core/` - Configuration and database
  - `app/models/` - SQLAlchemy models
  - `app/schemas/` - Pydantic schemas
  - `app/crud/` - Database operations
  - `app/services/` - Business logic (financial calculations, AI insights)
  - `app/api/v1/endpoints/` - API routes
- `frontend/` - SvelteKit frontend application
  - `src/lib/components/` - Reusable components
  - `src/lib/stores/` - Svelte stores
  - `src/lib/api/` - API client
  - `src/routes/` - Page routes
- `database/` - Database backups
- `docs/` - Project documentation

## Documentation

- [INITIAL.md](./INITIAL.md) - Detailed setup guide
- [CLAUDE.md](./CLAUDE.md) - Development guidelines for Claude Code
- [PRPs/](./PRPs/) - Feature specifications and requirements
- [WealthFlow_Web_Design_Brief.md](./WealthFlow_Web_Design_Brief.md) - Complete design specifications

## Color Palette

- **Primary:** Deep Midnight Blue (#1A1A2E), Charcoal (#2C2C34)
- **Accents:** Electric Emerald Green (#00D9A3), Cyan Blue (#00B4D8), Metallic Gold (#FFD700)
- **Glass Effects:** Semi-transparent overlays with backdrop blur

## Development

### Claude Code Commands

- `/generate-prp [feature-name]` - Generate a PRP for a new feature
- `/execute-prp [prp-file]` - Execute a PRP implementation

### Critical Patterns

- Always use `Decimal` for currency (never float)
- Server-side calculations for all financial totals
- User ownership verification on all operations
- Glassmorphism styling consistency

## License

MIT
