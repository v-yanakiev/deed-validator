## Approach

### AI is isolated to one step
The LLM (called in `extractor.py`) does only one thing: convert unstructured text to a typed Python object.
It is given explicit instructions NOT to "fix" values.
All validation is done in deterministic Python code afterward.

### Date validation
Caught with a simple `date_recorded < date_signed` comparison.

### Amount mismatch
`word2number` independently parses the written-out amount.
In our case, we flag the discrepancy of 50 thousand dollars and reject the deed

### County matching
`rapidfuzz` fuzzy-matches "S.Clara" -> "Santa Clara" with a confidence threshold.
If confidence < 70%, we reject rather than guess.

### On generalizability
This solution is scoped to the provided deed format.
In production, parsed fields would carry a confidence score,
and validation output would be a triage signal (auto-approve / human review / hard reject),
rather than binary valid / invalid.