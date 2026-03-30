import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from models import ParsedDeed

load_dotenv()

SYSTEM_PROMPT= """\
You are a document parser. Extract fields from a raw OCR deed and return them as a single JSON object.
Clean up obvious OCR noise (dots in acronyms, HTML entities like &amp;) 
but do NOT correct logical errors - return dates and amounts exactly as they appear in the source text.

Return only the JSON object, no commentary.

Required keys:
    doc_id (string)
    county_raw (string, abbreviation is fine)
    state (string, 2-letter code)
    date_signed (string, YYYY-MM-DD)
    date_recorded (string, YYYY-MM-DD)
    grantor (string, cleaned up)
    grantee (string, cleaned up)
    amount_numeric (number, from the $ figure)
    amount_words (string, the written-out English form, no trailing "Dollars")
    apn (string)
    status (string)
"""