"""Pass 12088: the CKM phase is not a cube-root clock phase -- NEGATIVE (Claude track; 12005, 12080, 12082).

Hypothesis. Clocks are cube roots of unity (12080) and the Klein clock vacuum breaks CP (12082); perhaps the CP phase
of the Barr row of the corpus quark model (12005) is quantised to multiples of pi/3. Test, overdetermined: the 12005
model (up sector fixed by the Weber point; down theta matrix with y_d, e_d, z and one vectorlike Barr row b) with
b = r (1, e^{i k pi/3}, e^{i l pi/3}) -- equal magnitudes, quantised phases -- has 4 continuous parameters for 6
observables (m_s/m_b, m_d/m_s, |V_us|, |V_cb|, |V_ub|, J).
Results (least squares, log residuals):
  * control: equal magnitudes with CONTINUOUS phases (6 parameters) fits exactly (|res| ~ 1e-14); the fitted phases are
    0.62 and 5.62 in units of pi/3 -- not multiples.
  * all 36 quantised (k, l): best |res| = 0.053 at (0, 5).
  * baseline: 36 RANDOM fixed phase pairs with the same 4-parameter fit: best |res| = 0.021, second 0.047, median 0.52.
Conclusion. Quantised pi/3 phases fit no better than random fixed phases: in this model the CP phase is not a clock
(cube-root) phase. Scope: this model and parametrisation; the frozen numbers come from the search driver
(analysis/search_drivers_12088/), and the producer re-runs the control and the best quantised fit.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares, root

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12088_the_ckm_phase_is_not_a_clock_phase.json"
n = np.arange(-10, 11)
n1, n2 = np.meshgrid(n, n, indexing="ij")
v1 = n1[None, None, :, :] + np.arange(3)[:, None, None, None] / 3
v2 = n2[None, None, :, :] + np.arange(3)[None, :, None, None] / 3
D = np.exp(1j * np.pi * np.arange(3) ** 2 / 3)
RECORD = dict(quantised_best=0.0533, quantised_best_kl=[0, 5], random_best=[0.0208, 0.0473, 0.065, 0.0863, 0.1545], random_median=0.5249,
              control_phases_over_pi3=[0.6223, 5.6185])


def theta(y, eu, yd, ed, z, up=False):
    O11 = 1 + 1j * y
    O22 = O11 if up else 1j * yd
    e = 1j * (eu if up else ed)
    A = np.exp(3j * np.pi * (O11 * v1 * v1 + 2 * e * v1 * v2 + O22 * v2 * v2) + 6j * np.pi * v2 * (0 if up else 1j * z)).sum(axis=(-2, -1))
    A = D.conj()[:, None] * A
    if up:
        A = A * D.conj()[None, :]
    return A.real / np.linalg.norm(A)


def main():
    checks, res = {}, {}
    Ut = np.array([.620 / 168.26, 1.23e-3 / .620])
    r = root(lambda p: np.log(np.array((lambda a: [a[1] / a[0], a[2] / a[1]])(np.linalg.svd(theta(p[0], p[1], 0, 0, 0, True), compute_uv=False))) / Ut), [.8745, .00552])
    y, eu = r.x
    Uu = np.linalg.svd(theta(y, eu, 0, 0, 0, True))[0]
    target = np.array([.053 / 2.86, 2.67e-3 / .053, .225, .0411, .00382, 3.08e-5])

    def obs(yd, ed, zi, b):
        m = theta(y, eu, yd, ed, zi)
        K = np.eye(3) - np.outer(b.conj(), b) / (1 + np.vdot(b, b).real)
        ev, O = np.linalg.eigh(K)
        A = (O * np.sqrt(ev)) @ O.conj().T
        Ud, sd, _ = np.linalg.svd(m @ A)
        V = (Uu.conj().T @ Ud)[::-1, ::-1]
        J = np.imag(V[0, 0] * V[1, 1] * V[0, 1].conj() * V[1, 0].conj())
        return np.array([sd[1] / sd[0], sd[2] / sd[1], abs(V[0, 1]), abs(V[1, 2]), abs(V[0, 2]), J])

    def fit(make, npar, starts, seed):
        rng = np.random.default_rng(seed)
        best = None
        for _ in range(starts):
            p0 = np.r_[rng.uniform(-3, .2), rng.uniform(.005, .07), rng.uniform(-.06, .06), rng.normal(0, 3, npar - 3)]

            def F(p):
                try:
                    if y * np.exp(p[0]) - p[1] ** 2 < .005:
                        return np.ones(6) * 100
                    o = obs(np.exp(p[0]), p[1], p[2], make(p))
                    return np.r_[np.log(np.maximum(o[:5], 1e-30) / target[:5]), (o[5] - target[5]) / target[5]]
                except Exception:  # noqa: BLE001
                    return np.ones(6) * 100
            f = least_squares(F, p0, max_nfev=800)
            if best is None or np.linalg.norm(f.fun) < np.linalg.norm(best.fun):
                best = f
        return best
    c = fit(lambda p: p[3] * np.array([1, np.exp(1j * p[4]), np.exp(1j * p[5])]), 6, 40, 0)
    q = fit(lambda p: p[3] * np.array([1, 1, np.exp(5j * np.pi / 3)]), 4, 40, 7)
    res["control_residual"] = float(np.linalg.norm(c.fun))
    res["control_phases_over_pi3"] = ((np.array(c.x[4:6]) / (np.pi / 3)) % 6).tolist()
    res["quantised_05_residual"] = float(np.linalg.norm(q.fun))
    res["record"] = RECORD
    checks["control (continuous equal-magnitude phases) fits exactly; phases not multiples of pi/3"] = bool(
        res["control_residual"] < 1e-8 and all(min(abs(x - round(x)), 1) > 0.1 for x in res["control_phases_over_pi3"]))
    checks["best quantised fit (0,5) misses at |res| ~ 0.053 (4 parameters, 6 observables)"] = abs(res["quantised_05_residual"] - 0.0533) < 0.005
    checks["frozen baseline: random fixed phases do as well (best 0.021 < 0.053): no evidence for pi/3 quantisation"] = (
        RECORD["random_best"][0] < RECORD["quantised_best"])
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
