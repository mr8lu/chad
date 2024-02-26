import logging
import json
from logging.handlers import TimedRotatingFileHandler


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_message = {
            "level": record.levelname,
            "name": record.name,
            "msg": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
        }
        if hasattr(record, 'extra_field'):
            log_message['extra_field'] = record.extra_field
        return json.dumps(log_message)


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.extra_field = 'extra_value'  # Example dynamic value
        return True


def configure_logging(debug_mode, log_file):
    logger = logging.getLogger('debug_logger')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Prevent logging messages from being duplicated to the root logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(log_file, when="midnight")
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    logger.addFilter(ContextFilter())

    return logger
