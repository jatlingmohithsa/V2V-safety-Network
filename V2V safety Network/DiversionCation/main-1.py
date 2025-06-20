import cv2
import winsound
import time
import os

# Load the Haar Cascade classifier for vehicle detection
# Use the full path to the cars.xml file
cascade_path = 'D:\\V2V safety Network\\DiversionCation\\cars.xml'
if not os.path.exists(cascade_path):
    print(f"Error: Haar Cascade file not found at {cascade_path}")
    print("Please ensure 'cars.xml' is in the 'D:\\V2V safety Network\\DiversionCation\\' directory or provide the correct path.")
    exit()
car_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize video capture with the path to your video file
video_path = 'D:\\V2V safety Network\\DiversionCation\\video.mp4'
cap = cv2.VideoCapture(video_path)
# To use a webcam, change the above line to:
# cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(f"Error: Could not open video file: {video_path}")
    print("Please ensure 'video.mp4' is in the 'D:\\V2V safety Network\\DiversionCation\\' directory or provide the correct path.")
    exit()

# Function to send notification and beep
def notify_and_beep():
    print("Notification: A vehicle is passing by, please slow down!")
    try:
        winsound.Beep(440, 500)  # Frequency 440 Hz, duration 500 ms
    except AttributeError:
        print("Warning: winsound module not available on this platform (non-Windows).")

# Loop to continuously capture frames
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video stream.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect vehicles in the frame
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    # Check if any vehicles are detected
    if len(cars) > 0:
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # Assuming a threshold for a potentially "close" vehicle
            # Adjust these thresholds based on your video and desired sensitivity
            if w > 80 or h > 80:
                notify_and_beep()

    # Display the resulting frame
    cv2.imshow('Vehicle Detection', frame)

    # Break the loop on 'Esc' key press
    if cv2.waitKey(33) == 27:
        print("Exiting on 'Esc' key press.")
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
print("Video capture released and windows closed.")