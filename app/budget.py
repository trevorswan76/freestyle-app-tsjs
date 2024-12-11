from flask import Blueprint, render_template_string, request, session, redirect, url_for
import csv
import os

budget_bp = Blueprint('budget', __name__)

# Directory to store individual CSV files
DATA_DIR = "expense_data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_user_csv():
    """Get the CSV file path for the current user session."""
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    return os.path.join(DATA_DIR, f"{user_id}_expenses.csv")

def init_csv(file_path):
    """Ensure the CSV file exists and has a header."""
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])

@budget_bp.route('/', methods=['GET', 'POST'])
def manage_budget():
    csv_file = get_user_csv()
    init_csv(csv_file)

    # Handle budget setting
    if request.method == 'POST':
        budget = request.form['budget']
        session['budget'] = float(budget)
        return redirect(url_for('budget.manage_budget'))

    # Load expenses
    expenses = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)

    # Calculate total spending
    total_spending = sum(float(expense["Amount"]) for expense in expenses)

    # Get budget from session
    budget = session.get('budget', 0)
    allowed_spending = budget - total_spending

    return render_template_string("""
        <h1>Manage Your Budget</h1>
        <h2>Total Spending: ${{ total_spending }}</h2>
        <h2>Budget: ${{ budget }}</h2>
        <h2>Allowed Spending: ${{ allowed_spending }}</h2>

        <form method="POST">
            <label for="budget">Set Budget:</label>
            <input type="number" step="0.01" id="budget" name="budget" required>
            <button type="submit">Set Budget</button>
        </form>

        <a href="/budget/add">Add Expense</a>
        <table border="1">
            <thead>
                <tr><th>Date</th><th>Category</th><th>Description</th><th>Amount</th></tr>
            </thead>
            <tbody>
                {% for expense in expenses %}
                <tr>
                    <td>{{ expense.Date }}</td>
                    <td>{{ expense.Category }}</td>
                    <td>{{ expense.Description }}</td>
                    <td>${{ expense.Amount }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    """, expenses=expenses, total_spending=total_spending, budget=budget, allowed_spending=allowed_spending)

@budget_bp.route('/add', methods=['GET', 'POST'])
def add_expense():
    csv_file = get_user_csv()
    init_csv(csv_file)

    if request.method == 'POST':
        date = datetime.now().strftime("%Y-%m-%d")
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']

        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, amount])

        return redirect(url_for('budget.manage_budget'))

    return render_template_string("""
        <h1>Add Expense</h1>
        <form method="POST">
            Category: <input type="text" name="category" required><br><br>
            Description: <input type="text" name="description" required><br><br>
            Amount: <input type="number" step="0.01" name="amount" required><br><br>
            <button type="submit">Add Expense</button>
        </form>
    """)
