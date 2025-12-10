import sys
import os
import requests
import json

# Add parent directory to path to import app if needed, but we will test via HTTP
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_URL = "http://127.0.0.1:5000"
USERNAME = "superadmin@bankedge.com"
PASSWORD = "SuperAdmin@123"

def run_test():
    print("=== BankEdge MVC System Verification ===")
    session = requests.Session()

    # 1. Login
    print("\n[1] Testing Login...")
    login_payload = {"email": USERNAME, "password": PASSWORD}
    try:
        res = session.post(f"{BASE_URL}/api/login", json=login_payload)
        res.raise_for_status()
        data = res.json()
        token = data.get('access_token')
        if not token:
            print("FAILED: No token received.")
            return
        print("SUCCESS: Logged in. Token received.")
    except Exception as e:
        print(f"FAILED: Login error: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Check Dashboard Data (Balance)
    print("\n[2] Testing Dashboard Data & Balance...")
    try:
        res = session.get(f"{BASE_URL}/api/dashboard-data", headers=headers)
        res.raise_for_status()
        data = res.json()
        
        balance = data.get('userBalance')
        devices = data.get('devices')
        transactions = data.get('transactions')

        print(f"    - User Balance: RM {balance}")
        print(f"    - Devices Count: {len(devices) if devices else 0}")
        print(f"    - Transactions Count: {len(transactions) if transactions else 0}")

        if balance is not None:
            print("SUCCESS: Balance retrieved.")
        else:
            print("FAILED: User balance is missing.")
        
        if devices and len(devices) > 0:
            print("SUCCESS: Edge devices data retrieved.")
        else:
            print("FAILED: No edge devices found.")

    except Exception as e:
        print(f"FAILED: Dashboard data error: {e}")

    # 3. Validation Logic
    if balance is not None and devices:
        print("\n=== OVERALL STATUS: PASS ===")
    else:
        print("\n=== OVERALL STATUS: FAIL ===")

if __name__ == "__main__":
    run_test()
