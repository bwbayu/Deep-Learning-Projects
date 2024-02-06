from PIL import Image
import cv2
import torch
import time
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('model_file_30epochs.h5')

emotion_labels = {0: 'sad', 1: 'disgust', 2: 'angry', 3: 'neutral', 4: 'fear', 5: 'surprise', 6: 'happy'}

def predict_emotion(faceDetect,frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 3)

    for x, y, w, h in faces:
        sub_face_img = gray[y:y+h, x:x+w]
        resized = cv2.resize(sub_face_img, (48, 48))
        normalize = resized / 255.0
        reshaped = np.reshape(normalize, (1, 48, 48, 1))
        result = model.predict(reshaped)
        label = np.argmax(result, axis=1)[0]
        label = emotion_labels[label]
        return label

def main():
    video_path = 'human_expression.mp4'  # Replace with your video file path
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    emotion_counts = {label: 0 for label in emotion_labels.values()}

    start_time = time.time()
    interval = 10  # seconds

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        current_time = time.time()
        elapsed_time = current_time - start_time

        # Make predictions every 10 seconds
        if elapsed_time >= interval:
            emotion = predict_emotion(faceDetect,frame)
            emotion_counts[emotion] += 1
            print(f"Predicted Emotion in last 10 seconds: {emotion}")
            start_time = current_time

        # Display the frame
        cv2.imshow('Camera', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1 / fps)

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Calculate percentage distribution
    total_frames = sum(emotion_counts.values())
    percentage_distribution = {label: count / total_frames * 100 for label, count in emotion_counts.items()}

    # Print the results
    print("\nEmotion Counts:")
    for label, count in emotion_counts.items():
        print(f"{label}: {count} times")

    print("\nPercentage Distribution:")
    for label, percentage in percentage_distribution.items():
        print(f"{label}: {percentage:.2f}%")

if __name__ == '__main__':
    main()
