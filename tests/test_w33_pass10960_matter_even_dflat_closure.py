"""Regression for Pass 10960: exact re-verification of the matter-even D-flat closure."""
import gzip
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "p10960", ROOT / "analysis" / "w33_pass10960_matter_even_dflat_closure.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)
CERT = json.loads((ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json").read_text())
LEDGER, SHA = P.load_ledger()
Z2 = json.loads(gzip.decompress((ROOT / "data" / "w33_pass10960_z2_character_certificates.json.gz").read_bytes()))


def singlet_types(model):
    left = []
    for f in model["left"]:
        dims = f["dim"].split(",")
        left.append(dict(name=f["name"], base=P.base_of(f["name"]),
                         trivial=all(abs(int(P.re.match(r"(-?\d+)", d).group(1))) == 1 and "adj" not in d
                                     for d in dims),
                         q=[Fraction(x) for x in f["q"]]))
    lab = [f for f in left if f["base"] in P.SMY]
    y = P.solve_affine([f["q"] for f in lab], [P.SMY[f["base"]] for f in lab])[0]
    types = {}
    for f in left:
        if f["trivial"] and P.dot(y, f["q"]) == 0:
            types.setdefault(tuple(f["q"]), []).append(f["name"])
    return left, types


def test_ledger_hash_and_summary():
    assert SHA == CERT["ledger_sha256"]
    s = CERT["summary"]
    assert s["models"] == 215 and s["anomaly_free"] == 4
    # positive controls: the prior repo counts are reproduced
    assert (s["dflat_any_Z6I"], s["dflat_any_Z6II"]) == (23, 105)
    assert s["bl_direction"] == 88
    # the result
    assert s["bl_counterexamples"] == 0
    assert (s["bl_closed_no_dflat"], s["bl_closed_farkas_union"], s["bl_closed_by_rays"]) == (64, 23, 1)
    assert s["z2_characters"] == 1024 and s["z2_even_dflat"] == 0


@pytest.mark.parametrize("name", sorted(k for k, v in CERT["models"].items() if v.get("bl_direction")))
def test_bl_family_farkas_certificates(name):
    rec = CERT["models"][name]
    left, types = singlet_types(LEDGER[name])
    T = list(types)
    s = 1 if Fraction(rec["trace_anomalous"]) > 0 else -1
    C = [s * t[0] for t in T]
    M = [list(t[1:]) for t in T]
    if "farkas_all" in rec:
        lam = [Fraction(v) for v in rec["farkas_all"]]
        assert all(c + P.dot(lam, m) >= 0 for c, m in zip(C, M))
    elif "farkas_ever_even" in rec:
        lam = [Fraction(v) for v in rec["farkas_ever_even"]]
        never = {tuple(t["fields"]) for t in rec["never_even_types"]}
        ever = [i for i, t in enumerate(T) if tuple(types[t]) not in never]
        assert len(ever) == rec["ever_even_types"]
        assert all(C[i] + P.dot(lam, M[i]) >= 0 for i in ever)
        # every never-even type has fixed odd 3(B-L) = +-3: a B-L = +-1 (sneutrino-type) singlet
        assert all(t["three_BminusL"] in ("3", "-3") for t in rec["never_even_types"])
        # and a genuine D-flat direction exists (it must use a never-even type)
        assert rec["dflat_any"] and rec["dflat_witness"]
        wit = set(rec["dflat_witness"])
        assert wit & {f for t in rec["never_even_types"] for f in t["fields"]}
    else:
        assert rec["bl_verdict"].startswith("closed: every")
        assert rec["realizable_even_rays"] == 0 and rec["anomaly_cancelling_rays"] == 304


def test_z2_character_certificates():
    checked = 0
    for name, certs in Z2.items():
        if not certs:
            continue
        left, types = singlet_types(LEDGER[name])
        T = list(types)
        rec = CERT["models"][name]
        s = 1 if Fraction(rec["trace_anomalous"]) > 0 else -1
        r, coords = P.lattice_coords([f["q"] for f in left])
        idx = {f["name"]: i for i, f in enumerate(left)}
        for c in certs:
            par = [sum(e * x for e, x in zip(c["eps"], co)) % 2 for co in coords]
            assert all(p == 1 for p, f in zip(par, left) if f["base"] in P.MATTER)
            ev = [t for t in T if par[idx[types[t][0]]] == 0]
            lam = [Fraction(v) for v in c["lambda"]]
            assert all(s * t[0] + P.dot(lam, list(t[1:])) >= 0 for t in ev)
            checked += 1
    assert checked == CERT["summary"]["z2_characters"]


def test_realizability_solver_controls():
    # alpha + beta t = 2m : solvable and unsolvable controls
    ok, why = P.realizable([Fraction(1)], [[Fraction(1)]])
    assert ok and Fraction(why["t"][0]) % 2 == 1  # t odd makes 1 + t even
    ok, _ = P.realizable([Fraction(1), Fraction(0)], [[Fraction(2)], [Fraction(2)]])
    assert not ok  # 1 + 2t and 2t cannot both be even
    ok, _ = P.realizable([Fraction(3), Fraction(0)], [[Fraction(0)], [Fraction(1)]])
    assert not ok  # a fixed odd value is never even
