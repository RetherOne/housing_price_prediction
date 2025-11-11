import logging
import sys


def _setup_logger():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    return logging.getLogger("my_FastAPI")


logger = _setup_logger()
