from flask import Blueprint,Response
from app.services.emotion_detector import get_emotion
video_bp = Blueprint('video',__name__)

@video_bp.route('/video_feed')
def video():
    return Response(get_emotion(),mimetype='multipart/x-mixed-replace; boundary=frame')