import multiprocessing as mp
from config import load_config
from core.camera import camera_process
from core.detection import detection_process
from core.depth_estimation import depth_process
from core.correction import correction_viz_process

if __name__ == "__main__":
    config = load_config()

    frame_queue = mp.Queue()
    detection_queue = mp.Queue()
    depth_queue = mp.Queue()

    processes = [
        mp.Process(target=camera_process, args=(frame_queue, config, 0)),
        mp.Process(target=detection_process, args=(frame_queue, detection_queue, 1)),
        mp.Process(target=depth_process, args=(detection_queue, depth_queue, 2)),
        mp.Process(target=correction_viz_process, args=(depth_queue, 3))
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()