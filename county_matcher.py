import json
from pathlib import Path

from rapidfuzz import process as fuzz_process

from config import COUNTIES_FILE, FUZZY_THRESHOLD
from exceptions import CountyNotFoundError
from models import County

def load_counties(path: Path = COUNTIES_FILE) -> list[County]:
    with path.open() as file_handle:
        return [County.model_validate(c) for c in json.load(file_handle)]

