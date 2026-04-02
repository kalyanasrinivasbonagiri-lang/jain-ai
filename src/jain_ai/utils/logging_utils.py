import logging


def configure_logging(level):
    logging.basicConfig(
        level=str(level).upper(),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def get_logger(name):
    return logging.getLogger(name)
