"""Pass 11932: blow-up protection is residual Z3 charge 2, and the theta-zero law follows from the generation charges.

1. For the up (2A2) and Weinberg (2A2') mediators at Omega = w.1, the 4-dim space of modes vanishing at all 9 fixed
   points (Pass 11930) EQUALS the rho-charge-2 eigenspace (projector distance ~1e-15): charge-2 modes vanish at every
   fixed point because no fixed point carries local phase 2 for these bundles. The down mediator (4.1) has a 7-dim
   protected space that is not a charge sector.
   => The assumption of Pass 11930 (positive localised blow-up masses) is replaced by a discrete one: the mediator
   carries residual charge 2.
2. Analytic form of the law. In the rho-eigenbasis of the generations (charges 0, 0, 2), a charge-2 mediator couples
   only pairs with q_a + q_b = 2 mod 3, i.e. the (0,2) pairs, so the symmetric Yukawa is
       [[0, 0, x], [0, 0, y], [x, y, 0]]   with singular values (sqrt(|x|^2+|y|^2), sqrt(|x|^2+|y|^2), 0),
   which is (1,1,0) exactly. Checked: in the charge basis the (0,0), (0,0)', (0,0'), (2,2) entries vanish (~1e-15) for
   random charge-2 mediators, and the spectrum is (1,1,0).
3. Near the point the broken rho fills the forbidden entries at O(eps), giving the (1, 1 - a eps, b eps^2) scalings of
   Pass 11930.
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

OUT = ROOT / "data" / "w33_pass11932_protection_is_charge_two.json"
A2, A2M = [[2, 1], [1, 2]], [[2, -1], [-1, 2]]


def charge_basis(R):
    w, U = np.linalg.eig(R)
    q = np.array([int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in w])
    return q, U


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    rng = np.random.default_rng(11932)
    res = dict(pass_id=11932)
    for name, N, NH in (("up", A2, [[4, 2], [2, 4]]), ("weinberg", A2M, [[4, -2], [-2, 4]]), ("down", None, [[4, 0], [0, 4]])):
        z = E.zgrid(E.OM0, 16)
        nH = np.sqrt(np.mean(abs(np.array([F.psi_at(z, j, NH, E.OM0) for j in F.chars(NH)])) ** 2, axis=1))
        V = np.array([P.vals(NH, p) / nH for p in P.fixed_points()])
        u, s, vh = np.linalg.svd(V)
        K = vh[np.sum(s > 1e-9 * s[0]):].conj().T
        qH, UH = charge_basis(E.rho_matrix(NH))
        rec = dict(protected_dim=K.shape[1], charge_multiplicities=[int((qH == c).sum()) for c in range(3)])
        S, _ = np.linalg.qr(UH[:, qH == 2])
        rec["distance_to_charge2_sector"] = float(np.linalg.norm(K @ K.conj().T - S @ S.conj().T)) if S.shape[1] == K.shape[1] else None
        if N is not None:
            qg, Ug = charge_basis(E.rho_matrix(N))           # generation charge basis (coefficient space)
            T0 = P.tensor(N, N, NH, E.OM0)
            forb, dev = 0.0, 0.0
            for _ in range(6):
                c = S @ (rng.normal(size=S.shape[1]) + 1j * rng.normal(size=S.shape[1]))
                Y = np.tensordot(c.conj(), T0, 1)
                Yc = Ug.T @ Y @ Ug                                # Yukawa in the generation charge basis
                allowed = np.array([[(qg[a] + qg[b]) % 3 == 2 for b in range(3)] for a in range(3)])
                forb = max(forb, float(np.max(abs(Yc[~allowed])) / np.max(abs(Yc))))
                sv = np.linalg.svd(Y, compute_uv=False)
                dev = max(dev, float(abs(1 - sv[1] / sv[0]) + sv[2] / sv[0]))
            rec.update(generation_charges=sorted(int(x) for x in qg), forbidden_entries_max=forb, spectrum_dev_from_110=dev)
        res[name] = rec
    res["checks"] = {k: bool(v) for k, v in dict(
        protected_equals_charge2_up=res["up"]["distance_to_charge2_sector"] is not None and res["up"]["distance_to_charge2_sector"] < 1e-9,
        protected_equals_charge2_weinberg=res["weinberg"]["distance_to_charge2_sector"] is not None and res["weinberg"]["distance_to_charge2_sector"] < 1e-9,
        down_protected_not_a_charge_sector=res["down"]["protected_dim"] == 7,
        generations_002=res["up"]["generation_charges"] == [0, 0, 2] and res["weinberg"]["generation_charges"] == [0, 0, 2],
        only_02_pairs_couple=max(res["up"]["forbidden_entries_max"], res["weinberg"]["forbidden_entries_max"]) < 1e-9,
        spectrum_110=max(res["up"]["spectrum_dev_from_110"], res["weinberg"]["spectrum_dev_from_110"]) < 1e-9,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
