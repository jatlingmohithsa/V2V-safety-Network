import cv2
import os

# Load the Haar Cascade classifier for vehicle detection
cascade_path = 'D:\V2V safety Network\DiversionCation\cars.xml'
if not os.path.exists(cascade_path):
    print("Haar Cascade file not found.")
    exit()

car_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize video capture (0 for webcam or provide video file path)
cap = cv2.VideoCapture('video.mp4')

# Function to send notification
def send_notification():
    print("Notification: A vehicle is passing by, please slow down!")

# Loop to continuously capture frames
while True:
    ret, frames = cap.read()
    if not ret:
        print("Failed to capture video")
        break

    # Convert frames to grayscale
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

    # Detect vehicles in the frame
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Check if any vehicles are detected
    if len(cars) > 0:
        for (x, y, w, h) in cars:
            cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 0, 255), 2)
            send_notification()  # Call this without the width check

    # Display the resulting frame
    cv2.imshow('Vehicle Detection', frames)

    # Break the loop on 'Esc' key press
    if cv2.waitKey(33) == 27:
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()