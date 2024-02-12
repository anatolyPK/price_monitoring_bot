import logging
import os
from logging.handlers import RotatingFileHandler

script_dir = os.path.dirname(os.path.abspath(__file__))

base_log_file_path = os.path.join(script_dir, "logs", "information.log")


def setup_logger(name, level=logging.DEBUG, log_file_path=base_log_file_path, max_bytes=10485760, backup_count=5):

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s')

    file_handler = RotatingFileHandler(log_file_path, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
