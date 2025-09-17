# capture.py
import cv2
import time
import os

CAPTURE_FPS = 30  # Target FPS for capture

def capture_thread(frame_q, source=0):
    """
    Continuously capture frames from a camera or video file and push to frame_q.
    
    Args:
        frame_q (queue.Queue): Queue to store captured frames
        source (int or str): Camera index (0,1,2...) OR video file path
    """
    # If source is a string and exists as a file → treat as video file
    if isinstance(source, str) and os.path.exists(source):
        print(f"🎥 Using video file: {source}")
        cap = cv2.VideoCapture(source)
    else:
        print(f"📷 Using camera index: {source}")
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("❌ Error: Could not open source.")
        return

    last_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ End of video stream or frame capture failed.")
            break  # Exit loop if video ends or frame is invalid

        # Throttle to target FPS
        if time.time() - last_time < 1 / CAPTURE_FPS:
            continue

        # Put frame in queue
        if not frame_q.full():
            frame_q.put(frame)

        last_time = time.time()

    cap.release()
    print("✅ Capture thread ended.")

