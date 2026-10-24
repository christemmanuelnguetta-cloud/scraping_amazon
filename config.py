"""Configuration du scraper Amazon."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_SEARCH_URL = "https://www.amazon.fr/s?k=casque+bluetooth+sans+fil"
DEFAULT_LIMIT = 10
MAX_LIMIT = 10
DEFAULT_DATABASE = PROJECT_ROOT / "data" / "casques_bluetooth.db"
PAGE_LOAD_TIMEOUT_SECONDS = 30
