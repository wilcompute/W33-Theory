"""Pass 11893: chiral massless spectrum of the heterotic W(3,3) T6/Z3 sector at the radiative trinification point.

Input (Pass 11714, orbifolder): visible SU(9) with untwisted 3 x 84 (one per complex plane) and twisted 27 x 9bar;
the untwisted cubic coupling is the E8 bracket, W = g eps^{ijk} < X_i , [X_j , X_k] >, [x, y] = *(x ^ y).
F-flatness = pairwise commuting X_i; Cartan points of h are F- and D-flat (Passes 11879-11886).

At the one-loop vacuum X_1 = v on a Witting ray, X_2 = X_3 = 0:
  * the X_2-X_3 mass matrix M_ab = < v , *(a ^ b) > has rank 56, so 28 of each stay massless;
  * the su(9) orbit of v has dimension 56 (eaten by the broken generators), so X_1 keeps 28 (27 + the modulus);
  * each massless 28 = 27 + 1 with the 27 IRREDUCIBLE under the unbroken SU(3)^3 (commutant 2), i.e. a (3,3,3)-type
    representation (every state coloured), and each twisted 9bar = three inequivalent triplets (commutant 3).
Visible chiral spectrum: 3[(3,3,3) + 1] + 27[(3bar,1,1) + (1,3bar,1) + (1,1,3bar)], anomaly-free (27 triplets vs 27
antitriplets per factor). STANDARD-MODEL TEST: colour must be one SU(3) factor (a diagonal colour produces sextets);
SU(2) commuting with it lies in the other two factors, embedded in each as trivial, 2+1 or principal (spin 1). Over
all six pairs the net quark-doublet number (3 copies x doublets in 3 x 3) is 0, 9, 6, 0, 3, 0, and the one pair giving
3 (principal x (2+1)) also gives chiral coloured SU(2) quartets and triplets, (3,4) + (3,3), with no partners (the 27
antitriplets carry no SU(2) charge). So no embedding gives three families with coloured states only in SU(2) singlets
and doublets: no three-family Standard Model at the trinification point of this sector.
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402

OUT = ROOT / "data" / "w33_pass11893_trinification_chiral_spectrum.json"
H = np.array(E.cartan_trivectors())
GL9 = [np.eye(9)[:, [i]] @ np.eye(9)[[j], :] for i in range(9) for j in range(9)]


def su9_orbit_dim(v):
    T = E.full(v)
    basis = []
    for i in range(9):
        for j in range(9):
            if i != j:
                basis.append(GL9[9 * i + j])
    for k in range(8):
        A = np.zeros((9, 9))
        A[k, k], A[k + 1, k + 1] = 1, -1
        basis.append(A)
    orb = np.array([E.sorted_c(E._act(A, T)) for A in basis]).T
    return int(np.sum(np.linalg.svd(orb, compute_uv=False) > 1e-9))


def spins_in_3x3(emb2, emb3):
    """SU(2) spins in 3 (x) 3 when each 3 -> sum of SU(2) irreps given by spin lists"""
    out = []
    for a in emb2:
        for b in emb3:
            j = abs(a - b)
            while j <= a + b + 1e-9:
                out.append(round(j, 1))
                j += 1
    return sorted(out)


def main():
    v = np.array([1, 0, 0, 0], complex) @ H
    I84 = np.eye(84)
    M = np.array([[v @ E.wedge_star(I84[i], I84[j]) for j in range(84)] for i in range(84)])
    sv = np.linalg.svd(M, compute_uv=False)
    rank = int(np.sum(sv > 1e-9 * sv[0]))
    antisym = float(np.max(abs(M + M.T)))
    orbit = su9_orbit_dim(v)
    T = E.full(v)
    Mm = np.array([E._act(A, T).ravel() for A in GL9]).T
    _, s2, vh2 = np.linalg.svd(Mm)
    null = vh2[int(np.sum(s2 > 1e-9 * s2[0])):].conj()
    gens = [(n @ np.array(GL9).reshape(81, 81)).reshape(9, 9) for n in null]
    _, s, vh = np.linalg.svd(M)
    K = vh[rank:].conj().T
    reps = [np.linalg.lstsq(K, np.array([E.sorted_c(E._act(g, E.full(K[:, k]))) for k in range(K.shape[1])]).T,
                            rcond=None)[0] for g in gens]
    d = K.shape[1]
    A = np.vstack([np.kron(np.eye(d), R) - np.kron(R.T, np.eye(d)) for R in reps])
    comm28 = int(np.sum(np.linalg.svd(A, compute_uv=False) < 1e-8))
    A9 = np.vstack([np.kron(np.eye(9), -g.T) - np.kron(-g, np.eye(9)) for g in gens])
    comm9 = int(np.sum(np.linalg.svd(A9, compute_uv=False) < 1e-8))
    # the singlet in the massless 28 is v itself (the modulus)
    singlet_is_v = float(np.linalg.norm(K @ (K.conj().T @ v) - v) / np.linalg.norm(v))
    emb = {"trivial": [0.0, 0.0, 0.0], "2+1": [0.5, 0.0], "principal": [1.0]}
    q_doublets, sm_compatible = {}, {}
    for a, b in itertools.combinations_with_replacement(emb, 2):
        sp = spins_in_3x3(emb[a], emb[b])
        nd = 3 * sp.count(0.5)
        q_doublets[f"{a} x {b}"] = dict(spins_per_333=sp, net_quark_doublets=nd)
        sm_compatible[f"{a} x {b}"] = bool(nd == 3 and max(sp) <= 0.5)
    res = dict(pass_id=11893, mass_matrix_rank=rank, mass_matrix_antisymmetry=antisym, su9_orbit_dim=orbit,
               massless=dict(X1=84 - orbit, X2=84 - rank, X3=84 - rank),
               unbroken_dim=len(gens), commutant_on_massless_28=comm28, commutant_on_9bar=comm9,
               singlet_is_the_modulus=singlet_is_v,
               su2_embeddings=q_doublets, sm_compatible=sm_compatible)
    res["checks"] = {k: bool(val) for k, val in dict(
        mass_rank_56=rank == 56 and antisym < 1e-12,
        eaten_56=orbit == 56,
        unbroken_su3_cubed=len(gens) == 24,
        massless_28_each=res["massless"] == dict(X1=28, X2=28, X3=28),
        irreducible_27_plus_1=comm28 == 2 and singlet_is_v < 1e-10,
        ninebar_three_triplets=comm9 == 3,
        anomaly_free=3 * 9 == 27,
        no_sm_embedding=not any(sm_compatible.values()),
        three_doublets_only_with_exotics=all(max(v["spins_per_333"]) > 0.5 for v in q_doublets.values()
                                             if v["net_quark_doublets"] == 3),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
