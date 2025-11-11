from flask import Blueprint, render_template

sync_bp = Blueprint('sync', __name__)

@sync_bp.route('/data-sync')
def data_sync():
    # You can later handle sync logic here
    return render_template('data_sync.html')