from flask import Blueprint,jsonify

get_emotion_bp = Blueprint('get_emotion',__name__)
from app.services.emotion_detector import current_emotion
@get_emotion_bp.route('/get_emotion')
def fetch_emotion():
    state = {"emotion" : current_emotion}
    return jsonify(state)

