"""Pass 11847: a finite bulk path integral on the finite AdS4 of two qutrits.

Bulk: the 36 Kramers reversals, Gaussian field phi with the crosscap propagator G = 6I + 2A - J of Pass 11839
(A = orthogonality graph; G = 12 x projector onto the bulk 15).  Boundary: the 40 contexts, O_x = sum_p N(x,p) phi_p with
N the orthogonality incidence (each reversal sees 10 contexts, each context 9 reversals).  Interaction: the cubic
contact vertex lambda sum_p phi_p^3 (the S15^3 invariant of Pass 11841 is unique).

Computed: the boundary two-point function (and that it is a multiple of the projector onto the boundary 15); the tree
three-point contact Witten diagram and its proportionality to the boundary-intrinsic cubic (forced by multiplicity one);
the one-loop bubble and the bulk modes that circulate in it (the hidden 20); the vanishing of the 20 on the boundary.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11831_11833_finite_ads4 as F  # noqa: E402

OUT = ROOT / "data" / "w33_pass11847_finite_bulk_path_integral.json"


def r(x, nd=8):
    return round(float(x), nd)


def setup():
    K = [k for k in F.PTS if F.Q[k] == 2]
    X = [k for k in F.PTS if F.Q[k] == 0]
    A = np.array([[1.0 if a != b and F.beta(a, b) == 0 else 0.0 for b in K] for a in K])
    J = np.ones((36, 36))
    G = 6 * np.eye(36) + 2 * A - J
    N = np.array([[1.0 if F.beta(x, p) == 0 else 0.0 for p in K] for x in X])
    Cx = np.array([[1.0 if x != y and F.beta(x, y) == 0 else 0.0 for y in X] for x in X])
    return K, X, A, G, N, Cx


def eigenprojectors(M):
    w, V = np.linalg.eigh(M)
    out = {}
    for lam in sorted(set(np.round(w, 6))):
        Vs = V[:, np.isclose(w, lam, atol=1e-6)]
        out[float(lam)] = Vs @ Vs.T
    return out


def main():
    K, X, A, G, N, Cx = setup()
    res = {"pass_id": 11847}
    P = eigenprojectors(A)  # bulk: 15 (const), 3 (the 15), -3 (the 20)
    Pb = eigenprojectors(Cx)  # boundary contexts: collinearity SRG(40,12,2,4): 12, 2 (24), -4 (15)
    res["bulk_spectrum"] = {str(k): int(round(np.trace(v))) for k, v in P.items()}
    res["boundary_spectrum"] = {str(k): int(round(np.trace(v))) for k, v in Pb.items()}
    res["G_equals_12_projector_15"] = bool(np.allclose(G, 12 * P[3.0]))
    # two-point
    two = N @ G @ N.T
    rel = Counter()
    for i in range(40):
        for j in range(40):
            tag = "same" if i == j else ("meet" if Cx[i, j] else "opposite")
            rel[(tag, r(two[i, j], 6))] += 1
    res["boundary_two_point"] = {f"{a}:{b}": c for (a, b), c in sorted(rel.items(), key=str)}
    P15b = Pb[-4.0]
    c2 = np.trace(two) / np.trace(P15b)
    res["two_point_is_multiple_of_boundary_15_projector"] = bool(np.allclose(two, c2 * P15b))
    res["two_point_coefficient"] = r(c2)
    res["hidden_20_invisible"] = bool(np.allclose(N @ P[-3.0], 0))
    # tree contact Witten diagram: W(x,y,z) = sum_p Kb(x,p) Kb(y,p) Kb(z,p), Kb = N G
    Kb = N @ G
    W = np.einsum("xp,yp,zp->xyz", Kb, Kb, Kb)
    # boundary-intrinsic cubic on the boundary 15: U(x,y,z) = sum_w P15(x,w) P15(y,w) P15(z,w)
    U = np.einsum("xw,yw,zw->xyz", P15b, P15b, P15b)
    c3 = float(np.sum(W * U) / np.sum(U * U))
    res["tree_three_point_nonzero"] = bool(np.abs(W).max() > 1e-9)
    res["tree_three_point_equals_c_times_boundary_cubic"] = bool(np.allclose(W, c3 * U, atol=1e-8 * np.abs(W).max()))
    res["tree_three_point_coefficient"] = r(c3, 6)
    vals = Counter(r(v, 6) for v in W.ravel())
    res["tree_three_point_distinct_values"] = len(vals)
    # one-loop bubble: Sigma = lambda^2/2 (G o G) between two bulk vertices; components on bulk modes
    GG = G * G
    comp = {str(k): r(np.trace(GG @ v) / max(np.trace(v), 1)) for k, v in P.items()}
    res["bubble_G_hadamard_G_eigen_components"] = comp
    loop = N @ G @ GG @ G @ N.T
    c_loop = np.trace(loop) / np.trace(P15b)
    res["one_loop_two_point_is_multiple_of_boundary_15"] = bool(np.allclose(loop, c_loop * P15b))
    res["one_loop_over_tree_two_point"] = r(c_loop / c2, 6)
    # the hidden 20 inside the bubble: G o G projected on the 20
    res["hidden_20_circulates_in_bubble"] = bool(np.linalg.norm(P[-3.0] @ GG @ P[-3.0]) > 1e-8)
    json.dump(res, open(OUT, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
