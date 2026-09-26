#!/usr/bin/env python3
"""Pass 10974: with the R-symmetries established by the orbifold CFT, the plane-rotation door of Pass 10968
closes; three more W(3,3) orbifold families are censused.

Bizet, Kobayashi, Mayorga Pena, Parameswaran, Schmitz, Zavala (arXiv:1301.2322) derive the R-charge selection
rule from the worldsheet-instanton symmetries.  The old per-plane rule sum_alpha R^i = -1 mod N_i with
R^i = q_sh^i - N^i + Nbar^i is recovered ONLY for prime planes of factorizable orbifolds.  For a non-prime plane
the gamma-phase of the fixed-point combination contributes (R = q_sh - N + Nbar + N gamma), and non-prime planes
merge into one law.  orbifolder 1.2 (used for Pass 10968) applies the old rule on every plane.

A. Z6-II on G2 x SU(3) x SU(2)^2: the SU(3) (order 3) and SU(2)^2 (order 2) planes are prime -> Z3^R, Z2^R valid;
   the G2 plane (order 6) is not.  With the valid R-symmetries only, matter parity exists in Z6II_23 alone and
   every one of its 304 FI-cancelling extreme rays is parity-obstructed: 0/128.  (Removing a symmetry can only
   remove parity elements, so every other Z6-II closure of Passes 10960-10968 stands.)
B. Adding the gamma-corrected G2-plane charge R1' = R1 + 6 gamma (gamma = theta-eigenphase of the fixed-point
   combination, component 0 of the orbifolder's centralizer gamma list; frozen from a gamma-phase dump) keeps
   Z6II_23 closed: 304 FI rays, 0 realizable.
C. Families (frozen ledgers; general parity = torus x space group, + W-invariant R-combinations where the
   geometry defines R-symmetries):  Z2xZ6-I 29 SMs (from Pass 10968), Z3xZ6 5 SMs -- no parity-preserving
   FI-cancelling vacuum in either.
D. Z12-I on the non-factorizable E6 lattice: no R-rule is established (1301.2322 treats Z12-I on SU(3)xF4);
   the 9 Pass 10968 verdicts that used per-plane rules are reclassified 'undetermined'; the 5 obtained with
   gauge + point-group rules alone stand.
"""
from __future__ import annotations

import gzip
import importlib.util
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10967", ROOT / "analysis" / "w33_pass10967_fi_vacuum_regenerates_rpv.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
GAMMA = ROOT / "data" / "w33_pass10974_z6ii23_gamma_phases.json.gz"
FAMILIES = {"Z2xZ6-I": ROOT / "data" / "w33_pass10968_z2xz6_ledger.json.gz",
            "Z3xZ6": ROOT / "data" / "w33_pass10974_z3xz6_ledger.json.gz"}
P10968 = ROOT / "data" / "w33_pass10968_r_symmetry_parity_and_massless_exotics.json"
OUT = ROOT / "data" / "w33_pass10974_valid_r_rules_close_the_rotation_door.json"
Z6II23 = "Z6-II|Z6II_23__SM_20260917_2913"


def with_R(name, model, disc, R_cols, orders, W):
    """general parity with extra R coordinates (list of per-field charge lists) and W offsets."""
    d2 = json.loads(json.dumps(disc))
    d2["nonR_orders"] = disc["nonR_orders"] + orders
    for f, v in d2["fields"].items():
        v["nonR"] = v["nonR"] + [str(x) for x in R_cols[f]]
    nq = len(model["left"][0]["q"])
    wvec = [Fraction(0)] * (nq + len(disc["nonR_orders"])) + [Fraction(w) / n for n, w in zip(orders, W)]
    orig = M.realizable
    M.general_parity.__globals__["realizable"] = lambda vecs, odd, _o=orig: _o(vecs + [wvec], odd)
    try:
        r = M.general_parity(name, model, d2)
    finally:
        M.general_parity.__globals__["realizable"] = orig
    r.pop("farkas", None)
    return r


def summarize(r):
    return {k: r.get(k) for k in ("parity_exists", "verdict", "fi_cancelling_rays", "realizable_rays", "anomaly_free")}


def main():
    ledger, sha = M.P.load_ledger()
    disc = M.load(M.DISC)
    # ---- A: valid prime-plane R-symmetries only (Z3^R, Z2^R)
    A, Asum = {}, Counter()
    for name in sorted(ledger):
        if not name.startswith("Z6-II|"):
            continue
        d = disc[name.split("|")[1]]
        RN = [(int(x.split(":")[0]), Fraction(x.split(":")[1])) for x in d["R"]]
        assert [n for n, _ in RN] == [6, 3, 2]
        Rc = {f: [Fraction(v["R"][1]), Fraction(v["R"][2])] for f, v in d["fields"].items()}
        r = with_R(name, ledger[name], d, Rc, [3, 2], [RN[1][1], RN[2][1]])
        A[name] = summarize(r)
        Asum["models"] += 1
        Asum["parity_exists"] += r["parity_exists"]
        v = r.get("verdict", "")
        Asum["closed"] += v.startswith("closed")
        Asum["open"] += v == "COUNTEREXAMPLE"
        print("A" if r["parity_exists"] else ".", end="", flush=True)
    print("\nA", dict(Asum), flush=True)
    # ---- B: gamma-corrected G2-plane R charge for Z6II_23
    with gzip.open(GAMMA, "rt") as fh:
        G = json.load(fh)
    d = disc[Z6II23.split("|")[1]]
    for f, v in d["fields"].items():
        assert [Fraction(x) for x in v["R"]] == [Fraction(x) for x in G[f]["R"].split(",")], f
    Rc = {}
    for f, v in d["fields"].items():
        R = [Fraction(x) for x in G[f]["R"].split(",")]
        gam = [Fraction(x) for x in G[f]["gamma"].split(",")]
        Rc[f] = [R[0] + 6 * gam[0], R[1], R[2]]
    B = summarize(with_R(Z6II23, ledger[Z6II23], d, Rc, [6, 3, 2], [-1, -1, -1]))
    print("B", B, flush=True)
    # ---- C: families
    Cres = {}
    for fam, path in FAMILIES.items():
        with gzip.open(path, "rt") as fh:
            blob = json.load(fh)
        L, D = blob["ledger"], blob["disc"]
        cs = Counter()
        for name in sorted(L):
            b = name.split("|")[1]
            r0 = M.general_parity(name, L[name], D[b])
            cs["models"] += 1
            cs["parity_torus_sg"] += r0["parity_exists"]
            cs["open_torus_sg"] += r0.get("verdict") == "COUNTEREXAMPLE"
            if D[b]["R"]:
                RN = [(int(x.split(":")[0]), Fraction(x.split(":")[1])) for x in D[b]["R"]]
                Rc = {f: [Fraction(x) for x in v["R"]] for f, v in D[b]["fields"].items()}
                r1 = with_R(name, L[name], D[b], Rc, [n for n, _ in RN], [w for _, w in RN])
                cs["parity_with_R"] += r1["parity_exists"]
                cs["open_with_R"] += r1.get("verdict") == "COUNTEREXAMPLE"
        Cres[fam] = dict(cs)
        print("C", fam, dict(cs), flush=True)
    # ---- D: Z12-I reclassification
    z12 = json.loads(P10968.read_text())["z12_models"]
    Dres = Counter()
    for r in z12.values():
        v = r.get("verdict", "")
        if "robust" in v:
            Dres["dead_robust"] += 1
        elif "tentative" in v:
            Dres["undetermined"] += 1
        elif "support" in r:
            Dres["other_with_vacuum"] += 1
    print("D", dict(Dres), flush=True)
    OUT.write_text(json.dumps(dict(pass_id=10974, ledger_sha256=sha, A=dict(summary=dict(Asum), models=A), B=B,
                                   C=Cres, D=dict(Dres)), indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
