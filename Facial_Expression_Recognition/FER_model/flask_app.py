from flask import Flask, render_template, Response, redirect, url_for
from deepface import DeepFace
import cv2
import time
import threading

app = Flask(__name__)

emotion_labels = {0: 'sad', 1: 'disgust', 2: 'angry', 3: 'neutral', 4: 'fear', 5: 'surprise', 6: 'happy'}
emotion_counts = {label: 0 for label in emotion_labels.values()}

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)
faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

running = True

def capture_frames():
    global running
    while running:
        ret, frame = cap.read()

        if ret:
            try:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray_frame, 1.3, 3)
                if len(faces) > 0:
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                    emotion = result[0]['dominant_emotion']
                    emotion_counts[emotion] += 1
            except Exception as e:
                print(f"Error analyzing emotion: {e}")

            time.sleep(1 / fps)

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_camera')
def start_camera():
    global running
    running = True
    threading.Thread(target=capture_frames).start()
    return "Camera started"

@app.route('/stop_camera')
def stop_camera():
    global running
    running = False
    return redirect(url_for('result'))

@app.route('/result')
def result():
    total_frames = sum(emotion_counts.values())
    percentage_distribution = {label: count / total_frames * 100 for label, count in emotion_counts.items()}

    # Print the results
    result_text = "\nEmotion Counts:\n"
    for label, count in emotion_counts.items():
        result_text += f"{label}: {count} times\n"

    result_text += "\nPercentage Distribution:\n"
    for label, percentage in percentage_distribution.items():
        result_text += f"{label}: {percentage:.2f}%\n"

    return result_text

if __name__ == '__main__':
    app.run(debug=True)
