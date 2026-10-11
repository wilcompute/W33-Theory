"""Pass 11900: three generations over a point of W(3,3).

Passes 11897-11898: the Kahler moduli of two Z3 tori act on the nine twisted fixed points through the two-qutrit Weil
representation (Sp(4,3) = Aut W(3,3)). Three-generation Z3 models need Wilson lines on two of the three tori, leaving one
Wilson-line-free (family) torus (Pass 11105; Ibanez-Kim-Nilles-Quevedo). Restrict to the family torus 1 and a Wilson-line
torus 2:

  * The Wilson line on torus 2 labels fixed points by f2 through the holonomy operator Z2 (Z2|f> = w^{f2}|f>): a
    nontrivial Pauli, i.e. a POINT p of W(3,3). The duality transformations compatible with it are the centraliser of
    Z2: linear order 1296, projective 648 = the W(3,3) point stabiliser (corpus: 2026-09-21 Clifford-648 bridge).
  * The families are the three Z2 eigenspaces (fixed f2, varying f1): each is one qutrit, p-perp / p.
  * On the Wilson-line-NEUTRAL class (f2 = 0) the residual Kahler dualities act as T' only (projective 24); the space-
    group Delta(54) is needed to complete the one-qutrit Clifford group. On the two CHARGED classes the dualities alone
    already generate the full one-qutrit Clifford group (projective 216): the GL(2,Z[w]) transvection restricts to the
    shift X1^{a} and the off-diagonal B-shift (gate w^{2 f1 f2}) to the clock Z1^{2a}. The "traditional" flavour group of
    the families is the shadow of the entangling (off-diagonal) Kahler dualities.
  * Yukawa consequence. With families on torus 1 and left/right fields in Wilson-line classes differing by a, the
    renormalisable twisted mass spectrum is (theta_(0,a), theta_(1,a), theta_(2,a)) up to the other tori. For a = 0 the
    light pair is degenerate EXACTLY, for all moduli (theta even: theta_(2,0) = theta_(1,0)); for a != 0 it is degenerate
    at diagonal moduli and split at THIRD order by the off-diagonal Kahler modulus: each torus's Z3 rotation fixes its
    cosets (w = 1 mod sqrt(-3)) and the splitting is odd under f1 -> -f1, so the first allowed term is (x1bar x2)^3,
    i.e. Z12^3 (measured: split / s^3 constant). Mixing is still absent at this level
    (diagonal selection rule; Casas-Gomez-Munoz, Abel-Munoz).
"""

import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11897_11898_kahler_moduli_two_qutrit_weil as K  # noqa: E402

OUT = ROOT / "data" / "w33_pass11900_three_generations_over_a_w33_point.json"
W = np.exp(2j * np.pi / 3)


def key(M, proj):
    if proj:
        v = M.ravel()
        k = np.flatnonzero(abs(v) > 1e-6)[0]
        M = M * abs(v[k]) / v[k]
    return (np.round(M, 4) + 0).tobytes()


def closure(G, proj):
    I = np.eye(G[0].shape[0], dtype=complex)
    seen = {key(I, proj): I}
    q = deque([I])
    while q:
        x = q.popleft()
        for g in G:
            y = g @ x
            k = key(y, proj)
            if k not in seen:
                seen[k] = y
                q.append(y)
    return seen


def main():
    rng = np.random.default_rng(11900)
    G9 = np.array(K.closure(list(K.GENS.values()), False))
    Z2 = K.PAULIS[((0, 0), (0, 1))]
    X1 = K.PAULIS[((1, 0), (0, 0))]
    Z1 = K.PAULIS[((0, 0), (1, 0))]
    C = [g for g in G9 if np.allclose(g @ Z2, Z2 @ g, atol=1e-9)]
    proj_C = len({key(g, True) for g in C})
    cls = [[K.IDX[(f1, a)] for f1 in range(3)] for a in range(3)]
    leak = float(max(np.max(abs(np.delete(g[:, cls[a]], cls[a], axis=0))) for g in C for a in range(3)))
    images = {}
    for a in range(3):
        I = cls[a]
        mod = list({key(g[np.ix_(I, I)], False): g[np.ix_(I, I)] for g in C}.values())
        full = mod + [X1[np.ix_(I, I)], Z1[np.ix_(I, I)]]
        images[a] = dict(modular_linear=len(closure(mod, False)), modular_projective=len(closure(mod, True)),
                         with_space_group_projective=len(closure(full, True)))
    # explicit restriction identities on class a
    U = K.GENS["U"]  # (f1, f2) -> (f1 + f2, f2)
    Toff = K.GENS["Toff"]  # w^{2 f1 f2}
    ident = {}
    for a in range(3):
        I = cls[a]
        x1, z1 = X1[np.ix_(I, I)], Z1[np.ix_(I, I)]
        ident[a] = dict(transvection_is_X1a=float(np.max(abs(U[np.ix_(I, I)] - np.linalg.matrix_power(x1, a)))),
                        offdiag_B_is_Z1_2a=float(np.max(abs(Toff[np.ix_(I, I)] - np.linalg.matrix_power(z1, 2 * a)))))
    # Yukawa degeneracy
    O = K.lattice(7)
    deg = []
    for _ in range(4):
        Z = K.rand_Z(rng)
        t = K.theta2(Z, O)
        th = {(c, a): t[K.IDX[(c, a)]] for c in range(3) for a in range(3)}
        deg.append(dict(neutral=float(abs(th[(1, 0)] - th[(2, 0)]) / abs(th[(1, 0)])),
                        charged=float(abs(th[(1, 1)] - th[(2, 1)]) / abs(th[(1, 1)]))))
    Zd = K.rand_Z(rng)
    Zd[0, 1] = Zd[1, 0] = 0
    td = K.theta2(Zd, O)
    diag_split = float(abs(td[K.IDX[(1, 1)]] - td[K.IDX[(2, 1)]]) / abs(td[K.IDX[(1, 1)]]))
    lin = []
    D = rng.normal(size=2) + 1j * rng.normal(size=2)
    for s in (1e-2, 5e-3, 2.5e-3):
        Zs = Zd.copy()
        Zs[0, 1], Zs[1, 0] = s * D[0], s * D[1]
        ts = K.theta2(Zs, O)
        lin.append(float(abs(ts[K.IDX[(1, 1)]] - ts[K.IDX[(2, 1)]]) / abs(ts[K.IDX[(1, 1)]]) / s**3))
    res = dict(pass_id=11900, centraliser_linear=len(C), centraliser_projective=proj_C, class_leak=leak,
               class_images={str(k): v for k, v in images.items()},
               restriction_identities={str(k): v for k, v in ident.items()}, yukawa_degeneracy=deg,
               diagonal_moduli_charged_split=diag_split, split_over_offdiag_cubed=lin)
    res["checks"] = {k: bool(v) for k, v in dict(
        centraliser_is_point_stabiliser=len(C) == 1296 and proj_C == 648,
        classes_preserved=leak < 1e-12,
        neutral_class_only_T_prime=images[0]["modular_projective"] == 24,
        charged_classes_full_clifford=images[1]["modular_projective"] == 216 and images[2]["modular_projective"] == 216,
        all_classes_clifford_with_space_group=all(images[a]["with_space_group_projective"] == 216 for a in range(3)),
        transvection_and_B_restrict_to_paulis=all(max(v.values()) < 1e-12 for v in ident.values()),
        neutral_light_pair_exactly_degenerate=max(d["neutral"] for d in deg) < 1e-12,
        charged_light_pair_split=min(d["charged"] for d in deg) > 1e-4,
        degenerate_at_diagonal_moduli=diag_split < 1e-12,
        split_cubic_in_offdiag=max(lin) / min(lin) < 1.05 and min(lin) > 1e-3,
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
