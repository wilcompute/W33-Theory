"""Pass 11926: the symmetric tangent dynamics at a Witting ray cannot produce the up hierarchy.

At a Witting ray of the E8 84-Higgs Cartan the transverse tangent carries G25, whose projective image is the qutrit
Clifford group (order 216; parallel packet 34e149d79), and the flavour Higgs is that tangent qutrit. A G25-symmetric
potential for the tangent direction t is a sum of Clifford-invariant Hermitian forms of bidegree (k, k).

1. Invariants (Reynolds averages over the 216 projective elements): on the unit sphere bidegree (2,2) has NO non-constant
   invariant (so the quartic, like the quadratic, is isotropic), bidegree (3,3) has one, bidegree (4,4) has two.
2. Minima of random combinations of the (3,3) and (4,4) invariants (120 draws, frozen statistics) land on five
   special orbits (polished here to exact symmetric points):
     strange states        M2 = log 2,     stabiliser 24, orbit 9    (61 hits)  -> (1,1,0): theta-zero law, locked
     stabiliser states     M2 = 0,         stabiliser 18, orbit 12   (37 hits)  -> (1,eps,eps): charm-up lock
     M2 = log(8/5), max Pauli (1+sqrt3)/4,  stabiliser 4,  orbit 54   (17 hits)  -> unlocked
     M2 = log(9/5), max Pauli 1/sqrt3,      stabiliser 3,  orbit 72   ( 4 hits)  -> unlocked
     M2 = 0.6908,   max Pauli 0.5348,        stabiliser 3,  orbit 72   ( 1 hit )  -> unlocked
3. The unlocking orbits are NOT hierarchical: for g = (1, eps, eps) and every member of each orbit, m_c/m_t stays >= 0.36
   as eps -> 0 (0.367, 0.532, 0.510 for the three orbits).
Reading: no G25-symmetric vacuum of the Witting tangent gives the observed up hierarchy (m_c/m_t ~ 4e-3,
m_u/m_c ~ 2e-3); it needs a small G25-breaking parameter, e.g. the H27-covariant cubic of 34e149d79.
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass11926_g25_tangent_vacua.json"
FROZEN = ROOT / "data" / "w33_pass11926_orbit_reps_frozen.json"
W = np.exp(2j * np.pi / 3)
X = np.roll(np.eye(3), 1, axis=0)
Z = np.diag([1, W, W * W])
FH = np.array([[W ** (i * j) for j in range(3)] for i in range(3)]) / np.sqrt(3)
PG = np.diag([1, 1, W])
PAULIS = [np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b) for a in range(3) for b in range(3)]


def clifford():
    def key(A):
        v = A.ravel()
        i = np.flatnonzero(abs(v) > 1e-9)[0]
        A = A * abs(v[i]) / v[i]
        return tuple(np.round(A.ravel(), 8))

    G = {key(np.eye(3)): np.eye(3, dtype=complex)}
    frontier = [np.eye(3, dtype=complex)]
    while frontier:
        nf = []
        for a in frontier:
            for g in (X, Z, FH, PG):
                b = g @ a
                k = key(b)
                if k not in G:
                    G[k] = b
                    nf.append(b)
        frontier = nf
    return list(G.values())


def kron_pow(g, k):
    out = np.eye(1)
    for _ in range(k):
        out = np.kron(out, g)
    return out


def M2(h):
    return float(-np.log(sum(abs(np.vdot(h, P @ h)) ** 4 for P in PAULIS) / 3))


def pmax(h):
    return float(max(abs(np.vdot(h, P @ h)) for P in PAULIS[1:]))


def Y(h, g):
    return np.array([[h[(a + b) % 3] * g[(a - b) % 3] for b in range(3)] for a in range(3)])


def polish(t, G):
    t = t / np.linalg.norm(t)
    S = [g for g in G if abs(abs(np.vdot(t, g @ t)) - 1) < 1e-5]
    P = sum(np.outer(g @ t, (g @ t).conj()) for g in S) / len(S)
    w, V = np.linalg.eigh(P)
    u = V[:, -1]
    return u, len([g for g in G if abs(abs(np.vdot(u, g @ u)) - 1) < 1e-10])


def main():
    G = clifford()
    rng = np.random.default_rng(11926)
    ranks = {}
    for k in (2, 3, 4):
        n = 3 ** k
        forms = []
        for _ in range(3):
            A0 = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
            A0 = A0 + A0.conj().T
            forms.append(sum(kron_pow(g, k).conj().T @ A0 @ kron_pow(g, k) for g in G) / len(G))
        pts = [(lambda z: z / np.linalg.norm(z))(rng.normal(size=3) + 1j * rng.normal(size=3)) for _ in range(60)]
        M = np.array([[np.real(np.vdot(kron_pow(p.reshape(3, 1), k).ravel(), A @ kron_pow(p.reshape(3, 1), k).ravel()))
                       for A in forms] + [1.0] for p in pts])
        ranks[k] = int(np.linalg.matrix_rank(M, tol=1e-9)) - 1     # non-constant invariants
    fz = json.loads(FROZEN.read_text())
    orbits = []
    for rec in fz["orbits"]:
        t = np.array(rec["re"]) + 1j * np.array(rec["im"])
        u, stab = polish(t, G)
        gaps = []
        for _ in range(50):
            e = rng.normal() + 1j * rng.normal()
            g = np.array([rng.normal() + 1j * rng.normal(), e, e])
            s = np.linalg.svd(Y(u, g), compute_uv=False)
            gaps.append(min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0])
        members = [g @ u for g in G]
        mcmt = min(np.linalg.svd(Y(m, np.array([1, 1e-3, 1e-3])), compute_uv=False)[1] /
                   np.linalg.svd(Y(m, np.array([1, 1e-3, 1e-3])), compute_uv=False)[0] for m in members)
        orbits.append(dict(hits=rec["hits"], M2=M2(u), pmax=pmax(u), stabiliser=stab, orbit=len(G) // stab,
                           max_gap=float(max(gaps)), min_gap=float(min(gaps)), min_mc_mt_over_orbit_eps1e3=float(mcmt)))
    res = dict(pass_id=11926, clifford_projective_order=len(G), nonconstant_invariants_by_bidegree=ranks, orbits=orbits,
               draws=fz["draws"])
    by = {round(o["M2"], 4): o for o in orbits}
    locked = [by[round(np.log(2), 4)], by[0.0]]
    unlocked = [o for o in orbits if o not in locked]
    res["checks"] = {k: bool(v) for k, v in dict(
        clifford_order_216=len(G) == 216,
        invariant_counts_0_1_2=ranks == {2: 0, 3: 1, 4: 2},
        strange_and_stabiliser_orbits=locked[0]["stabiliser"] == 24 and locked[1]["stabiliser"] == 18,
        log8over5_and_log9over5_orbits=abs(unlocked[0]["M2"] - np.log(8 / 5)) < 1e-9 and abs(unlocked[1]["M2"] - np.log(9 / 5)) < 1e-9,
        symmetric_endpoints_lock=all(o["max_gap"] < 1e-10 for o in locked),
        other_orbits_unlock=all(o["min_gap"] > 1e-4 for o in unlocked),
        no_orbit_gives_up_hierarchy=all(o["min_mc_mt_over_orbit_eps1e3"] > 0.3 for o in unlocked),
    ).items()}
    res["all_checks_pass"] = all(res["checks"].values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
