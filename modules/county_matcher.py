import json
from pathlib import Path

from rapidfuzz import process as fuzz_process

from modules.config import COUNTIES_FILE, FUZZY_THRESHOLD
from modules.exceptions import CountyNotFoundError
from modules.models import County

def load_counties(path: Path = COUNTIES_FILE) -> list[County]:
    with path.open() as file_handle:
        return [County.model_validate(c) for c in json.load(file_handle)]

def match_county(county_raw: str, counties: list[County]) -> County:
    names = [c.name for c in counties]
    result = fuzz_process.extractOne(county_raw,names)

    if result is None:
        raise Exception(f"County list is empty, could not match '{county_raw}.'")
    
    match, score, index = result

    if score <FUZZY_THRESHOLD:
        raise CountyNotFoundError(county_raw,match,score,FUZZY_THRESHOLD)
    
    return counties[index]