"""Pass 11852: bulk quartic and exchange dynamics on the finite AdS4, and the boundary four-point function.

Bulk fields on the 36 Kramers reversals: phi (the 15-mode, crosscap propagator G15 = 12 Pi_15, Pass 11839) and chi (the
hidden 20-mode, propagator Pi_20).  Vertices: phi^4 contact, phi^3, phi^2 chi (the S15.S15.b20 coupling of Pass 11841).
Boundary operators O_x = sum_p N(x,p) phi_p (Pass 11847), bulk-to-boundary propagator K = N G15.

Tree-level connected boundary four-point structures:
  contact  C(x,y,z,w)  = sum_p K K K K
  15-exchange E15      = sum_{p,q} K(x,p)K(y,p) G15(p,q) K(z,q)K(w,q) + t + u
  20-exchange E20      = same with Pi_20
Computed: their norms, the dimension of the space of Sp(4,3)-invariant symmetric quartics on the boundary 15 (character
sum over all 51 840 elements), the rank of {C, E15, E20} and whether E20 lies in span{C, E15}: whether the hidden bulk
mode, invisible in two- and three-point functions, is detected by the boundary four-point function.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11831_11833_finite_ads4 as F  # noqa: E402
import w33_pass11834_11837_singletons_bulk_poincare_e8 as S  # noqa: E402
import w33_pass11847_finite_bulk_path_integral as BP  # noqa: E402

OUT = ROOT / "data" / "w33_pass11852_bulk_four_point.json"


def channels(K, G):
    A = np.einsum("xp,yp->xyp", K, K).reshape(-1, K.shape[1])
    s = (A @ G @ A.T).reshape(40, 40, 40, 40)
    t = s.transpose(0, 2, 1, 3)
    u = s.transpose(0, 3, 2, 1)
    return s + t + u


def sym4_invariants():
    keys, mats, Vs, index, _ = S.weil_group()
    C = S.characters(keys, mats, Vs, index)
    chi = S.sym2(C["chie"], C["sq"])  # the 15 = Sym^2 Rac
    sq, cu = C["sq"], C["cu"]
    q4 = np.array([index[F.key(F.m(g, g, g, g))] for g in mats])
    s4 = (chi**4 + 6 * chi**2 * chi[sq] + 3 * chi[sq] ** 2 + 8 * chi * chi[cu] + 6 * chi[q4]) / 24
    s3 = (chi**3 + 3 * chi * chi[sq] + 2 * chi[cu]) / 6
    s2 = (chi**2 + chi[sq]) / 2
    return dict(sym2=round(float(np.real(np.mean(s2))), 6), sym3=round(float(np.real(np.mean(s3))), 6),
                sym4=round(float(np.real(np.mean(s4))), 6))


def main():
    K36, X, A, G, N, Cx = BP.setup()
    P = BP.eigenprojectors(A)
    P15, P20 = P[3.0], P[-3.0]
    G15 = 12 * P15
    Kb = N @ G15
    res = {"pass_id": 11852}
    C = np.einsum("xp,yp,zp,wp->xyzw", Kb, Kb, Kb, Kb)
    E15 = channels(Kb, G15)
    E20 = channels(Kb, P20)
    flat = np.array([C.ravel(), E15.ravel(), E20.ravel()])
    gram = flat @ flat.T
    ev = np.linalg.eigvalsh(gram / np.max(abs(gram)))
    res["norms"] = dict(contact=float(np.linalg.norm(C)), exchange15=float(np.linalg.norm(E15)), exchange20=float(np.linalg.norm(E20)))
    res["rank_of_three_structures"] = int(np.sum(ev > 1e-10))
    # residual of E20 after projection on span{C, E15}
    M = flat[:2].T
    coef, *_ = np.linalg.lstsq(M, flat[2], rcond=None)
    resid = np.linalg.norm(flat[2] - M @ coef) / np.linalg.norm(flat[2])
    res["E20_relative_residual_outside_span_C_E15"] = float(resid)
    res["hidden_20_detected_at_four_points"] = bool(resid > 1e-6)
    # sanity: all structures fully symmetric and supported on the boundary 15
    Pb = BP.eigenprojectors(Cx)[-4.0]
    proj = np.einsum("xa,yb,zc,wd,abcd->xyzw", Pb, Pb, Pb, Pb, E20, optimize=True)
    res["E20_supported_on_boundary_15"] = bool(np.allclose(proj, E20, atol=1e-6 * abs(E20).max()))
    res["structures_symmetric"] = bool(all(np.allclose(T_, T_.transpose(1, 0, 2, 3)) and np.allclose(T_, T_.transpose(0, 2, 1, 3))
                                           for T_ in (C, E15, E20)))
    res["invariant_symmetric_forms_on_boundary_15"] = sym4_invariants()
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
