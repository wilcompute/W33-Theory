"""Pass 12078: clocks as Wilson lines -- the one-loop (Hosotani) potential of commuting clock holonomies on T^k, and
what matter selects (Claude track; 12056-12057, 12071, 12077).

Setting. Compactify on a torus T^k (equal radii) with commuting order-2 holonomies theta_1..theta_k, each an inner
involution of E8 (identity, clock or split). A root alpha with parity pattern eps in {0,1}^k contributes
S_k(|eps|) = sum_{n in Z^k, n != 0} cos(pi n.eps) / |n|^{4+k} (the cubic lattice makes S depend only on |eps|);
V = -(N_B - N_F) sum_alpha S_k(|eps_alpha|) (Cartan: eps = 0), with N_B bosonic and N_F periodic adjoint-fermion
degrees of freedom. So only the root pattern histogram of the holonomy set and the sign of the imbalance matter.
Exact results:
  * k = 1: S_1(0) = 2 zeta(5), S_1(1) = -(15/8) zeta(5). A clock holonomy gives V_B = -62 zeta(5) (136 even, 112 odd)
    and a split one gives V_B = 0 EXACTLY (120 * 2 = 128 * 15/8). Among non-trivial holonomies, bosonic loops choose a
    clock (one time) and fermion-dominated loops a split form -- the 12056 dichotomy from a lattice identity.
  * k = 2 (two clocks): Klein pairs (product a clock; e6 + u(1)^2, histogram 72/112/56) have lower V_B than non-Klein
    pairs (d6 + 2a1, 64/128/48).
  * k = 3 (three clocks, all five triple types of 12077): the Klein triple (72/0/168/0, e6 + u(1)^2) has the lowest V_B;
    fermion domination picks the type (32/96/96/16).
Reading. Wherever clocks enter as Wilson lines, bosonic matter chooses the clocks that keep the most of E8 -- one clock,
then a Klein group of clocks with the grand-unified e6 + u(1)^2 -- and fermion domination chooses the opposite, as in
12056-12057 (where a, the boson-fermion imbalance, decided one time). The trivial holonomy is always lowest for bosons;
the statements compare non-trivial clock holonomies (forced, e.g., by twisted boundary conditions).
Scope: equal radii, first-order Hosotani sums (lattice sums to |n_i| <= 60, checked against 40).
"""

import itertools
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.special import zeta

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12078_wilson_line_clocks_and_matter.json"


@lru_cache(None)
def S(m, k, N=60):
    rng = np.arange(-N, N + 1)
    grid = np.array(np.meshgrid(*([rng] * k), indexing="ij")).reshape(k, -1).T
    grid = grid[np.any(grid != 0, axis=1)]
    eps = np.array([1] * m + [0] * (k - m))
    return float(np.sum(np.cos(np.pi * grid @ eps) / np.linalg.norm(grid, axis=1) ** (4 + k)))


def VB(hist, k, N=60):
    h = list(hist)
    h[0] += 8
    return -sum(h[m] * S(m, k, N) for m in range(k + 1))


def main():
    checks, res = {}, {}
    Adj, invs, tick, fib = setup()
    C = np.array([s for k, s in invs if k == "clock"], dtype=np.int8)
    Sp = np.array([s for k, s in invs if k == "split"], dtype=np.int8)
    z5 = zeta(5)
    checks["S_1(0) = 2 zeta(5), S_1(1) = -(15/8) zeta(5) (lattice sum, N = 60)"] = abs(S(0, 1) - 2 * z5) < 1e-6 and abs(S(1, 1) + 15 / 8 * z5) < 1e-6
    hc = [240 - 112, 112]
    hs = [240 - int(Sp[0].sum()), int(Sp[0].sum())]
    res["k1"] = dict(clock=VB(hc, 1), split=VB(hs, 1))
    checks["k = 1: clock V_B = -62 zeta(5); split V_B = 0 exactly (all 135 splits odd on 128)"] = bool(
        abs(VB(hc, 1) + 62 * z5) < 1e-5 and set(Sp.sum(1)) == {128} and abs(VB(hs, 1)) < 1e-5 and (136 * 2 - 112 * 15 / 8 - 62) == 0
        and 120 * 2 == 128 * 15 / 8)
    hist2 = Counter()
    for a, b in [(0, x) for x in range(1, 120)]:
        h = tuple(int(np.sum(C[a] + C[b] == m)) for m in range(3))
        hist2[h] += 1
    res["k2_histograms"] = {str(h): VB(h, 2) for h in hist2}
    checks["k = 2: two pair types; the Klein pair (72,112,56) has lower V_B than (64,128,48)"] = (
        set(hist2) == {(72, 112, 56), (64, 128, 48)} and VB((72, 112, 56), 2) < VB((64, 128, 48), 2))
    types3 = [(72, 0, 168, 0), (40, 96, 72, 32), (32, 96, 96, 16), (40, 88, 88, 24), (32, 104, 80, 24)]
    v3 = {t: VB(t, 3) for t in types3}
    res["k3"] = {str(t): v for t, v in v3.items()}
    checks["k = 3: the Klein triple has the lowest V_B, type (32,96,96,16) the highest (fermion choice)"] = (
        min(v3, key=v3.get) == (72, 0, 168, 0) and max(v3, key=v3.get) == (32, 96, 96, 16))
    conv = all(abs(VB(h, k, 40) - VB(h, k, 60)) < 1e-3 * abs(VB(h, k, 60)) for k, h in ((2, (72, 112, 56)), (2, (64, 128, 48)), (3, (72, 0, 168, 0))))
    checks["lattice sums converged (N = 40 vs 60)"] = bool(conv)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
