from models import County, ParsedDeed, ValidatedDeed

def enrich_with_tax_rate(deed: ParsedDeed, county: County) -> ValidatedDeed:
    tax_rate= county.tax_rate

    return ValidatedDeed(
        parsed=deed,
        county_name=county.name,
        tax_rate=tax_rate,
        closing_cost=deed.amount_numeric * tax_rate
    )