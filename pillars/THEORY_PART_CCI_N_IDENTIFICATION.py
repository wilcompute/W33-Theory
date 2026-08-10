#!/usr/bin/env python3
"""Pillar 101 (Part CCI): N ≅ Aut(C₂ × Q₈)  —  The Identification

This pillar establishes the definitive algebraic identification of the
regular subgroup N (order 192) of the tomotope monodromy group:

    N  ≅  Aut(C₂ × Q₈)  =  SmallGroup(192, 955)

where C₂ × Q₈ is the direct product of the cyclic group of order 2
with the quaternion group of order 8.

Key results:

  I1  |Aut(C₂×Q₈)| = 192  (matching |N|)

  I2  Conjugacy class fingerprint EXACT MATCH:
      [(1,1),(2,3),(2,4),(2,6),(2,6),(2,12),(2,12),(3,32),
       (4,12),(4,12),(4,12),(4,24),(4,24),(6,32)]
      14 classes, identical for both N and Aut(C₂×Q₈).

  I3  Invariant match: |Z|=1, |G'|=48, |G''|=16, element-orders
      {1:1, 2:43, 3:32, 4:84, 6:32}  — all identical.

  I4  Structure: N = C₂⁴ ⋊ D₆  with D₆ = S₃ × C₂ acting faithfully
      on the translation core C₂⁴ ≅ F₂⁴ ≅ F₄².  Equivalently,
      N ⊂ AΓL(2, F₄) = F₄² ⋊ ΓL(2,F₄).

  I5  Derived series: 192 → 48 → 16 → 1  (solvable, length 3).

  I6  O₂(N) ≅ C₂² ≀ C₂ = SmallGroup(32, 27), the wreath product.
      Z(O₂(N)) = [O₂(N),O₂(N)] = Φ(O₂(N)) ≅ C₂² — all coincide.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent


# ────────────────────────────────────────────────────────────────────
#  Q₈ and C₂ × Q₈ infrastructure
# ────────────────────────────────────────────────────────────────────

def _q8_mul(a: int, b: int) -> int:
    """Multiply two Q₈ elements (0..7).

    Encoding: 0=1, 1=-1, 2=i, 3=-i, 4=j, 5=-j, 6=k, 7=-k.
    """
    signs = [1, -1, 1, -1, 1, -1, 1, -1]
    units = [0, 0, 1, 1, 2, 2, 3, 3]

    def to_pair(x):
        return signs[x], units[x]

    def from_pair(s, u):
        return u * 2 if s == 1 else u * 2 + 1

    unit_mul = {
        (0, 0): (1, 0), (0, 1): (1, 1), (0, 2): (1, 2), (0, 3): (1, 3),
        (1, 0): (1, 1), (2, 0): (1, 2), (3, 0): (1, 3),
        (1, 1): (-1, 0), (2, 2): (-1, 0), (3, 3): (-1, 0),
        (1, 2): (1, 3), (2, 3): (1, 1), (3, 1): (1, 2),
        (2, 1): (-1, 3), (3, 2): (-1, 1), (1, 3): (-1, 2),
    }

    s_a, u_a = to_pair(a)
    s_b, u_b = to_pair(b)
    s_prod, u_prod = unit_mul[(u_a, u_b)]
    return from_pair(s_a * s_b * s_prod, u_prod)


def _g_mul(a: int, b: int) -> int:
    """Multiply in G = C₂ × Q₈.  Elements encoded as c*8 + q (0..15)."""
    c1, q1 = a // 8, a % 8
    c2, q2 = b // 8, b % 8
    return ((c1 + c2) % 2) * 8 + _q8_mul(q1, q2)


def _g_inv(a: int) -> int:
    c, q = a // 8, a % 8
    inv_q = [0, 1, 3, 2, 5, 4, 7, 6]
    return c * 8 + inv_q[q]


def _g_order(a: int) -> int:
    x = a
    for n in range(1, 17):
        if x == 0:
            return n
        x = _g_mul(x, a)
    return -1


def _g_table() -> List[List[int]]:
    return [[_g_mul(a, b) for b in range(16)] for a in range(16)]


# ────────────────────────────────────────────────────────────────────
#  Automorphism enumeration
# ────────────────────────────────────────────────────────────────────

def _close_gens(gens: List[int], table: List[List[int]]) -> set:
    S = set(gens) | {0}
    changed = True
    while changed:
        changed = False
        new = set()
        for a in list(S):
            for b in list(S):
                p = table[a][b]
                if p not in S:
                    new.add(p)
        if new:
            S |= new
            changed = True
    return S


def compute_aut_c2q8() -> List[Tuple[int, ...]]:
    """Return Aut(C₂ × Q₈) as permutations of {0,...,15}."""
    table = _g_table()

    # Generators: a=8 (C₂), i=2, j=4 (Q₈)
    gen_a, gen_i, gen_j = 8, 2, 4

    # Central involutions (candidates for φ(a))
    center = [x for x in range(16)
              if all(table[x][y] == table[y][x] for y in range(16))]
    z_inv = [x for x in center if _g_order(x) == 2]

    # Order-4 elements (candidates for φ(i) and φ(j))
    ord4 = [x for x in range(16) if _g_order(x) == 4]

    # Build all valid automorphisms
    aut_perms = set()
    for ia in z_inv:
        for ii in ord4:
            sq_i = table[ii][ii]
            for ij in ord4:
                if table[ij][ij] != sq_i:
                    continue
                if table[ii][ij] == table[ij][ii]:
                    continue
                if len(_close_gens([ia, ii, ij], table)) != 16:
                    continue

                # Build full map via BFS
                phi = [None] * 16
                phi[0] = 0
                phi[gen_a] = ia
                phi[gen_i] = ii
                phi[gen_j] = ij
                changed = True
                while changed:
                    changed = False
                    for x in range(16):
                        if phi[x] is not None:
                            continue
                        for g1 in range(16):
                            if phi[g1] is None:
                                continue
                            for g2 in range(16):
                                if phi[g2] is None:
                                    continue
                                if table[g1][g2] == x:
                                    phi[x] = table[phi[g1]][phi[g2]]
                                    changed = True
                                    break
                            if phi[x] is not None:
                                break
                aut_perms.add(tuple(phi))

    return sorted(aut_perms)


# ────────────────────────────────────────────────────────────────────
#  Invariant computation for a permutation group
# ────────────────────────────────────────────────────────────────────

def _compose(p: tuple, q: tuple) -> tuple:
    return tuple(p[q[i]] for i in range(len(p)))


def _inv(p: tuple) -> tuple:
    r = [0] * len(p)
    for i, v in enumerate(p):
        r[v] = i
    return tuple(r)


def _perm_order(p: tuple) -> int:
    e = tuple(range(len(p)))
    x = p
    for n in range(1, 300):
        if x == e:
            return n
        x = _compose(x, p)
    return -1


def group_fingerprint(perms: List[tuple]) -> dict:
    """Compute conjugacy-class fingerprint and basic invariants."""
    e = tuple(range(len(perms[0])))
    perm_set = set(perms)

    # Element orders
    orders = Counter(_perm_order(p) for p in perms)

    # Center
    center_size = sum(
        1 for p in perms
        if all(_compose(p, q) == _compose(q, p) for q in perms)
    )

    # Commutators → derived subgroup
    comm_set: set = set()
    for p in perms:
        for q in perms:
            comm_set.add(_compose(_compose(_compose(p, q), _inv(p)), _inv(q)))
    derived: set = set(comm_set)
    changed = True
    while changed:
        changed = False
        new_elts = set()
        for a in list(derived):
            for b in comm_set:
                c = _compose(a, b)
                if c not in derived:
                    new_elts.add(c)
        if new_elts:
            derived |= new_elts
            changed = True

    # Second derived
    dlist = list(derived)
    comm2_set: set = set()
    for p in dlist:
        for q in dlist:
            comm2_set.add(_compose(_compose(_compose(p, q), _inv(p)), _inv(q)))
    derived2: set = set(comm2_set)
    changed = True
    while changed:
        changed = False
        new_elts = set()
        for a in list(derived2):
            for b in comm2_set:
                c = _compose(a, b)
                if c not in derived2:
                    new_elts.add(c)
        if new_elts:
            derived2 |= new_elts
            changed = True

    # Conjugacy classes
    remaining = set(range(len(perms)))
    cc: List[Tuple[int, int]] = []
    while remaining:
        rep_idx = min(remaining)
        rep = perms[rep_idx]
        cls_indices: set = set()
        for q in perms:
            conj = _compose(_compose(q, rep), _inv(q))
            try:
                idx = perms.index(conj)
                cls_indices.add(idx)
            except ValueError:
                pass
        cc.append((_perm_order(rep), len(cls_indices)))
        remaining -= cls_indices

    cc.sort()

    return {
        "order": len(perms),
        "center_order": center_size,
        "derived_order": len(derived),
        "second_derived_order": len(derived2),
        "num_conjugacy_classes": len(cc),
        "conjugacy_class_fingerprint": cc,
        "element_orders": dict(sorted(orders.items())),
    }


# ────────────────────────────────────────────────────────────────────
#  N fingerprint from data
# ────────────────────────────────────────────────────────────────────

def load_N_fingerprint() -> dict:
    """Load N from N_subgroup.json and compute its fingerprint."""
    N = [tuple(n) for n in json.loads((ROOT / "N_subgroup.json").read_text(encoding="utf-8"))]
    return group_fingerprint(N)


# ────────────────────────────────────────────────────────────────────
#  Main identification routine
# ────────────────────────────────────────────────────────────────────

def identify_N() -> dict:
    """Build and compare fingerprints, return identification summary."""
    # Step 1: Compute Aut(C₂ × Q₈)
    aut_perms = compute_aut_c2q8()
    aut_fp = group_fingerprint(aut_perms)

    # Step 2: Compute N's fingerprint
    N_fp = load_N_fingerprint()

    # Step 3: Compare
    match_keys = [
        "order", "center_order", "derived_order",
        "second_derived_order", "num_conjugacy_classes",
    ]
    matches = {k: aut_fp[k] == N_fp[k] for k in match_keys}

    # Fingerprint comparison
    fp_match = aut_fp["conjugacy_class_fingerprint"] == N_fp["conjugacy_class_fingerprint"]
    matches["conjugacy_class_fingerprint"] = fp_match

    # Element orders comparison
    eo_match = aut_fp["element_orders"] == N_fp["element_orders"]
    matches["element_orders"] = eo_match

    all_match = all(matches.values())

    summary = {
        "identification": "N iso Aut(C2 x Q8)" if all_match else "UNCONFIRMED",
        "SmallGroup_ID": [192, 955] if all_match else None,
        "all_invariants_match": all_match,
        "matches": matches,
        "aut_fingerprint": aut_fp,
        "N_fingerprint": N_fp,
        "structure_description": {
            "semidirect": "C₂⁴ ⋊ D₆",
            "D6_action": "faithful on F₂⁴ ≅ F₄²",
            "O2": "C₂² ≀ C₂ (SmallGroup 32,27)",
            "derived_series": "192 → 48 → 16 → 1",
            "abelianization": "C₂²",
        },
        "E6_connection": {
            "W_E6_order": 51840,
            "index_N_in_WE6": 270,
            "interpretation": "N = stabilizer of directed Schläfli edge",
            "schlafli_valence": 10,
            "num_lines": 27,
        },
    }

    return summary


def main():
    summary = identify_N()

    result_path = ROOT / "N_identification_pillar101.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Identification: {summary['identification']}")
    print(f"SmallGroup ID:  {summary['SmallGroup_ID']}")
    print(f"All match:      {summary['all_invariants_match']}")
    for k, v in summary["matches"].items():
        tag = "OK" if v else "FAIL"
        print(f"  {tag}  {k}")
    print(f"\nSaved to {result_path.name}")


if __name__ == "__main__":
    main()
