"""Regression for Pass 10965: baryon triality is impossible in all 215 W(3,3) Z6 models."""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10965", ROOT / "analysis" / "w33_pass10965_baryon_triality_impossible.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
CERT = json.loads((ROOT / "data" / "w33_pass10965_baryon_triality_impossible.json").read_text())
LEDGER, SHA = M.P.load_ledger()


def test_summary():
    s = CERT["summary"]
    assert CERT["ledger_sha256"] == SHA
    assert s == {"models": 215, "b3_possible": 0, "su5_single_copy_relation": 214,
                 "relation_certificates": 1, "zero_target_control_ok": 215}


def test_su5_relation_kills_b3_for_every_hypercharge_shift():
    # u^c + e^c - 2q: B3 gives 2, the hypercharge shift 6Y gives 0 (mod 3)
    assert (M.B3["bu"] + M.B3["be"] - 2 * M.B3["q"]) % 3 == 2
    assert (M.Y6["bu"] + M.Y6["be"] - 2 * M.Y6["q"]) % 3 == 0


def test_relation_certificates_are_exact():
    for name, rec in CERT["models"].items():
        if rec["relation_certificate"] is None:
            continue
        left = {f["name"]: f for f in LEDGER[name]["left"]}
        w = rec["relation_certificate"]
        n = len(next(iter(left.values()))["q"])
        tot = [sum(c * F(left[k]["q"][i]) for k, c in w.items()) for i in range(n)]
        assert all(v == 0 for v in tot)
        assert sum(c * M.B3[M.P.base_of(k)] for k, c in w.items()) % 3 != 0
        assert sum(c * M.Y6[M.P.base_of(k)] for k, c in w.items()) % 3 == 0
