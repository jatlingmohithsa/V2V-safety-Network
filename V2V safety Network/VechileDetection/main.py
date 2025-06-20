# import cv2
# from ultralytics import YOLO

# # Load the YOLOv8 pretrained model (YOLOv8n is light, you can use YOLOv8s, m, l, or x)
# model = YOLO('yolov8n.pt')  # Make sure you downloaded the model or it'll auto-download

# # Define vehicle classes (based on COCO dataset IDs)
# vehicle_classes = ['car', 'motorcycle', 'bus', 'truck', 'bicycle']

# # Open the video file
# video_path = 'video.mp4'  # Replace with your file
# cap = cv2.VideoCapture(video_path)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Run YOLOv8 inference on the frame
#     results = model(frame)

#     # Draw bounding boxes
#     for result in results:
#         for box in result.boxes:
#             cls_id = int(box.cls[0])
#             class_name = model.names[cls_id]
#             if class_name in vehicle_classes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 label = f"{class_name} {box.conf[0]:.2f}"
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, label, (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     cv2.imshow('Vehicle Detection', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

"""import cv2
from ultralytics import YOLO
from playsound import playsound
import threading

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Define vehicle classes
vehicle_classes = ['car', 'motorcycle', 'bus', 'truck', 'bicycle']

# Load video
video_path = 'video.mp4'
cap = cv2.VideoCapture(video_path)

# Sound function to play in separate thread
def play_warning_sound():
    playsound('warning.mp3')  # Place a short beep mp3 in your directory

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            if class_name == 'car':
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                box_width = x2 - x1
                box_height = y2 - y1
                box_area = box_width * box_height

                # Threshold for "closeness" (you can tune this based on video resolution)
                if box_area > 50000:
                    # Red box and warning label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, 'WARNING: Car too close!', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # Play sound in separate thread (non-blocking)
                    threading.Thread(target=play_warning_sound, daemon=True).start()
                else:
                    # Normal green box
                    label = f"{class_name} {box.conf[0]:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Vehicle Detection with Warning', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""
import cv2
import os
from ultralytics import YOLO
from playsound import playsound
import threading

# Load YOLOv8 model
try:
    model = YOLO('yolov8n.pt')
    print("YOLOv8 model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLOv8 model: {e}")
    exit()

# Define vehicle classes (optional, as the model detects many objects)
vehicle_classes = ['car', 'motorcycle', 'bus', 'truck', 'bicycle']

# Load video
script_directory = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_directory, 'video.mp4')
print(f"Attempting to open video at path: {video_path}") # Debugging
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Error: Could not open video file: {video_path}")
    print("Please ensure 'video.mp4' is in the same directory as this script or provide the correct path.")
    exit()
else:
    print(f"Video file opened successfully: {video_path}")

# Sound function to play in a separate thread
def play_warning_sound():
    try:
        playsound('warning.mp3')  # Place a short beep mp3 in your directory
        print("Warning sound played.")
    except Exception as e:
        print(f"Error playing sound: {e}")
        print("Please ensure 'warning.mp3' is in the same directory as this script.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video stream.")
        break

    results = model(frame)
    # print(f"Number of detections in this frame: {len(results)}") # Debugging

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]
            confidence = box.conf[0]
            xyxy = box.xyxy[0].cpu().numpy().round().astype(int)
            x1, y1, x2, y2 = xyxy

            # print(f"Detected: {class_name} with confidence {confidence:.2f} at ({x1}, {y1}), ({x2}, {y2})") # Debugging

            if class_name == 'car':
                box_width = x2 - x1
                box_height = y2 - y1
                box_area = box_width * box_height
                # print(f"Car box area: {box_area}") # Debugging

                # Threshold for "closeness" (tune this based on your video resolution and desired sensitivity)
                if box_area > 50000:
                    # Red box and warning label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, 'WARNING: Car too close!', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    # Play sound in a separate thread (non-blocking)
                    threading.Thread(target=play_warning_sound, daemon=True).start()
                else:
                    # Normal green box with confidence
                    label = f"{class_name} {confidence:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                # For other detected objects (not cars), draw a green box with confidence
                label = f"{class_name} {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Vehicle Detection with Warning', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting on 'q' key press.")
        break

cap.release()
cv2.destroyAllWindows()
print("Video capture released and windows closed.")