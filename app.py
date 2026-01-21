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
# Increase SQLite timeout to reduce "database is locked" errors
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"timeout": 30}
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secrets
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')

# Stripe (keys only stored – logic handled fully inside transactions_controller)
app.config['STRIPE_PUBLISHABLE_KEY'] = os.environ.get('STRIPE_PUBLISHABLE_KEY')
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')

# JWT Token Expiry
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

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
# Database Auto-Creation (First Run Only)
# -------------------------------------------------
# -------------------------------------------------
# Database Auto-Creation & Seeding
# -------------------------------------------------
def seed_admin_user():
    """Ensures the default admin user exists."""
    from models import User
    try:
        admin_email = "admin.kl@bankedge.com"
        existing = User.query.filter_by(username=admin_email).first()
        if not existing:
            print(f"Seeding default admin: {admin_email}")
            user = User(username=admin_email, role='admin', balance=100000.0)
            user.set_password("Admin@123")
            db.session.add(user)
            db.session.commit()
            print("Default admin created.")
    except Exception as e:
        print(f"Failed to seed admin user: {e}")

with app.app_context():
    # Ensure 'instance' folder exists
    db_path = os.path.join(basedir, 'instance', 'bankedge.db')
    
    # Check if instance folder exists
    instance_dir = os.path.dirname(db_path)
    if not os.path.exists(instance_dir):
        try:
            os.makedirs(instance_dir)
            print(f"Created instance directory: {instance_dir}")
        except OSError as e:
            print(f"Error creating instance directory: {e}")

    # Re-configure URI if using default SQLite (Critical for Gunicorn)
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. Creating tables...")
        try:
            db.create_all()
            print("Tables created successfully.")
            seed_admin_user() 
        except Exception as e:
            print(f"Error creating database: {e}")
    else:
        # DB exists, but maybe empty? Ensure admin exists.
        seed_admin_user()

# -------------------------------------------------
# Start Server
# -------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
