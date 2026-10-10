"""Passes 11887-11889: inside E8, the one-loop trinification vacuum is E6 x U(1)^2_family at a W(3,3) point.

Pass 11884-11886: SU(9) + 84 (the Z3-twisted half of E8) has its one-loop vacuum at the 40 Witting rays of the Vinberg
Cartan h, where SU(9) -> SU(3)^3. Here the same vev x is viewed as an element of e8 = sl9 + Lambda^3 + Lambda^6
(Pass 11681 bracket).

  * 11887 E6. The centraliser of x in e8 is 80-dimensional with Z3-grade dimensions (24, 28, 28); its derived algebra
    is 78-dimensional and acts irreducibly on a 27-dimensional weight space (so it is e6, not so(13) or sp(12)), and
    its centre is 2-dimensional: z(x) = e6 + u(1)^2, whose grade-0 part is SU(3)^3. A generic Cartan vev has the
    8-dimensional centraliser of a Cartan subalgebra, grades (0, 4, 4).
  * 11888 THREE FAMILIES. Under z(x), 248 = 80 + six 27-dimensional U(1)^2 weight spaces + six singlets. Three of the
    27 weights sum to zero (the weights of a 3 of SU(3)), the other three are their negatives (27bar), and the singlet
    weights are their differences (the six roots of A2): 248 = (78,1)+(1,8)+(27,3)+(27bar,3bar) with the family SU(3)
    broken to its Cartan by the vev.
  * 11889 THE W(3,3) POINT. For every one of the 40 Witting rays, exactly one W(3,3) point P has a Pauli operator fixing
    all of z(x); its fixed algebra is 86-dimensional (E6 + A2, the Pauli centraliser of a point, Pass 11687), and the
    map ray -> point is a bijection 40 <-> 40. So the one-loop vacuum IS a W(3,3) point: E6 x SU(3)_family with the Higgs
    vev in the family Cartan.
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11681_e8_from_two_qutrits as E  # noqa: E402
from w33_pass11879_11883_e8_higgs_siegel_modulus import witting_rays  # noqa: E402

OUT = ROOT / "data" / "w33_pass11887_11889_e6_family_at_w33_point.json"
H = np.array(E.cartan_trivectors())
Z84 = np.zeros(84, complex)


def e8_basis():
    B = []
    for i in range(9):
        for j in range(9):
            if i != j:
                A = np.zeros((9, 9), complex)
                A[i, j] = 1
                B.append((A, Z84.copy(), Z84.copy()))
    for k in range(8):
        A = np.zeros((9, 9), complex)
        A[k, k], A[k + 1, k + 1] = 1, -1
        B.append((A, Z84.copy(), Z84.copy()))
    for i in range(84):
        v = Z84.copy()
        v[i] = 1
        B.append((np.zeros((9, 9), complex), v, Z84.copy()))
    for i in range(84):
        v = Z84.copy()
        v[i] = 1
        B.append((np.zeros((9, 9), complex), Z84.copy(), v))
    return B


BASIS = e8_basis()
FULLM = np.array([E._vec(b) for b in BASIS]).T


def to_el(v):
    A = np.zeros((9, 9), complex)
    idx = 0
    for i in range(9):
        for j in range(9):
            if i != j:
                A[i, j] = v[idx]
                idx += 1
    for k in range(8):
        A[k, k] += v[idx]
        A[k + 1, k + 1] -= v[idx]
        idx += 1
    return (A, v[80:164], v[164:])


def centraliser(el):
    M = np.array([E._vec(E.bracket(el, b)) for b in BASIS]).T
    _, s, vh = np.linalg.svd(M)
    k = int(np.sum(s < 1e-9 * s[0]))
    return vh[len(s) - k:].conj() if k else np.zeros((0, 248))


def rank(m, tol=1e-8):
    return int(np.sum(np.linalg.svd(m, compute_uv=False) > tol)) if m.size else 0


def ad(el):
    return np.linalg.lstsq(FULLM, np.array([E._vec(E.bracket(el, b)) for b in BASIS]).T, rcond=None)[0]


def ray_element(c):
    return (np.zeros((9, 9), complex), np.asarray(c, complex) @ H, Z84.copy())


def part_e6(rng):
    out = {}
    for name, c in (("witting_e0", [1, 0, 0, 0]), ("generic", rng.normal(size=4) + 1j * rng.normal(size=4))):
        null = centraliser(ray_element(c))
        out[name] = dict(dim=int(null.shape[0]), grades=[rank(null[:, :80]), rank(null[:, 80:164]), rank(null[:, 164:])])
    null = centraliser(ray_element([1, 0, 0, 0]))
    Zel = [to_el(n) for n in null]
    Zm = np.array([E._vec(z) for z in Zel])

    def coords(vec):
        return np.linalg.lstsq(Zm.T, vec, rcond=None)[0]
    br = np.array([E._vec(E.bracket(a, b)) for i, a in enumerate(Zel) for b in Zel[i + 1:]])
    derived = int(np.sum(np.linalg.svd(br, compute_uv=False) > 1e-8 * np.linalg.norm(br)))
    Cm = np.vstack([np.array([coords(E._vec(E.bracket(a, b))) for b in Zel]).T for a in Zel])
    _, s, vh = np.linalg.svd(Cm)
    cdim = int(np.sum(s < 1e-8 * s[0]))
    cent = [to_el(vh[-i - 1].conj() @ null) for i in range(cdim)]
    A1, A2 = ad(cent[0]), ad(cent[1])
    w_, V = np.linalg.eig(A1 + np.pi * A2)
    pairs = []
    for i in range(len(w_)):
        v = V[:, i]
        pairs.append((complex(np.round((v.conj() @ A1 @ v) / (v.conj() @ v), 6)),
                      complex(np.round((v.conj() @ A2 @ v) / (v.conj() @ v), 6))))
    cnt = Counter(pairs)
    w27 = [np.array(k) for k, v in cnt.items() if v == 27]
    w1 = [np.array(k) for k, v in cnt.items() if v == 1]
    triple = None
    for a, b, c in itertools.combinations(range(len(w27)), 3):
        if np.max(abs(w27[a] + w27[b] + w27[c])) < 1e-4:
            triple = (a, b, c)
            break
    neg_ok = triple is not None and all(min(np.max(abs(w27[i] + w)) for w in w27) < 1e-4 for i in triple)
    roots_ok = triple is not None and all(
        min(np.max(abs((w27[i] - w27[j]) - w)) for w in w1) < 1e-4 for i in triple for j in triple if i != j)
    key = next(k for k, v in cnt.items() if v == 27)
    idxs = [i for i, p in enumerate(pairs) if p == key]
    S = V[:, idxs]
    reps = [np.linalg.lstsq(S, ad(el) @ S, rcond=None)[0] for el in Zel]
    d = S.shape[1]
    Acomm = np.vstack([np.kron(np.eye(d), r) - np.kron(r.T, np.eye(d)) for r in reps])
    comm = int(np.sum(np.linalg.svd(Acomm, compute_uv=False) < 1e-7))
    return dict(centralisers=out, derived_dim=derived, centre_dim=cdim,
                weight_multiplicities=sorted(cnt.values()), commutant_on_27=comm,
                family_triple_sums_to_zero=triple is not None, family_negatives_present=bool(neg_ok),
                singlets_are_roots=bool(roots_ok))


def pauli(a, b, c, d):
    X1, Z1 = E.X1, E.Z1
    return np.kron(np.linalg.matrix_power(X1, a) @ np.linalg.matrix_power(Z1, b),
                   np.linalg.matrix_power(X1, c) @ np.linalg.matrix_power(Z1, d))


def act_aut(g, el):
    A, x_, k_ = el
    gi = np.linalg.inv(g)
    T = np.einsum("ai,bj,ck,ijk->abc", g, g, g, E.full(x_))
    S = np.einsum("ia,jb,kc,ijk->abc", gi, gi, gi, E.full(k_))
    return (g @ A @ gi, E.sorted_c(T), E.sorted_c(S))


POINTS = [v for v in itertools.product(range(3), repeat=4) if any(v) and next(t for t in v if t) == 1]


def part_bijection():
    images = []
    fixed_dims = set()
    for r in witting_rays():
        Zel = [to_el(n) for n in centraliser(ray_element(r))]
        hits = []
        for v in POINTS:
            g = pauli(*v)
            if all(np.allclose(E._vec(act_aut(g, z)), E._vec(z), atol=1e-9) for z in Zel):
                hits.append(v)
        images.append(hits)
        if len(hits) == 1 and len(fixed_dims) < 2:
            g = pauli(*hits[0])
            Mf = np.array([E._vec(act_aut(g, b)) - E._vec(b) for b in BASIS]).T
            fixed_dims.add(int(np.sum(np.linalg.svd(Mf, compute_uv=False) < 1e-9)))
    unique = all(len(h) == 1 for h in images)
    distinct = len({h[0] for h in images if h}) if unique else 0
    return dict(hits_per_ray=sorted({len(h) for h in images}), distinct_points=distinct, pauli_fixed_algebra_dims=sorted(fixed_dims))


def main():
    rng = np.random.default_rng(11887)
    res = dict(pass_ids=[11887, 11888, 11889])
    a = res["11887_11888_e6_and_families"] = part_e6(rng)
    b = res["11889_w33_point"] = part_bijection()
    res["checks"] = {k: bool(v) for k, v in dict(
        ray_centraliser_80=a["centralisers"]["witting_e0"] == dict(dim=80, grades=[24, 28, 28]),
        generic_centraliser_cartan=a["centralisers"]["generic"] == dict(dim=8, grades=[0, 4, 4]),
        e6=a["derived_dim"] == 78 and a["commutant_on_27"] == 1 and a["centre_dim"] == 2,
        decomposition=a["weight_multiplicities"] == [1] * 6 + [27] * 6 + [80],
        three_families=a["family_triple_sums_to_zero"] and a["family_negatives_present"] and a["singlets_are_roots"],
        unique_w33_point_per_ray=b["hits_per_ray"] == [1],
        bijection_40=b["distinct_points"] == 40,
        pauli_centraliser_E6A2=b["pauli_fixed_algebra_dims"] == [86],
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, default=str))
    print(json.dumps(res["checks"], indent=1))
    print(json.dumps(b))
    print("all", res["all_checks_pass"])


if __name__ == "__main__":
    main()
