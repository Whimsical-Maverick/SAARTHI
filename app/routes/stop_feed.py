from flask import Blueprint,jsonify
stop_feed_bp = Blueprint('stop_feed',__name__)
import app.services.state as state
@stop_feed_bp.route('/stop_feed')
def feedstop():
    state.is_running = False
    data = {"message":"FEED_STOPPED"}
    return jsonify(data)
