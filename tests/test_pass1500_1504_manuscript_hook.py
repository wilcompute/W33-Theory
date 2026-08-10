from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "paper" / "sections" / "sec_complement_duality.tex"
BODY = ROOT / "paper" / "sections" / "sec_complement_duality_body.tex"
INSERT = ROOT / "paper" / "sections" / "sec_bt1500_bt1504_five_frontiers.tex"
AUDIT = ROOT / "data" / "pass1500_1504_manuscript_hook_audit.json"


def test_reversible_hook():
    text = WRAPPER.read_text(encoding="utf-8")
    assert text.count(r"\input{sections/sec_complement_duality_body}") == 1
    assert text.count(r"\input{sections/sec_bt1500_bt1504_five_frontiers}") == 1
    assert BODY.exists() and INSERT.exists()
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["status"] == "PASS"
    assert audit["properties"]["original_preserved_byte_for_byte"] is True
    assert audit["properties"]["mathematical_release_unchanged"] is True
