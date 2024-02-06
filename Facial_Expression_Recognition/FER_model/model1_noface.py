from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import cv2
import torch
import time
import numpy as np

# Load model directly
processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")

def predict_emotion_from_frame(frame):
    try:
        # Convert the OpenCV BGR image to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert the grayscale frame to RGB (Pillow format)
        image = Image.fromarray(cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB))
        # # Convert the OpenCV BGR image to RGB (Pillow format)
        # image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        inputs = processor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=1).item()
        emotion = model.config.id2label[predictions]
        return emotion
    except Exception as e:
        return str(e)

emotion_labels = {0: 'sad', 1: 'disgust', 2: 'angry', 3: 'neutral', 4: 'fear', 5: 'surprise', 6: 'happy'}
def main():
    # Open the video file
    video_path = 'human_expression.mp4'  # Replace with your video file path
    cap = cv2.VideoCapture(video_path)
    # Open the default camera (camera index 0)
    # cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)

    faceDetect=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    emotion_counts = {label: 0 for label in emotion_labels.values()}

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Display the frame
        cv2.imshow('Camera', frame)
        

        # Make predictions continuously
        if int(time.time()) % 3 == 0:
            emotion = predict_emotion_from_frame(frame)
            print("Predicted Emotion:", emotion)
            emotion_counts[emotion] += 1

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