import argparse

def load_config():
    parser = argparse.ArgumentParser(description="Self Driving AI Config")

    parser.add_argument("--source", type=str, default="webcam",
                        choices=["webcam", "video", "dataset"],
                        help="Input source: webcam | video | dataset")

    parser.add_argument("--camera_index", type=int, default=0,
                        help="Webcam index (0 = default)")

    parser.add_argument("--video_path", type=str, default="data/sample_video.mp4",
                        help="Path to video file if source=video")

    parser.add_argument("--dataset_path", type=str, default="data/images/*.jpg",
                        help="Path to dataset folder if source=dataset")

    args = parser.parse_args()

    CONFIG = {
        "camera_source": args.source,
        "camera_index": args.camera_index,
        "video_path": args.video_path,
        "dataset_path": args.dataset_path
    }
    return CONFIG