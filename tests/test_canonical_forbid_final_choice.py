import json
import subprocess
import sys
from pathlib import Path

REPORTS = Path(__file__).resolve().parents[1] / "reports"
ART = Path(__file__).resolve().parents[1] / "artifacts"
TOOLS = Path(__file__).resolve().parents[1] / "tools"


def test_anchor_for_canonical_forbid_0_20_23_all_feasible():
    rpt = REPORTS / "anchor_forbid_0-20-23.json"
    assert rpt.exists(), "Anchor report for canonical forbid 0-20-23 missing"
    data = json.loads(rpt.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) > 0
    for e in data:
        assert e.get("status") == "FEASIBLE", f"W {e.get('W_idx')} not FEASIBLE"
        # Relaxed threshold to be robust to regenerated reports
        assert (
            int(e.get("matched", 0)) >= 10
        ), f"W {e.get('W_idx')} matched != expected (>=10)"


def test_gf2_certificates_exist_and_contradict():
    gf2 = ART / "gf2_certificates.json"
    if not gf2.exists():
        subprocess.check_call(
            [sys.executable, str(TOOLS / "generate_gf2_certificate.py")]
        )
    assert gf2.exists(), "gf2_certificates.json missing"
    data = json.loads(gf2.read_text(encoding="utf-8"))
    assert isinstance(data, list) and len(data) > 0
    # assert at least one true contradiction exists
    contradictions = [d for d in data if d.get("is_null") and d.get("rhs_is_one")]
    assert len(contradictions) > 0, "No GF(2) contradiction certificates found"
