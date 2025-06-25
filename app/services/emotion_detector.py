import cv2 as cv
from ultralytics import YOLO
import app.services.state as state
label_dict = {
   0:"Anger",
   1:"Contempt",
   2:"Disgust" ,
   3:"Fear",
   4:"Happy",
   5:"Neutral",
   6:"Sad",
   7:"Surprise",
}
current_emotion = ""
def get_emotion():
    global current_emotion
    video = cv.VideoCapture(0)
    model = YOLO(r'app\models\best.pt')
    while state.is_running:
        res,frame = video.read()
        result=model(frame)[0]
        for box in result.boxes:
            x1,y1,x2,y2 = map(int,box.xyxy[0])
            conf =float(box.conf[0])
            cls = int(box.cls[0])
            emotion = label_dict[cls]
            current_emotion = emotion
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(frame, emotion, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX,0.8, (0, 255, 0), 2)
        # Encode the frame to send it to the frontend
        ret, buffer = cv.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')