"""Regression for Pass 10962: exact re-verification of the hidden-sector tier certificates."""
import gzip
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p10962", ROOT / "analysis" / "w33_pass10962_hidden_sector_dflat_tiers.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
P = M.P
CERT = json.loads((ROOT / "data" / "w33_pass10962_hidden_sector_dflat_tiers.json").read_text())
LEDGER, SHA = P.load_ledger()
GRAW = (ROOT / "data" / "w33_pass10962_hidden_gauge_ledger.json.gz").read_bytes()
GAUGE = json.loads(gzip.decompress(GRAW))
C60 = json.loads((ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json").read_text())["models"]


def test_provenance_and_summary():
    assert CERT["ledger_sha256"] == SHA
    assert CERT["gauge_ledger_sha256"] == hashlib.sha256(GRAW).hexdigest()
    s = CERT["summary"]
    assert s.get("A: closed for every hidden-sector direction (exact)") == 32
    assert s.get("B: closed over all listed invariant generators (exact Farkas)") == 55
    assert sum(v for k, v in s.items() if k[:2] in ("A:", "B:", "C:", "OP")) == 88
    assert "OPEN" not in s
    # the four anomaly-free models admit no matter parity at all
    assert s["anomaly_free_models_with_any_matter_parity"] == 0 and len(CERT["anomaly_free_models"]) == 4


def test_weight_systems():
    # dimensions and weight sums of the hidden representations used
    assert len(M.weights(["SU", 5], "10")) == 10 and len(M.weights(["SU", 5], "-5")) == 5
    assert len(M.weights(["SU", 4], "6")) == 6
    assert len(M.weights(["SO", 5], "16")) == 16 and len(M.weights(["SO", 5], "-16")) == 16
    assert len(M.weights(["SO", 4], "8c")) == 8 and len(M.weights(["SO", 4], "8s")) == 8
    for g, x in ((["SU", 3], "3"), (["SU", 5], "10"), (["SO", 5], "16"), (["SU", 2], "2")):
        ws = M.weights(g, x)
        assert all(sum(w[i] for w in ws) == 0 for i in range(len(ws[0])))  # weights of a rep sum to 0
    # SO(10): 16-bar is minus 16
    s16 = set(M.weights(["SO", 5], "16"))
    assert set(tuple(-v for v in w) for w in s16) == set(M.weights(["SO", 5], "-16"))


@pytest.mark.parametrize("name", sorted(k for k, v in CERT["models"].items()
                                        if v["verdict"].startswith(("A:", "B:"))))
def test_tier_certificates(name):
    rec = CERT["models"][name]
    groups = GAUGE[name]
    fl, hidden, x0, N = M.model_data(name, LEDGER[name], groups)
    s = 1 if Fraction(C60[name]["trace_anomalous"]) > 0 else -1
    if rec["verdict"].startswith("A:"):
        C, Mm, U = M.tier_a_data(fl, hidden, groups, x0, N, s)
        lam = [Fraction(v) for v in rec["tier_a"]["farkas"]]
        # the stored Farkas vector, checked exactly on every ever-even weight component
        assert len(U) == rec["tier_a"]["ever_even"]
        assert all(C[i] + P.dot(lam, Mm[i]) >= 0 for i in U)
    else:
        out, (T, types, C, Mm, alpha, beta, U) = M.tier_b(fl, groups, x0, N, s)
        lam = [Fraction(v) for v in rec["tier_b"]["farkas"]]
        assert all(C[i] + P.dot(lam, Mm[i]) >= 0 for i in U)
        assert rec["tier_b"]["incomplete_because"]  # completeness is honestly not claimed
