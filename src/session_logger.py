# session_logger.py
from datetime import datetime

def start_log(output_dir: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = f"{output_dir}/logs/scan_log_{timestamp}.txt"
    return open(log_path, "w", encoding="utf-8")  # Caller is responsible for closing it
