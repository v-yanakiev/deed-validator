from county_matcher import load_counties, match_county
from enricher import enrich_with_tax_rate
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