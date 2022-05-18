import logging


def create_logger():
    logger = logging.getLogger('basic')
    logger.setLevel('INFO')

    file_handler = logging.FileHandler('logs/basic.txt')
    logger.addHandler(file_handler)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    return logger
