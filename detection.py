def detection_thread(frame_q, det_q, det_fps_q):
    last_time = 0
    while True:
        if time.time() - last_time < 1 / DETECTOR_FPS:
            continue
        if frame_q.empty():
            continue
        frame = frame_q.get()
        dets = detect_objects(frame)
        if not det_q.full():
            det_q.put(dets)

        fps = 1 / (time.time() - last_time + 1e-6)
        if not det_fps_q.full():
            det_fps_q.put(fps)

        last_time = time.time()
