import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")
validate = jsonschema.validate

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_JSON = ROOT / "archive" / "json"


def first_existing(*paths):
    for path in paths:
        path = Path(path)
        if path.exists():
            return path
    joined = ", ".join(str(path) for path in paths)
    raise FileNotFoundError(f"None of the expected fixtures exist: {joined}")


def load(path):
    return json.loads(Path(path).read_text())


def test_summary_matches_schema():
    s_path = ROOT / "schemas" / "summary_results.schema.json"
    schema = load(s_path)
    data = load(
        first_existing(
            ROOT / "SUMMARY_RESULTS.json",
            ARCHIVE_JSON / "SUMMARY_RESULTS.json",
        )
    )
    validate(instance=data, schema=schema)


def test_numeric_comparisons_matches_schema():
    s_path = ROOT / "schemas" / "numeric_comparisons.schema.json"
    schema = load(s_path)
    data = load(
        first_existing(
            ROOT / "NUMERIC_COMPARISONS.json",
            ARCHIVE_JSON / "NUMERIC_COMPARISONS.json",
        )
    )
    validate(instance=data, schema=schema)
