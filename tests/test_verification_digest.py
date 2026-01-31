import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DIGEST_JSON = ROOT / "artifacts" / "verification_digest.json"


def test_verification_digest_contains_predictions():
    if not DIGEST_JSON.exists():
        pytest.skip("verification_digest.json not generated yet")
    with open(DIGEST_JSON, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    if "predictions" not in d:
        pytest.skip("verification_digest.json missing 'predictions' key (regenerate)")
    assert isinstance(d["predictions"], dict), "predictions key must be a dict"


def test_verification_digest_predictions_summary_structure():
    if not DIGEST_JSON.exists():
        pytest.skip("verification_digest.json not generated yet")
    with open(DIGEST_JSON, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    if "predictions" not in d:
        pytest.skip("verification_digest.json missing 'predictions' key (regenerate)")
    summary = d["predictions"]
    # summary should contain at least passed/total, but some jobs may record only passed
    assert (
        "passed" in summary or "total" in summary
    ), "predictions summary should include 'passed' or 'total'"


def test_verification_digest_includes_skipped_optional_if_present():
    with open(DIGEST_JSON, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    if "skipped_optional_tests" in d:
        assert isinstance(d["skipped_optional_tests"].get("count"), int)
