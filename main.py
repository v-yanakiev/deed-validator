import sys

from modules.config import RAW_OCR_TEXT
from modules.county_matcher import load_counties, match_county
from modules.enricher import enrich_with_tax_rate
from modules.exceptions import AmountMismatchError, CountyNotFoundError, DateOrderError, DeedValidationError
from modules.extractor import extract_with_llm
from modules.validator import validate_amount_consistency, validate_date_order


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
        parsed=result.parsed
        
        print("\n--- Validated Deed ---")
        print(f"Document ID : {parsed.doc_id}" )
        print(f"Grantor : {parsed.grantor}" )
        print(f"Grantee : {parsed.grantee}" )
        print(f"Signed : {parsed.date_signed.date()}" )
        print(f"Recorded : {parsed.date_recorded.date()}" )
        print(f"County : {result.county_name}" )
        print(f"State : {parsed.state}" )
        print(f"APN : {parsed.apn}" )
        print(f"Sale Amount : {parsed.amount_numeric:,.2f}" )
        print(f"Tax Rate : {result.tax_rate:.1%}" )
        print(f"Closing Cost : {result.closing_cost:,.2f}" )
        print(f"Status : {parsed.status}" )
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

if __name__=="__main__":
    main()