import logging
import os

## Creating a log folder

LOG_DIR="logs"
os.makedirs(LOG_DIR,exist_ok=True)


def get_logger(filename:str)->logging.Logger:
    log_file=os.path.splitext(filename)[0]+".log"

    log_path=os.path.join(LOG_DIR,log_file)

    ## Creating a logger object
    Logger=logging.getLogger(log_file)

    Logger.setLevel(logging.DEBUG)

    if not Logger.handlers:
        file_handler=logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | "
            "%(filename)s:%(lineno)d | "
            "%(funcName)s() | %(message)s"
        )
        file_handler.setFormatter(formatter)

        Logger.addHandler(file_handler)

    return Logger