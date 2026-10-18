"""Pass 12049: the coloured threshold inventory for the strong-CP divisor of Pass 11950. Restoring a GUT by a
continuous Wilson line V supplies exactly e^{-8 pi^2 f3} ~ V^-3 when the restored group is SU(5) and exactly one
vectorlike 5 + 5bar becomes light with it. That is the single Nelson-Barr row of 12004/12005, and its hypercharge mass
ratio is the Clebsch 2/3 of 12047 (Claude track). Conditional on identifying the separating divisor Omega_12 = 0
with the GUT-restoring locus.

The target (Codex 11950). det Y_u = C eps^3 + O(eps^5) near the separating divisor eps = Omega_12 = 0 (TOE38/39). So
theta-bar = arg[e^{-8 pi^2 f3} det Y_u det Y_d] winds unless e^{-8 pi^2 f3} ~ eps^-3, i.e.
8 pi^2 f3 = (3/2) log chi10 + regular. 11950 left the coefficient 3/2 as "a falsifiable target for an actual colored
threshold inventory".

Inventory (exact group theory). Integrating out states of holomorphic mass m with SU(3) beta coefficient b gives
e^{-8 pi^2 f3} ~ prod m^b. Suppose a Wilson line V along the generator H restores a group G at V = 0. The broken vector
multiplets (masses ~ q_H V) give b_vec = -3T + T = -2T, where T is the SU(3) index of the broken generators (vector
plus eaten chiral; the same for N = 2). Each vectorlike coloured pair 3 + 3bar whose mass is ~ V gives +1. Regularity
against a total determinant winding W (3 per sector winding in V) requires
        b_vec + n = -W,   i.e.   n = -W - b_vec.
Computed here from explicit real Lie-algebra matrices (broken subspace = image of ad_H; SU(3) index from
tr ad_X^2; control: SU(3) fundamental T = 1/2):
  SU(5) -> SU(3) x SU(2) x U(1)_Y (H = Y):              T = 2, b_vec = -4 -> W = 3 needs n = 1.
  SO(10) -> SU(5) x U(1)_X (H = complex structure):       T = 3, b_vec = -6 -> W = 3: n = 3; W = 6: n = 0.
  SO(10) -> U(3) x SO(4) (H = J on 3 complex coordinates):  T = 5, b_vec = -10 -> W = 3: n = 7; W = 6: n = 4.
  (E6 patterns, quoted branchings, not computed: E6 -> SO(10) x U(1) T = 4 (n = 5 or 2); E6 -> SU(3)^3 T = 9.)
The minimal case: SU(5) restored by a hypercharge-direction Wilson line, plus exactly ONE vectorlike 5 + 5bar
light with it, gives b = -4 + 1 = -3 and so exactly the coefficient 3/2 on log chi10.
Coherence with earlier passes (not proof):
  * n = 1 is the single vectorlike row that 12004/12005 found necessary and sufficient for CP-real theta quarks.
  * If that pair's mass comes from the same hypercharge Wilson line, mu_L/mu_D = |Y(L_H)|/|Y(D)| = 3/2. So the
    lepton row is b_e = (2/3) b, the adjoint-mass Clebsch, the one rule of 12047 that fits both lepton ratios
    (branch C at M_Z).
  * With mu ~ eps M, the Barr row |b| = |B|/mu ~ 1/eps_u = 181 for B ~ M; the 12045 branches have |b| = 117-284.
Tensions, stated plainly.
  (i) Interpretation. In the magnetized reading of 11942, Omega_12 is a complex-structure modulus and the hypercharge
      Wilson line is z. The identification here needs a heterotic (T, U, V)-type reading, where Wilson-line moduli are
      period-matrix entries. This pass does not construct it.
  (ii) The down divisor. det Y_d also winds 3 in its own eps_d. With one SU(5) line, eps_d must not wind in V (W = 3).
      If up and down shared V (W = 6), SU(5) is impossible (n = -2), and SO(10) -> SU(5) x U(1)_X with n = 0 is the
      solution.
  (iii) Light X, Y. With M_X ~ eps_u M_c, a standard M_X needs a very high compactification scale, or else proton
      decay is fast. This is not computed here.
Not new: thresholds of massive vector multiplets and vectorlike states (textbook); Wilson-line GUT breaking (Hosotani;
Ibanez-Nilles-Quevedo; Witten 1985); Igusa forms in heterotic thresholds (Kawai hep-th/9512046; Mayr-Stieberger);
modular strong CP (Feruglio-Marrone-Strumia-Titov arXiv:2505.20395, arXiv:2608.13796); the divisor target (Codex 11950).
New: the inventory and selection rule n = -W - b_vec, and its coherence with 12004/12005/12047.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass11942_hypercharge_wilson_leptons import theta  # noqa: E402

OUT = ROOT / "data" / "w33_pass12049_coloured_divisor_inventory.json"
GM = [np.array(m, complex) for m in (
    [[0, 1, 0], [1, 0, 0], [0, 0, 0]], [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
    [[0, 0, 1], [0, 0, 0], [1, 0, 0]], [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], [[0, 0, 0], [0, 0, 1], [0, 1, 0]],
    [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], np.diag([1, 1, -2]) / np.sqrt(3))]


def realify(M):
    """complex n x n -> real 2n x 2n acting on (Re, Im) pairs interleaved per complex coordinate."""
    n = M.shape[0]
    R = np.zeros((2 * n, 2 * n))
    for i in range(n):
        for j in range(n):
            a, b = M[i, j].real, M[i, j].imag
            R[2 * i:2 * i + 2, 2 * j:2 * j + 2] = [[a, -b], [b, a]]
    return R


def su_n_basis(n):
    B = []
    for i in range(n):
        for j in range(i + 1, n):
            E = np.zeros((n, n), complex); E[i, j] = 1; E[j, i] = -1; B.append(E)
            E = np.zeros((n, n), complex); E[i, j] = 1j; E[j, i] = 1j; B.append(E)
    for k in range(n - 1):
        E = np.zeros((n, n), complex); E[k, k] = 1j; E[k + 1, k + 1] = -1j; B.append(E)
    return B


def so_n_basis(n):
    B = []
    for i in range(n):
        for j in range(i + 1, n):
            E = np.zeros((n, n)); E[i, j] = 1; E[j, i] = -1; B.append(E)
    return B


def index_on_broken(basis, H, X):
    """SU(3) Dynkin index T of the broken subspace image(ad_H), using X = i t_a: T = -tr(ad_X^2 | image)."""
    Bm = np.array([b.ravel() for b in basis]).T          # columns = basis vectors (complex or real flattened)
    Bm = np.vstack([Bm.real, Bm.imag]) if np.iscomplexobj(Bm) else Bm
    coords = lambda M: np.linalg.lstsq(Bm, np.concatenate([M.ravel().real, M.ravel().imag]) if np.iscomplexobj(Bm[:0]) or np.iscomplexobj(M) else M.ravel(), rcond=None)[0]  # noqa: E731

    def vec(M):
        v = M.ravel()
        return np.concatenate([v.real, v.imag]) if Bm.shape[0] == 2 * v.size else v.real

    def ad(Y):
        return np.array([np.linalg.lstsq(Bm, vec(Y @ b - b @ Y), rcond=None)[0] for b in basis]).T
    AH = ad(H)
    U, s, _ = np.linalg.svd(AH)
    img = U[:, s > 1e-9 * s.max()]
    AX = ad(X)
    # the image of ad_H is ad_X-invariant (X commutes with H); restrict via the orthonormal image basis
    R = img.T @ AX @ img
    resid = np.abs(img @ R - AX @ img).max()
    return float(-np.trace(R @ R)), int(img.shape[1]), float(resid)


def main():
    checks, res = {}, {}
    # control: SU(3) fundamental (real 6-dim C^3) has T(3 + 3bar) = 1
    X3 = 1j * GM[2] / 2
    T_fund = float(-np.trace(realify(X3) @ realify(X3)))
    res["control_fundamental_T(3+3bar)"] = T_fund

    # SU(5) -> SM, H = Y
    Y = np.diag([-1 / 3, -1 / 3, -1 / 3, 1 / 2, 1 / 2]).astype(complex)
    X = np.zeros((5, 5), complex); X[:3, :3] = 1j * GM[2] / 2
    T5, d5, r5 = index_on_broken(su_n_basis(5), 1j * Y, X)
    # SO(10) -> SU(5) x U(1)_X, H = complex structure J on C^5
    J = realify(1j * np.eye(5))
    X10 = realify(X)
    T10, d10, r10 = index_on_broken(so_n_basis(10), J, X10)
    # SO(10) -> U(3) x SO(4): H = J restricted to the first three complex coordinates
    J3 = realify(np.diag([1j, 1j, 1j, 0, 0]))
    T10b, d10b, r10b = index_on_broken(so_n_basis(10), J3, X10)
    pats = {"SU(5)->SU(3)xSU(2)xU(1)": (T5, d5, r5), "SO(10)->SU(5)xU(1)": (T10, d10, r10), "SO(10)->U(3)xSO(4)": (T10b, d10b, r10b)}
    table = {}
    for k, (T, d, r) in pats.items():
        bvec = -2 * T
        table[k] = dict(T=T, broken_real_dim=d, invariance_resid=r, b_vec=bvec, n_for_W3=-3 - bvec, n_for_W6=-6 - bvec)
    res["inventory"] = table
    checks["control: SU(3) fundamental index T(3+3bar) = 1"] = bool(abs(T_fund - 1) < 1e-12)
    checks["SU(5)->SM: 12 broken generators, T = 2, b_vec = -4, so exactly one vectorlike pair (n = 1) gives -3"] = bool(
        d5 == 12 and abs(T5 - 2) < 1e-9 and abs(table["SU(5)->SU(3)xSU(2)xU(1)"]["n_for_W3"] - 1) < 1e-9 and r5 < 1e-9)
    checks["SO(10)->SU(5)xU(1): 20 broken, T = 3, b_vec = -6 (n = 3 for W = 3, n = 0 for W = 6)"] = bool(
        d10 == 20 and abs(T10 - 3) < 1e-9 and r10 < 1e-9)

    # the divisor itself: det Y_u winds 3 and chi10 winds 2 around eps = 0 at the fitted up home
    tau = 1 + 0.8744698731421595j
    ph = np.linspace(0, 2 * np.pi, 721)
    dets = np.array([np.linalg.det(theta(np.array([[tau, 2e-3 * np.exp(1j * p)], [2e-3 * np.exp(1j * p), tau]]))) for p in ph])
    wind_det = float(np.sum(np.diff(np.unwrap(np.angle(dets)))) / (2 * np.pi))
    res["winding_detYu_small_circle"] = wind_det
    res["required_compensator"] = "e^{-8 pi^2 f3} ~ eps^-3 = chi10^{-3/2} (chi10 ~ pi^2 eps^2 Delta Delta, Pass 12048)"
    checks["det Y_u winds 3 around the separating divisor at the fitted up home (TOE38/39, 11950)"] = bool(abs(wind_det - 3) < 1e-6)
    checks["SU(5) inventory -4 + 1 = -3 cancels it exactly: total winding 3 + (-4 + 1) = 0"] = bool(round(wind_det) + (-4 + 1) == 0)

    # coherence: hypercharge mass ratio of the vectorlike 5 = (3,1,-1/3) + (1,2,1/2)
    kappa = abs(-1 / 3) / abs(1 / 2)
    res["coherence"] = dict(kappa_mu_D_over_mu_L=kappa, clebsch_12047="adjoint mass 2/3", inverse_eps_u=1 / 0.005520606513514881,
                            branch_abs_b={"A": 283.7, "B": 244.0, "C": 117.0})
    checks["coherence: the hypercharge-Wilson-line mass of the vectorlike 5 gives kappa = 2/3 (12047's Clebsch)"] = bool(abs(kappa - 2 / 3) < 1e-15)

    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2, default=float))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    print(json.dumps(table, indent=1))
    return res


if __name__ == "__main__":
    main()
