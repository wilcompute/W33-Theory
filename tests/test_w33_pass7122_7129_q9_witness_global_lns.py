from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "data" / "PART_W33_PASS7122_7129_Q9_WITNESS_GLOBAL_LNS.json"
WIT = ROOT / "data" / "PART_W33_Q9_PARTIAL_OVOID_51.json"
PRODUCER = ROOT / "analysis" / "w33_pass7122_7129_q9_witness_global_lns.py"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_frozen_witness_is_self_contained():
    w = load(WIT)
    assert w["q"] == 9 and w["size"] == 51
    assert len(w["points"]) == len(w["point_indices"]) == 51
    assert w["verified_pairwise_noncollinear"] is True
    assert w["zero_blockers"] == 0 and w["one_blockers"] == 1
    assert w["blocker_moment_sum"] == 4590
    assert w["blocker_pair_moment_sum"] == 12750
    assert w["gram_rank_over_GF9"] == 4


def test_blocker_profile_and_exchange_rigidity_are_frozen():
    d = load(CERT)
    assert d["pass_7123_blocker_moments"]["histogram"] == {
        "1":1,"2":22,"3":50,"4":102,"5":156,"6":120,"7":142,"8":107,"9":53,"10":16
    }
    assert d["pass_7124_maximality"]["therefore_inclusion_maximal"] is True
    assert d["pass_7124_maximality"]["unique_one_for_one_exchange"] == {"add":40,"remove":80}
    assert d["pass_7125_exchange_rigidity"]["stable_through_removed_points"] == 7
    assert all(v["augmenting_set"] is None
               for v in d["pass_7125_exchange_rigidity"]["exact_search"].values())


def test_producer_replays_frozen_certificate():
    before = load(CERT)
    subprocess.run([sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
                   capture_output=True, text=True)
    assert load(CERT) == before


def test_scope_does_not_claim_optimality():
    d = load(CERT)["pass_7127_scope"]
    assert d["lower_bound"] == 51 and d["published_upper_bound"] == 73
    assert "alpha(W(3,9)) = 51" in d["not_proved"]
    assert "nonexistence of a 52-set" in d["not_proved"]
