import random
from flask import Blueprint, jsonify
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__, url_prefix='/api')

# --- Data Generation Logic (Translated to Python) ---

locations = ["Johor", "Kedah", "Kelantan", "Malacca", "NegeriSembilan", "Pahang", "Penang", "Perak", "Perlis", "Sabah", "Sarawak", "Selangor", "Terengganu", "KL", "Labuan", "Putrajaya"]
merchants = ['TNG eWallet', 'Maybank', 'CIMB Bank', 'GrabPay', 'ShopeePay', 'Public Bank', 'Boost', 'RHB Bank']

def generate_edge_devices():
    devices = []
    for i, loc in enumerate(locations):
        devices.append({
            'id': f'edge-{i + 1}',
            'name': f'Edge Node {loc}',
            'location': f'{loc}, Malaysia',
            'status': 'offline' if random.random() < 0.1 else 'online',
            'latency': random.uniform(10, 40),
            'load': random.uniform(10, 90),
            'transactionsPerSec': random.uniform(50, 250),
            'region': 'Federal Territory' if loc in ['KL', 'Labuan', 'Putrajaya'] else 'State',
            'lastSync': (datetime.utcnow() - timedelta(minutes=random.uniform(1, 10))).isoformat() + 'Z',
            'syncStatus': 'pending' if random.random() < 0.2 else 'synced'
        })
    return devices

def generate_transactions(count=5):
    transactions = []
    now = datetime.utcnow()
    for i in range(count):
        ml_prediction = random.random()
        if ml_prediction < 0.8:
            ml_status, stripe_status = 'approved', 'succeeded'
        elif ml_prediction < 0.95:
            ml_status, stripe_status = 'flagged', 'failed'
        else:
            ml_status, stripe_status = 'pending', 'processing'

        processed_at = 'edge' if random.random() > 0.3 else 'cloud'

        transactions.append({
            'id': f'txn-{int(now.timestamp()) - i * 10}',
            'amount': random.uniform(50, 5000),
            'type': 'Withdrawal' if random.random() > 0.5 else 'Transfer',
            'mlPrediction': ml_status,
            'stripeStatus': stripe_status,
            'confidence': 0.8 + random.random() * 0.2,
            'timestamp': (now - timedelta(minutes=i*random.uniform(1, 5))).isoformat() + 'Z',
            'deviceId': f'edge-{random.randint(1, 16)}',
            'processedAt': processed_at,
            'latency': random.uniform(10, 30) if processed_at == 'edge' else random.uniform(70, 120),
            'customerId': f'cus_{random.randint(10000, 99999)}',
            'merchantName': random.choice(merchants)
        })
    return transactions

def generate_latency_history(points=15):
    data = []
    now = datetime.utcnow()
    for i in range(points):
        data.append({
            'timestamp': (now - timedelta(seconds=(points - i) * 5)).isoformat() + 'Z',
            'edge': random.uniform(10, 25),
            'cloud': random.uniform(80, 120),
            'hybrid': random.uniform(35, 55)
        })
    return data

def generate_ml_metrics(points=20):
    data = []
    now = datetime.utcnow()
    for i in range(points):
        data.append({
            'timestamp': (now - timedelta(seconds=(points - i) * 10)).isoformat() + 'Z',
            'accuracy': 0.85 + random.random() * 0.12,
            'precision': 0.82 + random.random() * 0.15,
            'recall': 0.88 + random.random() * 0.1,
            'f1Score': 0.85 + random.random() * 0.12
        })
    return data

def generate_processing_decisions(count=10):
    data = []
    reasons = {
        'edge': ["Real-time fraud check", "Simple validation", "Low latency required", "Cached data sufficient"],
        'cloud': ["Historical analysis needed", "Complex pattern recognition", "Regulatory compliance check", "Cross-account analysis"]
    }
    types = ["Transaction", "Authentication", "Balance Inquiry", "New Account Flag"]
    now = datetime.utcnow()
    for i in range(count):
        decision = 'edge' if random.random() > 0.3 else 'cloud'
        data.append({
            'id': f'dec-{int(now.timestamp()) - i}',
            'dataType': random.choice(types),
            'decision': decision,
            'reason': random.choice(reasons[decision]),
            'priority': random.choice(['high', 'medium', 'low']),
            'size': f'{random.uniform(5, 105):.1f}',
            'timestamp': (now - timedelta(minutes=i)).isoformat() + 'Z'
        })
    return data

def get_system_admins():
    return [
        {'id': 'adm_001', 'username': 'admin.kl@bankedge.com', 'role': 'admin', 'email': 'admin.kl@bankedge.com', 'createdAt': '2025-01-15T08:00:00Z', 'lastLogin': '2025-10-28T09:30:00Z', 'status': 'active', 'apiKey': 'sk_live_abc123xyz789'},
        {'id': 'adm_002', 'username': 'superadmin@bankedge.com', 'role': 'superadmin', 'email': 'superadmin@bankedge.com', 'createdAt': '2025-01-01T08:00:00Z', 'lastLogin': '2025-10-28T10:15:00Z', 'status': 'active', 'apiKey': 'sk_live_def456uvw012'},
        {'id': 'adm_003', 'username': 'admin.penang@bankedge.com', 'role': 'admin', 'email': 'admin.penang@bankedge.com', 'createdAt': '2025-02-20T08:00:00Z', 'lastLogin': '2025-10-27T16:45:00Z', 'status': 'active', 'apiKey': 'sk_live_ghi789rst345'}
    ]

def get_ml_models():
    return [
        {'id': 'model_001', 'version': 'v2.4.1', 'uploadedAt': '2025-10-28T08:00:00Z', 'uploadedBy': 'superadmin@bankedge.com', 'size': '4.2 MB', 'status': 'active', 'accuracy': 96.8, 'deployedNodes': 16},
        {'id': 'model_002', 'version': 'v2.4.0', 'uploadedAt': '2025-10-20T08:00:00Z', 'uploadedBy': 'admin.kl@bankedge.com', 'size': '4.1 MB', 'status': 'archived', 'accuracy': 95.2, 'deployedNodes': 0},
        {'id': 'model_003', 'version': 'v2.5.0-beta', 'uploadedAt': '2025-10-27T14:30:00Z', 'uploadedBy': 'superadmin@bankedge.com', 'size': '4.5 MB', 'status': 'pending', 'accuracy': 97.1, 'deployedNodes': 3}
    ]

def get_audit_logs():
    return [
        {'id': 'log_001', 'timestamp': '2025-10-28T10:15:32Z', 'user': 'superadmin@bankedge.com', 'action': 'LOGIN', 'resource': 'Authentication', 'status': 'success', 'ipAddress': '203.106.94.23'},
        {'id': 'log_002', 'timestamp': '2025-10-28T10:14:18Z', 'user': 'admin.kl@bankedge.com', 'action': 'UPDATE_MODEL', 'resource': 'ML Model v2.4.1', 'status': 'success', 'ipAddress': '118.107.46.89'},
        {'id': 'log_003', 'timestamp': '2025-10-28T10:10:05Z', 'user': 'admin.penang@bankedge.com', 'action': 'TRIGGER_SYNC', 'resource': 'Edge Node PENANG-01', 'status': 'success', 'ipAddress': '60.53.218.142'},
        {'id': 'log_004', 'timestamp': '2025-10-28T09:58:23Z', 'user': 'superadmin@bankedge.com', 'action': 'CREATE_ADMIN', 'resource': 'User: admin.johor@bankedge.com', 'status': 'success', 'ipAddress': '203.106.94.23'},
        {'id': 'log_005', 'timestamp': '2025-10-28T09:45:12Z', 'user': 'admin.kl@bankedge.com', 'action': 'FAILED_LOGIN', 'resource': 'Authentication', 'status': 'failed', 'ipAddress': '118.107.46.89'}
    ]

# --- API Routes ---

# Dashboard Page
@api_bp.route('/dashboard-data')
def dashboard_data():
    return jsonify({
        'devices': generate_edge_devices(),
        'latency': generate_latency_history(),
        'transactions': generate_transactions(5)
    })

# Edge Devices Page
@api_bp.route('/devices')
def devices():
    return jsonify(generate_edge_devices())

# ML Insights Page
@api_bp.route('/ml-data')
def ml_data():
    return jsonify({
        'metrics': generate_ml_metrics(),
        'transactions': generate_transactions(20),
        'decisions': generate_processing_decisions()
    })

# Transactions Page
@api_bp.route('/transactions')
def transactions():
    return jsonify(generate_transactions(30))

# System Management Page
@api_bp.route('/system-data')
def system_data():
    return jsonify({
        'admins': get_system_admins(),
        'auditLogs': get_audit_logs(),
        'mlModels': get_ml_models(),
        'edgeNodes': generate_edge_devices()
    })

# Single Device Sync (for Edge Devices Page)
@api_bp.route('/devices/sync/<device_id>', methods=['POST'])
def sync_device(device_id):
    # Find the original device to get its loc
    all_devices = generate_edge_devices()
    original_device = next((d for d in all_devices if d['id'] == device_id), None)

    if not original_device:
        return jsonify({'error': 'Device not found'}), 404

    # Simulate syncing by generating a new device with 'online' and 'synced' status
    synced_device = {
        **original_device, # Keep location and name
        'status': 'online',
        'latency': random.uniform(10, 40),
        'load': random.uniform(10, 90),
        'transactionsPerSec': random.uniform(50, 250),
        'lastSync': datetime.utcnow().isoformat() + 'Z',
        'syncStatus': 'synced'
    }
    return jsonify(synced_device)