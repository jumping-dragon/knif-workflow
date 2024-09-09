import logging

from .config import LOGGER_LEVEL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(filename)s#%(lineno)d: %(message)s",
)
logger = logging.getLogger("intel-feed")
logger.setLevel(LOGGER_LEVEL)
