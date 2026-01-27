import json
from pathlib import Path
import pytest


def test_part_cvii_sage_results():
    """Ensure PART_CVII_sage_results.json exists and contains expected core values."""
    p = Path("PART_CVII_sage_results.json")
    if not p.exists():
        pytest.skip("PART_CVII_sage_results.json not found — run the E8 Sage test to generate it")

    data = json.loads(p.read_text(encoding="utf-8"))

    assert data.get("vertices") == 40
    assert data.get("edges") == 240
    assert data.get("e8_roots") == 240
    assert data.get("match") is True
