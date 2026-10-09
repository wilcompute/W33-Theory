"""Passes 11802-11807: the W(3,3) heterotic Standard Models in two-qutrit levels, II -- twisted families, charge
quantisation, an all-order exotic obstruction, the cubic up texture, the Z6-II scope, and an exact bracket certificate.

Input: data/w33_pass11802_a8_class_states.json.gz (orbifolder 1.2 'print all states' for every model whose theta^2
shift 2V has an A8 = SU(9) half: 47 Z6-I parents of Pass 11089 and 13 of the 128 Z6-II models in ~/orb/scan/cp2/out;
only the SU(9)-half momenta are kept).  Levels: the nine weights eps_i of that SU(9) (Pass 11714); the occupation
profile of a state with momentum p is occ_i = <p, eps_i> - mean.

11802 (twisted families).  The twisted SM matter with integral occupation is single-level: in the flagship the twisted
d^c and L have occupation profile exactly eps_i (one fermion in one colour level, resp. one weak level).  A family is
therefore a three-fermion 10 (two GUT levels + one flavour level, untwisted) plus a one-fermion 5bar (a GUT level,
twisted).  Census of profile types over the 28 Pass-11715 models is in the certificate.

11803 (THEOREM + census: charge quantisation is level integrality).  The hypercharge and T3 are diagonal on the levels,
so Q_em = sum_i q_i occ_i with level charges q = 1/3 (colour), 0 or -1 (weak), 0 (flavour).  Hence integral occupation
implies standard charges (colour singlets integral, triplets in Z +- 1/3).  In the 28 models every SM-charged weight with
a fractional (non-standard) electric charge has fractional occupation, and all of them are twisted; integral-occupation
weights are all standard.  (The converse fails: some fractional-occupation weights have standard charges.)

11804 (an all-order exotic obstruction).  Gauge invariance conserves the total SU(9)-half momentum, so the fractional
class f = occ mod Z (modulo uniform shifts) adds to zero in every coupling.  A mass term for an SM-charged state in class
f needs a conjugate partner in class -f unless some condensate has fractional class.  In all 28 models the SM-charged
fractional states are class-unbalanced, so if every condensate has integral occupation, some fractionally charged
exotics stay massless at every order: decoupling them requires condensates of fractional-occupation (SU(9)-breaking,
twisted) fields.

11805 (cubic up texture, Higgs, Weinberg angle).  All momentum-conserving untwisted Q.u^c.X couplings in the 28 models
are Q(planes 1,2) u^c(planes 1,2) H(plane 3) and Q(3) u^c(3) H(3); the latter is forbidden by the untwisted
one-field-per-plane rule.  So the tree-level up Yukawa is g epsilon_ab on the two degenerate planes: singular values
(g, g, 0) -- m_t = m_c at string tree level, the qutrit-plane family massless at cubic order.  The neutral component of
H = weak ^ c ^ d has Q_em = 0 (level charges), so its vev preserves the level-diagonal electromagnetism; and the level
traces give sin^2 theta_W = Tr T3^2 / Tr Q^2 = (1/2)/(4/3) = 3/8.  The Higgs here is untwisted matter, not an adjoint
background: the escape "different Higgs representation" from Codex Pass 11731's obstruction is the one these vacua use.

11806 (Z6-II and the benchmark).  13 of the 128 Z6-II models have an A8 half in 2V; in 7 the SM lies in that SU(9),
and there the untwisted sector carries only 1-2 net quark doublets, so the 2+1 level dictionary is Z6-I specific.  The
Codex benchmark Z6II_34__SM_20260917_1558 has theta^2 classes (D7+U1, D7+U1) at every fixed point (2V + n W3, n = 0,1,2):
it belongs to the W(3,3) anomaly class (Holotrade fbd2c5f: all Z6-II shifts are anomaly class 1) but not to the strict
A8/SU(9) class, so the two-qutrit level dictionary does not apply to it literally.  A scope note, not a correction of
its results.

11807 (exact certificate).  With Pass 11681's bracket, [e_A, e_B] for trivectors is nonzero exactly when A, B are
disjoint, equals sign(A,B,C) e*_C with C the complement, and has no other components: 1680 = 9!/(3!)^3 nonzero
couplings, all partitions, constant exactly 1.  The untwisted cubic coupling is the nine-level determinant.
"""

from __future__ import annotations

import gzip
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
import w33_pass11714_11716_heterotic_two_qutrit_levels as P  # noqa: E402

IN = ROOT / "data" / "w33_pass11802_a8_class_states.json.gz"
OUT = ROOT / "data" / "w33_pass11802_11807_levels_charges_textures.json"


def load():
    with gzip.open(IN, "rt") as f:
        return json.load(f)["models"]


def occ_profile(p, eps):
    prof = [P.dot(p, e) for e in eps]
    m = sum(prof) / 9
    return [x - m for x in prof]


def integral(occ):
    return all((x - occ[0]).denominator == 1 for x in occ)


def frac_class(occ):
    return tuple((x - occ[0]) % 1 for x in occ)


def neg(c):
    return tuple((-x) % 1 for x in c)


def conj(r):
    return r[1:] if r.startswith("-") else ("-" + r if r in ("3", "6") else r)


def model_frame(mod):
    V = tuple(Fr(x) for x in mod["shift"])
    h = mod["A8_half"]
    eps = P.su9_levels(tuple(2 * x for x in V[8 * h:8 * h + 8]))
    blocks = [dict(label=b["label"], plane=tuple(b["plane"]),
                   states=[dict(label=s[0], rep=s[1], chir=s[2], p=tuple(Fr(x) for x in s[3]), other=s[4]) for s in b["states"]])
              for b in mod["blocks"]]
    # colour/weak levels and rep positions from the gauge bosons that live in the SU(9) half
    adj = defaultdict(set)          # factor -> SU(9) levels (empty set: factor lives in the other E8 half)
    for b in blocks:
        for s in b["states"]:
            if s["chir"] == "v":
                pos = [i for i, x in enumerate(s["rep"]) if "adj" in x]
                if not pos:
                    continue
                key = (pos[0], s["rep"][pos[0]])
                adj.setdefault(key, set())
                ls = P.level_set(s["p"], eps) if any(s["p"]) and not s["other"] else None
                if ls and ls[0] == "adj":
                    adj[key].update(ls[1:])
    return eps, blocks, adj


def sm_choice(blocks, adj):
    best = None
    for c3 in [k for k in adj if k[1] == "8_adj"]:
        for c2 in [k for k in adj if k[1] == "3_adj"]:
            tot = unt = 0
            for b in blocks:
                for s in b["states"]:
                    if s["chir"] == "l" and s["rep"][c3[0]] in ("3", "-3") and s["rep"][c2[0]] == "2":
                        sg = 1 if s["rep"][c3[0]] == "3" else -1
                        tot += sg
                        unt += sg if b["label"] == "U" else 0
            cand = (c3, c2, tot // 6, unt // 6)
            score = (abs(tot // 6) == 3, bool(adj[c3]) and bool(adj[c2]), abs(unt // 6) == 3)
            if best is None or score > best[0]:
                best = (score, cand)
    return best[1] if best else None


def analyse(mod):
    eps, blocks, adj = model_frame(mod)
    ch = sm_choice(blocks, adj)
    res = dict(family=mod["family"], label=mod["label"], file=mod["file"])
    if ch is None:
        res["sm_in_su9"] = False
        return res
    c3, c2, net, netU = ch
    col, weak = sorted(adj[c3]), sorted(adj[c2])
    res.update(sm_in_su9=len(col) == 3 and len(weak) == 2, net_32=net, net_32_untwisted=netU if net >= 0 else -netU,
               colour_levels=col, weak_levels=weak)
    if not res["sm_in_su9"]:
        return res
    flav = [i for i in range(9) if i not in col and i not in weak]
    q = [Fr(1, 3) if i in col else Fr(0) for i in range(9)]
    q[weak[1]] = Fr(-1)                      # Q = T3 + Y on the two weak levels: 0 and -1
    y = [Fr(1, 3) if i in col else Fr(-1, 2) if i in weak else Fr(0) for i in range(9)]
    charge, profiles, frac = Counter(), Counter(), Counter()
    for b in blocks:
        for s in b["states"]:
            if s["chir"] != "l" or s["other"] and not any(s["p"]):
                continue
            r3, r2 = s["rep"][c3[0]], s["rep"][c2[0]]
            occ = occ_profile(s["p"], eps)
            Y = sum(a * o for a, o in zip(y, occ))
            if r3 == "1" and r2 == "1" and Y == 0:
                continue
            Q = sum(a * o for a, o in zip(q, occ))
            if (3 * Q).denominator != 1:
                std = False
            elif r3 in ("1", "8_adj"):
                std = Q.denominator == 1
            else:
                std = int(3 * Q) % 3 != 0
            charge[(integral(occ), std, b["label"] == "U")] += 1
            if integral(occ) and b["label"] != "U":
                nz = sorted(set(occ))
                shape = "single level (9/9bar)" if len(nz) == 2 and (occ.count(max(occ)) == 1 or occ.count(min(occ)) == 1) else f"other {len(nz)}-valued"
                profiles[(r3, r2, shape)] += 1
            if not integral(occ) and (r3 != "1" or r2 != "1"):
                frac[(r3, r2, frac_class(occ))] += 1
    idx = {k: v - frac.get((conj(k[0]), k[1], neg(k[2])), 0) for k, v in frac.items()}
    res["charge_census"] = {str(k): v for k, v in charge.items()}
    res["twisted_integral_profiles"] = {str(k): v for k, v in profiles.items()}
    res["sm_fractional_weights"] = sum(frac.values())
    res["class_unbalanced_weights"] = sum(abs(v) for v in idx.values()) // 2
    # untwisted level table and cubic up couplings
    st = defaultdict(list)
    for b in blocks:
        if b["label"] != "U":
            continue
        for s in b["states"]:
            if s["chir"] != "l" or s["other"]:
                continue
            ls = P.level_set(s["p"], eps)
            if ls and ls[0] in (1, -1):
                kind = "".join(sorted("C" if i in col else "W" if i in weak else "o" for i in ls[1]))
                st[kind].append((b["plane"], s["p"], frozenset(ls[1])))
    cub = Counter()
    for pq, qq, Lq in st["CWo"]:
        for pu, uu, Lu in st["CCo"]:
            for kind, lst in st.items():
                for ph, hh, Lh in lst:
                    if all(a + b2 + c == 0 for a, b2, c in zip(qq, uu, hh)):
                        cub[f"Q{pq} u{pu} {kind}{ph}"] += 1
    res["up_cubics"] = dict(cub)
    res["up_cubics_allowed_by_plane_rule"] = {k: v for k, v in cub.items()
                                              if not (k.startswith("Q(3,)") and "u(3,)" in k)}
    hneutral = [occ_profile(hh, eps) for ph, hh, Lh in st.get("Woo", [])]
    res["higgs_component_charges"] = sorted({str(sum(a * o for a, o in zip(q, occ))) for occ in hneutral})
    return res


def bracket_certificate():
    Z9, Z84 = np.zeros((9, 9), complex), np.zeros(84, complex)
    nz = bad = 0
    ratios = set()
    for a in range(84):
        xa = Z84.copy()
        xa[a] = 1
        for b in range(84):
            xb = Z84.copy()
            xb[b] = 1
            A, x, k = E.bracket((Z9, xa, Z84), (Z9, xb, Z84))
            assert np.abs(A).max() < 1e-12 and np.abs(x).max() < 1e-12
            hits = np.nonzero(np.abs(k) > 1e-12)[0]
            if not set(E.TR[a]) & set(E.TR[b]):
                assert len(hits) == 1
            for c in hits:
                T = E.TR[a] + E.TR[b] + E.TR[c]
                if sorted(T) != list(range(9)):
                    bad += 1
                    continue
                nz += 1
                ratios.add(round(float((k[c] / E.psign(T)).real), 12))
    return dict(nonzero=nz, expected=1680, non_partition=bad, coupling_over_sign=sorted(ratios))


def weinberg_level_trace():
    q = [Fr(1, 3)] * 3 + [Fr(0), Fr(-1)] + [Fr(0)] * 4
    t3 = [Fr(0)] * 3 + [Fr(1, 2), Fr(-1, 2)] + [Fr(0)] * 4
    return str(sum(x * x for x in t3) / sum(x * x for x in q))


def main():
    models = load()
    rows = [analyse(m) for m in models]
    z6i = [r for r in rows if r["family"] == "Z6-I" and r.get("sm_in_su9")]
    core = [r for r in z6i if abs(r["net_32"]) == 3 and r["net_32_untwisted"] == 3]
    z6ii = [r for r in rows if r["family"] == "Z6-II"]
    agg = Counter()
    for r in core:
        for k, v in r["charge_census"].items():
            agg[k] += v
    tw = Counter()
    for r in core:
        for k, v in r["twisted_integral_profiles"].items():
            tw[k] += v
    up = Counter(json.dumps(sorted(r["up_cubics_allowed_by_plane_rule"])) for r in core)
    res = dict(pass_ids=list(range(11802, 11808)), core_models=len(core),
               p11802_twisted_integral_profiles=dict(tw),
               p11803_charge_census_integral_standard_untwisted=dict(agg),
               p11803_every_fractional_charge_has_fractional_occupation=all(
                   not (eval(k)[0] and not eval(k)[1]) for r in core for k in r["charge_census"]),
               p11804_models_class_unbalanced=sum(r["class_unbalanced_weights"] > 0 for r in core),
               p11805_up_cubic_patterns=dict(up),
               p11805_higgs_component_charges=sorted({c for r in core for c in r["higgs_component_charges"]}),
               p11805_sin2_theta_w=weinberg_level_trace(),
               p11806_z6ii=dict(a8_models=len(z6ii), sm_in_su9=sum(bool(r.get("sm_in_su9")) for r in z6ii),
                                untwisted_net_doublets=dict(Counter(r.get("net_32_untwisted") for r in z6ii if r.get("sm_in_su9")))),
               p11806_benchmark=benchmark_classes(),
               p11807_bracket=bracket_certificate(),
               per_model=rows)
    print(json.dumps({k: v for k, v in res.items() if k != "per_model"}, indent=1, default=str))
    json.dump(res, open(OUT, "w"), indent=1, default=str)


def benchmark_classes():
    V = [Fr(x) for x in "0 0 0 0 1/6 1/6 1/3 2/3 0 0 0 0 0 0 0 1/3".split()]
    W3 = [Fr(x) for x in "0 1/3 1 1 -1 -1/3 1 -2/3 -1 -1 0 0 1/3 1/3 1/3 1".split()]
    R = P.e8_roots()
    out = {}
    for n in range(3):
        for k in (2, 4):
            s = [k * v + n * w for v, w in zip(V, W3)]
            out[f"{k}V+{n}W3"] = [sum(1 for r in R if P.dot(r, s[8 * h:8 * h + 8]).denominator == 1) for h in (0, 1)]
    out["reading"] = "84 integral roots per half = D7+U1; the A8 (SU(9)) class would have 72"
    return out


if __name__ == "__main__":
    main()
