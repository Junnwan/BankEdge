from flask import Blueprint, render_template

edge_bp = Blueprint('edge', __name__)

@edge_bp.route('/edge-devices')
def edge_devices():
    # You can later fetch edge device data here from DB or API
    return render_template('edge_devices.html')