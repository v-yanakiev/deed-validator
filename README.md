# deed-validator

## Setup
Requires [uv](https://docs.astral.sh/uv/)
```bash
uv sync
cp .env.example .env # add your OPENAI_API_KEY
uv run main.py
```
## Expected output

```
Extracting fields with LLM...
Matching county...
Validating date order...

[DATE ORDER ERROR] Date order violation: recorded 2024-01-10 is before signed 2024-01-15.
```

The deed also contains a 50 thousand dollars discrepancy between the numeric and written-out amounts.
The date error is caught first and halts execution - fix the dates and the amount error surfaces next:
```
Extracting fields with LLM...
Matching county...
Validating date order...
Validating amount consistency...

[AMOUNT MISMATCH ERROR] Amount mismatch: numeric figure is $1,250,000.00 but written words resolve to $1,200,000.00 (difference: $50,000.00).
```

## Approach

### AI is isolated to one step
The LLM (called in `extractor.py`) does only one thing: convert unstructured text to a typed Python object.
It is given explicit instructions NOT to "fix" values.
All validation is done in deterministic Python code afterward.

### Date validation
Caught with a simple `date_recorded < date_signed` comparison.

### Amount mismatch
`numerizer` independently parses the written-out amount.
In our case, we flag the discrepancy of 50 thousand dollars and reject the deed

### County matching
`rapidfuzz` fuzzy-matches "S.Clara" -> "Santa Clara" with a confidence threshold.
If confidence < 70%, we reject rather than guess.

### On generalizability
This solution is scoped to the provided deed format.
In production, parsed fields would carry a confidence score,
and validation output would be a triage signal (auto-approve / human review / hard reject),
rather than binary valid / invalid.