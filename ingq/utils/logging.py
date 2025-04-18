import logging


def get_logger(name: str, log_file: str = "ingq.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

    if not logger.handlers:
        # Colsole
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # File
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
    else:
        logger.debug(f"'{name}' 핸들러가 존재합니다. 핸들러 생성을 건너뜁니다.")

    return logger
