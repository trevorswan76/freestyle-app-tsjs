from flask import Blueprint, render_template_string, request, session, redirect, url_for

budget_bp = Blueprint('budget', __name__)

# Route to set and view budget
@budget_bp.route('/', methods=['GET', 'POST'])
def manage_budget():
    # Handle budget setting
    if request.method == 'POST':
        budget = request.form.get('budget', type=float)
        session['budget'] = budget
        return redirect(url_for('budget.manage_budget'))

    # Retrieve budget from session
    budget = session.get('budget', 0)
    return render_template_string("""
        <h1>Manage Your Budget</h1>
        <h2>Current Budget: ${{ budget }}</h2>
        <form method="POST">
            <label for="budget">Set Budget:</label>
            <input type="number" step="0.01" id="budget" name="budget" required>
            <button type="submit">Update Budget</button>
        </form>
    """, budget=budget)
