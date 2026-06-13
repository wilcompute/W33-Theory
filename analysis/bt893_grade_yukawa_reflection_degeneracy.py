#!/usr/bin/env python3
"""
BT893 - Grade Yukawa Reflection Degeneracy Theorem.

This finishes/corrects the CKM calculation queued after BT891.

BT891 established the exact Z3 grade-selection rule for the cubic Yukawa
skeleton:

    g_a + g_b + g_H = 0 (mod 3).

At the 3x3 generation-grade level this is one nonzero entry per row and
column, but it is NOT a pure cyclic shift.  It is the shifted reflection

    b = -a - g_H,

so the three Higgs-grade skeletons are the three reflections in D3 ~= S3.
Their products are the generation rotations.  Since each skeleton is a
permutation/reflection, all singular values are equal.  Therefore the exact
Z3 grade skeleton fixes support and flavor group structure, but it does not
by itself determine physical CKM/PMNS angles: the grade-level masses are
maximally degenerate and the observable mixing lives in the within-grade
q^2=9 blocks/profiles.
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np

MOD = 3
GRADES = range(MOD)


def yukawa_mask(higgs_grade: int) -> np.ndarray:
    """Return the 3x3 grade support matrix Y_g[a,b]=1 iff a+b+g=0 mod3."""
    y = np.zeros((MOD, MOD), dtype=int)
    for a, b in product(GRADES, repeat=2):
        if (a + b + higgs_grade) % MOD == 0:
            y[a, b] = 1
    return y


def rotation(step: int) -> np.ndarray:
    """Permutation matrix for a -> a+step on Z3, row=input, col=output."""
    r = np.zeros((MOD, MOD), dtype=int)
    for a in GRADES:
        r[a, (a + step) % MOD] = 1
    return r


def perm_from_matrix(m: np.ndarray) -> tuple[int, ...]:
    return tuple(int(np.argmax(m[a])) for a in GRADES)


def compose_perm(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def order_perm(p: tuple[int, ...]) -> int:
    ident = tuple(range(len(p)))
    cur = p
    o = 1
    while cur != ident:
        cur = compose_perm(p, cur)
        o += 1
        if o > 100:
            raise RuntimeError("permutation order runaway")
    return o


def main() -> None:
    masks = {g: yukawa_mask(g) for g in GRADES}
    rotations = {s: rotation(s) for s in GRADES}

    checks: dict[str, object] = {}

    # T1: support is the shifted reflection b=-a-g, not S^{-g}.
    support_maps = {}
    for g, y in masks.items():
        support_maps[str(g)] = list(perm_from_matrix(y))
        expected = np.zeros_like(y)
        for a in GRADES:
            expected[a, (-a - g) % MOD] = 1
        assert np.array_equal(y, expected)
        assert all(y.sum(axis=0) == 1)
        assert all(y.sum(axis=1) == 1)
    checks["T1_shifted_reflection_support"] = True

    # T2: every skeleton is symmetric involutive with singular values 1,1,1.
    singular_values = {}
    for g, y in masks.items():
        assert np.array_equal(y, y.T)
        assert np.array_equal(y @ y, np.eye(MOD, dtype=int))
        vals = sorted(np.linalg.svd(y.astype(float), compute_uv=False).round(12).tolist())
        singular_values[str(g)] = vals
        assert vals == [1.0, 1.0, 1.0]
    checks["T2_symmetric_involutions_degenerate_singular_values"] = True

    # T3: products of two Higgs-grade reflections are generation rotations.
    product_table: dict[str, list[list[int]]] = {}
    for gu, gd in product(GRADES, repeat=2):
        prod = masks[gu] @ masks[gd]
        # With row-vector convention, this is rotation by gu-gd.
        step = (gu - gd) % MOD
        product_table[f"{gu},{gd}"] = prod.tolist()
        assert np.array_equal(prod, rotations[step])
    checks["T3_reflection_products_are_Z3_rotations"] = True

    # T4: the generated permutation group is S3/D3: 6 elements, orders 1,2,3.
    generators = [perm_from_matrix(masks[g]) for g in GRADES]
    group = {tuple(range(MOD))}
    frontier = list(generators)
    while frontier:
        p = frontier.pop()
        if p in group:
            continue
        group.add(p)
        for q in list(group) + generators:
            frontier.append(compose_perm(p, q))
            frontier.append(compose_perm(q, p))
    order_hist: dict[str, int] = {}
    for p in group:
        order_hist[str(order_perm(p))] = order_hist.get(str(order_perm(p)), 0) + 1
    assert len(group) == 6
    assert order_hist == {"1": 1, "2": 3, "3": 2}
    checks["T4_Higgs_grade_reflections_generate_S3"] = True

    # T5: different Higgs-grade skeletons do not commute as matrices.
    commutator_norms: dict[str, int] = {}
    for gu, gd in product(GRADES, repeat=2):
        comm = masks[gu] @ masks[gd] - masks[gd] @ masks[gu]
        norm2 = int(np.sum(comm * comm))
        commutator_norms[f"{gu},{gd}"] = norm2
        if gu == gd:
            assert norm2 == 0
        else:
            assert norm2 == 6
    checks["T5_distinct_grade_reflections_do_not_commute"] = True

    # T6: but YY^T = I for every grade skeleton, so grade-level left mass
    # operators are identical and triply degenerate. CKM angles are therefore
    # not fixed until a within-grade q^2=9 profile breaks the degeneracy.
    for _g, y in masks.items():
        assert np.array_equal(y @ y.T, np.eye(MOD, dtype=int))
    grade_mass_eigenvalues = [1, 1, 1]
    checks["T6_grade_mass_operator_is_identity_degenerate"] = True

    q = 3
    within_grade_dim = q * q
    result = {
        "theorem": "BT893 Grade Yukawa Reflection Degeneracy Theorem",
        "input_selection_rule": "g_a + g_b + g_H = 0 mod 3",
        "corrected_support_law": "b = -a - g_H mod 3",
        "not_pure_shift": True,
        "masks": {str(g): masks[g].tolist() for g in GRADES},
        "support_maps_row_to_column": support_maps,
        "singular_values_by_higgs_grade": singular_values,
        "product_law": "Y_gu Y_gd = rotation(gu-gd)",
        "product_table": product_table,
        "commutator_frobenius_norm_squared": commutator_norms,
        "generated_group": "S3 ~= D3",
        "generated_group_order": len(group),
        "generated_group_order_histogram": order_hist,
        "grade_mass_eigenvalues": grade_mass_eigenvalues,
        "within_grade_dimension": within_grade_dim,
        "physical_interpretation": (
            "The derived Z3 grade skeleton fixes the Yukawa support as the "
            "three S3 reflection axes. At grade level all singular values "
            "are degenerate, so numerical CKM/PMNS angles are not determined "
            "by the 3x3 grade skeleton alone. Observable hierarchy and mixing "
            "must be produced by the q^2=9 within-grade Higgs profiles."
        ),
        "checks": checks,
    }

    out_path = Path("data/PART_BT893_GRADE_YUKAWA_REFLECTION_DEGENERACY_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("BT893 Grade Yukawa Reflection Degeneracy Theorem")
    print("T1 support law: Y_g[a,b]=1 iff b=-a-g mod 3")
    print("T2 each Y_g is a symmetric involution with singular values", grade_mass_eigenvalues)
    print("T3 product law: Y_gu Y_gd = generation rotation by gu-gd")
    print("T4 generated group: S3/D3, order", len(group), "hist", order_hist)
    print("T5 distinct Higgs-grade skeletons noncommute; commutator norm^2 = 6")
    print("T6 grade-level mass operator is identity; mixing is within-grade q^2=9")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
