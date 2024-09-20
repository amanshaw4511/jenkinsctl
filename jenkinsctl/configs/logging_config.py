import logging
import sys

def setup_logging(log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    file_handler = logging.FileHandler('jenkinsctl.log')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger