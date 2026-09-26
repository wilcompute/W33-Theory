"""Regression for Pass 10967: the FI vacuum regenerates R-parity violation."""
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10967", ROOT / "analysis" / "w33_pass10967_fi_vacuum_regenerates_rpv.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
CERT = json.loads((ROOT / "data" / "w33_pass10967_fi_vacuum_regenerates_rpv.json").read_text())
LEDGER, SHA = M.P.load_ledger()


def test_ledger_hash():
    assert CERT["ledger_sha256"] == SHA


def test_realizability_known_answers():
    one, two = [F(1)], [F(2)]
    assert M.realizable([one], [0])                      # x = 1/2
    assert M.realizable([two], [0])                      # x = 1/4
    assert M.realizable([one, two], [0])                 # x = 1/2 makes 2x = 1 even
    assert not M.realizable([one, two], [0, 1])          # 2x cannot be odd if x is
    e1, e2, e12 = [F(1), F(0)], [F(0), F(1)], [F(1), F(1)]
    assert M.realizable([e1, e2, e12], [0, 1])
    assert not M.realizable([e1, e2, e12], [0, 1, 2])    # odd + odd = odd is impossible


def test_general_parity_summary():
    assert CERT["summary"]["A"] == {"models": 215, "parity_exists": 88, "closed_farkas": 87,
                                    "closed_rays": 1, "counterexamples": 0}


def test_general_parity_is_not_vacuous():
    # the D-flat models ARE D-flat with the FI term once parity is ignored (Pass 10960)
    base = json.loads((ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json").read_text())["models"]
    dflat_bl = [n for n, r in base.items() if r.get("dflat_any") and r.get("bl_direction")]
    assert len(dflat_bl) == 24
    for n in dflat_bl:
        assert CERT["general_parity"][n]["parity_exists"]
        assert CERT["general_parity"][n]["ever_even_types"] < CERT["general_parity"][n]["singlet_types"]


def test_forced_singlets_carry_the_rpv_charge():
    B = CERT["summary"]["B"]
    assert B["forced_singlets"] == 302 and B["bl_models"] == 88
    assert B["udd:n*op qld:n*op lle:n*op"] == 290
    assert "none" not in B


def test_forced_relation_exact_in_flagship():
    name = "Z6-I|Z6I_06__SM_20260917_2"
    q = {f["name"]: [F(x) for x in f["q"]] for f in LEDGER[name]["left"]}
    tot = [a + b + c + d for a, b, c, d in zip(q["n_12"], q["bu_1"], q["bd_1"], q["bd_2"])]
    assert all(v == 0 for v in tot)


def test_string_couplings():
    C = CERT["summary"]["C"]
    assert C["Z6-I_dflat_models"] == 23 and C["Z6-I_no_cubic_rpv_all_forced_regenerate_all_three"] == 23
    z = CERT["string_couplings"]["Z6-II|Z6II_23__SM_20260917_2913"]
    assert z["qld_order3"] > 0 and z["lle_order3"] > 0 and z["udd_order3"] == 0
    assert z["udd_by_order"] == {"5": 144, "6": 1216}
