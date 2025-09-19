import cv2
import numpy as np
from utils import compute_distance, update_k_scale

def visualization_thread(frame_q, depth_q, det_q):
    k_scale = 1.0
    while True:
        if frame_q.empty() or depth_q.empty() or det_q.empty():
            continue

        frame = frame_q.get()
        depth_map = depth_q.get()
        dets = det_q.get()

        distances = []
        for det in dets:
            bbox = det["bbox"]
            d, k_scale = compute_distance(depth_map, bbox, k_scale)
            distances.append(d)
            x1, y1, x2, y2 = bbox.astype(int)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"cls {det['class']} : {d:.2f}m", 
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.6, (0, 255, 0), 2)

        cv2.imshow("YOLO + Depth Anything", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
