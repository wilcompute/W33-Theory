"""Pass 11930: the fixed-point-avoiding Higgs at the Eisenstein point realises the theta-zero law, and in the Weinberg
channel it is an inverted neutrino spectrum with an almost massless nu_3.

Setting: magnetized SU(5) on T4 with the A2 dual pair at Omega = w.1 (Pass 11928). The 9 rho-fixed points of
T4/Z3 form a W(3,3) line; a blow-up modulus at a fixed point p gives a localised mass proportional to the coherent
projector |psi^H(p)><psi^H(p)|. Higgs modes vanishing at all 9 fixed points are untouched by every blow-up, whatever
the blow-up sizes: if the localised masses are positive, they are the light Higgs directions (an assumption, stated).

1. Up channel (Higgs flux 2A2, 12 modes) and Weinberg channel (Higgs-pair flux 2A2', L.L, 12 modes): the fixed-point
   value matrix has rank 8, so the fixed-point-avoiding space is 4-dimensional, and it is pure rho-charge 2.
2. EVERY Higgs in that space gives the Yukawa spectrum (1, 1, 0) exactly at Omega = w (checked on random combinations):
   the theta-zero law of Pass 11904 (massless lightest, degenerate pair), i.e. the strange-state class of Pass 11925.
3. Near the point, Omega = w + eps(a + bJ): 1 - s2/s1 ~ eps (slope 1) and s3/s1 ~ eps^2 (slope 2).
4. Down channel (H_d flux 4.1, 16 modes): fixed-point rank 9, a 7-dim avoiding space of mixed charges with generic O(1)
   spectra -- no structure.
Reading: for up quarks the pattern is wrong (top = charm), so the up Higgs cannot be this mode. In the Weinberg
channel it is an INVERTED ordering with a quasi-degenerate pair split linearly in eps (the solar splitting) and
m_3/m_1 ~ eps^2: matching Dm2_21/|Dm2_32| ~ 0.03 fixes eps ~ 0.02-0.05 and gives m_3 ~ 3e-4 - 2e-3 m_1 (~2e-5 - 1e-4 eV).
This is conditional on the Weinberg mediator being the blow-up-protected mode; normal ordering is mildly preferred by
current global fits, so the reading is falsifiable (JUNO, DUNE, 0nu-beta-beta at m_bb ~ 15-50 meV).
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11928_eisenstein_point as E  # noqa: E402

OUT = ROOT / "data" / "w33_pass11930_fixed_point_avoiding_higgs.json"
J = E.J
A2, A2M = [[2, 1], [1, 2]], [[2, -1], [-1, 2]]


def fixed_points():
    rot = lambda p: ((-p[2]) % 3, (-p[3]) % 3, (p[0] - p[2]) % 3, (p[1] - p[3]) % 3)
    return [p for p in itertools.product(range(3), repeat=4) if rot(p) == p]


def vals(N, p):
    x, y = np.array(p[:2]) / 3, np.array(p[2:]) / 3
    z = (x + E.OM0 @ y)[None, :]
    return np.array([F.psi_at(z, j, N, E.OM0)[0] for j in F.chars(N)])


def tensor(N1, N2, NH, Om, G=14):
    z = E.zgrid(Om, G)
    A, B, H = E.modes(N1, Om, z), E.modes(N2, Om, z), E.modes(NH, Om, z)
    return np.einsum("ap,bp,hp->hab", A, B, np.conj(H)) / z.shape[0]


def study(N1, N2, NH, rng, ntest=6):
    z = E.zgrid(E.OM0, 16)
    nH = np.sqrt(np.mean(abs(np.array([F.psi_at(z, j, NH, E.OM0) for j in F.chars(NH)])) ** 2, axis=1))
    V = np.array([vals(NH, p) / nH for p in fixed_points()])
    u, s, vh = np.linalg.svd(V)
    r = int(np.sum(s > 1e-9 * s[0]))
    K = vh[r:].conj().T
    RH = E.rho_matrix(NH)
    ch = sorted(int(round(np.angle(x) / (2 * np.pi / 3))) % 3 for x in np.linalg.eigvals(K.conj().T @ RH @ K))
    T0 = tensor(N1, N2, NH, E.OM0)
    Te = {e: tensor(N1, N2, NH, E.OM0 + e * (np.eye(2) + (0.4 + 0.3j) * J)) for e in (1e-2, 1e-3)}
    at_w, near = [], []
    for _ in range(ntest):
        c = K @ (rng.normal(size=K.shape[1]) + 1j * rng.normal(size=K.shape[1]))
        c /= np.linalg.norm(c)
        sv = np.linalg.svd(np.tensordot(c.conj(), T0, 1), compute_uv=False)
        at_w.append((float(1 - sv[1] / sv[0]), float(sv[2] / sv[0])))
        row = []
        for e in (1e-2, 1e-3):
            sv = np.linalg.svd(np.tensordot(c.conj(), Te[e], 1), compute_uv=False)
            row.append((float(1 - sv[1] / sv[0]), float(sv[2] / sv[0])))
        near.append(dict(split=[row[0][0], row[1][0]], light=[row[0][1], row[1][1]],
                         slope_split=float(np.log10(row[0][0] / row[1][0])), slope_light=float(np.log10(row[0][1] / row[1][1])),
                         a=float(row[1][0] / 1e-3), b=float(row[1][1] / 1e-6)))
    return dict(modes=V.shape[1], fixed_point_rank=r, avoiding_dim=K.shape[1], charges=ch, at_w=at_w, near=near)


def main():
    F.NS = np.array([(a, b) for a in range(-7, 8) for b in range(-7, 8)])
    rng = np.random.default_rng(11930)
    up = study(A2, A2, [[4, 2], [2, 4]], rng)
    nu = study(A2M, A2M, [[4, -2], [-2, 4]], rng)
    dn = study(A2, A2M, [[4, 0], [0, 4]], rng, ntest=3)
    res = dict(pass_id=11930, fixed_points=len(fixed_points()), up=up, weinberg=nu, down=dn)
    # neutrino reading: inverted ordering, Dm2_21/|Dm2_32| = 0.0305 ~ 2 delta with delta = 1 - m2/m1 = a eps
    ratio = 7.42e-5 / 2.43e-3
    eps_fit = [ratio / 2 / x["a"] for x in nu["near"]]
    m3_over_m1 = [x["b"] * e ** 2 for x, e in zip(nu["near"], eps_fit)]
    res["neutrino_reading"] = dict(dm2_ratio=ratio, eps_fit=eps_fit, m3_over_m1=m3_over_m1,
                                   m3_eV_for_m1_0p05=[0.05 * m for m in m3_over_m1])
    res["checks"] = {k: bool(v) for k, v in dict(
        nine_fixed_points=res["fixed_points"] == 9,
        up_and_weinberg_avoiding_space_4dim_charge2=all(c["fixed_point_rank"] == 8 and c["avoiding_dim"] == 4 and c["charges"] == [2, 2, 2, 2]
                                                       for c in (up, nu)),
        theta_zero_law_exact_at_w=all(max(max(a, b) for a, b in c["at_w"]) < 1e-9 for c in (up, nu)),
        split_linear_light_quadratic=all(all(abs(x["slope_split"] - 1) < 0.1 and abs(x["slope_light"] - 2) < 0.1 for x in c["near"]) for c in (up, nu)),
        down_channel_generic=dn["avoiding_dim"] == 7 and min(b for a, b in dn["at_w"]) > 0.05,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    print(json.dumps(res["checks"], indent=1), res["all_checks_pass"])
    print("eps_fit", np.round(eps_fit, 4), " m3/m1", ["%.1e" % m for m in m3_over_m1])


if __name__ == "__main__":
    main()
