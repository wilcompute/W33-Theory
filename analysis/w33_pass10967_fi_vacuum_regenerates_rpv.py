#!/usr/bin/env python3
"""Pass 10967: the FI vacuum regenerates R-parity violation, and no matter parity of any kind survives.

Builds on Pass 10960 (matter-even D-flat closure over the B-L family and Z2 lattice characters),
Pass 10962 (hidden sector), Pass 10964 (the forced field is the nu^c of 16_{-3} in 78 of E6) and
Pass 10965 (no baryon triality).  Three exact statements over the 215 W(3,3) Z6 Standard Models:

A. The most general matter parity.  Pass 10960 scanned the B-L family and Z2 characters of the
   U(1) charge lattice that are +-1 on EVERY field.  A matter parity only has to be -1 on
   q, u^c, d^c, e^c and +1 on the condensing singlets; other fields may carry any phase.  So the
   general object is ANY element of (gauge U(1) torus) x (space-group non-R discrete group:
   Z6 point-group rule, Z3 and, in Z6-II, Z2 x Z2 fixed-point rules; charges frozen from the
   orbifolder).  Realizability of {v.x in Z on the even set, in 1/2+Z on the odd set} is decided
   exactly by a Smith normal form (rows of the left transform beyond the rank span the saturated
   integer left kernel).  Result: such an element exists in exactly the 88 B-L models; in 87 the
   singlets that can be even are never D-flat with the FI term (one exact Farkas vector each), in
   Z6II_23 every FI-cancelling extreme ray (304 of 3334) is obstructed.  0/215.  In all 87 Z6-I
   models the even-able singlet types are exactly those of the B-L family: generality adds nothing.

B. Why the forced field is odd under EVERY matter parity.  290 of the 302 forced (never-even)
   singlets satisfy, with single copies of the fields, the exact U(1) identities
        Q(n) = -Q(u^c d^c d^c) = -Q(q l d^c) = -Q(l l e^c),
   the SO(10) invariant 16^4 restricted to nu^c.  Every matter parity is -1 on each cubic, so it
   is -1 on n.  The other 12 obey one or two of the identities (or their conjugates).

C. The string selection rules regenerate all three RPV operators.  With the orbifolder's full
   coupling rules (gauge, space group, R-charges): in the 23 D-flat Z6-I models with B-L none of
   u^c d^c d^c, q l d^c, l l e^c is allowed at order 3, yet each of the 9 forced singlets of every
   model appears in allowed quartic couplings n.u^c d^c d^c, n.q l d^c and n.l l e^c.  The FI
   term forces <n> != 0 (Pass 10960/10964), so all three are regenerated with strength <n>/M_s.
   Z6II_23 has q l d^c and l l e^c at order 3 and u^c d^c d^c at order 5 (two singlets).

Scope: couplings are listed at the level of orbifolder labels (bd includes vector-like exotic
d-type triplets; the light d^c are mixtures after decoupling).  Coupling coefficients are not
computed: 'allowed' means allowed by every selection rule the orbifolder implements.
"""
from __future__ import annotations

import gzip
import importlib.util
import itertools
import json
import re
from collections import Counter
from fractions import Fraction
from math import lcm
from pathlib import Path

import sympy as sp
from sympy.matrices.normalforms import smith_normal_decomp

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p10960", ROOT / "analysis" / "w33_pass10960_matter_even_dflat_closure.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)
DISC = ROOT / "data" / "w33_pass10967_space_group_discrete_charges.json.gz"
RPV = ROOT / "data" / "w33_pass10967_rpv_coupling_dump.json.gz"
OUT = ROOT / "data" / "w33_pass10967_fi_vacuum_regenerates_rpv.json"
SHAPES = {"udd": ("bu", "bd", "bd"), "qld": ("q", "l", "bd"), "lle": ("l", "l", "be")}


def load(path):
    with gzip.open(path, "rt") as fh:
        return json.load(fh)


def kernel_mod2(vecs):
    L = lcm(*[v.denominator for vec in vecs for v in vec]) if vecs else 1
    A = sp.Matrix([[int(v * L) for v in vec] for vec in vecs])
    S, U, _ = smith_normal_decomp(A, domain=sp.ZZ)
    r = sum(1 for i in range(min(S.shape)) if S[i, i] != 0)
    return [[int(U[i, j]) % 2 for j in range(A.rows)] for i in range(r, A.rows)]


def realizable(vecs, odd):
    """exists real x with v.x in Z (v not odd) and v.x in 1/2 + Z (v odd)?"""
    return all(sum(k[i] for i in odd) % 2 == 0 for k in kernel_mod2(vecs))


def fields(model, disc):
    orders = disc["nonR_orders"]
    out = []
    for f in model["left"]:
        dims = f["dim"].split(",")
        ch = disc["fields"][f["name"]]["nonR"]
        out.append(dict(name=f["name"], base=P.base_of(f["name"]), k=int(f["k"]),
                        trivial=all(abs(int(re.match(r"(-?\d+)", d).group(1))) == 1 and "adj" not in d for d in dims),
                        dimprod=abs(eval("*".join(re.match(r"(-?\d+)", d).group(1) for d in dims))),
                        q=[Fraction(x) for x in f["q"]],
                        ext=[Fraction(c) / o for c, o in zip(ch, orders)]))
    return orders, out


def general_parity(name, model, disc):
    orders, left = fields(model, disc)
    # the point-group charge is the sector k (up to orientation)
    assert all(Fraction(disc["fields"][f["name"]]["nonR"][0]) % orders[0] in (f["k"] % orders[0], (-f["k"]) % orders[0])
               for f in left)
    nq, nd = len(left[0]["q"]), len(orders)
    vec = lambda f: f["q"] + f["ext"]
    virtual = [[Fraction(0)] * nq + [Fraction(int(i == j)) for j in range(nd)] for i in range(nd)]
    tr0 = sum((f["dimprod"] * f["q"][0] for f in left), Fraction(0))
    lab = [f for f in left if f["base"] in P.SMY]
    y = P.solve_affine([f["q"] for f in lab], [P.SMY[f["base"]] for f in lab])[0]
    sing = [f for f in left if f["trivial"] and P.dot(y, f["q"]) == 0]
    mv = [list(k) for k in dict.fromkeys(tuple(vec(f)) for f in left if f["base"] in P.MATTER)]
    base_vecs, odd = mv + virtual, list(range(len(mv)))
    rec = dict(discrete_orders=orders, matter_types=len(mv), parity_exists=realizable(base_vecs, odd),
               anomaly_free=tr0 == 0)
    if not rec["parity_exists"] or tr0 == 0:
        return rec
    sv = list(dict.fromkeys(tuple(vec(f)) for f in sing))
    ever = [k for k in sv if realizable(base_vecs + [list(k)], odd)]
    utypes = sorted({k[:nq] for k in ever})
    s = 1 if tr0 > 0 else -1
    rec.update(singlet_types=len(sv), ever_even_types=len(ever), ever_even_u1_types=len(utypes))
    lam = P.farkas([s * t[0] for t in utypes], [list(t[1:]) for t in utypes]) if utypes else []
    if lam is not None:
        rec["verdict"] = "closed: Farkas on the even-able singlets"
        rec["farkas"] = [str(v) for v in lam]
        return rec
    rays = P.cone_rays([list(t[1:]) for t in utypes])
    neg = [r for r in rays if sum((s * utypes[i][0] * r[i] for i in range(len(utypes))), Fraction(0)) < 0]
    hits = 0
    for r in neg:
        sup = [utypes[i] for i in range(len(utypes)) if r[i] != 0]
        choices = [[list(k) for k in ever if k[:nq] == u] for u in sup]
        hits += any(realizable(base_vecs + list(ch), odd) for ch in itertools.product(*choices))
    rec.update(extreme_rays=len(rays), fi_cancelling_rays=len(neg), realizable_rays=hits,
               verdict="COUNTEREXAMPLE" if hits else "closed: every FI-cancelling ray obstructed")
    return rec


def forced_singlets(model):
    left = [dict(name=f["name"], base=P.base_of(f["name"]), dim=f["dim"], q=tuple(Fraction(x) for x in f["q"]))
            for f in model["left"]]
    lab = [f for f in left if f["base"] in P.SMY]
    y = P.solve_affine([list(f["q"]) for f in lab], [P.SMY[f["base"]] for f in lab])[0]
    sol = P.solve_affine([list(f["q"]) for f in left if f["base"] in P.BL], [P.BL[f["base"]] for f in left if f["base"] in P.BL])
    if sol is None:
        return None, left
    x0, N = sol
    sing = [f for f in left if all(abs(int(re.match(r"(-?\d+)", d).group(1))) == 1 and "adj" not in d
                                   for d in f["dim"].split(",")) and P.dot(y, list(f["q"])) == 0]
    never = [f for f in sing if not any(P.dot(n, list(f["q"])) for n in N) and (3 * P.dot(x0, list(f["q"]))) % 2 != 0]
    return never, left


def cubic_relations(s, left):
    bysp = {}
    for f in left:
        bysp.setdefault(f["base"], set()).add(f["q"])
    tags = []
    for sh, (a, b, c) in SHAPES.items():
        hit = None
        for qa, qb, qc in itertools.product(bysp.get(a, ()), bysp.get(b, ()), bysp.get(c, ())):
            tot = tuple(x + y + z for x, y, z in zip(qa, qb, qc))
            if all(t == -u for t, u in zip(tot, s["q"])):
                hit = "n*op"
                break
            if hit is None and tot == s["q"]:
                hit = "nbar*op"
        if hit:
            tags.append(f"{sh}:{hit}")
    return " ".join(tags) or "none"


def main():
    ledger, sha = P.load_ledger()
    disc, dump = load(DISC), load(RPV)
    A, Asum = {}, Counter()
    for name in sorted(ledger):
        base = name.split("|")[1]
        rec = general_parity(name, ledger[name], disc[base])
        A[name] = rec
        Asum["models"] += 1
        Asum["parity_exists"] += rec["parity_exists"]
        v = rec.get("verdict", "")
        Asum["closed_farkas"] += v.startswith("closed: Farkas")
        Asum["closed_rays"] += v.startswith("closed: every")
        Asum["counterexamples"] += v == "COUNTEREXAMPLE"
    B, Bsum = {}, Counter()
    for name in sorted(ledger):
        never, left = forced_singlets(ledger[name])
        if never is None:
            continue
        Bsum["bl_models"] += 1
        tags = {s["name"]: cubic_relations(s, left) for s in never}
        B[name] = tags
        for t in tags.values():
            Bsum[t] += 1
            Bsum["forced_singlets"] += 1
    C, Csum = {}, Counter()
    base10960 = json.loads((ROOT / "data" / "w33_pass10960_matter_even_dflat_closure.json").read_text())["models"]
    for name, r in sorted(base10960.items()):
        if not (r.get("dflat_any") and r.get("bl_direction")):
            continue
        b = name.split("|")[1]
        forced = {f for t in r["never_even_types"] for f in t["fields"]}
        row = {"forced_singlets": len(forced)}
        for op in SHAPES:
            lines = dump[b][op]
            row[f"{op}_order3"] = sum(1 for l in lines if not any(x.startswith("n_") for x in l))
            row[f"{op}_forced_in_quartic"] = len({x for l in lines for x in l if x.startswith("n_")} & forced)
        if "udd_to_order6" in dump[b]:
            row["udd_by_order"] = dict(sorted(Counter(str(len(l)) for l in dump[b]["udd_to_order6"]).items()))
        C[name] = row
        cls = name.split("|")[0]
        Csum[f"{cls}_dflat_models"] += 1
        full = all(row[f"{op}_forced_in_quartic"] == row["forced_singlets"] and row[f"{op}_order3"] == 0 for op in SHAPES)
        Csum[f"{cls}_no_cubic_rpv_all_forced_regenerate_all_three"] += full
    summary = dict(A=dict(Asum), B=dict(Bsum), C=dict(Csum))
    OUT.write_text(json.dumps(dict(pass_id=10967, ledger_sha256=sha, summary=summary,
                                   general_parity=A, forced_cubic_relations=B, string_couplings=C),
                              indent=1, sort_keys=True))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
