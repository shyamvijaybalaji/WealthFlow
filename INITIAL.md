# WealthFlow - Initial Setup Guide

Complete guide for setting up the WealthFlow financial planner application from scratch.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - Backend runtime
- **Node.js 20 or higher** - Frontend runtime
- **Docker Desktop** - For PostgreSQL database
- **Git** - Version control
- **OpenAI API Key** - For AI financial insights (get from https://platform.openai.com/api-keys)

## Project Overview

**WealthFlow** is a premium AI-driven personal finance and budget planner with:
- Real-time financial dashboard
- Budget tracking with visual alerts
- Savings goals management
- Investment portfolio tracking
- AI-powered financial insights
- Glassmorphism dark mode UI

**Tech Stack:**
- Frontend: SvelteKit + TypeScript + TailwindCSS + Chart.js
- Backend: FastAPI + Python + SQLAlchemy
- Database: PostgreSQL
- AI: OpenAI API (GPT-4)

---

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd Financial_Planner
```

---

### Step 2: Database Setup

**Start PostgreSQL using Docker Compose:**

```bash
docker-compose up -d postgres
```

**Verify database is running:**

```bash
docker ps
```

You should see a container named `wealthflow-postgres` running.

**Access PgAdmin (Optional):**
- Open http://localhost:5050
- Login with credentials from docker-compose.yml
- Add server: Host: postgres, Database: wealthflow, User: postgres, Password: postgres

---

### Step 3: Backend Setup

**Navigate to backend directory:**

```bash
cd backend
```

**Create Python virtual environment:**

```bash
python -m venv .venv
```

**Activate virtual environment:**

- **Linux/Mac:**
  ```bash
  source .venv/bin/activate
  ```

- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

**Install Python dependencies:**

```bash
pip install -r requirements.txt
```

**Create environment file:**

```bash
cp .env.example .env
```

**Edit .env file and configure:**

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wealthflow
SECRET_KEY=your-super-secret-key-change-in-production
OPENAI_API_KEY=sk-your-openai-api-key-here
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

**IMPORTANT:** Replace `OPENAI_API_KEY` with your actual OpenAI API key.

**Run database migrations:**

```bash
alembic upgrade head
```

**Start the backend server:**

```bash
uvicorn app.main:app --reload --port 8001
```

The backend API will be available at:
- API: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health

---

### Step 4: Frontend Setup

**Open a new terminal and navigate to frontend directory:**

```bash
cd frontend
```

**Install Node.js dependencies:**

```bash
npm install
```

**Create environment file:**

```bash
cp .env.example .env
```

**Edit .env file:**

```env
PUBLIC_API_URL=http://localhost:8001/api/v1
```

**Start the development server:**

```bash
npm run dev
```

The frontend will be available at:
- Frontend: http://localhost:5173

---

### Step 5: Verify Everything Works

1. **Open frontend:** http://localhost:5173
2. **Register a new account** or use the test account:
   - Email: demo@example.com
   - Password: demo123
3. **Check API documentation:** http://localhost:8001/docs
4. **Test the dashboard:** Create an account and add a transaction

**Expected behavior:**
- Registration/login works
- Dashboard loads with balance card
- Can create transactions
- Glassmorphism UI displays correctly

---

## Development Workflow

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Making Database Changes

**Create a new migration:**

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations:**

```bash
alembic upgrade head
```

**Rollback last migration:**

```bash
alembic downgrade -1
```

**View migration history:**

```bash
alembic history
```

### Code Quality

**Backend (Python):**

```bash
# Type checking
mypy app/

# Linting
ruff check .

# Format code
black app/
```

**Frontend (TypeScript):**

```bash
# Type checking
npm run check

# Linting
npm run lint

# Format code
npm run format
```

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:**
Ensure you're in the `backend` directory and the virtual environment is activated:
```bash
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Issue: "Could not connect to PostgreSQL"

**Solution:**
1. Check if Docker container is running: `docker ps`
2. Restart the database: `docker-compose restart postgres`
3. Check DATABASE_URL in .env matches docker-compose.yml

### Issue: "alembic: command not found"

**Solution:**
Install alembic in your virtual environment:
```bash
pip install alembic
```

### Issue: "npm install fails"

**Solution:**
1. Delete `node_modules` and `package-lock.json`
2. Clear npm cache: `npm cache clean --force`
3. Re-run: `npm install`

### Issue: "CORS errors in browser"

**Solution:**
Check that BACKEND_CORS_ORIGINS in backend/.env includes your frontend URL:
```env
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

### Issue: "OpenAI API errors"

**Solution:**
1. Verify your OPENAI_API_KEY in backend/.env
2. Check your OpenAI account has credits
3. Ensure API key has proper permissions

---

## Project Structure

```
Financial_Planner/
├── .claude/
│   └── commands/              # Claude Code automation
├── backend/
│   ├── app/
│   │   ├── core/             # Configuration, database, security
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── crud/             # Database operations
│   │   ├── services/         # Business logic
│   │   └── api/v1/endpoints/ # API routes
│   ├── alembic/              # Database migrations
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # Svelte components
│   │   │   ├── stores/      # State management
│   │   │   └── api/         # API client
│   │   └── routes/          # Page routes
│   └── package.json         # Node dependencies
├── PRPs/                    # Product Requirement Prompts
├── docker-compose.yml       # Database configuration
└── README.md
```

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Change SECRET_KEY in backend/.env to a strong random value
- [ ] Update BACKEND_CORS_ORIGINS to your production domain
- [ ] Set DATABASE_URL to production PostgreSQL instance
- [ ] Configure proper SMTP settings for email
- [ ] Add OPENAI_API_KEY for AI insights
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up proper logging and monitoring
- [ ] Configure database backups
- [ ] Review and tighten CORS policies
- [ ] Set up environment-specific .env files
- [ ] Configure rate limiting
- [ ] Review security headers
- [ ] Test all critical financial calculations
- [ ] Verify Decimal precision for all currency operations

---

## Next Steps

1. **Read CLAUDE.md** - Development guidelines and critical patterns
2. **Explore PRPs/** - Feature specifications and implementation guides
3. **Use Claude Code commands:**
   - `/generate-prp [feature-name]` - Generate a feature PRP
   - `/execute-prp [prp-file]` - Execute a PRP implementation

---

## Support

For issues or questions:
- Check this guide first
- Review CLAUDE.md for coding patterns
- Check existing PRPs for implementation examples
- Read the WealthFlow_Web_Design_Brief.md for design specifications

---

**Happy coding! Welcome to WealthFlow development!**
