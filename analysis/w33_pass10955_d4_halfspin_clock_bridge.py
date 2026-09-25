#!/usr/bin/env python3
"""Pass 10955: D4 half-spin / clock determinant bridge.

The Pass10954 oriented A2^4 sign cover is the standard 16-sign model for the
two D4 half-spin weight sets.  This pass embeds the exact 48-element
GL(2,3) clock/tetracode group as signed permutation matrices preserving the
D4 root system and proves that determinant is exactly the half-spin swap
character.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10951_clock_pin_spin_central_sign_bridge as p51

P46 = p51.p46
OUT = ROOT / "data/w33_pass10955_d4_halfspin_clock_bridge.json"
def signed_matrix(m):
    perm, scales = P46.monomial_pullback(m)
    r = np.zeros((4, 4), dtype=int)
    for i in range(4):
        r[i, perm[i]] = 1 if scales[i] == 1 else -1
    return r


def key(v):
    return tuple(int(x) for x in v)


def matrix_key(a):
    return tuple(int(x) for x in a.ravel())


def cycle_lengths(perm):
    seen = set()
    out = []
    for i in range(len(perm)):
        if i in seen:
            continue
        j = i
        n = 0
        while j not in seen:
            seen.add(j)
            n += 1
            j = perm[j]
        out.append(n)
    return tuple(sorted(out))


def main():
    gl = []
    for e in itertools.product(range(3), repeat=4):
        m = ((e[0], e[1]), (e[2], e[3]))
        if P46.det2(m):
            gl.append(m)
    assert len(gl) == 48
    # Faithful 4D signed-permutation representation.
    images = {matrix_key(signed_matrix(m)) for m in gl}
    assert len(images) == 48
    for a in gl:
        for b in gl:
            assert np.array_equal(
                signed_matrix(p51.mm(a, b)),
                signed_matrix(a) @ signed_matrix(b),
            )

    # D4 roots: all +/-e_i +/-e_j.
    roots = set()
    for i in range(4):
        for j in range(i + 1, 4):
            for si, sj in itertools.product((-1, 1), repeat=2):
                v = np.zeros(4, dtype=int)
                v[i] = si
                v[j] = sj
                roots.add(key(v))
    assert len(roots) == 24
    assert all(
        {key(signed_matrix(m) @ np.array(r)) for r in roots} == roots
        for m in gl
    )

    # Vector and half-spin weights.  We store twice the spinor weights so all
    # coordinates remain integral: S+/- are the even/odd sign demicubes.
    vector_weights = {
        key(s * np.eye(4, dtype=int)[i])
        for i in range(4)
        for s in (-1, 1)
    }
    splus = set()
    sminus = set()
    for signs in itertools.product((-1, 1), repeat=4):
        minus_parity = sum(x == -1 for x in signs) % 2
        (splus if minus_parity == 0 else sminus).add(signs)
    assert len(vector_weights) == len(splus) == len(sminus) == 8
    det_action = Counter()
    outer_actions = set()
    for m in gl:
        r = signed_matrix(m)
        im_v = {key(r @ np.array(v)) for v in vector_weights}
        im_p = {key(r @ np.array(v)) for v in splus}
        im_m = {key(r @ np.array(v)) for v in sminus}
        assert im_v == vector_weights
        det = P46.det2(m)
        if det == 1:
            assert im_p == splus and im_m == sminus
            action = ("V", "S+", "S-")
        else:
            assert im_p == sminus and im_m == splus
            action = ("V", "S-", "S+")
        det_action[(det, action)] += 1
        outer_actions.add(action)

        # W(D4) is exactly the even-sign-flip signed permutation subgroup.
        _, scales = P46.monomial_pullback(m)
        flip_parity = sum(x == 2 for x in scales) % 2
        assert flip_parity == (0 if det == 1 else 1)
    assert det_action == Counter({
        (1, ("V", "S+", "S-")): 24,
        (2, ("V", "S-", "S+")): 24,
    })
    assert len(outer_actions) == 2
    # Exact order-eight clock.
    g = ((0, 1), (1, 1))
    rg = signed_matrix(g)
    assert P46.det2(g) == 2
    assert np.array_equal(np.linalg.matrix_power(rg, 4), -np.eye(4, dtype=int))
    assert np.array_equal(np.linalg.matrix_power(rg, 8), np.eye(4, dtype=int))
    assert not np.array_equal(np.linalg.matrix_power(rg, 4), np.eye(4, dtype=int))

    g2 = p51.mm(g, g)
    assert P46.det2(g2) == 1
    assert np.array_equal(signed_matrix(g2), rg @ rg)

    # Clock action on the union of two half-spin sheets.
    spin_union = sorted(splus | sminus)
    sid = {v: i for i, v in enumerate(spin_union)}
    perm16 = tuple(
        sid[key(rg @ np.array(v))]
        for v in spin_union
    )
    assert cycle_lengths(perm16) == (8, 8)
    for i, v in enumerate(spin_union):
        target = spin_union[perm16[i]]
        assert (v in splus) != (target in splus)

    perm16_2 = tuple(perm16[perm16[i]] for i in range(16))
    for i, v in enumerate(spin_union):
        target = spin_union[perm16_2[i]]
        assert (v in splus) == (target in splus)
    # Four ticks are the central sign on all three D4 minuscule weight sets.
    r4 = np.linalg.matrix_power(rg, 4)
    assert all(key(r4 @ np.array(v)) == key(-np.array(v)) for v in vector_weights)
    assert all(key(r4 @ np.array(v)) == key(-np.array(v)) for v in splus)
    assert all(key(r4 @ np.array(v)) == key(-np.array(v)) for v in sminus)

    # Cross-check the previously independent D4/demicube certificate.
    old = json.loads(
        (ROOT / "data/w33_pass540_symplectic_separator_chainring.json")
        .read_text(encoding="utf-8")
    )
    oldq3 = old["q3"]
    assert oldq3["GL_product_character_by_determinant"] == [[1, 1], [2, 2]]
    assert "D4 spinor and conjugate-spinor weight sets" in oldq3["theorem"]

    p54 = json.loads(
        (ROOT / "data/w33_pass10954_regular_c8_clock_completion.json")
        .read_text(encoding="utf-8")
    )
    assert p54["oriented_A2_4_clock_cover"]["clock_cycle_lengths"] == [8, 8]
    assert p54["shared_determinant_character"]["all48_exact"] is True

    p52 = json.loads(
        (ROOT / "data/w33_pass10952_clock_complete_positivity_firewall.json")
        .read_text(encoding="utf-8")
    )
    cp_rows = p52["complete_positivity_firewall"]["all_eight_powers"]
    assert len(cp_rows) == 8
    assert all(
        row["completely_positive"] == (row["power"] % 2 == 0)
        for row in cp_rows
    )
    assert all(
        row["kind"] == ("unitary_CPTP" if row["power"] % 2 == 0
                       else "positive_TP_not_CP")
        for row in cp_rows
    )
    out = {
        "schema": "w33.pass10955.d4-halfspin-clock-bridge.v1",
        "status": "PASS_D4_HALFSPIN_CLOCK_DETERMINANT_BRIDGE",
        "signed_permutation_embedding": {
            "group": "GL(2,3)",
            "order": 48,
            "dimension": 4,
            "faithful": True,
            "all_48_squared_products_checked": True,
            "D4_root_count": len(roots),
            "all_elements_preserve_D4_roots": True,
            "ambient_signed_permutation_group": "W(B4)",
            "det_plus_subgroup": "SL(2,3) lies in W(D4)",
            "det_minus_coset":
                "odd-sign-flip root automorphisms in W(B4) minus W(D4)",
        },
        "D4_minuscule_weight_sets": {
            "vector_weights": 8,
            "half_spin_plus_weights": 8,
            "half_spin_minus_weights": 8,
            "orientation_bits_map":
                "x in F2^4 -> ( (-1)^x1,...,(-1)^x4 ) / 2",
            "S_plus": "even number of minus signs",
            "S_minus": "odd number of minus signs",
        },
        "outer_D4_action": {
            "det_plus_count": 24,
            "det_minus_count": 24,
            "det_plus_action": "fixes V, S+, S- as sets",
            "det_minus_action": "fixes V and swaps S+ <-> S-",
            "outer_image": "C2 inside Out(D4)=S3",
            "triality_boundary":
                "this realizes only the spinor-sheet transposition, not a triality 3-cycle",
        },
        "clock": {
            "matrix_F3": [list(row) for row in g],
            "signed_4D_matrix": rg.tolist(),
            "order": 8,
            "one_tick": "S+ <-> S-",
            "two_ticks": "preserves S+ and S- separately",
            "four_ticks": "-I4; negates every D4 vector and half-spin weight",
            "eight_ticks": "identity",
            "halfspin_union_cycle_lengths": list(cycle_lengths(perm16)),
        },
        "shared_character": {
            "determinant":
                "det=+1 preserves half-spin sheet; det=-1 swaps half-spin sheet",
            "pass10952_CP":
                "even clock powers are CPTP/unitary; odd powers are positive TP but non-CP",
            "pass10954_Fano":
                "det=+1 preserves and det=-1 flips the Fano-hinge orientation bipartition",
            "new_weld":
                "CP parity, Fano orientation parity and D4 half-spin-sheet parity are the same GL(2,3) character",
        },
        "repo_crosscheck": {
            "pass540":
                "independent full-support sign-word certificate identifies the two demicubes with D4 spinor/conjugate-spinor weights",
            "pass10954":
                "the same 16 sign states are the oriented A2^4 clock cover with two C8 orbits",
        },
        "theorem": (
            "The exact clock/tetracode GL(2,3) has a faithful four-dimensional "
            "signed-permutation representation preserving the D4 root system. "
            "Its determinant-one SL(2,3) subgroup lies in W(D4) and preserves "
            "the two half-spin demicubes separately; every determinant-minus-one "
            "element lies in the other signed-permutation coset, fixes the vector "
            "weight set, and swaps the two half-spin sheets. The Pass10951 clock "
            "generator has order eight, alternates S+ and S- each tick, has square "
            "inside W(D4), fourth power -I4, and two eight-cycles on S+ union S-. "
            "Thus the extended-Clifford/CP grading, the Pass10954 Fano orientation "
            "grading, and the D4 half-spin-sheet grading are one and the same "
            "determinant character."
        ),
        "boundary": (
            "Half-spin here is the exact D4 root/weight-system notion. This does "
            "not identify the finite sheets with observed fermion chirality, CPT, "
            "the Pass10950 Spin(1,9) Weyl field, or a continuum Pin/Spin bundle. "
            "A separate representation intertwiner is required for any such claim."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "embedding_order": 48,
        "outer_action": out["outer_D4_action"],
        "clock_cycles": out["clock"]["halfspin_union_cycle_lengths"],
    }, indent=2))


if __name__ == "__main__":
    main()
