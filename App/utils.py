import os
import uuid
import csv
from flask import session

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_user_csv():
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    return os.path.join(DATA_DIR, f"{user_id}_expenses.csv")

def init_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])
