import sys

from config import RAW_OCR_TEXT
from county_matcher import load_counties, match_county
from enricher import enrich_with_tax_rate
from exceptions import AmountMismatchError, CountyNotFoundError, DateOrderError, DeedValidationError
from extractor import extract_with_llm
from validator import validate_amount_consistency, validate_date_order


def process_deed(ocr_text:str):
    print("Extracting fields with LLM...")
    deed= extract_with_llm(ocr_text)

    print ("Matching county...")
    counties=load_counties()
    county=match_county(deed.county_raw,counties)

    print("Validating date order...")
    validate_date_order(deed)

    print("Validating amount consistency...")
    validate_amount_consistency(deed)

    print("Enriching with tax data...")
    return enrich_with_tax_rate(deed, county)

def main() -> None:
    try:
        result = process_deed(RAW_OCR_TEXT)
    except DateOrderError as exception:
        print (f"\n[DATE ORDER ERROR] {exception}", file= sys.stderr)
    except AmountMismatchError as exception:
        print(f"\n[AMOUNT MISMATCH ERROR {exception}",file=sys.stderr)
    except CountyNotFoundError as exception:
        print(f"\n[COUNTY LOOKUP ERROR] {exception}", file=sys.stderr)
        sys.exit(1)
    except DeedValidationError as exception:
        print(f"\n[VALIDATION ERROR] {exception}", file=sys.stderr)
        sys.exit(1)
        