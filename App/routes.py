from flask import render_template_string, request, redirect, url_for, session
import csv
import os
from datetime import datetime
import uuid
from .utils import get_user_csv, init_csv

# Initialize Routes
def init_routes(app):
    @app.route('/')
    def index():
        csv_file = get_user_csv()
        init_csv(csv_file)

        expenses = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)

        total_spending = sum(float(expense["Amount"]) for expense in expenses)
        return render_template_string('''
        <h1>Daily Expense Tracker</h1>
        <h2>Total Spending: ${{ total_spending }}</h2>
        <a href="/add">Add Expense</a>
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
        ''', expenses=expenses, total_spending=total_spending)

    @app.route('/add', methods=['GET', 'POST'])
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

            return redirect(url_for('index'))

        return render_template_string('''
        <h1>Add Expense</h1>
        <form method="POST">
            Category: <input type="text" name="category" required><br><br>
            Description: <input type="text" name="description" required><br><br>
            Amount: <input type="number" step="0.01" name="amount" required><br><br>
            <button type="submit">Add Expense</button>
        </form>
        ''')
