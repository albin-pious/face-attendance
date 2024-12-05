import cv2
import numpy as np
import os

video_path = '/home/albin/projects/face-recognise/face-app-2.0/utils/people_video1.mp4'

cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'

if not os.path.exists(cascade_path):
    print(f"Error: Cascade file not found at {cascade_path}")
    exit()

people_cascade = cv2.CascadeClassifier(cascade_path)

if people_cascade.empty():
    print("Error: Failed to load cascade classifier")
    exit()

cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Video processing complete")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    people = people_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in people:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.putText(frame, f'People: {len(people)}', 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 255, 0), 
                2)

    cv2.imshow('People Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()