import sys
import os
import requests
import json

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import db, User

BASE_URL = "http://127.0.0.1:5000"
USERNAME = "superadmin@bankedge.com"
PASSWORD = "SuperAdmin@123"

def fix_balance():
    print("[1] Fixing User Balance in Database...")
    with app.app_context():
        user = User.query.filter_by(username=USERNAME).first()
        if user:
            print(f"    Current Balance: {user.balance}")
            user.balance = 100000.0
            db.session.commit()
            print(f"    Updated Balance: {user.balance}")
        else:
            print("    User not found!")

def run_test():
    print("\n[2] Testing Payment API Flow...")
    session = requests.Session()

    # Login
    try:
        res = session.post(f"{BASE_URL}/api/login", json={"username": USERNAME, "password": PASSWORD})
        res.raise_for_status()
        token = res.json().get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        print("    LOGIN: Success")
    except Exception as e:
        print(f"    LOGIN: Failed ({e})")
        return

    # Init Payment
    pi_id = None
    try:
        res = session.post(f"{BASE_URL}/api/init-payment-intent", headers=headers)
        res.raise_for_status()
        data = res.json()
        pi_id = data.get('paymentIntentId')
        print(f"    INIT INTENT: Success (ID: {pi_id})")
    except Exception as e:
        print(f"    INIT INTENT: Failed ({e})")
        return

    # Update Payment (The step that was crashing with 500)
    try:
        payload = {
            "amount": "25.00",
            "recipientAccount": "123456",
            "reference": "Automated Test"
        }
        print(f"    UPDATE INTENT: Sending payload {payload}...")
        res = session.post(f"{BASE_URL}/api/update-payment-intent/{pi_id}", headers=headers, json=payload)
        
        if res.status_code == 200:
            print("    UPDATE INTENT: Success (200 OK)")
            print("    STATUS: PASS - The 500 Error is resolved.")
        elif res.status_code == 500:
            print("    UPDATE INTENT: Failed (500 Internal Server Error)")
            print(f"    Error Details: {res.text}")
            print("    STATUS: FAIL - The code still crashes.")
        else:
            print(f"    UPDATE INTENT: Unexpected Status {res.status_code}")
            print(res.text)

    except Exception as e:
        print(f"    UPDATE INTENT: Exception ({e})")

if __name__ == "__main__":
    fix_balance()
    run_test()
