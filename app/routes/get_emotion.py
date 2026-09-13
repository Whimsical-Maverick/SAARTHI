from flask import Blueprint,jsonify

get_emotion_bp = Blueprint('get_emotion',__name__)
import app.services.state as state
@get_emotion_bp.route('/get_emotion')
def fetch_emotion():
    return jsonify({"emotion": state.current_emotion})

