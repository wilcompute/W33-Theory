"""Pass 11931: the theta-zero law of the blow-up-protected Higgs (Pass 11930) is specific to the Eisenstein flux class.

At the Eisenstein point Omega = w.1 every symmetric det-3 flux N is compatible and rho-invariant. For each of the 12
det-3 forms (entries <= 4) take the channel N x N with mediator flux 2N (12 modes), the subspace of mediator modes
vanishing at all 9 rho-fixed points, and the Yukawa spectrum of random members of it.

Result:
* A2 and A2' (the Eisenstein / Z[w] norm form, class of A2): fixed-point rank 8, protected space 4-dim, and EVERY member
  gives (1, 1, 0) exactly (deviation ~1e-14) -- the theta-zero law.
* the ten forms of the x^2 + 3y^2 class: fixed-point rank 6, protected space 6-dim, generic O(1) spectra (deviation
  0.5-0.9).
Reading: the law -- and with it the conditional inverted-ordering reading of Pass 11930 -- needs flux lattice and
complex structure to be Eisenstein together. Of the two binary-form classes of determinant 3 (Pass 11915), only the A2
class supports it.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11928_eisenstein_point as E  # noqa: E402
import w33_pass11930_fixed_point_avoiding_higgs as P  # noqa: E402

OUT = ROOT / "data" / "w33_pass11931_theta_zero_needs_eisenstein_flux.json"


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    rng = np.random.default_rng(11931)
    forms = [[[a, b], [b, c]] for a in range(1, 5) for c in range(1, 5) for b in range(-3, 4) if a * c - b * b == 3]
    rows = []
    for N in forms:
        NH = (2 * np.array(N)).tolist()
        z = E.zgrid(E.OM0, 16)
        nH = np.sqrt(np.mean(abs(np.array([F.psi_at(z, j, NH, E.OM0) for j in F.chars(NH)])) ** 2, axis=1))
        V = np.array([P.vals(NH, p) / nH for p in P.fixed_points()])
        u, s, vh = np.linalg.svd(V)
        r = int(np.sum(s > 1e-9 * s[0]))
        K = vh[r:].conj().T
        T0 = P.tensor(N, N, NH, E.OM0)
        dev = []
        for _ in range(5):
            c = K @ (rng.normal(size=K.shape[1]) + 1j * rng.normal(size=K.shape[1]))
            sv = np.linalg.svd(np.tensordot(c.conj(), T0, 1), compute_uv=False)
            sv = sv / sv[0]
            dev.append(float(abs(1 - sv[1]) + sv[2]))
        eis = (N[0][0] == N[1][1] == 2)
        rows.append(dict(N=N, eisenstein_class=eis, fixed_point_rank=r, protected_dim=K.shape[1], max_dev=max(dev), min_dev=min(dev)))
    res = dict(pass_id=11931, rows=rows)
    eis = [x for x in rows if x["eisenstein_class"]]
    oth = [x for x in rows if not x["eisenstein_class"]]
    res["checks"] = {k: bool(v) for k, v in dict(
        twelve_forms=len(rows) == 12,
        eisenstein_pair_rank8_dim4_exact=len(eis) == 2 and all(x["fixed_point_rank"] == 8 and x["protected_dim"] == 4 and x["max_dev"] < 1e-9 for x in eis),
        other_class_rank6_dim6_generic=len(oth) == 10 and all(x["fixed_point_rank"] == 6 and x["protected_dim"] == 6 and x["min_dev"] > 1e-2 for x in oth),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])


if __name__ == "__main__":
    main()
