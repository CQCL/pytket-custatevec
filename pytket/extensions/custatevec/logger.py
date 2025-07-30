import logging  # noqa: D100
from logging import Logger


def set_logger(
    logger_name: str,
    level: int = logging.WARNING,
    file: str | None = None,
    fmt: str = "[%(asctime)s.%(msecs)03d] %(name)s (%(levelname)s) - %(message)s",
) -> Logger:
    """Initialises and configures a logger object.

    Args:
        logger_name: Name for the logger object.
        level: Logger output level.
        file: File to write the log on.
        fmt: Logger output format.

    Returns:
        New configured logger object.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = False

    handler: logging.StreamHandler
    handler = logging.StreamHandler() if file is None else logging.FileHandler(file)
    handler.setLevel(level)
    formatter = logging.Formatter(fmt, datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
