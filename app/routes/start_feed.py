from flask import Blueprint,jsonify
import app.services.state as state
start_feed_bp = Blueprint('start_feed',__name__)
@start_feed_bp.route('/start_feed')
def feedstart():
    state.is_running = True
    data = {"message":"FEED_STARTED...PLEASE KEEP LOOKING IN THE CAMERA"}
    return jsonify(data)