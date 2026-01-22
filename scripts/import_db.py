import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import db, User, Device, Transaction

INPUT_FILE = os.path.join(os.path.dirname(__file__), '../migrations/data_dump.json')

def import_data():
    if not os.path.exists(INPUT_FILE):
        print(f" [DB] Error: {INPUT_FILE} not found.")
        sys.exit(1)

    print(f" [DB] Reading data dump from {INPUT_FILE}...")
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    with app.app_context():
        print(f" [DB] Connected to: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # 1. Ensure Tables Exist
        print(" [DB] Step 1: Checking/Creating database tables...")
        try:
            db.create_all()
            print(" [DB] Tables verified.")
        except Exception as e:
            print(f" [DB] CRITICAL ERROR during create_all: {e}")
            return

        # 2. Import Devices
        print(" [DB] Step 2: Importing Devices...")
        d_count = 0
        for d_data in data.get("devices", []):
            existing = Device.query.get(d_data['id'])
            if not existing:
                device = Device(
                    id=d_data['id'],
                    name=d_data['name'],
                    location=d_data['location'],
                    status=d_data['status'],
                    region=d_data['region'],
                    last_sync=datetime.fromisoformat(d_data['last_sync']) if d_data['last_sync'] else None
                )
                db.session.add(device)
                d_count += 1
        
        db.session.commit()
        print(f" [DB] Successfully imported {d_count} devices.")
        
        # 3. Import Users
        print(" [DB] Step 3: Importing Users...")
        u_count = 0
        u_updated = 0
        for u_data in data.get("users", []):
            existing = User.query.filter_by(username=u_data['username']).first()
            if not existing:
                user = User(
                    username=u_data['username'],
                    password_hash=u_data['password_hash'], 
                    role=u_data['role'],
                    balance=u_data.get('balance', 100000.0),
                    last_login=datetime.fromisoformat(u_data['last_login']) if u_data['last_login'] else None
                )
                db.session.add(user)
                u_count += 1
            else:
                existing.balance = u_data.get('balance', 100000.0)
                existing.password_hash = u_data['password_hash']
                existing.role = u_data['role']
                u_updated += 1

        db.session.commit()
        print(f" [DB] Users: {u_count} created, {u_updated} updated.")

        # 4. Import Transactions
        print(" [DB] Step 4: Importing Transactions (Chunked)...")
        t_count = 0
        t_skipped = 0
        for t_data in data.get("transactions", []):
            existing = Transaction.query.get(t_data['id'])
            if not existing:
                txn = Transaction(
                    id=t_data['id'],
                    amount=t_data['amount'],
                    stripe_status=t_data['stripe_status'],
                    processing_decision=t_data['processing_decision'],
                    timestamp=datetime.fromisoformat(t_data['timestamp']),
                    old_balance_org=t_data.get('old_balance_org', 0.0),
                    new_balance_org=t_data.get('new_balance_org', 0.0),
                    is_fraud=t_data.get('is_fraud', False),
                    recipient_account=t_data.get('recipient_account'),
                    reference=t_data.get('reference'),
                    merchant_name=t_data.get('merchant_name'),
                    device_id=t_data.get('device_id'),
                    type=t_data.get('type'),
                    customer_id=t_data.get('customer_id'),
                    confidence=t_data.get('confidence', 0.0),
                    latency=t_data.get('latency', 0.0)
                )
                db.session.add(txn)
                t_count += 1
                
                if t_count % 100 == 0:
                    try:
                        db.session.commit()
                        print(f" [DB] Committed {t_count} transactions...")
                    except Exception as e:
                        db.session.rollback()
                        print(f" [DB] Chunk commit failed at {t_count}: {e}")
            else:
                t_skipped += 1

        try:
            db.session.commit()
            print(f" [DB] Final commit completed.")
            print(f" [DB] SUMMARY: {d_count} Devices, {u_count} Users, {t_count} Transactions imported.")
            print(f" [DB] {t_skipped} duplicate transactions were skipped.")
        except Exception as e:
            db.session.rollback()
            print(f" [DB] ERROR: Final import commit failed: {e}")

if __name__ == "__main__":
    import_data()
