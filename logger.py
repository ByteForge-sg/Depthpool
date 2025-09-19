import time
import psutil
import tensorflow as tf

LOG_DIR = "logs/pipeline"

# Create TensorBoard writer
writer = tf.summary.create_file_writer(LOG_DIR)

def log_data(step, fps_depth, fps_det, distances):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    # GPU usage (if NVIDIA available)
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        gpu = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    except:
        gpu = -1  # fallback if no GPU monitoring

    with writer.as_default():
        tf.summary.scalar("FPS/Depth", fps_depth, step=step)
        tf.summary.scalar("FPS/Detection", fps_det, step=step)
        tf.summary.scalar("System/CPU", cpu, step=step)
        tf.summary.scalar("System/GPU", gpu, step=step)
        tf.summary.scalar("System/RAM", ram, step=step)

        # Log each object distance separately
        for i, d in enumerate(distances):
            tf.summary.scalar(f"Distances/Object_{i}", d, step=step)

        writer.flush()
