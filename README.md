## Approach

## AI is isolated to one step
The LLM (called in `extractor.py`) does only one thing: convert unstructured text to a typed Python object.
It is given explicit instructions NOT to "fix" values.
All validation is done in deterministic Python code afterward.