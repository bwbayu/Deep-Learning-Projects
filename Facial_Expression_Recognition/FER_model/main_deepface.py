# MODEL : https://github.com/serengil/deepface

from deepface import DeepFace
import cv2
import time

emotion_labels = {0: 'sad', 1: 'disgust', 2: 'angry', 3: 'neutral', 4: 'fear', 5: 'surprise', 6: 'happy'}

def main():
    # video_path = 'human_expression.mp4'
    # cap = cv2.VideoCapture(video_path)
    cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    emotion_counts = {label: 0 for label in emotion_labels.values()}
    faceDetect=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow('Camera', frame)

        if int(time.time()) % 3 == 0:
            try:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray_frame, 1.3, 3)
                if len(faces) > 0: # face detect
                    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                    emotion = result[0]['dominant_emotion']
                    print("Predicted Emotion:", emotion)
                    emotion_counts[emotion] += 1
            except Exception as e:
                print(f"Error analyzing emotion: {e}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1 / fps)

    cap.release()
    cv2.destroyAllWindows()

    total_frames = sum(emotion_counts.values())
    percentage_distribution = {label: count / total_frames * 100 for label, count in emotion_counts.items()}

    # Print the results
    print("\nEmotion Counts:")
    for label, count in emotion_counts.items():
        print(f"{label}: {count}")

    print("\nPersentase:")
    for label, percentage in percentage_distribution.items():
        print(f"{label}: {percentage:.2f}%")

if __name__ == '__main__':
    main()
