import json
from pathlib import Path

from jsonschema import ValidationError, validate


def load(path):
    return json.loads(Path(path).read_text())


def test_summary_matches_schema():
    s_path = Path("schemas/summary_results.schema.json")
    schema = load(s_path)
    data = load("SUMMARY_RESULTS.json")
    validate(instance=data, schema=schema)


def test_numeric_comparisons_matches_schema():
    s_path = Path("schemas/numeric_comparisons.schema.json")
    schema = load(s_path)
    data = load("NUMERIC_COMPARISONS.json")
    validate(instance=data, schema=schema)
