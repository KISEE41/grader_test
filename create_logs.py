import os
from datetime import datetime

from loguru import logger


def create_logs(filename):
    # Prepare log directory and file
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'commit_{filename}.log')
        
        # Add a new log file configuration to the logger
    logger.add(log_file, format="{time} {level} {message}", level="DEBUG", rotation="10 MB", retention="10 days")
        