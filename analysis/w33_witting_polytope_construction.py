"""W(3,3) WITTING POLYTOPE EXPLICIT CONSTRUCTION AND VERIFICATION.

Constructs the 40 Witting rays in C^4 from the symplectic polar space
W(3,3) = totally isotropic 1-spaces of F_3^4 under the alternating form,
then verifies the overlap dichotomy |<v_i|v_j>|^2 in {0, 1/3} which
realizes the equiangular tight frame / Bell-Choi structure on a single
photon.

Construction:
  1. Enumerate all 40 totally isotropic 1-spaces (= 1-dim subspaces L of
     F_3^4 with alternating form omega(u, v) = 0 for all u, v in L).
  2. For each such 1-space, lift to a unit vector in C^4 by replacing
     entries 0, 1, 2 (in F_3) with normalised qutrit amplitudes.
  3. Compute the Gram matrix of inner products.
  4. Verify |<v_i|v_j>|^2 in {0, 1/3} for all 780 = C(40,2) pairs.
  5. Verify orbit structure: 1 + k + q^q = 1 + 12 + 27 = 40 around a
     fiducial ray.

The 40 totally isotropic 1-spaces of W(3,3) under the canonical
alternating form omega((u_1, u_2, u_3, u_4), (v_1, v_2, v_3, v_4))
   = u_1 v_3 - u_3 v_1 + u_2 v_4 - u_4 v_2.

A vector v in F_3^4 is on a totally isotropic 1-space (= the line F_3 * v
is totally isotropic) iff omega(v, v) = 0.  But by alternation,
omega(v, v) = 0 automatically.  So every 1-space (= every nonzero vector
modulo F_3^*) corresponds to a totally isotropic 1-space.  Wait -- but
then there are (3^4 - 1)/(3-1) = 40 such 1-spaces, matching v = 40.
That's exactly the substrate's expected count.
"""
from __future__ import annotations

import itertools
import json
import math
import numpy as np
from pathlib import Path


# Substrate constants
Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI6 = Q * Q - Q + 1
V = 40

# Primitive cube root of unity over the complex numbers
omega_c = np.exp(2j * np.pi / Q)


def enumerate_isotropic_1spaces() -> list[tuple[int, int, int, int]]:
    """Return one representative vector per totally isotropic 1-space of
    W(3,3) under the canonical symplectic form on F_3^4.  Since every
    1-space is totally isotropic (omega(v, v) = 0 by alternation), we just
    enumerate one representative per ray (= one per F_3^*-orbit on
    F_3^4 \ {0})."""
    rays = []
    for u in itertools.product(range(Q), repeat=4):
        if all(x == 0 for x in u):
            continue
        # find first nonzero coordinate
        first_nz = next(i for i, x in enumerate(u) if x != 0)
        if u[first_nz] == 1:
            # canonical representative: first nonzero entry is 1
            rays.append(u)
    assert len(rays) == V, f"Expected {V} rays, got {len(rays)}"
    return rays


def f3_to_qutrit_vector(u: tuple[int, int, int, int]) -> np.ndarray:
    """Lift F_3^4 vector u = (u_1, u_2, u_3, u_4) to a C^4 unit vector by
    sending each u_i in {0, 1, 2} to omega_c^{u_i}.  Normalise by 1/2 (since
    each component has magnitude 1, the 4-vector has norm 2)."""
    v = np.array([omega_c ** ui for ui in u], dtype=complex)
    v = v / np.linalg.norm(v)
    return v


def witting_rays() -> list[np.ndarray]:
    """Return the 40 Witting rays as unit C^4 vectors."""
    rays_f3 = enumerate_isotropic_1spaces()
    return [f3_to_qutrit_vector(u) for u in rays_f3]


def overlap_squared(v1: np.ndarray, v2: np.ndarray) -> float:
    return float(abs(v1.conj() @ v2) ** 2)


def verify_overlap_dichotomy() -> dict:
    rays = witting_rays()
    overlaps = []
    n_zero = 0
    n_third = 0
    n_other = 0
    other_values = []
    for i, j in itertools.combinations(range(V), 2):
        ov = overlap_squared(rays[i], rays[j])
        overlaps.append(ov)
        if np.isclose(ov, 0):
            n_zero += 1
        elif np.isclose(ov, 1.0 / Q):
            n_third += 1
        else:
            n_other += 1
            other_values.append(ov)

    return {
        "total_pairs": len(overlaps),
        "n_zero_overlap": n_zero,
        "n_third_overlap": n_third,
        "n_other": n_other,
        "other_values_sample": other_values[:5] if other_values else [],
        "dichotomy_holds": n_other == 0,
        "min_overlap": float(min(overlaps)),
        "max_overlap": float(max(overlaps)),
        "expected_total_pairs": V * (V - 1) // 2,
    }


def verify_orbit_shell() -> dict:
    """For a fiducial ray, count rays at each overlap value.
    Expected: 1 self + (k = 12) at zero overlap + (q^q = 27) at 1/q overlap
    = 40 total.

    Actually wait: on W(3,3), the Bell line has 4 = q+1 collinear rays
    (zero mutual overlap with each other? No, they all share the line),
    so the dichotomy may differ slightly from the heuristic above.

    Let's just measure the shell structure empirically.
    """
    rays = witting_rays()
    fiducial = rays[0]
    shell_zero = 0
    shell_third = 0
    for j in range(1, V):
        ov = overlap_squared(fiducial, rays[j])
        if np.isclose(ov, 0):
            shell_zero += 1
        elif np.isclose(ov, 1.0 / Q):
            shell_third += 1
    return {
        "fiducial_ray": rays[0].tolist(),
        "shell_zero_overlap": shell_zero,
        "shell_third_overlap": shell_third,
        "total_other_rays": V - 1,
        "match_sum": (shell_zero + shell_third) == (V - 1),
    }


def verify_substrate_counts() -> dict:
    return {
        "v": V,
        "expected_substrate": "(q^4 - 1)/(q-1)",
        "computed_substrate": (Q ** 4 - 1) // (Q - 1),
        "match": V == (Q ** 4 - 1) // (Q - 1),
    }


def gram_matrix_summary() -> dict:
    rays = witting_rays()
    G = np.zeros((V, V), dtype=complex)
    for i in range(V):
        for j in range(V):
            G[i, j] = rays[i].conj() @ rays[j]

    # Frame-theoretic check: sum |v_i><v_i| / V should be (1/4) * I (for
    # equiangular tight frame in C^4)
    P = sum(np.outer(rays[i], rays[i].conj()) for i in range(V)) / V
    expected_P = np.eye(4, dtype=complex) / 4

    return {
        "frame_resolution_check": bool(np.allclose(P, expected_P)),
        "expected_P_diag_value": 1.0 / 4,
        "computed_P_diag": [float(P[i, i].real) for i in range(4)],
        "computed_P_offdiag_max": float(np.max(np.abs(P - np.diag(np.diag(P)))).real),
    }


def main() -> None:
    print("=" * 78)
    print("W(3,3) WITTING POLYTOPE CONSTRUCTION AND VERIFICATION")
    print("=" * 78)

    print("\nSubstrate count check:")
    s = verify_substrate_counts()
    print(f"  v = {s['v']} = (q^4 - 1)/(q-1) = {s['computed_substrate']}: {s['match']}")

    print("\nOverlap dichotomy check (all 780 pairs):")
    o = verify_overlap_dichotomy()
    print(f"  total pairs: {o['total_pairs']} (expected {o['expected_total_pairs']})")
    print(f"  n_zero overlap:  {o['n_zero_overlap']}")
    print(f"  n_third overlap: {o['n_third_overlap']}")
    print(f"  n_other:         {o['n_other']}")
    print(f"  dichotomy holds: {o['dichotomy_holds']}")
    if o['other_values_sample']:
        print(f"  other sample: {o['other_values_sample']}")

    print("\nFiducial-ray shell structure:")
    sh = verify_orbit_shell()
    print(f"  rays at overlap 0:    {sh['shell_zero_overlap']}")
    print(f"  rays at overlap 1/q:  {sh['shell_third_overlap']}")
    print(f"  total = {sh['shell_zero_overlap'] + sh['shell_third_overlap']} = v - 1 = {V - 1}")

    print("\nFrame-theoretic check (sum |v_i><v_i| / V = I/4):")
    g = gram_matrix_summary()
    print(f"  diag values: {g['computed_P_diag']}")
    print(f"  max off-diag: {g['computed_P_offdiag_max']}")
    print(f"  ETF check: {g['frame_resolution_check']}")

    payload = {
        "substrate_counts":     s,
        "overlap_dichotomy":    o,
        "fiducial_shell":       sh,
        "frame_check":          g,
    }

    out = Path("data") / "w33_witting_polytope_construction.json"
    out.parent.mkdir(exist_ok=True)

    def json_safe(o):
        if isinstance(o, complex):
            return {"re": o.real, "im": o.imag}
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return [json_safe(x) for x in o.tolist()]
        if isinstance(o, dict):
            return {k: json_safe(v) for k, v in o.items()}
        if isinstance(o, list):
            return [json_safe(x) for x in o]
        return o

    out.write_text(json.dumps(json_safe(payload), indent=2), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
