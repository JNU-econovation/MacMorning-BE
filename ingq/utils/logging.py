import logging

def get_logger(name: str, log_file: str = "ingq.log"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Colsole
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    
    # File
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    return logger