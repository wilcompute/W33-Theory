#!/usr/bin/env python3
"""Pass 10964: the FI obstruction acts through one E6-shaped U(1) that only right-handed sneutrinos balance.

Pass 10960 showed that in the 23 W(3,3) Z6-I Standard Models that have FI-cancelling D-flat
singlet directions, every such direction condenses a singlet with 3(B-L) = 3 fixed by the
Standard Model.  Its certificates were arbitrary Farkas vertices.  This pass asks for a
CANONICAL certificate of a prescribed physical shape:

    f = s Q_anom + lambda . Q_nonanom      (a U(1) direction of the model)
    f = mu * 24/5  on every q, u^c, e^c    (the SU(5) 10)
    f = mu *  8/5  on every d^c and l      (the SU(5) 5-bar)
    mu > 0,  f >= 0 on every singlet that can be matter-even for some B-L choice.

On the families this is f = mu (4 Q_psi - (4/5) Q_chi) with Q_chi = 4Y - 5(B-L) and Q_psi = 1:
the U(1) combination of E6 > SO(10) x U(1)_psi > SU(5) x U(1)_chi x U(1)_psi.  Because
D-flatness forces sum_i f(q_i)|phi_i|^2 = s * (FI side) < 0, a D-flat vacuum needs a singlet
with f < 0.  The pass solves the shaped LP exactly (cdd, GMP), verifies every constraint in
exact arithmetic, and records the value of f on the forced (never-even) singlets.  For
(B-L, Y) = (1, 0) one has Q_chi = -5, and f = -8 mu then corresponds to Q_psi = -3: the
Standard-Model-singlet direction of the 16_{-3} in the adjoint 78 of E6.

The same shaped LP is also run on the 64 models with no D-flat direction at all (f >= 0 on
every singlet) as a secondary census.
"""
from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import cdd
import cdd.gmp as cg

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10960", ROOT / "analysis" / "w33_pass10960_matter_even_dflat_closure.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)
CERT = ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json"
OUT = ROOT / "data" / "w33_pass10964_e6_shaped_fi_mechanism.json"
TEN, FIVEB = ("q", "bu", "be"), ("bd", "l")


def fields(model):
    left = [dict(name=f["name"], base=P.base_of(f["name"]), dim=f["dim"], q=[F(x) for x in f["q"]]) for f in model["left"]]
    lab = [f for f in left if f["base"] in P.SMY]
    y = P.solve_affine([f["q"] for f in lab], [P.SMY[f["base"]] for f in lab])[0]
    sing = [f for f in left if all(abs(int(re.match(r"(-?\d+)", d).group(1))) == 1 and "adj" not in d
                                   for d in f["dim"].split(",")) and P.dot(y, f["q"]) == 0]
    return left, sing


def shaped_lp(left, sing, s, nu1):
    """exact LP: variables (lam_1..lam_{nu1-1}, mu); maximise mu (cdd)."""
    k = nu1 - 1
    rows, lin = [], []
    for f in left:
        if f["base"] in TEN + FIVEB:
            target = F(24, 5) if f["base"] in TEN else F(8, 5)
            rows.append([F(s * f["q"][0])] + list(f["q"][1:]) + [-target])
            lin.append(len(rows) - 1)
    for f in sing:
        rows.append([F(s * f["q"][0])] + list(f["q"][1:]) + [F(0)])
    rows.append([F(0)] * (k + 1) + [F(1)])       # mu >= 0
    rows.append([F(1)] + [F(0)] * k + [F(-1)])    # mu <= 1 (normalisation of the unbounded case)
    mat = cg.matrix_from_array(rows, lin_set=set(lin), rep_type=cdd.RepType.INEQUALITY)
    mat.obj_type = cdd.LPObjType.MAX
    mat.obj_func = tuple([F(0)] * (k + 1) + [F(1)])
    lp = cg.linprog_from_matrix(mat)
    cg.linprog_solve(lp)
    if lp.status != cdd.LPStatusType.OPTIMAL:
        return None
    sol = [F(v) for v in lp.primal_solution]
    return sol[:k], sol[k]


def main():
    ledger, sha = P.load_ledger()
    c60 = json.loads(CERT.read_text())["models"]
    res, census = {}, Counter()
    for name in sorted(c60):
        r = c60[name]
        if not r.get("bl_direction") or ("farkas_ever_even" not in r and "farkas_all" not in r):
            continue
        model = ledger[name]
        left, sing = fields(model)
        s = 1 if F(r["trace_anomalous"]) > 0 else -1
        dflat = "farkas_ever_even" in r
        never = {fld for t in r.get("never_even_types", []) for fld in t["fields"]} if dflat else set()
        use = [f for f in sing if f["name"] not in never]
        out = shaped_lp(left, use, s, model["nu1"])
        rec = dict(dflat_models_class=dflat, shaped=bool(out and out[1] > 0))
        if out and out[1] > 0:
            lam, mu = out
            fv = [F(s)] + lam
            fq = {f["name"]: P.dot(fv, f["q"]) for f in left}
            # exact verification of every constraint
            assert all(fq[f["name"]] == mu * (F(24, 5) if f["base"] in TEN else F(8, 5)) for f in left if f["base"] in TEN + FIVEB)
            assert all(fq[f["name"]] >= 0 for f in use)
            rec.update(mu=str(mu), lam=[str(v) for v in lam],
                       singlet_values_over_mu=sorted({str(fq[f["name"]] / mu) for f in sing}, key=lambda t: F(t)),
                       higgs_bl_values_over_mu=sorted({str(fq[f["name"]] / mu) for f in left if f["base"] == "bl"}, key=lambda t: F(t)))
            if dflat:
                neg = {f["name"]: fq[f["name"]] / mu for f in sing if fq[f["name"]] < 0}
                rec["negative_singlets_over_mu"] = sorted({str(v) for v in neg.values()})
                rec["negatives_subset_of_forced"] = set(neg) <= never and bool(neg)
        census[("D-flat (23)" if dflat else "no D-flat (64)", rec["shaped"])] += 1
        res[name] = rec
    summary = {f"{k[0]} shaped={k[1]}": v for k, v in sorted(census.items())}
    dflat_recs = [v for v in res.values() if v["dflat_models_class"]]
    summary["D-flat models whose f<0 singlets are all forced (B-L=+1) singlets"] = sum(1 for v in dflat_recs if v.get("negatives_subset_of_forced"))
    summary["D-flat models with f = -8 mu on the forced singlets"] = sum(1 for v in dflat_recs if v.get("negative_singlets_over_mu") == ["-8"])
    cert = dict(pass_id=10964, ledger_sha256=sha, summary=summary, models=res)
    OUT.write_text(json.dumps(cert, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
