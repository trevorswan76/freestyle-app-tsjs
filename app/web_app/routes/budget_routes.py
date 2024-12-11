from flask import Blueprint, render_template, request, redirect, url_for, session
import os
import csv
from datetime import datetime

# Define the blueprint
budget_routes = Blueprint('budget_routes', __name__)

# Directory to store user data (expenses)
DATA_DIR = "web_app/data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_user_csv():
    """Returns the path to the user's expense CSV file."""
    user_id = session.get('user_id')
    if not user_id:
        session['user_id'] = f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        user_id = session['user_id']
    return os.path.join(DATA_DIR, f"{user_id}_expenses.csv")

def init_csv(file_path):
    """Ensure the CSV file exists and has a header row."""
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Description", "Amount"])

@budget_routes.route('/budget', methods=['GET', 'POST'])
def manage_budget():
    """Handles budget display and updates."""
    csv_file = get_user_csv()
    init_csv(csv_file)

    # Handle budget submission
    if request.method == 'POST':
        budget = request.form.get('budget', type=float)
        session['budget'] = budget
        return redirect(url_for('budget_routes.manage_budget'))

    # Retrieve current budget
    budget = session.get('budget', 0)

    # Load and calculate expenses
    expenses = []
    total_spending = 0
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                expenses.append(row)
                total_spending += float(row['Amount'])

    # Remaining budget
    remaining_budget = budget - total_spending

    return render_template('budget.html', budget=budget, expenses=expenses, total_spending=total_spending, remaining_budget=remaining_budget)

@budget_routes.route('/budget/add', methods=['GET', 'POST'])
def add_expense():
    """Allows users to add new expenses."""
    csv_file = get_user_csv()
    init_csv(csv_file)

    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])
        date = datetime.now().strftime('%Y-%m-%d')

        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, category, description, amount])

        return redirect(url_for('budget_routes.manage_budget'))

    return render_template('add_expense.html')
