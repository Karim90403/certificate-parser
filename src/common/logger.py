import logging
import sys
from loguru import logger


def format_record(record: dict) -> str:
    if record.get("exception"):
        return "{exception}\n"
    return "{time} | {level} | {message}\n"


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def init_logging():
    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict)
    intercept_handler = InterceptHandler()
    for runners_logger in loggers:
        runners_logger.propagate = False
        runners_logger.handlers = [intercept_handler]

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logging.INFO,
                "format": format_record,
                "serialize": False,
            }
        ]
    )
    logger.info("Init logger")
