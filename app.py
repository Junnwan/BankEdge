from flask import Flask, render_template
from controllers.api_controller import api_bp # <-- ONLY blueprint we need

app = Flask(__name__)

# Register Blueprints (controllers)
app.register_blueprint(api_bp) # <-- API is registered

# --- Public Route ---
@app.route('/')
def login():
    """
    Serves the login page.
    """
    return render_template('login.html')

# --- Protected Dashboard Routes ---
@app.route('/dashboard')
def dashboard():
    """Serves the main dashboard page (index.html)."""
    return render_template('index.html', title='Dashboard')

@app.route('/edge-devices')
def edge_devices_route():
    """Serves the Edge Devices page."""
    return render_template('edge_devices.html', title='Edge Devices')

@app.route('/ml-insights')
def ml_insights():
    """Serves the ML Insights page."""
    return render_template('ml_insights.html', title='ML Insights')

@app.route('/transactions')
def transactions():
    """Serves the Transactions page."""
    return render_template('transactions.html', title='Transaction Processing')

@app.route('/system-management')
def system_management():
    """Serves the System Management page."""
    return render_template('system_management.html', title='System Management')

if __name__ == '__main__':
    app.run(debug=True)