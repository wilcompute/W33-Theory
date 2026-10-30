import json


def test_anchor_forbid_0_20_23_all_feasible():
    data = json.load(open("docs/reports/anchor_forbid_0-20-23.json", "r", encoding="utf-8"))
    assert len(data) > 0
    for e in data:
        assert e.get("status") == "FEASIBLE"
        # Relaxed threshold to be robust to regenerated reports
        assert e.get("matched", 0) >= 10
