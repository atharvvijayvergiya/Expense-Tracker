from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Expense
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///expenses.db')

db.init_app(app)    

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def home():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    category_totals = {}
    monthly_totals = {}

    for e in expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount
        month = e.date.strftime('%b %Y')
        monthly_totals[month] = monthly_totals.get(month, 0) + e.amount

    total_spent = sum(e.amount for e in expenses)
    top_category = max(category_totals, key=category_totals.get) if category_totals else 'N/A'

    return render_template('dashboard.html',
        category_labels=list(category_totals.keys()),
        category_values=list(category_totals.values()),
        monthly_labels=list(monthly_totals.keys()),
        monthly_values=list(monthly_totals.values()),
        total_spent=total_spent,
        top_category=top_category,
        expense_count=len(expenses)
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# routes
@app.route('/expenses')
@login_required
def expenses():
    category = request.args.get('category', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = Expense.query.filter_by(user_id=current_user.id)

    if category:
        query = query.filter_by(category=category)
    if start_date:
        query = query.filter(Expense.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Expense.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    user_expenses = query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in user_expenses)

    return render_template('expenses.html',
        expenses=user_expenses,
        total=total,
        selected_category=category,
        start_date=start_date,
        end_date=end_date
    )

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']

        expense = Expense(
            amount=amount,
            category=category,
            description=description,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense added!')
        return redirect(url_for('expenses'))

    return render_template('add_expense.html')

@app.route('/delete/<int:expense_id>')
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('Not allowed.')
        return redirect(url_for('expenses'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.')
    return redirect(url_for('expenses'))



#api route
@app.route('/insights')
@login_required
def insights():
    import anthropic

    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    if not expenses:
        flash('Add some expenses first to get insights.')
        return redirect(url_for('home'))

    expense_summary = []
    for e in expenses:
        expense_summary.append(f"{e.category}: ₹{e.amount} — {e.description or 'no description'}")

    expense_text = "\n".join(expense_summary)
    total = sum(e.amount for e in expenses)

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Here are my recent expenses:

{expense_text}

Total spent: ₹{total}

Please analyze my spending and tell me:
1. Where I am spending the most and why it might be a problem
2. Which specific expenses I can cut down
3. Practical alternative suggestions to reduce costs
4. One key habit I should change

Keep it conversational, specific, and actionable. Format with clear sections."""
            }
        ]
    )

    analysis = message.content[0].text
    return render_template('insights.html', analysis=analysis, total=total)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)