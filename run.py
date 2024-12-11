from flask import Flask
from app.budget import budget_bp  # Import the budget blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is secure for production

# Register the budget blueprint
app.register_blueprint(budget_bp, url_prefix="/budget")

# Existing code remains unchanged
if __name__ == '__main__':
    app.run(port=5000)

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
