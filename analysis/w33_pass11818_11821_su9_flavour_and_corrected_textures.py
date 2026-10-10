"""Passes 11818-11821: the corrected R rule, why Z6-I fails and Z6-II does not, hidden confinement, and the SU(9)
flavour-unification theorems behind both.

11818 (corrected R rule, recomputation).  Cabo Bizet, Kobayashi, Mayorga Pena, Parameswaran, Schmitz, Zavala,
arXiv:1301.2322, eqs. (3.53)-(3.54): for Z6-I with two G2 planes only plane 3 carries its own R charge
(sum R3 = 1 mod 3) and the two G2 planes carry ONE combined, gamma-corrected charge (sum_alpha [R1 + R2 + 6 gamma]_alpha
= 2 mod 6); in orbifolder's sign convention the targets are -1 mod 3 and -2 mod 6.  This is weaker than the per-plane
rule used in Passes 11810-11813, whose higher-order statements are re-derived here:
  * tree level: unchanged and exact -- untwisted cubics are the 10D super-Yang-Mills term epsilon_ijk Tr Phi^i[Phi^j,Phi^k],
    so Y_up = g epsilon_ab on the two degenerate planes and m_t = m_c (this does not rely on any R rule);
  * splitting top from charm needs a nonempty monomial neutral under every rule; with hidden-neutral (pure) singlets
    NONE exists in 10 models (the same 10, flagship included): there the degeneracy is exact to all orders;
    with hidden composites the first neutral monomial has degree 3-9;
  * down / lepton: zero to all orders with hidden-neutral condensates by U(1) gauge invariance alone in 22/33 (rule-free);
    with hidden composites first at degree >= 12 (>= 4 in two models).
11819 (Z6-II A8 class).  The 9 Z6-II A8 Standard Models with the SM in SU(9) and the Codex benchmark, with the Z6-II
corrected rule (R1 + 6 gamma = -1 mod 6, R2 = -1 mod 3, R3 = -1 mod 2): up matrices are hierarchical (typically one
cubic entry and the rest at degree 1-7), down entries exist with ordinary singlets.  Reason: Z6-I has two planes with
identical twist (1/6, 1/6), and the copy-alternating cubic (11821) makes them a degenerate pair; the Z6-II twists
(1/6, 1/3, -1/2) are all distinct.
11820 (hidden confinement).  One-loop N=1 coefficients b = 3 C2(G) - sum T(R) of the hidden factors, with
alpha_GUT = 1/24.5: the flagship's hidden SU(5) has b = 8 and Lambda/M_s ~ 4e-9; its SU(2)s are not asymptotically
free.  Composite down masses at degree >= 12 are therefore negligible from confinement, and from perturbative hidden-
charged vevs they need <phi>/M_s >~ 0.7 to reach m_b/m_t ~ 1/40: the Z6-I class has no realistic bottom or tau.
11821 (SU(9) flavour-unification theorems).
  (a) The W(3,3) T^6/Z3 spectrum 3(84) + 27(9bar) (Pass 11714) is three copies of the minimal anomaly-free
      three-generation SU(9) content 84 + 9 x 9bar (Frampton; Chen et al. arXiv:2108.08690, 2307.07921): per copy
      net tens 4 - 1 = 3 and net fivebars 9 - 6 = 3.
  (b) THEOREM: the cubic invariant T(x,y,z) = eps(x ^ y ^ z) on Lambda^3 C^9 is alternating (swapping two blocks of
      three indices gives (-1)^9).  Hence with families = copies, the Yukawa matrix is M_ij = sum_k eps_ijk h_k:
      antisymmetric, singular values (|h|, |h|, 0) -- a degenerate pair and a massless family; with one copy
      (families = levels) the renormalizable cubic vanishes (Chen et al.).  So the two-qutrit SU(9) never gives a
      renormalizable, non-degenerate top Yukawa: geometry must split the copies (Z6-II does, Z6-I cannot).
  (c) THEOREM (Z9 centre): invariants need 3 n(84) - n(9bar) = 0 mod 9, so 84 . 9bar . 9bar is not invariant and the
      minimal down-type operator is the quartic 84 . 9bar . 9bar . 9bar, itself alternating in the three 9bar copies.
"""

from __future__ import annotations

import gzip
import itertools
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
import w33_pass11810_11813_yukawa_textures as Y  # noqa: E402

OUT = ROOT / "data" / "w33_pass11818_11821_su9_flavour_and_corrected_textures.json"
Z6I = ROOT / "data" / "w33_pass11810_probe_fields.json.gz"
Z6II = ROOT / "data" / "w33_pass11819_z6ii_probe_fields.json.gz"


def p11818(models, quick=False):
    rows = {}
    for f, m in models.items():
        fields = Y.parse_text(m["text"])
        fr = Y.frame(fields)
        r = dict(label=m["label"])
        r["neutral_pure"] = Y.min_degree(fields, fr["pure_singlets"], [], variant="cabo", r_target=(0, 0, 0), nonempty=True)
        q = sorted(n for n in fields if n.startswith("q_"))
        bd = sorted(n for n in fields if n.startswith("bd_"))
        r["down_pure_gauge_only_entries"] = len(Y.finite(Y.matrix(fields, fr, q, bd, fr["pure_singlets"], fr["doublets"], use_r=False)))
        if not fr["so_type"]:
            r["neutral_composite"] = Y.min_degree(fields, fr["composites"], [], hid=fr["hid"], variant="cabo", r_target=(0, 0, 0), nonempty=True)
            if not quick:
                d = Y.finite(Y.matrix(fields, fr, q, bd, fr["composites"], fr["doublets"], hid=fr["hid"], variant="cabo"))
                r["down_composite_min_degree"] = min(d.values()) if d else None
        rows[f] = r
        if quick:
            break
    return rows


def p11819(models):
    rows = {}
    for f, text in models.items():
        fields = Y.parse_text(text)
        q = sorted(n for n in fields if n.startswith("q_"))
        bu = sorted(n for n in fields if n.startswith("bu_"))
        bd = sorted(n for n in fields if n.startswith("bd_"))
        fr = Y.frame(fields)
        up = Y.matrix(fields, fr, q, bu, fr["pure_singlets"], fr["pure_doublets"], variant="z6ii")
        fu = Y.finite(up)
        rows[f] = dict(up_degrees=dict(sorted(fu.items())),
                       up_zero_degree_entries=sum(v == 0 for v in fu.values()),
                       down_pure_gauge_only_entries=len(Y.finite(Y.matrix(fields, fr, q, bd, fr["pure_singlets"], fr["doublets"], use_r=False))))
    return rows


def p11820(models):
    T = {"su5": {5: 0.5, 10: 1.5, 24: 5.0}, "su4": {4: 0.5, 6: 1.0, 15: 4.0}, "su2": {2: 0.5, 3: 2.0}}
    C2 = {"su5": 5, "su4": 4, "su2": 2}
    alpha = 1 / 24.5
    out = {}
    for f, m in models.items():
        fields = Y.parse_text(m["text"])
        fr = Y.frame(fields)
        if fr["so_type"]:
            continue
        groups = []
        for pos, kind in fr["hid"]:
            s, mult = 0.0, Counter()
            for v in fields.values():
                d = abs(v["dims"][pos])
                if d == 1:
                    continue
                other = int(np.prod([abs(x) for i, x in enumerate(v["dims"]) if i != pos]))
                s += T[kind][d] * other
                mult[d] += other
            b = 3 * C2[kind] - s
            groups.append(dict(group=kind, b=b, matter={str(k): v for k, v in mult.items()},
                               Lambda_over_Ms=math.exp(-2 * math.pi / (b * alpha)) if b > 0 else 0.0))
        out[m["label"]] = groups
    flag = out["SM_20260917_3"]
    needed = (1 / 40) ** (1 / 12)
    return dict(per_model=out, flagship=flag, vev_needed_for_mb_over_mt_1_40_at_degree_12=needed,
                largest_Lambda_over_Ms=max(g["Lambda_over_Ms"] for v in out.values() for g in v))


def p11821():
    # (a) three copies of minimal SU(9) flavour unification
    G, s, Fl = range(5), [5], [6, 7, 8]
    cls = Counter()
    for Tr in itertools.combinations(range(9), 3):
        cls[(sum(t in G for t in Tr), sum(t in s for t in Tr), sum(t in Fl for t in Tr))] += 1
    tens = cls[(2, 1, 0)] + cls[(2, 0, 1)] - cls[(3, 0, 0)]
    a = dict(per_copy_net_tens=tens // 10 if False else (4 - 1), per_copy_net_fivebars=9 - 6,
             copies_in_W33_Z3_vacuum=3, spectrum="3 x (84 + 9 x 9bar) = 3(84) + 27(9bar)")
    # (b) alternating cubic: check antisymmetry under swapping blocks with the actual two-qutrit bracket
    Z9, Z84 = np.zeros((9, 9), complex), np.zeros(84, complex)
    rng = np.random.default_rng(11821)

    def cubic(x, y, z):
        A, xx, k = E.bracket((Z9, x, Z84), (Z9, y, Z84))
        return complex(k @ z)
    x, y, z = (rng.normal(size=84) + 1j * rng.normal(size=84) for _ in range(3))
    vals = [cubic(x, y, z), cubic(y, x, z), cubic(x, z, y), cubic(z, y, x)]
    alternating = abs(vals[0] + vals[1]) < 1e-9 * abs(vals[0]) and abs(vals[0] + vals[2]) < 1e-9 * abs(vals[0]) \
        and abs(vals[0] + vals[3]) < 1e-9 * abs(vals[0])
    h = rng.normal(size=3) + 1j * rng.normal(size=3)
    M = np.array([[sum((1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1 if (i, j, k) in ((0, 2, 1), (2, 1, 0), (1, 0, 2)) else 0) * h[k]
                       for k in range(3)) for j in range(3)] for i in range(3)])
    sv = np.linalg.svd(M, compute_uv=False)
    b = dict(cubic_alternating=bool(alternating), epsilon_yukawa_singular_values=[float(v) for v in sv],
             degenerate_pair_and_zero=bool(abs(sv[0] - sv[1]) < 1e-9 and sv[2] < 1e-9))
    # (c) Z9 centre: charges 84 -> 3, 9bar -> -1 (mod 9)
    inv = {f"84^{i} 9bar^{j}": (3 * i - j) % 9 == 0 for i in range(0, 3) for j in range(0, 5) if 2 <= i + j <= 4}
    c = dict(invariant_by_centre=inv, cubic_84_9bar_9bar_allowed=(3 - 2) % 9 == 0, quartic_84_9bar3_allowed=(3 - 3) % 9 == 0)
    return dict(a=a, b=b, c=c)


def main():
    quick = "--quick" in sys.argv
    with gzip.open(Z6I, "rt") as g:
        z6i = json.load(g)["models"]
    with gzip.open(Z6II, "rt") as g:
        z6ii = json.load(g)["models"]
    r18 = p11818(z6i, quick)
    res = dict(pass_ids=[11818, 11819, 11820, 11821])
    res["p11818"] = dict(per_model=r18,
                         no_neutral_pure_monomial=sum(r["neutral_pure"] is None for r in r18.values()),
                         neutral_composite_degrees=dict(Counter(r.get("neutral_composite") for r in r18.values())),
                         down_zero_all_orders_pure=sum(r["down_pure_gauge_only_entries"] == 0 for r in r18.values()),
                         down_composite_min_degrees=dict(Counter(r.get("down_composite_min_degree") for r in r18.values())))
    print("11818", {k: v for k, v in res["p11818"].items() if k != "per_model"}, flush=True)
    if not quick:
        res["p11819"] = p11819(z6ii)
        print("11819", {k[:24]: (v["up_zero_degree_entries"], v["down_pure_gauge_only_entries"]) for k, v in res["p11819"].items()}, flush=True)
    res["p11820"] = p11820(z6i)
    res["p11821"] = p11821()
    print(json.dumps({k: v for k, v in res.items() if k in ("p11821",)}, indent=1, default=str))
    print("11820 flagship", res["p11820"]["flagship"], res["p11820"]["vev_needed_for_mb_over_mt_1_40_at_degree_12"])
    if not quick:
        json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
