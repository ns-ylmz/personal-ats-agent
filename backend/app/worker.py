import threading
import queue
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

job_queue = queue.Queue()

def worker_loop():
    logger.info("Worker thread started.")
    while True:
        try:
            job = job_queue.get()
            if job is None:  # Poison pill to stop the thread
                logger.info("Worker thread stopping.")
                break
            
            logger.info(f"Processing job: {job}")
            time.sleep(2)  # Simulate work
            logger.info(f"Job {job} processed successfully.")
            
            job_queue.task_done()
        except Exception as e:
            logger.error(f"Error processing job: {e}")

def start_worker():
    thread = threading.Thread(target=worker_loop, daemon=True)
    thread.start()
    return thread
