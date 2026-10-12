"""Pass 11929: at the Eisenstein point the generations carry distinct joint Z3 x Z3 charges, but every Higgs that respects
the extra symmetry is locked -- the polynomial hierarchy of Pass 11928 needs a magic Higgs.

Setting as in Pass 11928 (A2 dual pair, Omega = w.1, rho: z -> w z). The rotation rho acts on the flavour qutrit of the 10
as an order-3 Clifford element; in characteristic 3 every order-3 element of SL(2,F3) is unipotent and fixes a line of
the Pauli plane, so some Pauli commutes with it. Here P = XZ.

1. rho P rho^-1 = P EXACTLY on the 10 (commutator phase 1), and the joint (rho, P) charges of the three generations are
   distinct: (2,1), (0,0), (0,2) -- P splits the charge-0 pair that Pass 11928 found degenerate. P (a K10 translation)
   is an exact symmetry for every Omega; rho only at w.
2. Up-Higgs space: of the 12 modes, a 3-dimensional combination never couples to Q.Q at any Omega (stacked Yukawa map of
   rank 9 over four moduli); the coupled part splits into three P-sectors of dimension 3, and rho preserves each
   (residual 0), so the joint residual group is consistent (Yukawa invariance forces commutator phase 1 on the Higgs).
3. In every one of the 9 joint (rho, P) Higgs sectors (dimensions 1,1,1 / 3,3,3 / 2,2,2) the up spectrum near the point
   is LOCKED: m_u/m_c ~ 1 or m_c/m_t ~ 1 (a degenerate pair), independent of eps. A Higgs that preserves P is a
   stabiliser-type flavour state and keeps a residual S3 (Passes 11923-11924).
Reading: the extra Z3 separates the generations' charges, but any vacuum respecting it re-locks charm and up. The
polynomial (non-Gaussian) hierarchies of Pass 11928 come from Higgs vectors that mix P-charges inside a rho-sector,
i.e. from a magic Higgs -- the Eisenstein-point hierarchy and the magic criterion of Pass 11923 are the same requirement.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11928_eisenstein_point as E  # noqa: E402

OUT = ROOT / "data" / "w33_pass11929_joint_residual_lock.json"
W = E.W
J = E.J
XP = np.roll(np.eye(3), 1, axis=0)
ZP = np.diag([1, W, W * W])
P = XP @ ZP


def tensor(Om, G=14):
    z = E.zgrid(Om, G)
    Q = E.modes(E.A2, Om, z)
    Hm = E.modes(E.HU, Om, z)
    return np.einsum("ap,bp,hp->hab", Q, Q, np.conj(Hm)) / z.shape[0]


def null(M, tol=1e-9):
    u, s, vh = np.linalg.svd(M)
    r = np.sum(s > tol * s[0])
    return vh[r:].conj().T


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    rng = np.random.default_rng(11929)
    res = dict(pass_id=11929)
    R10 = E.rho_matrix(E.A2)
    lam = np.trace(P.conj().T @ R10 @ P @ R10.conj().T) / 3
    w, U = np.linalg.eig(R10 + 0.37 * P)
    joint = []
    for k in range(3):
        u = U[:, k] / np.linalg.norm(U[:, k])
        joint.append((int(round(np.angle(np.vdot(u, R10 @ u)) / (2 * np.pi / 3))) % 3,
                      int(round(np.angle(np.vdot(u, P @ u)) / (2 * np.pi / 3))) % 3))
    res["rho_P_commutator_phase"] = [float(lam.real), float(lam.imag)]
    res["generation_joint_charges"] = sorted(joint)
    Oms = [E.OM0 + 0.05 * (rng.normal() + 1j * rng.normal()) * np.eye(2) + 0.05 * (rng.normal() + 1j * rng.normal()) * J
           for _ in range(4)]
    Ts = [tensor(Om) for Om in Oms]
    A = np.vstack([np.array([T[h].ravel() for h in range(12)]).T for T in Ts])
    B = np.vstack([np.array([(P @ T[h] @ P.T).ravel() for h in range(12)]).T for T in Ts])
    res["stacked_rank"] = int(np.linalg.matrix_rank(A, 1e-9))
    RH = E.rho_matrix(E.HU)
    psec = []
    for m in range(3):
        Nsp = null(B - W ** m * A)
        psec.append(Nsp.shape[1])
        d = Nsp @ (rng.normal(size=Nsp.shape[1]) + 1j * rng.normal(size=Nsp.shape[1]))
        e = RH @ d
        res.setdefault("rho_preserves_P_sector_residual", []).append(
            float(np.linalg.norm((B - W ** m * A) @ e) / np.linalg.norm(A @ e)))
    res["P_sector_dims_including_kernel"] = psec
    dd = rng.normal(size=2) + 1j * rng.normal(size=2)
    sectors = []
    for r in range(3):
        for m in range(3):
            Nsp = null(np.vstack([RH - W ** r * np.eye(12), B - W ** m * A]))
            keep = [k for k in range(Nsp.shape[1]) if np.linalg.norm(A @ Nsp[:, k]) > 1e-8]
            if not keep:
                continue
            Nsp = Nsp[:, keep]
            dvec = Nsp @ (rng.normal(size=Nsp.shape[1]) + 1j * rng.normal(size=Nsp.shape[1]))
            dvec /= np.linalg.norm(dvec)
            rows = []
            for eps in (1e-2, 1e-3):
                Om = E.OM0 + eps * (dd[0] * np.eye(2) + dd[1] * J)
                s = np.linalg.svd(np.tensordot(dvec, tensor(Om), 1), compute_uv=False)
                rows.append((eps, s[1] / s[0], s[2] / s[1]))
            sectors.append(dict(rho=r, P=m, dim=len(keep), rows=rows,
                                degenerate=bool(min(abs(rows[-1][1] - 1), abs(rows[-1][2] - 1)) < 0.05)))
    res["joint_sectors"] = sectors
    res["checks"] = {k: bool(v) for k, v in dict(
        rho_and_P_commute_exactly=abs(lam - 1) < 1e-9,
        generations_have_distinct_joint_charges=len(set(joint)) == 3 and res["generation_joint_charges"] == [(0, 0), (0, 2), (2, 1)],
        three_never_coupling_higgs=res["stacked_rank"] == 9,
        rho_preserves_each_P_sector=max(res["rho_preserves_P_sector_residual"]) < 1e-9,
        all_nine_joint_sectors_present=len(sectors) == 9 and sorted(s["dim"] for s in sectors) == [1, 1, 1, 2, 2, 2, 3, 3, 3],
        every_symmetric_higgs_locked=all(s["degenerate"] for s in sectors),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])


if __name__ == "__main__":
    main()
