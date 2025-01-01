import logging

class DevelopmentFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return record.levelname in ("DEBUG", "INFO", "ERROR")