import os
from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
from models import db, bcrypt
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

# Engine Options for both SQLite (timeout) and PostgreSQL (SSL/Pooling stability)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}

if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    app.config['SQLALCHEMY_ENGINE_OPTIONS']["connect_args"] = {"timeout": 30}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secrets
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

# Stripe (keys only stored – logic handled fully inside transactions_controller)
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

# Enable SQLite Write-Ahead Logging (WAL) for concurrency
if 'sqlite' in (app.config['SQLALCHEMY_DATABASE_URI'] or ''):
    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    # @event.listens_for(Engine, "connect")
    # def set_sqlite_pragma(dbapi_connection, connection_record):
    #     cursor = dbapi_connection.cursor()
    #     cursor.execute("PRAGMA journal_mode=WAL")
    #     cursor.close()

# -------------------------------------------------
# Register Blueprints
# -------------------------------------------------
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(transactions_bp)

# -------------------------------------------------
# Routes (Template Rendering Only)
# -------------------------------------------------
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
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
# -------------------------------------------------
# Database Initialization & Seeding
# -------------------------------------------------
def seed_admin_user():
    """Ensures a default admin user exists if the DB is empty."""
    from models import User
    try:
        admin_email = "admin.kl@bankedge.com"
        existing = User.query.filter_by(username=admin_email).first()
        if not existing:
            print(f" [DB] Seeding default startup admin: {admin_email}")
            user = User(username=admin_email, role='admin', balance=100000.0)
            user.set_password("Admin@123")
            db.session.add(user)
            db.session.commit()
            print(" [DB] Startup admin created.")
    except Exception as e:
        print(f" [DB] WARNING: Startup seeding skipped: {e}")

with app.app_context():
    # 1. Handle SQLite paths
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        db_path = os.path.join(basedir, 'instance', 'bankedge.db')
        instance_dir = os.path.dirname(db_path)
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir, exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    # 2. Synchronize Tables (PostgreSQL tables won't be deleted, only created if missing)
    try:
        db.create_all()
        seed_admin_user()
    except Exception as e:
        print(f" [DB] Database init error: {e}")

# -------------------------------------------------
# Pre-load ML Model (Crucial for Gunicorn --preload)
# -------------------------------------------------
from controllers.transactions_controller import init_model
with app.app_context():
    init_model()

# -------------------------------------------------
# Start Server
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
