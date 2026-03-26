# Expense Tracker

A full-stack web application for tracking personal expenses, built with Python and Flask. Features user authentication, expense management with filters, interactive charts, and AI-powered spending insights.

---

## Live Demo

[expense-tracker.onrender.com](https://expense-tracker-2gw0.onrender.com)

---

## Features

- **User authentication** — secure signup, login, and logout with bcrypt password hashing
- **Expense management** — add, view, and delete expenses with categories and descriptions
- **Filters** — filter expenses by category and date range
- **Dashboard with charts** — doughnut chart for spending by category, bar chart for monthly trends
- **AI spending insights** — Claude AI analyzes your expenses and suggests where to cut costs and how
- **Fully deployed** — live on Render with a public URL

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite, SQLAlchemy |
| Auth | Flask-Login, bcrypt |
| Frontend | HTML, CSS, Jinja2 |
| Charts | Chart.js |
| AI | Anthropic Claude API |
| Deployment | Render |

---

## Project Structure

```
expense-tracker/
├── app.py              # Flask app — all routes and logic
├── models.py           # SQLAlchemy models (User, Expense)
├── templates/
│   ├── base.html       # Shared layout and navbar
│   ├── dashboard.html  # Charts and summary stats
│   ├── expenses.html   # Expense list with filters
│   ├── add_expense.html
│   ├── login.html
│   ├── signup.html
│   └── insights.html   # AI analysis page
├── static/
│   └── style.css
├── requirements.txt
└── Procfile            # For Render deployment
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repo
git clone https://github.com/atharvvijayvergiya/expense-tracker.git
cd expense-tracker

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Run Locally

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

---

## Database Models

**User**
- `id`, `username`, `email`, `password_hash`
- One user has many expenses

**Expense**
- `id`, `amount`, `category`, `description`, `date`
- `user_id` — foreign key to User

---

## Deployment

This app is deployed on Render using gunicorn as the production server.

```
web: gunicorn app:app
```

Environment variables (`SECRET_KEY`, `ANTHROPIC_API_KEY`) are set securely in the Render dashboard — never committed to the repository.

---

## What I Learned

- Building a full-stack web app from scratch with Flask
- Designing and querying a relational database with SQLAlchemy
- Implementing secure user authentication with session management and password hashing
- Connecting a frontend to a Python backend using Jinja2 templating
- Integrating a third-party AI API (Anthropic Claude) to generate real insights
- Deploying a production web app with environment variable management

---

## Author

**Atharv Vijayvergiya**
[GitHub](https://github.com/atharvvijayvergiya) 
<!-- · [LinkedIn](https://linkedin.com/in/yourprofile) -->
