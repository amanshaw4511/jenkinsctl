import logging
import sys

def setup_logging(log_level=logging.INFO):
    # Configure the logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),  # Output logs to stdout
        ]
    )

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    return logger
