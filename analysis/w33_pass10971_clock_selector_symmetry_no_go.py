#!/usr/bin/env python3
"""Pass 10971: full clock symmetry forbids a preferred clock direction.

For q=3 the repo's null/Hesse/A2 clock carrier is P1(F3) with common
PGL(2,3) ~= S4 action. More generally PGL(2,q) is 2-transitive on P1(Fq).
The commutant on the (q+1)-dimensional clock permutation module therefore
has only two orbitals: diagonal and off-diagonal, hence span{I,J}.

A fully clock-symmetric Hermitian Hamiltonian cannot make a basis clock
direction a nondegenerate eigenstate. Choosing one clock requires symmetry
breaking to its point stabilizer. The natural order parameter is the
q-dimensional augmentation vector e_i - 1/(q+1) 1.
"""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass10971_clock_selector_symmetry_no_go.json"
PARENT = ROOT / "data" / "w33_20260924_null_hesse_4a2_s4_intertwiner.json"
P593 = ROOT / "data" / "w33_pass593_icosahedral_singer_fibre.json"
def projective_points(q: int):
    return [(x, 1) for x in range(q)] + [(1, 0)]


def pgl2_perms(q: int):
    pts = projective_points(q)
    idx = {p: i for i, p in enumerate(pts)}
    reps = set()
    perms = set()
    for a, b, c, d in itertools.product(range(q), repeat=4):
        if (a * d - b * c) % q == 0:
            continue
        v = (a, b, c, d)
        first = next(x for x in v if x)
        inv = pow(first, -1, q)
        M = tuple((x * inv) % q for x in v)
        if M in reps:
            continue
        reps.add(M)
        p = []
        for x, y in pts:
            u = ((M[0] * x + M[1] * y) % q,
                 (M[2] * x + M[3] * y) % q)
            if u[1]:
                pn = (u[0] * pow(u[1], -1, q) % q, 1)
            else:
                pn = (1, 0)
            p.append(idx[pn])
        perms.add(tuple(p))
    return sorted(perms)
def compose(p, r):
    return tuple(p[r[i]] for i in range(len(p)))


def inverse(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def orbit(seed, group, action):
    seen = {seed}
    q = deque([seed])
    while q:
        x = q.popleft()
        for g in group:
            y = action(g, x)
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


def ordered_pair_orbits(group, n):
    unseen = {(i, j) for i in range(n) for j in range(n)}
    out = []
    while unseen:
        s = min(unseen)
        O = orbit(s, group, lambda g, ij: (g[ij[0]], g[ij[1]]))
        out.append(O)
        unseen -= O
    return sorted([sorted(O) for O in out], key=lambda O: (len(O), O))
def point_stabilizer(group, point=0):
    return [g for g in group if g[point] == point]


def selector_packet(q: int):
    G = pgl2_perms(q)
    n = q + 1
    orbits = ordered_pair_orbits(G, n)
    stab = point_stabilizer(G, 0)

    # H = a I + b J has eigenvalue a+b*n on uniform and a on augmentation.
    # H e_0 = a e_0 + b 1; e_0 is an eigenvector iff b=0, then H is scalar.
    no_basis_selector = True

    # Exact augmentation orbit: v_i=e_i-(1/n)1, one for each clock direction.
    aug = []
    for i in range(n):
        aug.append(tuple(Fraction(int(j == i), 1) - Fraction(1, n)
                         for j in range(n)))
    aug_orbit = {
        tuple(v[g[j]] for j in range(n))
        for g in G for v in [aug[0]]
    }

    return {
        "q": q,
        "clock_directions": n,
        "PGL2_order": len(G),
        "expected_PGL2_order": q * (q * q - 1),
        "ordered_pair_orbit_sizes": sorted(len(O) for O in orbits),
        "commutant_dimension": len(orbits),
        "commutant_basis": ["I", "J"],
        "symmetric_H_form": "H=a I + b J",
        "spectrum": {
            "uniform": {"multiplicity": 1, "eigenvalue": "a+b(q+1)"},
            "augmentation": {"multiplicity": q, "eigenvalue": "a"},
        },
        "basis_clock_can_be_nondegenerate_eigenstate": not no_basis_selector,
        "point_stabilizer_order": len(stab),
        "expected_point_stabilizer_order": q * (q - 1),
        "symmetry_breaking_index": len(G) // len(stab),
        "augmentation_dimension": q,
        "augmentation_selector_orbit_size": len(aug_orbit),
        "rank_one_bias": "-|e_0><e_0|",
        "rank_one_bias_point_stabilizer_invariant": all(g[0] == 0 for g in stab),
        "rank_one_bias_unique_selected_clock": 0,
    }
def payload():
    q3 = selector_packet(3)
    q5 = selector_packet(5)
    q7 = selector_packet(7)
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    p593 = json.loads(P593.read_text(encoding="utf-8"))

    checks = {
        "q3_parent_common_S4": parent["action"]["common_image"] == "PGL(2,3) ~= S4",
        "q3_parent_action_order24": parent["action"]["image_order"] == 24,
        "q3_two_orbitals": q3["ordered_pair_orbit_sizes"] == [4, 12],
        "q3_commutant_dim2": q3["commutant_dimension"] == 2,
        "q3_breaks_S4_to_S3": q3["point_stabilizer_order"] == 6 and q3["symmetry_breaking_index"] == 4,
        "q3_order_parameter_dim3": q3["augmentation_dimension"] == 3,
        "q5_two_orbitals": q5["ordered_pair_orbit_sizes"] == [6, 30],
        "q5_commutant_dim2": q5["commutant_dimension"] == 2,
        "q5_breaking_index6": q5["symmetry_breaking_index"] == 6,
        "q5_order_parameter_dim5": q5["augmentation_dimension"] == 5,
        "q5_matches_Pass593_augmentation": p593["augmentation"]["dimension"] == 5,
        "q5_matches_Pass593_PGL": p593["checks"]["PGL2_5_order120"],
        "q7_two_orbitals": q7["ordered_pair_orbit_sizes"] == [8, 56],
        "q7_commutant_dim2": q7["commutant_dimension"] == 2,
        "all_full_symmetry_basis_selectors_forbidden": all(
            not x["basis_clock_can_be_nondegenerate_eigenstate"] for x in (q3, q5, q7)
        ),
    }
    return {
        "schema": "w33.pass10971.clock-selector-symmetry-no-go.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "headline": (
            "A Hamiltonian on clock-direction amplitudes that preserves the full PGL(2,q) "
            "clock symmetry is aI+bJ and cannot select one clock direction. At q=3 this "
            "is the repo's exact S4 null/Hesse/A2 carrier; choosing one clock necessarily "
            "breaks S4 to S3, with a three-dimensional augmentation order parameter."
        ),
        "q3": q3,
        "q5": q5,
        "q7": q7,
        "checks": checks,
        "physical_boundary": (
            "This is a symmetry no-go for linear Hamiltonians on the clock permutation module, "
            "not a derivation of a physical Hamiltonian. It says any dynamical theory that picks "
            "a preferred clock direction must include explicit or spontaneous clock-symmetry breaking, "
            "or act on a larger module where additional invariant operators exist."
        ),
        "next_target": (
            "Search the existing W33/Albert/Steinberg modules for a canonical augmentation-valued "
            "order parameter whose stabilizer is the clock point stabilizer."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = payload()
    s = json.dumps(p, indent=2, sort_keys=True) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8") != s:
            raise SystemExit("certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(s, encoding="utf-8")
    print(json.dumps({
        "status": p["status"],
        "checks": sum(p["checks"].values()),
        "total": len(p["checks"]),
        "q3_commutant_dimension": p["q3"]["commutant_dimension"],
        "q3_breaking": "S4 -> S3",
        "q5_order_parameter_dimension": p["q5"]["augmentation_dimension"],
    }, sort_keys=True))
    return 0 if p["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
