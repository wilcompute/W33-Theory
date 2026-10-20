"""Passes 12099-12100: one-loop ranking of the order-3 shifts, and a proton-decay bound on the Wilson-line scale
(Claude track; 12086, 12091, 12094).

12099 -- NEGATIVE: one loop does not select the three-family shift. A Z3 holonomy on a circle gives
  S(0) = 2 zeta(5), S(+-1/3) = sum_{n != 0} cos(2 pi n / 3)/n^5 = -(240/243) zeta(5) (exact), so
  V_B = -[N0 S(0) + (248 - N0) S(1/3)] depends only on N0 = the fixed dimension and is strictly decreasing in N0:
  bosons choose the largest fixed algebra, fermion domination the smallest. Among the 242 shifts compatible with a
  Standard-Model grading the fixed dimensions are {134, 92, 86, 80}; the three-family shifts (86) are neither extreme,
  so neither sign of the boson-fermion imbalance selects them.
12100 -- ESTIMATE: the X/Y bosons sit in a sector odd under a Z2 Wilson line (12094), so on a circle of radius R their
  lightest mode has M_X = 1/(2R). With the standard dimension-6 estimate tau_p ~ M_X^4 / (alpha_G^2 m_p^5) and the
  Super-Kamiokande bound tau(p -> e+ pi0) > 2.4 x 10^34 yr, alpha_G = 1/25 gives M_X > ~ 6 x 10^15 GeV and so
  1/R > ~ 1.2 x 10^16 GeV (order of magnitude; hadronic matrix elements and RG factors omitted). This is a bound on the
  compactification scale, not a prediction: the framework does not fix R.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.special import zeta

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12087_standard_model_sectors import Gradings  # noqa: E402

OUT = ROOT / "data" / "w33_pass12099_12100_selection_and_proton_bound.json"
SIMPLE = np.array([
    [0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5], [1, 1, 0, 0, 0, 0, 0, 0], [-1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, 0, 0], [0, 0, 0, 0, -1, 1, 0, 0], [0, 0, 0, 0, 0, -1, 1, 0]])


def main():
    checks, res = {}, {}
    z5 = zeta(5)
    n = np.arange(1, 200001, dtype=float)
    S0 = 2 * np.sum(1.0 / n ** 5)
    S13 = 2 * np.sum(np.cos(2 * np.pi * n / 3) / n ** 5)
    checks["12099: S(0) = 2 zeta(5), S(1/3) = -(240/243) zeta(5)"] = abs(S0 - 2 * z5) < 1e-12 and abs(S13 + 240 / 243 * z5) < 1e-12
    g = Gradings()
    R = g.R
    gens = g.sm_flag()
    gauge = [i for c in g.comps(g.fixedmask(g.span_of(gens))) for i in c]
    PH = np.round((np.array(list(itertools.product(range(3), repeat=8))) @ SIMPLE) @ R.T).astype(int) % 3
    dims = Counter(8 + int(np.sum(ph == 0)) for ph in PH if ph.any() and not np.any(ph[gauge] != 0))
    res["fixed_dims_of_compatible_shifts"] = dict(dims)
    VB = {d: -(d * S0 + (248 - d) * S13) for d in dims}
    res["V_B_by_fixed_dim"] = {str(k): v for k, v in VB.items()}
    checks["12099: 242 compatible shifts with fixed dims {134, 92, 86, 80}; V_B strictly decreasing in N0; 86 is neither extreme"] = (
        sum(dims.values()) == 242 and set(dims) == {134, 92, 86, 80} and min(VB, key=VB.get) == 134 and max(VB, key=VB.get) == 80
        and all(VB[a] < VB[b] for a, b in [(134, 92), (92, 86), (86, 80)]))
    # 12100
    hbar_GeV_s = 6.582119569e-25
    yr = 3.15576e7
    mp = 0.938272
    aG = 1 / 25
    tau_bound = 2.4e34 * yr / hbar_GeV_s     # in GeV^-1
    MX = (tau_bound * aG ** 2 * mp ** 5) ** 0.25
    res["12100"] = dict(alpha_G=aG, tau_bound_yr=2.4e34, MX_min_GeV=MX, invR_min_GeV=2 * MX)
    checks["12100: M_X > ~6e15 GeV and 1/R > ~1.2e16 GeV (order of magnitude, alpha_G = 1/25)"] = 1e15 < MX < 1e16 and 2e15 < 2 * MX < 2e16
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"], "%.2e" % MX)
    return res


if __name__ == "__main__":
    main()
