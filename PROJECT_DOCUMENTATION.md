# 🛒 FreshMarket — Online Grocery Store
## Complete Project Documentation

> **Built by:** Sai Charan | **Technology Stack:** Python Flask + SQLite + Gemini AI  
> **Date:** March 2026 | **Version:** 2.0 (with AI Assistant)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [Database Design](#database-design)
5. [Features & Modules](#features--modules)
6. [AI Chatbot — FreshBot](#ai-chatbot--freshbot)
7. [Authentication & Security](#authentication--security)
8. [UI/UX Design System](#uiux-design-system)
9. [How to Set Up & Run](#how-to-set-up--run)
10. [API Endpoints](#api-endpoints)
11. [File Structure](#file-structure)
12. [How I Built This Project](#how-i-built-this-project)

---

## 🎯 Project Overview

**FreshMarket** is a full-stack online grocery shopping platform built with Python Flask. It provides a seamless, modern shopping experience with features like product browsing, cart management, order processing, loyalty rewards, and an **AI-powered shopping assistant (FreshBot)**.

### Core Goals
- Allow users to browse and purchase fresh groceries online
- Provide personalized AI-driven shopping recommendations
- Deliver a premium, responsive UI using Material Design 3
- Include admin management capabilities for inventory and orders

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3 + Flask | Web framework & routing |
| **Database** | SQLite + SQLAlchemy | Data persistence & ORM |
| **Authentication** | Flask-Login + Google OAuth 2.0 | User auth |
| **AI Engine** | Google Gemini 1.5 Flash API | AI chatbot |
| **Frontend** | HTML5 + Vanilla CSS + JS | UI & interactivity |
| **Design** | Material Design 3 (MD3) | Design system |
| **Deployment** | Gunicorn + Render | Production hosting |
| **Environment** | python-dotenv | Config management |

---

## 🏗️ Project Architecture

```
FreshMarket/
│
├── app.py              ← Flask app factory & configuration
├── routes.py           ← All URL routes & business logic (1500+ lines)
├── models.py           ← SQLAlchemy database models
├── extensions.py       ← Flask extensions (db, login, oauth)
├── ai_chatbot.py       ← 🆕 AI chatbot engine (Gemini API)
│
├── templates/          ← Jinja2 HTML templates
│   ├── base.html       ← Master layout with nav, scripts
│   ├── index.html      ← Homepage (products, search, filters)
│   ├── login.html      ← Login / Sign-up page
│   ├── checkout.html   ← Checkout & payment flow
│   └── ...             ← 25+ more templates
│
├── static/             ← CSS, JS, images
│   ├── chatbot.css     ← 🆕 AI chatbot UI styles
│   ├── chatbot.js      ← 🆕 AI chatbot JavaScript
│   ├── style.css       ← Main application styles
│   └── ...             ← Material Design CSS files
│
├── instance/
│   └── grocery.db      ← SQLite database file
│
├── .env                ← API keys & environment config
└── requirements.txt    ← Python dependencies
```

### Request Flow
```
Browser → Flask Routes (routes.py) → Business Logic → Models (SQLAlchemy) → SQLite DB
                                                    ↘
                                              AI Chatbot (Gemini API) → JSON Response
```

---

## 🗄️ Database Design

The project uses **SQLite** with **SQLAlchemy ORM**. Here are all the database tables:

### Tables Overview

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    User     │────<│   CartItem   │>────│   Product   │
│─────────────│     │──────────────│     │─────────────│
│ id (PK)     │     │ id (PK)      │     │ id (PK)     │
│ username    │     │ user_id (FK) │     │ name        │
│ email       │     │ product_id   │     │ category    │
│ password    │     │ quantity     │     │ price       │
│ is_admin    │     └──────────────┘     │ stock       │
│ loyalty_pts │                          │ description │
└──────┬──────┘                          │ avg_rating  │
       │                                 └─────────────┘
       │     ┌──────────────┐
       ├────<│    Order     │
       │     │──────────────│
       │     │ id           │
       │     │ user_id (FK) │
       │     │ total_price  │
       │     │ status       │
       │     │ payment_method│
       │     │ pts_earned   │
       │     └──────┬───────┘
       │            │
       │     ┌──────────────┐
       │     │  OrderItem   │
       │     │──────────────│
       │     │ order_id (FK)│
       │     │ product_id   │
       │     │ quantity     │
       │     │ price_at_buy │
       │     └──────────────┘
       │
       ├────<│  Wishlist  │
       ├────<│  Review    │
       ├────<│  Address   │
       ├────<│LoyaltyTransaction│
       └────<│ScheduledOrder│
```

### Key Relationships
- **User → CartItem**: One-to-Many (user has many cart items)
- **User → Order**: One-to-Many (user has many orders)
- **Order → OrderItem**: One-to-Many (order contains many items)
- **Product → Review**: One-to-Many (product has many reviews)
- **User → Wishlist**: One-to-Many (user has wishlist items)

---

## ✨ Features & Modules

### 1. 🏠 Homepage & Product Browsing
- **Advanced Search**: Full-text search across product name, category, description
- **Filters**: Category, price range, minimum rating, in-stock only
- **Sorting**: By name (A-Z, Z-A), price (low/high), rating
- **Product Spotlight**: Auto-selects top-rated products
- **Quick Reorder**: Shows user's frequently ordered items
- **Fresh Drop Radar**: Displays newest products
- **Category Showcase**: Visual stacked cards per category

### 2. 🛒 Shopping Cart
- Add/remove items with AJAX (no page reload)
- Quantity management (+ / - buttons)
- Real-time cart badge count in navbar
- Out-of-stock prevention
- Cart persists across sessions (database-backed)

### 3. 💳 Checkout & Payments
- Multiple payment methods: COD, Debit Card, Credit Card, UPI
- UPI QR code payment page
- Coupon code application with AJAX validation
- Loyalty points redemption at checkout
- Scheduled delivery with date & time slot selection
- Recurring order setup (daily/weekly/monthly)
- Address selection/management

### 4. 📦 Order Management
- Order history with status tracking
- Detailed order view (items, prices, delivery info)
- Order success confirmation page with recap
- Admin order status management

### 5. ❤️ Wishlist
- Toggle wishlist from product cards (AJAX)
- Dedicated wishlist page
- One-click "Add to Cart" from wishlist

### 6. ⭐ Loyalty Rewards Program
- Earn **1 point per ₹10** spent
- Redeem **100 points = ₹10** discount
- Transaction history log
- Points balance dashboard

### 7. 👤 User Profile
- View order statistics (total orders, total spent)
- Edit profile (username, email, password)
- Avatar display
- Recent orders quick view

### 8. 📝 Product Reviews
- Star rating system (1-5 stars)
- Written reviews with timestamps
- One review per user per product (update allowed)
- Auto-calculated average rating on product

### 9. 🗓️ Scheduled Orders
- Schedule delivery for future dates
- Time slot selection (morning/afternoon/evening)
- Recurring orders (daily/weekly/monthly)
- Edit/cancel scheduled orders

### 10. 🔑 Authentication
- Register / Login with username & password
- Google OAuth 2.0 Sign-In
- Password reset via token
- Admin role with special dashboard access

### 11. 🛡️ Admin Dashboard
- View all orders and update statuses
- Add/edit/delete products
- Manage coupons (create, activate/deactivate)
- View platform statistics

### 12. 🤖 AI Chatbot — FreshBot *(NEW!)*
> *See dedicated section below*

---

## 🤖 AI Chatbot — FreshBot

### What is FreshBot?
FreshBot is an **AI-powered shopping assistant** integrated directly into the FreshMarket website. It uses **Google Gemini 1.5 Flash** (free tier) to provide intelligent, context-aware responses.

### FreshBot Capabilities

| Capability | Description |
|-----------|-------------|
| 🛒 **Product Recommendations** | Suggests products based on user needs/budget |
| 🍳 **Recipe Suggestions** | Creates recipes using in-stock products |
| 📦 **Order Tracking Help** | Answers order status and delivery questions |
| 💰 **Budget Tips** | Finds cheapest options in required categories |
| ⭐ **Loyalty Guidance** | Explains points earning & redemption |
| 🥗 **Nutrition Advice** | Healthy eating and dietary information |
| 🔍 **Search Assistance** | Helps users find specific items |

### How FreshBot Works (Technical Flow)

```
User types message
        ↓
chatbot.js (frontend) sends POST /api/chatbot
        ↓
routes.py → chatbot() function
        ↓
ai_chatbot.py → chat_with_ai()
        ↓
    ┌──────────────────────────┐
    │ Build Context:           │
    │ • Product catalog (live) │
    │ • User's recent orders   │
    │ • Current cart contents  │
    │ • Conversation history   │
    └──────────────────────────┘
        ↓
Google Gemini API (gemini-1.5-flash-latest)
        ↓
AI Response
        ↓
chatbot.js renders message in chat UI
```

### Context-Aware Intelligence
FreshBot is given **live context** on every request:
1. **Product Catalog**: All in-stock items with prices & ratings
2. **User Orders**: Past 3 orders for personalization
3. **Cart State**: Current items in the user's cart
4. **Conversation History**: Last 10 exchanges for continuity

### Fallback System
If the Gemini API key is not configured, FreshBot uses a **rule-based fallback engine** with 8 intelligent response categories, ensuring the chatbot always works.

### AI Configuration (`ai_chatbot.py`)

```python
# API Settings
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Generation Parameters
generationConfig = {
    "temperature": 0.7,      # Creativity level (0=strict, 1=creative)
    "topK": 40,              # Token selection breadth
    "topP": 0.95,            # Nucleus sampling threshold
    "maxOutputTokens": 500,  # Response length limit
}
```

### Chat UI Features
- **Glassmorphic design** with gradient header
- **Quick suggestion chips** for common queries
- **Typing indicator** with animated dots
- **Multi-turn conversation** (remembers context)
- **Markdown formatting** in responses (bold, lists)
- **Dark mode support** (syncs with site theme)
- **Mobile responsive** layout
- **Notification badge** on FAB button
- **Session-based history** reset button

---

## 🔐 Authentication & Security

### User Authentication
- **Passwords**: Stored as bcrypt hashes via `werkzeug.security.generate_password_hash`
- **Sessions**: Flask-Login manages login sessions
- **CSRF Protection**: OAuth state parameter prevents CSRF attacks

### Google OAuth 2.0 Flow
```
User clicks "Sign in with Google"
        ↓ 
App redirects to Google consent screen
        ↓
Google authenticates user
        ↓
Google redirects to /login/google/callback with auth code
        ↓
App exchanges code for access token
        ↓
App fetches user profile (email, name)
        ↓
Create account if new / Login if existing
        ↓
User logged in!
```

### Route Protection
- `@login_required` decorator on all protected routes
- Admin routes check `current_user.is_admin`
- Order ownership verification (prevents accessing other users' orders)

---

## 🎨 UI/UX Design System

### Design Philosophy
The UI follows **Material Design 3** principles with custom enhancements:

- **Glassmorphism**: Frosted glass effects with `backdrop-filter: blur()`
- **Gradient Accents**: Green-to-blue gradients throughout
- **Micro-animations**: Ripple effects, hover transitions, loading states
- **Dark Mode**: Full support with CSS `[data-theme="dark"]` toggle
- **Responsive**: Mobile-first, hamburger menu for small screens

### Color Palette

| Token | Light Mode | Dark Mode | Usage |
|-------|-----------|----------|-------|
| Primary | `#2E7D32` | `#A5D6A7` | Main green brand color |
| Secondary | `#1565C0` | `#90CAF9` | Blue accent |
| Surface | `#FFFFFF` | `#1C1E24` | Card backgrounds |
| On Surface | `#1A1A2E` | `#E8F5E9` | Text |

### Typography
- **Font**: Roboto (Google Fonts) — weights 300, 400, 500, 700
- **Heading Scale**: 24px → 20px → 16px → 14px
- **Body**: 14-15px line-height 1.5-1.6

### Key CSS Files
| File | Purpose |
|------|---------|
| `material-design.css` | MD3 design tokens & base components |
| `style.css` | Main application layout & product cards |
| `chatbot.css` | FreshBot chatbot UI |
| `new_features.css` | Loyalty, wishlist, scheduled order styles |
| `login_futuristic.css` | Login page glassmorphic design |
| `homepage_modern.css` | Homepage hero & category sections |
| `material-overrides.css` | Custom overrides on top of MD3 |

---

## 🚀 How to Set Up & Run

### Prerequisites
- Python 3.8+
- pip

### Step 1: Clone/Download the Project
```bash
# Project directory
cd "online grocessr store"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Edit `.env` file:
```bash
# Required for Google OAuth (optional for basic use)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Required for AI Chatbot (get FREE at https://aistudio.google.com)
GEMINI_API_KEY=your_gemini_api_key
```

> **Get FREE Gemini API Key**: Visit [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)  
> No credit card needed! Free tier: 15 requests/minute, 1,500/day

### Step 5: Initialize Database
```bash
python init_db.py
python add_products.py   # Add sample products
```

### Step 6: Run the Application
```bash
python app.py
```

App runs at: **http://localhost:5000**

### Step 7: Create Admin Account (Optional)
```python
# In Python shell:
from app import create_app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User(username='admin', email='admin@freshmarket.com', 
                 password_hash=generate_password_hash('admin123'), is_admin=True)
    db.session.add(admin)
    db.session.commit()
```

---

## 🔌 API Endpoints

### Public Routes
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Homepage with product listing |
| GET | `/product/<id>` | Product detail page |
| GET | `/login` | Login / register page |
| POST | `/login` | Process login form |
| POST | `/register` | Process registration |
| GET | `/login/google` | Google OAuth redirect |
| GET | `/login/google/callback` | Google OAuth callback |

### Protected Routes (Login Required)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/cart` | View shopping cart |
| GET | `/add_to_cart/<id>` | Add item to cart |
| GET | `/remove_from_cart/<id>` | Remove cart item |
| GET | `/checkout` | Checkout page |
| POST | `/process_order` | Place an order |
| POST | `/apply_coupon` | Validate & apply coupon |
| GET | `/orders` | Order history |
| GET | `/order/<id>` | Order detail |
| GET | `/wishlist` | Wishlist page |
| GET | `/wishlist/toggle/<id>` | Toggle wishlist item |
| GET | `/loyalty` | Loyalty rewards page |
| GET | `/profile` | User profile |
| POST | `/profile/edit` | Update profile |
| GET | `/addresses` | Saved addresses |
| GET | `/scheduled-orders` | Scheduled orders |

### AI Chatbot API
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/chatbot` | Send message to FreshBot |
| POST | `/api/chatbot/reset` | Reset conversation history |

**Request Body** (`/api/chatbot`):
```json
{ "message": "What vegetables do you have?" }
```

**Response**:
```json
{
  "success": true,
  "message": "We have fresh tomatoes, spinach, carrots...",
  "is_authenticated": true
}
```

### Admin Routes
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/admin` | Admin dashboard |
| GET/POST | `/admin/add_product` | Add new product |
| GET/POST | `/admin/edit_product/<id>` | Edit product |
| POST | `/admin/delete_product/<id>` | Delete product |
| GET/POST | `/admin/coupons` | Manage coupons |

---

## 📁 File Structure

```
online grocessr store/
│
├── 📄 app.py                    Flask application factory
├── 📄 routes.py                 All routes & business logic  
├── 📄 models.py                 Database models (SQLAlchemy)
├── 📄 extensions.py             Flask extensions init
├── 📄 ai_chatbot.py             🆕 AI chatbot engine
├── 📄 requirements.txt          Python dependencies
├── 📄 .env                      Environment variables (never commit!)
├── 📄 wsgi.py                   Production WSGI entry point
├── 📄 render.yaml               Render.com deployment config
│
├── 📂 templates/                HTML templates (Jinja2)
│   ├── base.html                Master layout template
│   ├── index.html               Homepage (largest—37KB)
│   ├── checkout.html            Checkout flow
│   ├── admin_dashboard.html     Admin panel
│   ├── order_success.html       Post-purchase confirmation
│   ├── login.html               Auth page
│   ├── profile.html             User dashboard
│   └── ... (20+ more)
│
├── 📂 static/                   Static assets
│   ├── chatbot.css              🆕 FreshBot chatbot styles
│   ├── chatbot.js               🆕 FreshBot chatbot JS
│   ├── style.css                Core application CSS
│   ├── material-design.css      MD3 design system
│   ├── material-overrides.css   Custom CSS overrides
│   ├── new_features.css         Feature-specific styles
│   ├── interactive-ui.js        UI interactions
│   ├── logo.png                 FreshMarket logo
│   └── ... (70+ images)
│
├── 📂 instance/
│   └── grocery.db               SQLite database
│
└── 📂 scripts/                  Database utility scripts
```

---

## 🧠 How I Built This Project

### Phase 1: Foundation (Flask App Setup)
I started by setting up the **Flask application factory pattern** in `app.py`. This pattern allows creating multiple instances of the app for testing and keeps configuration clean. I configured **SQLAlchemy** as the ORM with SQLite for local development (easily upgradeable to PostgreSQL for production).

**Key decisions:**
- Used **Flask Blueprints** to organize routes
- Chose **SQLite** for simplicity (single file DB, no setup)
- Used **Flask-Login** for session management

### Phase 2: Database Models
I designed the database schema thinking about real e-commerce requirements:
- **User model** with loyalty points built-in from day one
- **Product model** with rating aggregation fields (`average_rating`, `review_count`) stored directly to avoid expensive recalculations on every page load
- **Order/OrderItem** separation following the standard order-line-item pattern

### Phase 3: Core Features
Built features in order of importance:
1. **Product listing** with search & filtering using SQLAlchemy query chaining
2. **Shopping cart** with AJAX updates for smooth UX
3. **Checkout flow** with multiple payment methods
4. **User authentication** (register, login, logout)

### Phase 4: Advanced Features
Added premium features that differentiate the app:
1. **Google OAuth** using Authlib library
2. **Loyalty rewards** with transaction ledger pattern
3. **Product reviews** with star ratings
4. **Wishlists** with toggle functionality
5. **Scheduled/recurring orders**
6. **Admin dashboard** with CRUD operations

### Phase 5: UI/UX Polish
Invested heavily in Material Design 3:
- Built a complete **design token system** in CSS with custom properties
- Implemented **dark mode** with `localStorage` persistence
- Added **micro-animations** (ripple effects, hover transitions, fade-ins)
- Made the app fully **responsive** with a hamburger mobile menu
- Applied **glassmorphism** on the login page for a premium feel

### Phase 6: AI Integration (FreshBot) 🆕
The AI chatbot was designed to be **genuinely useful**, not just decorative:

1. **API Choice**: Selected Google Gemini 1.5 Flash for its excellent free tier and context window
2. **Context Engineering**: The system prompt dynamically injects live data (catalog, cart, orders) so the AI gives real, grounded answers — not hallucinations
3. **Fallback System**: Built a rule-based fallback so the chatbot works even without an API key
4. **Conversation Memory**: Used Flask sessions to maintain multi-turn conversations
5. **UI Design**: Created a floating glassmorphic chat window that doesn't interrupt browsing

### Key Technical Challenges & Solutions

| Challenge | Solution |
|-----------|---------|
| Cart updates causing page reloads | AJAX with `X-Requested-With` header detection |
| AI giving wrong product prices | Inject live catalog into every AI request |
| Chatbot history bloating sessions | Limit to 20 messages (10 exchanges) |
| Dark mode flash on page load | Read `localStorage` before first paint |
| Google OAuth in dev with HTTP | Used `127.0.0.1` to avoid HTTPS requirement |
| Product images breaking | Built cleanup and migration scripts |

### Performance Optimizations
- Product `average_rating` cached on the model (not computed on read)
- Database indexes on `user_id` and `product_id` foreign keys
- AJAX cart updates avoid full page reloads
- CSS performance file with `contain` properties
- Image optimization scripts (`optimize_images.py`)

---

## 📚 Dependencies

```
flask              - Web framework
flask-sqlalchemy   - Database ORM
flask-login        - User authentication
flask-wtf          - Form handling & CSRF
email_validator    - Email validation
authlib            - OAuth 2.0 (Google Sign-In)
python-dotenv      - Environment variable management
requests           - HTTP client (for Gemini API)
gunicorn           - Production WSGI server
```

---

## 🌐 Deployment

The app is configured for **Render.com** deployment (`render.yaml`):

```yaml
services:
  - type: web
    name: freshmarket
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn wsgi:app
```

For local development: `python app.py` (debug mode with auto-reload)

---

## 📄 License & Acknowledgments

- **Material Design 3** guidelines by Google
- **Google Gemini AI** for the chatbot intelligence  
- **Flask** ecosystem for the robust Python web foundation
- **Authlib** for seamless OAuth 2.0 integration

---

*Documentation prepared by: Sai Charan*  
*Last Updated: March 2026*
