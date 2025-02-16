import cv2
from boxmot import BYTETracker
import numpy as np
from ultralytics import YOLO

# Load the YOLO v8n model
model = YOLO('../weights/yolov8n.pt')
model = model.to('cuda')

# Initialize the ByteTracker
tracker = BYTETracker(
    track_thresh=0.25,
    track_buffer=30,
    match_thresh=0.8,
    frame_rate=30
)

# Open your video source
video = cv2.VideoCapture(0)  # Use 0 for webcam or provide a video file path

while True:
    ret, frame = video.read()
    if not ret:
        break
    
    # Run YOLO v8 inference on the frame, looking for exclusively for the person class
    results = model(frame, classes=0)
    
    # Run the object detection model to get detections
    detections = results[0].boxes.data.cpu().numpy() # a NumPy array
    
    # Update the tracker with new detections
    tracks = tracker.update(detections, frame)
    
    # Process and display the tracks
    for track in tracks:
        x1, y1, x2, y2, track_id = track[:5]
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {int(track_id)}", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow('Tracking', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

