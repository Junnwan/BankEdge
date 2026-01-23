import os
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from models import db, bcrypt, User  # Ensure User is imported if referenced, though unused in init now
from controllers.api_controller import api_bp
from controllers.transactions_controller import transactions_bp

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

app = Flask(__name__)

# -------------------------------------------------
# Flask Configuration
# -------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))

database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///' + os.path.join(basedir, 'bankedge.db')

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    db_path = os.path.join(basedir, 'instance', 'bankedge.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['SQLALCHEMY_ENGINE_OPTIONS']["connect_args"] = {"timeout": 30}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secrets
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

# Stripe
app.config['STRIPE_PUBLISHABLE_KEY'] = os.environ.get('STRIPE_PUBLISHABLE_KEY')
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')

# JWT Token Expiry
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)

# -------------------------------------------------
# Initialize Extensions
# -------------------------------------------------
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# -------------------------------------------------
# Register Blueprints
# -------------------------------------------------
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(transactions_bp)

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html', title='Dashboard')

@app.route('/edge-devices')
def edge_devices_page():
    return render_template('edge_devices.html', title='Edge Devices')

@app.route('/ml-insights')
def ml_insights_page():
    return render_template('ml_insights.html', title='ML Insights')

@app.route('/transactions')
def transactions_page():
    return render_template('transactions.html', title="Transactions")

@app.route('/system-management')
def system_management_page():
    return render_template('system_management.html', title='System Management')

# -------------------------------------------------
# Database Initialization (Schema Only)
# -------------------------------------------------
with app.app_context():
    try:
        # Create tables if they don't exist
        db.create_all()
        print(f" [DB] Schema synchronized. Connected to: {app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1]}")
    except Exception as e:
        print(f" [DB] WARNING: Schema synchronization failed: {e}")

# -------------------------------------------------
# Pre-load ML Model
# -------------------------------------------------
if os.environ.get('SKIP_ML_LOAD') != 'true':
    from controllers.transactions_controller import init_model
    with app.app_context():
        init_model()
    print(" [ML] Model pre-loaded successfully.")
else:
    print(" [ML] Skipping model load (Maintenance Mode).")

# -------------------------------------------------
# Start Server
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)