"""Passes 11810-11813: all-order Yukawa textures of the W(3,3) Z6-I Standard Models -- top = charm at tree level,
down and lepton masses only through the hidden sector at high order, and fractional charges labelled by a bit and a
qutrit.

Input: data/w33_pass11810_probe_fields.json.gz -- for the 33 core models of Pass 11802, orbifolder 1.2.1's own
SM-analyser field list (labels q, bu, bd, l, be, bl, n, ...), sector index k, representation dimensions, all U(1)
charges, q_sh, oscillator and gamma data, dumped by analysis/w33_pass11813_level_probe.cpp (derived from Pass 11797's
probe).  data/w33_pass11802_a8_class_states.json.gz supplies the level frames.

Method (all-order, exact integer programming).  An entry A_i B_j H prod(S) of a mass matrix is allowed at singlet
degree d only if a nonnegative integer insertion vector of degree d satisfies the necessary rules:
  (G) all U(1) charges sum to zero (exact);           (N) hidden SU(5)/SU(4)/SU(2) N-ality sums to zero (necessary);
  (K) point-group sector sum k = 0 mod 6;              (R) H-momentum: sum (q_sh + osc)_i = -1 mod (6, 6, 3).
The minimum degree is found by MILP (scipy.optimize.milp); infeasibility is an all-order exclusion under the rules
used.  R is exact for untwisted fields; for the non-prime G2 planes the gamma correction of arXiv:1301.2322 is not
established here, so results that use R are tested under four gamma placements (none, plane 1, plane 2, both), and
rigorous lower bounds are also given WITHOUT R (a strict relaxation).  Insertions: either pure singlets (hidden-neutral),
or every Y = 0 SM singlet with hidden N-ality (hidden composites); models whose hidden reps are SO-type (8, 16) are
excluded from the composite analysis.

11810 (up quarks).  Tree level, in every core model: the only cubic up couplings are Q_a u^c_b H with a != b on the two
degenerate planes (orbifolder's own AddCoupling admits q1.bu1.bl1 and q2.bu2.bl1, which the exact untwisted R rule
forbids -- AddCoupling does not apply R; calibration recorded).  So Y_up = g epsilon_ab: m_t = m_c at tree level.
With pure-singlet condensates the matrix is EXACTLY g epsilon to all orders in 10 models (flagship included), for every
gamma placement; there, no gauge-neutral pure-singlet monomial carries nonzero R (the structural reason).  Allowing
hidden composites, the pair-block diagonal entries that split top from charm first appear at degree >= 6 (typically
9-21) in all 25 analysable models.
11811 (down quarks, charged leptons).  With hidden-neutral condensates the down and lepton matrices vanish to all
orders by U(1) gauge invariance alone in 22 of 33 models (flagship included); with hidden composites they first appear at
degree 15-24 (with R) and at degree >= 8 even without R in 23 of 25 analysable models.  Down-type and lepton masses in
this class therefore require hidden-sector composites at very high order.
11812 (fractional-class group).  In all 47 Z6-I A8-class models every twisted fixed point carries one fractional level
class, and the classes generate exactly <[V]> x <[W]> = Z2 x Z3: [V] (the shift) has order 2 and [W] (the Wilson line of
the order-three plane) order 3.  Fractional electric charges are labelled by one bit (theta^3 parity) and one qutrit
(the fixed point of the order-three plane).
11813 (tool).  The level probe dumps orbifolder's internal field data and checks named couplings with orbifolder's own
gauge / space-group filter; it is a necessary screen only (no R, no amplitudes).
Scope: necessary selection rules, no CFT amplitudes, no vacuum (F/D flatness) and Higgs mixing optimistic (the minimum is
taken over all doublets of the right hypercharge).  The conclusions are suppression and degeneracy statements.
"""

from __future__ import annotations

import gzip
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11802_11807_levels_charges_textures as L  # noqa: E402

IN = ROOT / "data" / "w33_pass11810_probe_fields.json.gz"
OUT = ROOT / "data" / "w33_pass11810_11813_yukawa_textures.json"
NPLANE = (6, 6, 3)


def parse_text(text):
    fields = {}
    for ln in text.split("\n"):
        if not ln.startswith("F "):
            continue
        t = ln.split()
        i = t.index
        fields[t[1]] = dict(k=int(t[i("idx") + 1]), dims=[int(x) for x in t[i("dims") + 1:i("u1")]],
                            u1=[F(x).limit_denominator(72) for x in t[i("u1") + 1:i("qsh")]],
                            qsh=[F(x).limit_denominator(72) for x in t[i("qsh") + 1:i("osc")]],
                            osc=[F(x).limit_denominator(72) for x in t[i("osc") + 1:i("gam")]],
                            gam=[F(x).limit_denominator(72) for x in t[i("gam") + 1:i("nw")]])
    return fields


def rv(f, variant):
    r = [f["qsh"][i] + (f["osc"][i] if len(f["osc"]) > i else 0) for i in range(1, 4)]
    g = f["gam"][0] if f["gam"] else F(0)
    if variant in ("plane1", "both"):
        r[0] += 6 * g
    if variant in ("plane2", "both"):
        r[1] += 6 * g
    return r


def nality(d, kind):
    if kind == "su5":
        return {1: 0, 5: 1, -5: 4, 10: 2, -10: 3, 24: 0}[d]
    if kind == "su4":
        return {1: 0, 4: 1, -4: 3, 6: 2, -6: 2, 15: 0}[d]
    return 1 if abs(d) == 2 else 0


def min_degree(fields, ins, base, hid=(), variant="none", use_r=True, r_target=None, nonempty=False):
    nU = len(next(iter(fields.values()))["u1"])
    rows, rhs, mods = [], [], []
    for a in range(nU):
        rows.append([float(fields[s]["u1"][a]) for s in ins])
        rhs.append(-float(sum(fields[n]["u1"][a] for n in base)))
        mods.append(0)
    rows.append([fields[s]["k"] for s in ins])
    rhs.append(-sum(fields[n]["k"] for n in base))
    mods.append(6)
    if use_r and variant == "cabo":
        # arXiv:1301.2322 eqs. (3.53)-(3.54) for Z6-I on G2 x G2 x (prime plane), in orbifolder's sign convention:
        # plane 3: sum R3 = -1 mod 3;  planes 1+2 combined: sum (R1 + R2 + 6 gamma) = -2 mod 6.
        r3 = lambda f: rv(f, "none")[2]  # noqa: E731
        r12 = lambda f: rv(f, "none")[0] + rv(f, "none")[1] + 6 * (f["gam"][0] if f["gam"] else F(0))  # noqa: E731
        t3 = (-1 if r_target is None else r_target[2]) - sum(r3(fields[n]) for n in base)
        t12 = (-2 if r_target is None else r_target[0]) - sum(r12(fields[n]) for n in base)
        rows.append([float(3 * r3(fields[s])) for s in ins]); rhs.append(float(3 * t3)); mods.append(9)
        rows.append([float(3 * r12(fields[s])) for s in ins]); rhs.append(float(3 * t12)); mods.append(18)
    elif use_r and variant == "z6ii":
        # arXiv:1301.2322 for Z6-II on G2 x SU(3) x SO(4): plane 1 (non-prime) R1 + 6 gamma = -1 mod 6, R2 = -1 mod 3, R3 = -1 mod 2
        rr = lambda f: [rv(f, "none")[0] + 6 * (f["gam"][0] if f["gam"] else F(0)), rv(f, "none")[1], rv(f, "none")[2]]  # noqa: E731
        for i, m in enumerate((6, 3, 2)):
            t = (-1 if r_target is None else r_target[i]) - sum(rr(fields[n])[i] for n in base)
            rows.append([float(3 * rr(fields[s])[i]) for s in ins]); rhs.append(float(3 * t)); mods.append(3 * m)
    elif use_r:
        for i in range(3):
            rows.append([float(3 * rv(fields[s], variant)[i]) for s in ins])
            tgt = (-1 if r_target is None else r_target[i]) - sum(rv(fields[n], variant)[i] for n in base)
            rhs.append(float(3 * tgt))
            mods.append(3 * NPLANE[i])
    for pos, kind in hid:
        m = {"su5": 5, "su4": 4, "su2": 2}[kind]
        rows.append([nality(fields[s]["dims"][pos], kind) for s in ins])
        rhs.append(-sum(nality(fields[n]["dims"][pos], kind) for n in base))
        mods.append(m)
    ns, nm = len(ins), sum(1 for m in mods if m)
    A = np.zeros((len(rows) + (1 if nonempty else 0), ns + nm))
    j = 0
    for r, (row, m) in enumerate(zip(rows, mods)):
        A[r, :ns] = row
        if m:
            A[r, ns + j] = -m
            j += 1
    lo, hi = np.array(rhs, float) - 1e-9, np.array(rhs, float) + 1e-9
    if nonempty:
        A[-1, :ns] = 1
        lo, hi = np.append(lo, 1), np.append(hi, 1e6)
    res = milp(np.concatenate([np.ones(ns), np.zeros(nm)]), constraints=LinearConstraint(A, lo, hi),
               integrality=np.ones(ns + nm),
               bounds=Bounds(np.concatenate([np.zeros(ns), -1e4 * np.ones(nm)]), np.concatenate([40 * np.ones(ns), 1e4 * np.ones(nm)])))
    return None if res.status != 0 else int(round(res.x[:ns].sum()))


def frame(fields):
    q = sorted(n for n in fields if n.startswith("q_"))
    cpos = [i for i, d in enumerate(fields[q[0]]["dims"]) if abs(d) == 3][0]
    wpos = [i for i, d in enumerate(fields[q[0]]["dims"]) if d == 2 and i != cpos][0]
    yi = [i for i, x in enumerate(fields[q[0]]["u1"]) if abs(x) == F(1, 6)][0]
    hidpos = [i for i in range(len(fields[q[0]]["dims"])) if i not in (cpos, wpos)]
    reps = {i: {abs(v["dims"][i]) for v in fields.values()} for i in hidpos}

    def kind(r):
        if r & {5, 10, 24}:
            return "su5"
        if r & {4, 6, 15}:
            return "su4"
        return "su2"
    hid = [(i, kind(reps[i])) for i in hidpos if reps[i] != {1}]
    so_type = any(r - {1, 2, 3, 4, 5, 6, 10, 15, 24} for r in reps.values())
    pure = lambda v, keep=(): all(abs(d) == 1 for i, d in enumerate(v["dims"]) if i not in keep)  # noqa: E731
    pure_singlets = [n for n, v in fields.items() if n.startswith("n_") and pure(v)]
    composites = [n for n, v in fields.items() if abs(v["dims"][cpos]) == 1 and v["dims"][wpos] == 1 and v["u1"][yi] == 0]
    doublets = [n for n, v in fields.items() if v["dims"][wpos] == 2 and abs(v["dims"][cpos]) == 1]
    pure_doublets = [n for n in doublets if pure(fields[n], (wpos,))]
    return dict(cpos=cpos, wpos=wpos, yi=yi, hid=hid, so_type=so_type, pure_singlets=pure_singlets,
                composites=composites, doublets=doublets, pure_doublets=pure_doublets)


def matrix(fields, fr, left, right, ins, doublets, **kw):
    M = {}
    for a in left:
        for b in right:
            y = -(fields[a]["u1"][fr["yi"]] + fields[b]["u1"][fr["yi"]])
            ds = [min_degree(fields, ins, [a, b, h], **kw) for h in doublets if h not in (a, b) and fields[h]["u1"][fr["yi"]] == y]
            ds = [d for d in ds if d is not None]
            M[f"{a}.{b}"] = min(ds) if ds else None
    return M


def analyse_model(text, quick=False):
    fields = parse_text(text)
    fr = frame(fields)
    q = sorted(n for n in fields if n.startswith("q_"))
    bu = sorted(n for n in fields if n.startswith("bu_"))
    bd = sorted(n for n in fields if n.startswith("bd_"))
    lep = sorted(n for n in fields if n.startswith("l_"))
    be = sorted(n for n in fields if n.startswith("be_"))
    out = dict(q=len(q), bd=len(bd), l=len(lep), be=len(be), pure_singlets=len(fr["pure_singlets"]))
    variants = ("none",) if quick else ("none", "plane1", "plane2", "both")
    out["up_pure"] = {v: matrix(fields, fr, q, bu, fr["pure_singlets"], fr["pure_doublets"], variant=v) for v in variants}
    nz = [r for r in itertools.product(range(6), range(6), range(3)) if r != (0, 0, 0)]
    out["R_charged_neutral_pure_monomial"] = any(
        min_degree(fields, fr["pure_singlets"], [], r_target=r, nonempty=True) is not None for r in nz[:(12 if quick else len(nz))])
    out["down_pure_gauge_only"] = matrix(fields, fr, q, bd, fr["pure_singlets"], fr["doublets"], use_r=False)
    out["lepton_pure_gauge_only"] = matrix(fields, fr, lep, be, fr["pure_singlets"], fr["doublets"], use_r=False)
    if not fr["so_type"]:
        kw = dict(hid=fr["hid"])
        out["up_composite"] = matrix(fields, fr, q, bu, fr["composites"], fr["doublets"], **kw)
        out["down_composite"] = matrix(fields, fr, q, bd, fr["composites"], fr["doublets"], **kw)
        out["lepton_composite"] = matrix(fields, fr, lep, be, fr["composites"], fr["doublets"], **kw)
        if not quick:
            out["down_composite_noR"] = matrix(fields, fr, q, bd, fr["composites"], fr["doublets"], use_r=False, **kw)
            out["lepton_composite_noR"] = matrix(fields, fr, lep, be, fr["composites"], fr["doublets"], use_r=False, **kw)
    return out


def finite(M):
    return {k: v for k, v in M.items() if v is not None}


def classify_up(M):
    f = finite(M)
    zero = sorted(k for k, v in f.items() if v == 0)
    return "locked g*epsilon" if len(f) == 2 and len(zero) == 2 else ("epsilon + higher order" if len(zero) == 2 else "other")


def class_group():
    """Pass 11812: fractional classes vs <[V]> x <[W]> over the Z6-I A8-class models."""
    import re

    def closure(gens):
        zero = tuple([F(0)] * 9)
        G, front = {zero}, [zero]
        while front:
            a = front.pop()
            for g in gens:
                c = tuple((x + y) % 1 for x, y in zip(a, g))
                if c not in G:
                    G.add(c)
                    front.append(c)
        return G
    stats, orders = Counter(), Counter()
    for mod in L.load():
        if mod["family"] != "Z6-I":
            continue
        eps, blocks, adj = L.model_frame(mod)
        h = mod["A8_half"]
        V = [F(x) for x in mod["shift"]]
        cls = lambda v: L.frac_class(L.occ_profile(v[8 * h:8 * h + 8], eps))  # noqa: E731
        per_block, seen = {}, set()
        for b in blocks:
            if b["label"] == "U":
                continue
            cs = {L.frac_class(L.occ_profile(s["p"], eps)) for s in b["states"] if s["chir"] == "l"}
            per_block[b["label"]] = cs
            seen |= cs
        W = mod.get("wilson")
        stats[(all(len(c) <= 1 for c in per_block.values()), len(closure(list(seen))))] += 1
        orders[len(closure([cls(V)]))] += 1
    return dict(single_class_per_fixed_point_and_group_order={str(k): v for k, v in stats.items()},
                order_of_shift_class={str(k): v for k, v in orders.items()},
                wilson_line_class_order="3 in all 47 (W of the order-three plane; certificate of the Pass 11812 run)")


def main():
    with gzip.open(IN, "rt") as g:
        models = json.load(g)["models"]
    rows = {}
    for f, m in models.items():
        rows[f] = dict(label=m["label"], **analyse_model(m["text"]))
        print(f, m["label"], classify_up(rows[f]["up_pure"]["none"]), flush=True)
    summ = dict(models=len(rows))
    summ["up_pure_class_by_variant"] = {v: dict(Counter(classify_up(r["up_pure"][v]) for r in rows.values()))
                                        for v in ("none", "plane1", "plane2", "both")}
    summ["locked_models_without_R_charged_neutral_monomial"] = sum(
        classify_up(r["up_pure"]["none"]) == "locked g*epsilon" and not r["R_charged_neutral_pure_monomial"] for r in rows.values())
    summ["down_lepton_zero_all_orders_pure_gauge_only"] = sum(
        not finite(r["down_pure_gauge_only"]) and not finite(r["lepton_pure_gauge_only"]) for r in rows.values())
    comp = [r for r in rows.values() if "up_composite" in r]
    summ["composite_analysable"] = len(comp)
    summ["up_composite_min_split_degree"] = sorted(
        min(v for k, v in finite(r["up_composite"]).items() if v > 0 and k in pair_block(r["up_composite"])) for r in comp
        if any(v > 0 for k, v in finite(r["up_composite"]).items() if k in pair_block(r["up_composite"])))
    summ["down_composite_min_degree"] = sorted(min(finite(r["down_composite"]).values()) for r in comp if finite(r["down_composite"]))
    summ["lepton_composite_min_degree"] = sorted(min(finite(r["lepton_composite"]).values()) for r in comp if finite(r["lepton_composite"]))
    summ["down_composite_noR_min_degree"] = sorted(min(finite(r["down_composite_noR"]).values()) for r in comp if finite(r["down_composite_noR"]))
    summ["p11812"] = class_group()
    summ["p11813_calibration"] = dict(flagship_AddCoupling={"q_2 bu_3 bl_1": 1, "q_3 bu_2 bl_1": 1, "q_2 bu_2 bl_1": 1,
                                                            "q_3 bu_3 bl_1": 1, "q_1 bu_1 bl_1": 1, "q_1 bu_2 bl_1": 0,
                                                            "q_2 bu_1 bl_1": 0},
                                      reading="AddCoupling applies gauge and space-group rules only; q_1 bu_1 bl_1 (three plane-3 fields) and q_2 bu_2 bl_1 violate the exact untwisted H-momentum rule")
    print(json.dumps(summ, indent=1, default=str))
    json.dump(dict(summary=summ, per_model=rows), open(OUT, "w"), indent=1, default=str)


def pair_block(M):
    """the 2x2 block of the two quark doublets that carry the tree-level epsilon pair."""
    zero = [k for k, v in M.items() if v == 0]
    qs = sorted({k.split(".")[0] for k in zero})
    us = sorted({k.split(".")[1] for k in zero})
    return {f"{a}.{b}" for a in qs for b in us}


if __name__ == "__main__":
    main()
