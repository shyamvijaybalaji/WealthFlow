# WealthFlow - Web Application Design Brief

## Project Overview

**Product Name:** WealthFlow
**Type:** Premium AI-driven Personal Finance & Budget Planner (Web Application)
**Design Aesthetic:** Dark Mode, Glassmorphism, 3D Data Visualization, Modern Luxury

---

## 🎨 Global Design & Styling Guidelines

### Color Palette
- **Primary:** Deep Midnight Blue (#1A1A2E), Charcoal (#2C2C34)
- **Accents:**
  - Electric Emerald Green (#00D9A3) - Growth & Success
  - Cyan Blue (#00B4D8) - Technology & Trust
  - Metallic Gold (#FFD700) - Premium Features

### Visual Style
- **Glassmorphism:** Frosted glass effects, translucency, backdrop blur
- **3D Elements:** Depth with soft shadows and inner glows
- **Animations:** Smooth transitions, micro-interactions
- **Typography:** Inter or SF Pro (clean, high-contrast white sans-serif)

### Responsive Design
- **Desktop:** Full-width dashboard with sidebar navigation
- **Tablet:** Adaptive grid layout
- **Mobile:** Stacked cards, touch-optimized

---

## 📄 Page Structure & Features

### Page 1: Landing & Splash Screen
**Route:** `/` (unauthenticated)

**Design:**
- Full-screen hero section with deep midnight blue gradient background
- Center-aligned 3D gold-line logo animation
- Large heading: "Master Your Money with WealthFlow"
- Subheading: "AI-Driven Personal Finance & Budget Planning"
- Primary CTA: Glowing emerald green "Get Started" button with glassmorphism
- Secondary CTA: "Login" text link (cyan)

**Features:**
- Animated 3D logo on load
- Parallax scrolling for feature highlights
- Smooth scroll to features section

---

### Page 2: Authentication
**Route:** `/login`, `/register`

**Login Page Design:**
- Centered glassmorphism card overlay
- "WealthFlow" logo at top
- Email/Password input fields with frosted glass effect
- "Login" button (emerald green glow)
- "Forgot Password?" link (cyan)
- Divider with "OR"
- Social login buttons (Google, GitHub) with subtle glassmorphism
- "Don't have an account? Sign up" link

**Security Features:**
- JWT token authentication
- Password strength indicator
- Remember me checkbox
- Session management

---

### Page 3: Subscription Plans (WealthFlow Pro)
**Route:** `/pricing`

**Design:**
- Three-tier pricing cards with glassmorphism:
  1. **Basic** (Free) - Charcoal background
  2. **Pro** (Highlighted) - Metallic gold border, "Most Popular" badge
  3. **Elite** - Premium features

**Features per Tier:**
- Basic: Budget tracking, expense categorization, basic reports
- Pro: AI insights, advanced analytics, unlimited categories, priority support
- Elite: Investment tracking, crypto portfolio, tax optimization, dedicated advisor

**CTA:** Large gold "Start Free Trial" button

---

### Page 4: Main Dashboard (Overview)
**Route:** `/dashboard`

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  Sidebar Nav      │     Main Content Area       │
│                   │                             │
│  - Dashboard      │  ┌─────────────────────┐   │
│  - Budget         │  │  Total Balance      │   │
│  - Savings        │  │  $12,450.00         │   │
│  - Investments    │  └─────────────────────┘   │
│  - Transactions   │                             │
│  - Insights       │  [3D Line Chart - 30 days]  │
│  - Settings       │                             │
│                   │  ┌──────────┬──────────┐   │
│                   │  │ Income   │ Expenses │   │
│                   │  └──────────┴──────────┘   │
│                   │                             │
│                   │  Recent Transactions        │
│                   │  [List with icons]          │
└─────────────────────────────────────────────────┘
```

**Features:**
- Large frosted-glass balance card with glowing border
- Interactive 3D line chart (Chart.js or D3.js) showing wealth trend
- Income/Expense cards with month-over-month comparison
- Recent transactions list (scrollable, 5-10 items)
- Quick action buttons (Add Transaction, Create Budget, Set Goal)

---

### Page 5: Budgeting & Category Limits
**Route:** `/budget`

**Design:**
- Monthly budget overview card
- Category-based budget cards with progress bars:
  - **Housing** - 60% used (green)
  - **Dining** - 85% used (amber warning)
  - **Travel** - 105% used (red alert)
  - **Entertainment**, **Shopping**, etc.

**Interactive Elements:**
- Click category to expand details
- Edit budget limits inline
- Add new category with custom icon picker
- Monthly vs. Annual view toggle

**Visual Feedback:**
- Progress bars with gradient fills
- Warning states with pulsing glow
- Micro-animations on hover

---

### Page 6: Savings Goals
**Route:** `/savings`

**Design:**
- Grid of goal cards with 3D holographic bubble visualization
- Each goal shows:
  - Goal name (e.g., "New Home")
  - Target amount
  - Current amount
  - Progress percentage (animated circular progress)
  - Estimated completion date

**Goals:**
1. Emergency Fund - 40% ($8,000 / $20,000)
2. New Home Down Payment - 75% ($45,000 / $60,000)
3. Vacation Fund - 20% ($1,000 / $5,000)

**Features:**
- Large floating "+" button to add new goal
- Drag-to-reorder goals
- Allocate funds to specific goals
- Automated savings rules

---

### Page 7: Investment Portfolio & Markets
**Route:** `/investments`

**Design:**
- Top section: 3D donut chart showing asset allocation
  - Stocks: 60%
  - Crypto: 25%
  - Gold/Commodities: 10%
  - Cash: 5%

**Market Data:**
- Live stock ticker with real-time updates
- Watchlist with +/- indicators (green/red)
- Portfolio performance chart (1D, 1W, 1M, 1Y, ALL)

**Features:**
- Real-time market data (WebSocket connection)
- Add/Remove assets
- Performance analytics
- Asset detail pages

---

### Page 8: Transactions
**Route:** `/transactions`, `/transactions/:id`

**List View:**
- Filterable, sortable transaction table
- Search by merchant, category, amount
- Date range picker
- Export to CSV/PDF

**Detail View:**
- Large amount at top
- Transaction metadata (date, time, merchant, category)
- Location map (if available via Geolocation API)
- Receipt upload/view
- Split transaction feature
- Add tags and notes

---

### Page 9: AI Financial Insights
**Route:** `/insights`

**Design:**
- "Smart Insights" dashboard with AI-generated cards
- Insight examples:
  - "Your spending is down 12% this month 📉"
  - "You're on track to save $5,000 by June 🎯"
  - "Consider switching to a high-yield savings account 💡"

**Visualizations:**
- Spending trends bar chart
- Predicted future balance line chart
- Category breakdown pie chart
- Month-over-month comparison

**AI Features:**
- Personalized recommendations
- Anomaly detection (unusual spending)
- Budget optimization suggestions

---

### Page 10: Settings & Profile
**Route:** `/settings`

**Sections:**
- **Profile:** Name, email, avatar, password change
- **Preferences:** Currency, date format, notifications
- **Security:** Two-factor authentication, session management
- **Billing:** Subscription management, payment methods
- **Data:** Export data, delete account

---

## 🛠️ Technical Stack (Recommended)

### Frontend
- **Framework:** SvelteKit (same as Invoice Generator)
- **Styling:** TailwindCSS + Custom CSS for glassmorphism
- **Charts:** Chart.js or D3.js for 3D visualizations
- **Icons:** Lucide Icons or Heroicons
- **Animations:** Framer Motion or GSAP

### Backend
- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **AI/ML:** OpenAI API or local LLM for insights

### DevOps
- **Database:** PostgreSQL (Docker)
- **Caching:** Redis (optional)
- **Deployment:** Vercel (frontend), Railway/Render (backend)

---

## 📂 Project Structure

Following the AI_FullStack_Development_Kit pattern:

```
D:\Financial_Planner\
├── .claude/              # Claude Code configuration
├── PRPs/                 # Product Requirement Prompts
│   ├── templates/
│   ├── 01_authentication.md
│   ├── 02_dashboard.md
│   ├── 03_budgeting.md
│   ├── 04_savings_goals.md
│   ├── 05_investments.md
│   ├── 06_transactions.md
│   ├── 07_ai_insights.md
│   └── 08_subscription.md
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── crud/
│   │   ├── services/
│   │   └── core/
│   ├── alembic/
│   └── requirements.txt
├── frontend/             # SvelteKit frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   ├── api/
│   │   │   ├── stores/
│   │   │   └── utils/
│   │   └── routes/
│   └── package.json
├── database/
├── docs/
├── docker-compose.yml
├── README.md
└── INITIAL.md
```

---

## 🎯 Core Features Summary

1. ✅ **Authentication** - Secure login/register with JWT
2. ✅ **Dashboard** - Real-time financial overview
3. ✅ **Budgeting** - Category-based budget tracking with alerts
4. ✅ **Savings Goals** - Visual goal tracking with progress
5. ✅ **Investments** - Portfolio tracking with market data
6. ✅ **Transactions** - Complete transaction management
7. ✅ **AI Insights** - Personalized financial recommendations
8. ✅ **Subscription** - Tiered pricing (Basic, Pro, Elite)
9. ✅ **Settings** - User preferences and account management

---

## 🚀 Implementation Priority

### Phase 1: MVP (Core Features)
- Authentication system
- Basic dashboard with balance display
- Transaction CRUD operations
- Simple budgeting with categories

### Phase 2: Enhanced Features
- Savings goals tracking
- Budget alerts and warnings
- Advanced transaction filtering
- Charts and visualizations

### Phase 3: Premium Features
- Investment portfolio tracking
- AI-powered insights
- Subscription/billing system
- Advanced analytics

---

## 📊 Database Schema (High-Level)

**Tables:**
- users
- accounts (bank accounts, credit cards)
- transactions
- categories
- budgets
- savings_goals
- investments
- subscriptions

---

## 🎨 UI/UX Principles

1. **Dark First:** All interfaces use dark mode by default
2. **Glassmorphism:** Consistent frosted-glass aesthetic
3. **Progressive Disclosure:** Show details on demand
4. **Micro-Interactions:** Smooth animations for all actions
5. **Accessibility:** WCAG 2.1 AA compliance
6. **Performance:** < 2s page load, optimized images

---

## 📝 Notes

- Convert all "Page" references to "Route" or "View" for web context
- Replace mobile gestures (swipe, tap) with click/hover interactions
- Adapt mobile-first design to desktop-first with responsive breakpoints
- Implement keyboard shortcuts for power users
- Add breadcrumb navigation for deep pages
- Use server-side rendering (SSR) for SEO
