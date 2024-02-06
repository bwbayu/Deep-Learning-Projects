from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

emotion_labels = {0: 'sad', 1: 'disgust', 2: 'angry', 3: 'neutral', 4: 'fear', 5: 'surprise', 6: 'happy'}
emotion_counts = {label: 0 for label in emotion_labels.values()}

faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# frame prediction
@app.route('/process_frame', methods=['POST'])
def process_frame():
    # ambil data image
    data = request.json
    image_src = data.get('image')
    # convert ke format deepface
    img_np = cv2.imdecode(np.frombuffer(base64.b64decode(image_src.split(',')[1]), np.uint8), cv2.IMREAD_COLOR)

    # convert ke grayscale 
    gray_frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # deteksi muka
    faces = faceDetect.detectMultiScale(gray_frame, 1.3, 3)
    if len(faces) > 0:
        # model prediksi deepface
        result = DeepFace.analyze(img_np, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        print("EMOTION = " + emotion)
        emotion_counts[emotion] += 1


    return jsonify({'status': 'success'})

# show result
@app.route('/result')
def result():
    global emotion_counts # global variabel
    # hitung percentage
    total_frames = sum(emotion_counts.values())
    percentage_distribution = {label: count / total_frames * 100 for label, count in emotion_counts.items()}
    
    # re deklarasi variabel global
    temp = emotion_counts    
    emotion_counts = {label: 0 for label in emotion_labels.values()}

    return jsonify({'status':'success', 'percentage_distribution':percentage_distribution, 'emotion_counts':temp})

@app.route('/')
def index():
    return "reload complete"

if __name__ == '__main__':
    app.run(debug=True)
