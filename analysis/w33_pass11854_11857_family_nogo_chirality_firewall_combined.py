"""Passes 11854, 11855, 11857: family no-go, chirality firewall, and one finite group (spinorial Lorentz + central Z3).

11854  Three generations as an exact family SU(3).  Inside E8 > SU(5)_L x SU(5)_GUT (Passes 11845, 11849) take the family
       su(3) as the upper-left sl3 of su(5)_L.  The centraliser of su(5)_GUT + su(3)_fam (and of SM + su(3)_fam) is
       computed.  With C_E8(SU(5)_GUT) = SU(5)_L connected, a finite Lorentz group commuting with GUT and family lies in
       C_SU(5)_L(SU(3)) = U(2); A6 and SL(2,9) have no nontrivial homomorphism to U(2).
11855  Chirality firewall.  Every automorphism commuting with the spinorial Lorentz group SL(2,9) acts on Di by a scalar
       (Schur) inside Sp(4), hence by +-1; on (32, Di) its fixed space is V_{+-1}(32) x Di.  The so(11) spinor 32 is
       quaternionic, its quaternionic structure J commutes with Spin(11) and preserves real eigenspaces, so every
       kept spectrum is self-conjugate: vector-like.  Verified in an explicit Spin(11) Clifford model over many finite-
       order elements (16 versus 16bar content via the Spin(10) chirality), with the Lorentz-breaking contrast
       (a phase i on Di) that does produce chirality.
11857  One finite group.  The commutant of <spinorial SL(2,9) lift, central Z3 translation t_c>.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11843_e8_tits_lorentz_commutant as T  # noqa: E402
import w33_pass11844_11846_e8_poincare_lifts_matter as L  # noqa: E402
import w33_pass11849_11851_spinor_lorentz_central_z3_generations as M  # noqa: E402

OUT = ROOT / "data" / "w33_pass11854_11857_family_nogo_chirality_firewall_combined.json"
N = T.N


def analyse_any(B, Bs, rng):
    return L.analyse_complex(B, Bs, rng) if Bs.shape[1] else dict(dim=0)


# ---------------------------------------------------------------- 11855 Clifford model
def gamma_matrices(n):
    """Euclidean gamma matrices for Cl(n), n odd = 2m+1, dimension 2^m (Jordan-Wigner); last = normalised volume."""
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]], complex)
    sz = np.array([[1, 0], [0, -1]], complex)
    I2 = np.eye(2)
    m = (n - 1) // 2
    gs = []
    for k in range(m):
        for s in (sx, sy):
            mats = [sz] * k + [s] + [I2] * (m - k - 1)
            g = mats[0]
            for x in mats[1:]:
                g = np.kron(g, x)
            gs.append(g)
    vol = gs[0]
    for g in gs[1:]:
        vol = vol @ g
    c = 1.0 if np.allclose(vol @ vol, np.eye(2**m)) else 1j
    gs.append(c * vol)
    for a in range(n):
        for b in range(n):
            assert np.allclose(gs[a] @ gs[b] + gs[b] @ gs[a], 2 * (a == b) * np.eye(2**m))
    return gs


def chirality_firewall(rng, trials=200):
    gs = gamma_matrices(11)
    D = 32
    gens = [gs[a] @ gs[b] / 2 for a, b in itertools.combinations(range(11), 2)]
    # antilinear J = C K commuting with Spin(11):  C conj(S) = S C  <=>  (I (x) S^dag - S (x) I) vec_r(C) = 0
    Mn = np.zeros((D * D, D * D), complex)
    for S in gens:
        K = np.kron(np.eye(D), S.conj().T) - np.kron(S, np.eye(D))
        Mn += K.conj().T @ K
    w0, U0 = np.linalg.eigh(Mn)
    assert w0[0] < 1e-8 and w0[1] > 1e-6  # one-dimensional commutant (Schur)
    Cs = U0[:, 0].reshape(D, D)
    Cs = Cs / np.sqrt(abs((Cs @ Cs.conj().T)[0, 0]))
    JJ = Cs @ Cs.conj()
    quaternionic = bool(np.allclose(JJ, JJ[0, 0] * np.eye(D)) and np.real(JJ[0, 0]) < 0)
    commutes = bool(all(np.allclose(Cs @ S.conj(), S @ Cs, atol=1e-8) for S in gens))
    vectorlike_all, worst, nonempty = True, 0.0, 0
    for _ in range(trials):
        k = int(rng.integers(2, 9))
        R = np.linalg.qr(rng.normal(size=(11, 11)))[0]
        rot = [sum(R[a, i] * gs[i] for i in range(11)) for a in range(11)]
        h = sum(int(rng.integers(-3, 4)) * rot[2 * j] @ rot[2 * j + 1] / 2 for j in range(5))
        g = expm(2 * np.pi * h / k)
        for sign in (1, -1):  # the element acts on Di by sign (Schur + Sp(4))
            w, V = np.linalg.eig(g)
            keep = V[:, np.isclose(w, sign, atol=1e-7)]
            if keep.shape[1]:
                nonempty += 1
                Jkeep = Cs @ keep.conj()
                P = keep @ np.linalg.pinv(keep)
                err = float(abs(P @ Jkeep - Jkeep).max())
                worst = max(worst, err)
                vectorlike_all &= err < 1e-6
    # contrast: omega = gamma_1...gamma_10 lies in Spin(10) < Spin(11), omega^2 = -1, +-i on 16 / 16bar.
    omega = gs[0]
    for g in gs[1:10]:
        omega = omega @ g
    assert np.allclose(omega @ omega, -np.eye(D))
    chir = 1j * omega  # +-1 on 16 / 16bar
    w, V = np.linalg.eig(omega)
    out = {}
    for name, di_phase in (("lorentz_commuting_+1", 1), ("lorentz_commuting_-1", -1), ("lorentz_breaking_i", 1j), ("lorentz_breaking_-i", -1j)):
        keep = V[:, np.isclose(w * di_phase, 1, atol=1e-7)]
        net = float(np.real(np.trace(np.linalg.pinv(keep) @ chir @ keep))) if keep.shape[1] else 0.0
        out[name] = dict(kept_dim_in_32=int(keep.shape[1]), net_16_minus_16bar=round(net, 6))
    return dict(spinor_dim=D, quaternionic_structure=quaternionic, J_commutes_with_spin11=commutes, trials=trials,
                nonempty_kept_spaces=nonempty, all_kept_spaces_J_invariant=bool(vectorlike_all), worst_J_error=worst,
                spin10_volume_projection=out)


# ---------------------------------------------------------------- main (E8 parts)
def main():
    rng = np.random.default_rng(11854)
    B, sub = L.setup(rng)
    chain = sub["chain"]
    tits = [T.tits(B, b) for b in chain]
    adj_gens = [tits[i] @ tits[i + 1] for i in range(4)]
    C_gut = T.fixed_subalgebra(adj_gens)
    C_L = M.centraliser(B, C_gut)
    phi, herr, _ = M.chevalley_sl5(B, C_L, rng)
    res = {"pass_ids": [11854, 11855, 11857], "sl5_homomorphism_error": herr}
    # ---- 11854: family su(3) = upper-left sl3 of su(5)_L
    fam = []
    for i in range(3):
        for j in range(3):
            if i != j:
                X = np.zeros((5, 5))
                X[i, j] = 1
                fam.append(phi(X))
    for i in range(2):
        X = np.zeros((5, 5))
        X[i, i], X[i + 1, i + 1] = 1, -1
        fam.append(phi(X))
    fam = np.column_stack(fam)
    c1 = M.centraliser(B, np.hstack([C_gut, fam]))
    res["centraliser_gut_plus_family"] = analyse_any(B, c1, rng)
    # SM + family: SM = commutant of <A6, t_c> (Pass 11850)
    Gmod3 = L.weyl_mod3(chain)
    subs = L.submodules(Gmod3)
    W5 = next(s for s in subs if len(s) == 5)
    c = next(v for v in L.span_vectors(W5) if any(v) and all(T.ip(v, w) % 3 == 0 for w in W5))
    tc = L.torus_order3(np.array(c))
    C_sm = T.fixed_subalgebra(adj_gens + [tc])
    c2 = M.centraliser(B, np.hstack([C_sm, fam]))
    res["centraliser_sm_plus_family"] = analyse_any(B, c2, rng)
    print("11854", res["centraliser_gut_plus_family"], res["centraliser_sm_plus_family"], flush=True)
    # ---- 11857: spinorial lift + central Z3
    gens4, minus4, fs, order, *_ = M.di_generators(rng)

    def auto(D):
        g5 = np.eye(5, dtype=complex)
        g5[:4, :4] = D
        return expm(T.ad(B, phi(M.log_su(g5))))
    A = [auto(D) for D in gens4]
    commute = [float(abs(a @ tc - tc @ a).max()) for a in A]
    C_spin = M.fixed_c(A)
    C_both = M.fixed_c(A + [tc])
    both = analyse_any(B, C_both, rng)
    both["contains_su3_A2"] = L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A2"]]), C_both)
    both["contains_su2_alpha"] = L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A1"]]), C_both)
    both["inside_SM_of_11850"] = L.basis_contains(C_both, C_sm)
    # ideal structure: centraliser of su(2)_alpha inside the commutant, and its derived algebra
    su2a = np.column_stack([T.vec_root(r) for r in sub["A1"]] + [np.concatenate([np.array(sub["A1"][0], float), np.zeros(240)])])
    cz = M.centraliser(B, su2a)
    inter = M.nullspace(np.hstack([C_both, -cz]))
    K = C_both @ inter[:C_both.shape[1]]
    q_, r_ = np.linalg.qr(K)
    K = q_[:, np.abs(np.diag(r_)) > 1e-8]
    kinfo = analyse_any(B, K, rng)
    kinfo["contains_su3_A2"] = L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A2"]]), K)
    both["centraliser_of_su2_alpha_inside"] = kinfo
    # centraliser of su(3)_A2 inside the commutant: expected so(5) + u(1) (dim 11, derived 10, rank 3)
    su3 = np.column_stack([T.vec_root(r) for r in sub["A2"]] + [np.concatenate([np.array(r, float), np.zeros(240)]) for r in sub["A2"][:2]])
    c3_ = M.centraliser(B, su3)
    inter3 = M.nullspace(np.hstack([C_both, -c3_]))
    K3 = C_both @ inter3[:C_both.shape[1]]
    q3, r3 = np.linalg.qr(K3)
    K3 = q3[:, np.abs(np.diag(r3)) > 1e-8]
    k3 = analyse_any(B, K3, rng)
    k3["contains_su2_alpha"] = L.basis_contains(np.column_stack([T.vec_root(r) for r in sub["A1"]]), K3)
    both["centraliser_of_su3_inside"] = k3
    both["structure_su3_u1_so5"] = bool(both["dim"] == 19 and k3["dim"] == 11 and k3["derived_dim"] == 10 and k3["rank"] == 3)
    res["combined"] = dict(tc_commutes_with_spinor_lift=commute, so11_dim=int(C_spin.shape[1]), commutant=both)
    print("11857", res["combined"], flush=True)
    # ---- 11855: chirality firewall (Clifford model)
    res["chirality_firewall"] = chirality_firewall(rng)
    print("11855", res["chirality_firewall"], flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
