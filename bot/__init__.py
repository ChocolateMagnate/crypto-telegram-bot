import sys
import logging
from pathlib import Path

PARENT_DIRECTORY = Path(__file__).parent
CRYPTO_PROJECTS_PATH = PARENT_DIRECTORY / "crypto-projects.json"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)