import logging
import sys


def setup_logger(name=__name__, level=logging.INFO):
    logger = logging.getLogger(name)

    # Avoid multiple handlers
    if not logger.hasHandlers():
        logger.setLevel(level)

        # Create the handler
        file_handler = logging.FileHandler("../logs/app.log", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        # Create a formatter to be set on the handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Adding handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
