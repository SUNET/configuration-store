from typing import Optional
from os import path
import sys
import logging
from logging.handlers import SysLogHandler

LOGGER_NAME = "confstore"


def get_logger(stdout: Optional[bool] = False,
               debug: Optional[bool] = False) -> logging.Logger:
    """Get logger.

    :output: s generates SysLogHandler, otherwise StreamHandler
    :debug: set debug
    """

    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

        if stdout:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = (SysLogHandler(address="/dev/log")
                       if path.exists("/dev/log")
                       else SysLogHandler())

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger
