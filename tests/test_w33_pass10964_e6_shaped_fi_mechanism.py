"""Regression for Pass 10964: the E6-shaped FI functional, re-verified exactly."""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10964", ROOT / "analysis" / "w33_pass10964_e6_shaped_fi_mechanism.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
P = M.P
CERT = json.loads((ROOT / "data" / "w33_pass10964_e6_shaped_fi_mechanism.json").read_text())
C60 = json.loads((ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json").read_text())["models"]
LEDGER, SHA = P.load_ledger()
DFLAT = sorted(k for k, v in CERT["models"].items() if v["dflat_models_class"])


def test_summary():
    assert CERT["ledger_sha256"] == SHA
    s = CERT["summary"]
    assert s["D-flat (23) shaped=True"] == 23 and len(DFLAT) == 23
    assert s["D-flat models whose f<0 singlets are all forced (B-L=+1) singlets"] == 23
    assert s["D-flat models with f = -8 mu on the forced singlets"] == 23


def test_e6_charges_reproduce_the_shape():
    # f/mu = 4 Q_psi - (4/5) Q_chi with Q_chi = 4Y - 5(B-L)
    def f(Y, BL, psi):
        return 4 * psi - F(4, 5) * (4 * Y - 5 * BL)
    assert f(F(1, 6), F(1, 3), 1) == F(24, 5)   # q in 16_1
    assert f(F(-2, 3), F(-1, 3), 1) == F(24, 5)  # u^c
    assert f(F(1), F(1), 1) == F(24, 5)          # e^c
    assert f(F(1, 3), F(-1, 3), 1) == F(8, 5)    # d^c
    assert f(F(-1, 2), F(-1), 1) == F(8, 5)      # l
    assert f(F(1, 2), F(0), -2) == F(-48, 5)     # H_u in 10_{-2}
    assert f(F(0), F(1), -3) == F(-8)            # nu^c direction of 16_{-3} in the 78
    assert f(F(0), F(1), 1) == F(8)              # nu^c of the matter 16_1


@pytest.mark.parametrize("name", DFLAT)
def test_certificate_exact(name):
    rec = CERT["models"][name]
    left, sing = M.fields(LEDGER[name])
    s = 1 if F(C60[name]["trace_anomalous"]) > 0 else -1
    fv = [F(s)] + [F(v) for v in rec["lam"]]
    mu = F(rec["mu"])
    assert mu > 0
    never = {fld for t in C60[name]["never_even_types"] for fld in t["fields"]}
    for fl in left:
        val = P.dot(fv, fl["q"])
        if fl["base"] in M.TEN:
            assert val == mu * F(24, 5)
        elif fl["base"] in M.FIVEB:
            assert val == mu * F(8, 5)
    vals = {fl["name"]: P.dot(fv, fl["q"]) / mu for fl in sing}
    assert set(vals.values()) <= {F(-8), F(0), F(8)}
    assert all(v >= 0 for n, v in vals.items() if n not in never)
    assert {n for n, v in vals.items() if v < 0} <= never
