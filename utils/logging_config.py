import logging
from pathlib import Path


def configure_file_logging() -> None:
    log_path = Path("logs/test_run.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        if getattr(handler, "_api_test_file_handler", False):
            root_logger.removeHandler(handler)
            handler.close()

    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    file_handler._api_test_file_handler = True
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)
