"""TOE82: exact H27 character of the native 27-octagon tritangent H1.

Independent finite-group calculation using the *same* five H27 coset
directions frozen in TOE77/TOE78.  No floating-point arithmetic.

Over characteristic zero:
 H1 = 2 * sum(nontrivial 1-dimensional H27 characters)
      + 8 * V_omega + 8 * V_omega^2,
where V_omega and V_omega^2 are the two 3D Schrödinger irreps.
In particular H1^H27 = 0.  Do NOT infer this for characteristic 3.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def mul(x, y):
    """TOE77's H27 law: (a,b,c)*(A,B,C)=(a+A,b+B,c+C-b*A)."""
    a, b, c = x
    A, B, C = y
    return ((a + A) % 3, (b + B) % 3, (c + C - b * A) % 3)


def rank2(rows):
    pivots = {}
    for row in rows:
        while row:
            k = row.bit_length() - 1
            if k in pivots:
                row ^= pivots[k]
            else:
                pivots[k] = row
                break
    return len(pivots)


def certificate():
    H = list(itertools.product(range(3), repeat=3))
    identity = (0, 0, 0)
    index = {h: i for i, h in enumerate(H)}
    # Exactly the five native-compatible directions in TOE77.
    directions = ((0, 0, 1), (0, 1, 1), (1, 0, 1),
                  (1, 1, 0), (1, 2, 2))
    faces = set()
    face_by_direction = []
    for d in directions:
        d2 = mul(d, d)
        orbit = {tuple(sorted(index[mul(g, t)]
                              for t in (identity, d, d2)))
                 for g in H}
        assert len(orbit) == 9
        faces.update(orbit)
        face_by_direction.append(orbit)
    assert len(faces) == 45
    faces = sorted(faces)
    edges = sorted({tuple(sorted(pair))
                    for face in faces
                    for pair in itertools.combinations(face, 2)})
    assert len(edges) == 135
    assert len({e for f in faces for e in itertools.combinations(f, 2)}) == 135
    edge_index = {e: i for i, e in enumerate(edges)}
    vertex_rows = [sum(1 << edge_index[e] for e in edges if v in e)
                   for v in range(27)]
    face_rows = [sum(1 << edge_index[e]
                     for e in itertools.combinations(face, 2))
                 for face in faces]
    assert rank2(vertex_rows) == 26
    assert rank2(face_rows) == 45
    assert all((v & f).bit_count() % 2 == 0
               for v in vertex_rows for f in face_rows)
    assert 135 - 26 - 45 == 64

    face_set = set(faces)
    edge_set = set(edges)
    character = {}
    fixed_counts = {}
    for h in H:
        p = [index[mul(h, g)] for g in H]
        assert sorted(p) == list(range(27))
        assert {tuple(sorted(p[v] for v in f)) for f in faces} == face_set
        assert {tuple(sorted(p[v] for v in e)) for e in edges} == edge_set
        c0 = sum(p[i] == i for i in range(27))
        # H27 has exponent 3; no nonidentity element can reverse
        # an oriented edge or an oriented triangle.
        c1 = sum(tuple(sorted(p[i] for i in e)) == e for e in edges)
        c2 = sum(tuple(sorted(p[i] for i in f)) == f for f in faces)
        chi = 1 - c0 + c1 - c2  # equivariant Euler/Lefschetz identity
        character[h] = chi
        fixed_counts[h] = (c0, c1, c2)
    assert character[identity] == 64
    assert all(character[h] == -8 for h in H
               if h != identity and h[:2] == (0, 0))
    assert all(character[h] == -2 for h in H if h[:2] != (0, 0))
    assert sum(character.values()) == 0  # no H27-fixed H1 over Q/C

    # Exact Fourier inner products with the nine linear characters.
    # 1 + omega + omega^2 = 0, no complex-number roundoff.
    linear_multiplicities = {}
    for u, v in itertools.product(range(3), repeat=2):
        phase_sums = [0, 0, 0]
        for (a, b, c), trace in character.items():
            phase_sums[(u * a + v * b) % 3] += trace
        assert phase_sums[1] == phase_sums[2]
        assert (phase_sums[0] - phase_sums[1]) % 27 == 0
        multiplicity = (phase_sums[0] - phase_sums[1]) // 27
        assert multiplicity == (0 if (u, v) == (0, 0) else 2)
        linear_multiplicities[f"{u},{v}"] = multiplicity

    # The two 3D irreps vanish off the center and take
    # 3,3*omega,3*omega^2 on its three elements.
    central = [character[(0, 0, c)] for c in range(3)]
    assert central == [64, -8, -8]
    assert (3 * (central[0] - central[1])) % 27 == 0
    schr_multiplicity = 3 * (central[0] - central[1]) // 27
    assert schr_multiplicity == 8
    assert sum(linear_multiplicities.values()) + 2 * 3 * schr_multiplicity == 64
    return {
        "status": "PASS_TOE82_NATIVE_H27_H1_CHARACTER",
        "source": "TOE77 five native-compatible H27 right-coset directions",
        "complex": {"vertices": 27, "edges": 135, "faces": 45,
                    "boundary_ranks_F2": [26, 45], "H1_dimension": 64},
        "H27_character_values": {"identity": 64,
                                 "two_nonidentity_central_elements": -8,
                                 "twenty_four_noncentral_elements": -2},
        "character_value_histogram": dict(sorted(Counter(character.values()).items())),
        "linear_character_multiplicities": linear_multiplicities,
        "schrodinger_3d_irrep_multiplicities": {
            "central_character_omega": 8,
            "central_character_omega_squared": 8},
        "H27_invariant_H1_dimension_characteristic_zero": 0,
        "representation_identity": "H1_C = 2 sum_(chi nontrivial linear) chi + 8 V_omega + 8 V_omega^2",
        "limitation": "Characteristic 3 is modular; zero complex invariants do not imply zero F3 invariants. This is finite-complex representation theory, not a physical TOE."
    }


if __name__ == "__main__":
    result = certificate()
    path = ROOT / "data/w33_20261015_toe82_native_H27_h1_character.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["status"], result["H27_character_values"],
          result["H27_invariant_H1_dimension_characteristic_zero"])
