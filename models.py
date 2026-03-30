from datetime import datetime
from pydantic import BaseModel

class ParsedDeed(BaseModel):
    doc_id: str
    county_raw: str
    state: str
    date_signed: datetime
    date_recorded: datetime
    grantor: str
    grantee: str
    amount_numeric: float
    amount_words: str
    apn: str
    status: str

class ValidatedDeed(BaseModel):
    parsed: ParsedDeed
    county_name:str
    tax_rate: float
    closing_cost: float