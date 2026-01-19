import requests
import json
import os

BASE_URL = "http://localhost:5000/api"

def run_test():
    # 1. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/login", json={
        "username": "admin.kl@bankedge.com",
        "password": "Admin@123"
    })
    
    if resp.status_code != 200:
        print("Login failed", resp.text)
        return

    data = resp.json()
    token = data['access_token']
    print(f"Login success. Token obtained.")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Fetch Dashboard Data
    print("Fetching dashboard-data...")
    resp = requests.get(f"{BASE_URL}/dashboard-data", headers=headers)
    
    if resp.status_code != 200:
        print("Dashboard API failed", resp.text)
        return
        
    dash_data = resp.json()
    
    # 3. Analyze Data
    txns = dash_data.get('transactions', [])
    latency = dash_data.get('latency', [])
    
    print(f"Transactions count: {len(txns)}")
    if len(txns) > 0:
        print("Sample Transaction:", txns[0])
        
    print(f"Latency History points: {len(latency)}")
    for point in latency[:3]: # Show first 3
        print(f"  Point: {point}")
        
    # Check if data is all zeros
    non_zero_latency = [p for p in latency if p['edge'] > 0 or p['cloud'] > 0]
    print(f"Non-zero latency points: {len(non_zero_latency)}")

if __name__ == "__main__":
    run_test()
