import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name, level=logging.DEBUG, log_file_path="../logs/information.log", max_bytes=10485760, backup_count=5):
    log_file_path = os.path.abspath(log_file_path)

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
