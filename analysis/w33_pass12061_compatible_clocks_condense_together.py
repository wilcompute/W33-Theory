"""Pass 12061: compatible clocks condense together -- in the microscopic tick model, a two-tick condensate prefers
two JOINTLY MEASURABLE (collinear) events at every temperature, by an exact closed form (Claude track; 12055, 12060).

Model (12055): 120 ticks, positive generators h = I - Pi_k(p) on two qutrits, F_T(phi) = -T log Tr exp(-H/T).
12055 proved that at fixed total rate a single tick wins. Here the question is what a condensate that carries TWO
clocks prefers -- the case in which 12060 found rest frames (collinear) or only spin (non-collinear).
Exact spectra of H = h_a + h_b (beta = 1/T, x = e^-beta):
  same point (k != l):      {1^6, 2^3}                    Z_same = 6x + 3x^2
  collinear (p != q, any k, l): {0, 1^4, 2^4}             Z_col  = 1 + 4x + 4x^2
  non-collinear:            {(1 -+ 1/sqrt3)^3, 2^3}        Z_far  = 6x cosh(beta/sqrt3) + 3x^2
THEOREM. Z_col - Z_far = 4x [sinh^2(beta/2) - 3 sinh^2(beta/(2 sqrt3))] > 0 for every beta > 0, since sinh(t)/t is
increasing; and Z_col - Z_same = (1 - x)^2 > 0. So F_col < F_far and F_col < F_same at EVERY temperature. As T -> inf
the collinear/non-collinear gap closes only at fourth order, Z_col - Z_far = beta^4/18 - beta^5/18 + O(beta^6) (sympy series). The same ordering
holds for unequal weights (t, 1-t), checked on a grid of t and T.
Reading. If the dynamics carries two clocks, they are compatible -- jointly measurable events -- and by 12060 they
define exactly three rest frames (the mirror frames Jp = q), not a spin-only vacuum. The reason is the shared
eigenvector: compatible ticks have a common zero mode, incompatible ones (mutually unbiased) do not.
Scope: this microscopic model; why the condensate would carry two ticks (12055 prefers one) is not derived.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12055_microscopic_tick_model import ADJ, HS, free  # noqa: E402

OUT = ROOT / "data" / "w33_pass12061_compatible_clocks_condense_together.json"
S3 = np.sqrt(3)


def main():
    checks, res = {}, {}
    p = 0
    spectra = {"same": set(), "collinear": set(), "far": set()}
    for b in range(1, 120):
        q, l = divmod(b, 3)
        typ = "same" if q == p else ("collinear" if ADJ[p, q] else "far")
        e = np.round(np.linalg.eigvalsh(HS[0] + HS[b]), 9)
        spectra[typ].add(tuple(e))
    exact = {
        "same": tuple(sorted([1.0] * 6 + [2.0] * 3)),
        "collinear": tuple(sorted([0.0] + [1.0] * 4 + [2.0] * 4)),
        "far": tuple(sorted([round(1 - 1 / S3, 9)] * 3 + [round(1 + 1 / S3, 9)] * 3 + [2.0] * 3)),
    }
    checks["exact two-tick spectra: same {1^6,2^3}, collinear {0,1^4,2^4}, far {(1-+1/sqrt3)^3, 2^3} (all 119 partners)"] = all(
        len(v) == 1 and np.allclose(next(iter(v)), exact[k]) for k, v in spectra.items())
    Ts = np.geomspace(0.01, 100, 400)
    Fv = {k: np.array([free((np.eye(120)[0] + np.eye(120)[b]), T) for T in Ts]) for k, b in
          (("same", 1), ("collinear", 3 * int(np.nonzero(ADJ[p])[0][0])), ("far", 3 * int(next(q for q in range(1, 40) if not ADJ[p, q]))))}
    beta = 1 / Ts
    x = np.exp(-beta)
    Zc, Zf, Zs = 1 + 4 * x + 4 * x * x, 6 * x * np.cosh(beta / S3) + 3 * x * x, 6 * x + 3 * x * x
    checks["closed forms reproduce the model free energies, T in [0.01, 100]"] = bool(
        np.allclose(Fv["collinear"], -Ts * np.log(Zc), atol=1e-8) and np.allclose(Fv["far"], -Ts * np.log(Zf), atol=1e-8)
        and np.allclose(Fv["same"], -Ts * np.log(Zs), atol=1e-8))
    ident = 4 * x * (np.sinh(beta / 2) ** 2 - 3 * np.sinh(beta / (2 * S3)) ** 2)
    checks["identity Z_col - Z_far = 4x[sinh^2(b/2) - 3 sinh^2(b/(2 sqrt3))] > 0 and Z_col - Z_same = (1-x)^2"] = bool(
        np.allclose(Zc - Zf, ident, rtol=1e-9, atol=1e-14) and np.all(ident > 0) and np.allclose(Zc - Zs, (1 - x) ** 2))
    small = np.array([1e-2, 2e-2, 4e-2])
    xs = np.exp(-small)
    lead = (1 + 4 * xs + 4 * xs * xs - 6 * xs * np.cosh(small / S3) - 3 * xs * xs) / small ** 4
    res["high_T_coefficient"] = lead.tolist()
    checks["high-T: the gap closes at fourth order, (Z_col - Z_far)/beta^4 -> 1/18 (sympy: b^4/18 - b^5/18 + ...)"] = bool(np.allclose(lead, 1 / 18 - small / 18, atol=2e-4))
    checks["F_col < F_far < F_same at every T on the grid"] = bool(np.all(Fv["collinear"] < Fv["far"]) and np.all(Fv["far"] < Fv["same"]))
    worst = np.inf
    for t in np.linspace(0.05, 0.95, 19):
        for T in (0.05, 0.3, 1.0, 3.0, 10.0):
            c = free(t * np.eye(120)[0] + (1 - t) * np.eye(120)[3 * int(np.nonzero(ADJ[p])[0][0])], T)
            f = min(free(t * np.eye(120)[0] + (1 - t) * np.eye(120)[3 * q + l], T) for q in range(1, 40) if not ADJ[p, q] for l in range(3))
            worst = min(worst, f - c)
    res["unequal_weights_min_gap"] = float(worst)
    checks["unequal weights (t, 1-t), 19 x 5 grid: collinear below every non-collinear pair"] = bool(worst > 0)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
