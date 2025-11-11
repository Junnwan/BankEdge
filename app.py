from flask import Flask, render_template
from controllers.edge_controller import edge_bp
from controllers.sync_controller import sync_bp

app = Flask(__name__)

# Register Blueprints (controllers)
app.register_blueprint(edge_bp)
app.register_blueprint(sync_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)