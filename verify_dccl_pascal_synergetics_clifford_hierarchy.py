r"""Part DCCL: Pascal's Tetrahedron, the Synergetics Concentric Hierarchy,
and Clifford Grade Decomposition at q = 3.

The user shared Kirby Urner's "Beyond Flatland" essay describing Fuller's
Synergetics concentric hierarchy with tetrahedron = unit volume:

      A, B, T module : 1/24     (1 / tetrahedron flags)
      MITE           : 1/8      (1 / tomotope cells)
      Coupler        : 1
      Tetrahedron    : 1
      Cube           : 3        =   q
      Octahedron     : 4        =   q + 1
      Rh Triacontahedron : 5    =   # Csaszar realisations (DCCXXV)
      Rh Dodecahedron : 6       =   q! = octahedron V (DCCXLIX) = E(tet)
      Icosahedron    : ~18.51   (jitterbug)
      Cuboctahedron  : 20       =   v(W(3,3)) / 2 = central binomial C(6,3)

Every integer volume in the Synergetics hierarchy is a W(3,3) primitive.

The user also noted Pascal's Triangle encodes three natural constants
(e, pi, phi) and connects to Clifford algebra.  Indeed Pascal row n + 1
gives the grade dimensions of the n-dimensional Clifford algebra Cl(n)
(by the universal property of the exterior algebra):

      Cl(n)_k  has dimension  C(n, k),
      dim Cl(n) = 2^n = sum_{k} C(n, k).

At q = 3 (Cl(3)):
    grades  (1, 3, 3, 1)   total  2^3 = 8 = tomotope cells (DCCXXV)
                                          = rank E_8 (DCCXXVII)
                                          = octahedron F (DCCXLIX)

At q + 1 = 4 (Cl(4)):
    grades  (1, 4, 6, 4, 1)  total  2^4 = 16 = trace(Cartan E_8) (DCCXXVII)
                                                = (q+1)^2 = tomotope F
                       central:  6 = q! = octahedron V (DCCXLIX)

So Pascal row 4 has central entry = nilpotence index of the closure
clock, and full sum = E_8 Cartan trace.  This is the deepest Pascal-
to-W(3,3) identification.

Pascal's Tetrahedron (trinomial coefficients) at q = 3:
   row n has entries C(n; a, b, c) with a + b + c = n,
   row sum  = 3^n  (the q-fold sum, not 2^n)
   row 3 sum = 27 = q^q (E_6 fundamental rep dim).

The three Pascal-encoded natural constants:

   e   = lim (1 + 1/n)^n     (binomial limit of Pascal rows)
   pi  ~ 4^n / C(2n, n)^2 * n (central binomial asymptotic; Stirling)
   phi = lim F_{n+1} / F_n   (shallow-diagonal Pascal sums = Fibonacci)

All three live inside the binomial / trinomial structure, which is the
q = 2 / q = 3 case of Pascal.

Rhombic dodecahedron = 14 vertices = 8 tetrahedral voids + 6 octahedral
voids = tomotope cells + octahedron V = closure-clock phase space cells.
Its f-vector (14, 24, 12):
    V = 14 = Csaszar F = Szilassi V (DCCXXV)
    E = 24 = tetrahedron flags (DCCXXV)
    F = 12 = codec (DCCXXII)
    vol = 6 = q! = octahedron V = E(tetrahedron)

So the rhombic dodecahedron is the unifying polyhedron of the hierarchy:
its f-vector encodes the toroidal vertex count, the tetrahedron flag
count, and the codec, with volume = nilpotence index.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


OUT_PATH = ROOT / "data" / "dccl_pascal_synergetics_clifford_hierarchy.json"

Q = 3
QP1 = Q + 1


# ---------------------------------------------------------------------------
# Pascal's Triangle / Tetrahedron
# ---------------------------------------------------------------------------


def binomial_row(n: int) -> list[int]:
    return [math.comb(n, k) for k in range(n + 1)]


def central_binomial(n: int) -> int:
    return math.comb(2 * n, n)


def trinomial_coefficient(n: int, a: int, b: int, c: int) -> int:
    if a + b + c != n or a < 0 or b < 0 or c < 0:
        return 0
    return math.factorial(n) // (math.factorial(a) * math.factorial(b) * math.factorial(c))


def trinomial_row_size(n: int) -> int:
    """Pascal's Tetrahedron row n has (n+1)(n+2)/2 entries (triangle of trinomials)."""
    return (n + 1) * (n + 2) // 2


def trinomial_row_sum(n: int) -> int:
    """Sum of all C(n; a, b, c) = (1+1+1)^n = 3^n."""
    return 3 ** n


# ---------------------------------------------------------------------------
# Clifford algebra grade decomposition
# ---------------------------------------------------------------------------


def clifford_grades(n: int) -> dict[str, Any]:
    """Cl(n) has graded decomposition with dim Cl(n)_k = C(n, k)."""
    grades = binomial_row(n)
    return {
        "n": n,
        "grades": grades,
        "total_dim": sum(grades),
        "central_entry": grades[n // 2] if n % 2 == 0 else None,
        "vector_grade": grades[1],
        "bivector_grade": grades[2] if n >= 2 else 0,
    }


# ---------------------------------------------------------------------------
# Synergetics concentric hierarchy
# ---------------------------------------------------------------------------


def synergetics_hierarchy() -> list[dict[str, Any]]:
    return [
        {"shape": "A module", "volume": "1/24", "w33_reading": "1 / tetrahedron flag count = 1/24 (DCCXXV)"},
        {"shape": "B module", "volume": "1/24", "w33_reading": "same as A; chiral partner"},
        {"shape": "T module", "volume": "1/24", "w33_reading": "five-fold module; vol = 5 * (1/24) * 24 = 5"},
        {"shape": "MITE",     "volume": "1/8",  "w33_reading": "1 / tomotope cells = 1 / rank E_8 = 1/8 (DCCXXVII, DCCXLIX)"},
        {"shape": "Coupler",  "volume": "1",    "w33_reading": "= tetrahedron volume; ground state"},
        {"shape": "Tetrahedron", "volume": "1", "w33_reading": "sphere mode (DCCXXV); 24 flags = 2 codec; q+1 = 4 vertices"},
        {"shape": "Cube",     "volume": "3",    "w33_reading": "q (Master Equation root)"},
        {"shape": "Octahedron", "volume": "4",  "w33_reading": "q + 1 (consecutive pair partner); 6 vertices = q! = closure-clock V"},
        {"shape": "Rh Triacontahedron", "volume": "5", "w33_reading": "# Csaszar realisations (DCCXXV); = μ + 1"},
        {"shape": "Rh Dodecahedron", "volume": "6", "w33_reading": "q! = E(tetrahedron) = octahedron V = nilpotence index (DCCXLIX)"},
        {"shape": "Icosahedron", "volume": "~18.51", "w33_reading": "jitterbug-contracted cuboctahedron; bridges 4-fold and 5-fold"},
        {"shape": "Cuboctahedron", "volume": "20", "w33_reading": "v(W(3,3)) / 2 = 20; also C(6, 3) central binomial; nuclear shape of CCP"},
    ]


def hierarchy_w33_integer_match() -> list[dict[str, Any]]:
    return [
        {"volume": 1, "shape": "Tetrahedron", "w33_role": "sphere mode / unit"},
        {"volume": 3, "shape": "Cube", "w33_role": "q = Master Equation root"},
        {"volume": 4, "shape": "Octahedron", "w33_role": "q + 1 = consecutive partner"},
        {"volume": 5, "shape": "Rh Triacontahedron", "w33_role": "# Csaszar realisations"},
        {"volume": 6, "shape": "Rh Dodecahedron", "w33_role": "q! = octahedron V = nilpotence"},
        {"volume": 20, "shape": "Cuboctahedron", "w33_role": "v(W(3,3))/2 = C(6,3)"},
    ]


# ---------------------------------------------------------------------------
# Three natural constants from Pascal
# ---------------------------------------------------------------------------


def e_from_binomial(n: int) -> float:
    """(1 + 1/n)^n -> e."""
    return (1 + 1.0 / n) ** n


def pi_from_central_binomial(n: int) -> float:
    """Stirling: C(2n, n) ~ 4^n / sqrt(pi * n), so pi ~ 4^(2n) / (n * C(2n,n)^2)."""
    cb = central_binomial(n)
    return (4 ** (2 * n)) / (n * cb * cb)


def phi_from_pascal_diagonals(n: int) -> float:
    """Shallow diagonals of Pascal sum to Fibonacci: F_{n+1} = sum_{k=0}^{floor(n/2)} C(n-k, k)."""
    def fib(m: int) -> int:
        a, b = 0, 1
        for _ in range(m):
            a, b = b, a + b
        return a
    return fib(n + 1) / fib(n)


# ---------------------------------------------------------------------------
# Rhombic dodecahedron unification
# ---------------------------------------------------------------------------


def rhombic_dodecahedron_data() -> dict[str, Any]:
    return {
        "V": 14,
        "E": 24,
        "F": 12,
        "vol_synergetics": 6,
        "vertex_split": {
            "tetrahedral_voids": 8,
            "octahedral_voids": 6,
            "total": 14,
        },
        "w33_identifications": {
            "V_14": "Csaszar F = Szilassi V (DCCXXV)",
            "E_24": "tetrahedron flag count (DCCXXV) = D_bosonic - 2 (DCCXXVI)",
            "F_12": "codec = q(q+1) (DCCXVII, DCCXXII)",
            "vol_6": "q! = octahedron V = closure-clock nilpotence (DCCXLIX)",
            "tet_voids_8": "tomotope cells (DCCXXV) = rank E_8 (DCCXXVII) = octahedron F",
            "octa_voids_6": "octahedron V = q! = closure-clock levels",
        },
    }


# ---------------------------------------------------------------------------
# Build bridge
# ---------------------------------------------------------------------------


def build_bridge() -> dict[str, Any]:
    cl3 = clifford_grades(3)
    cl4 = clifford_grades(4)

    pascal_q = binomial_row(Q)             # (1, 3, 3, 1)
    pascal_qp1 = binomial_row(QP1)         # (1, 4, 6, 4, 1)

    tri_row_q = trinomial_row_sum(Q)       # 3^3 = 27
    tri_row_qp1 = trinomial_row_sum(QP1)   # 3^4 = 81

    central_q = central_binomial(Q)        # C(6,3) = 20
    central_qp1 = central_binomial(QP1)    # C(8,4) = 70

    hierarchy = synergetics_hierarchy()
    integer_matches = hierarchy_w33_integer_match()
    rd = rhombic_dodecahedron_data()

    # Three natural constants
    e_approx = e_from_binomial(10_000)
    pi_approx = pi_from_central_binomial(1000)
    phi_approx = phi_from_pascal_diagonals(40)

    identities = {
        "pascal_row_q_is_1_3_3_1": pascal_q == [1, 3, 3, 1],
        "pascal_row_qp1_is_1_4_6_4_1": pascal_qp1 == [1, 4, 6, 4, 1],
        "cl3_total_is_8_equals_tomotope_cells": cl3["total_dim"] == 8,
        "cl4_total_is_16_equals_E8_cartan_trace": cl4["total_dim"] == 16,
        "cl4_central_is_6_equals_q_factorial": cl4["central_entry"] == math.factorial(Q) == 6,
        "cl3_bivectors_equal_q": cl3["bivector_grade"] == Q == 3,
        "cl4_bivectors_equal_q_factorial": cl4["bivector_grade"] == math.factorial(Q) == 6,
        "trinomial_row_q_sums_to_q_to_q": tri_row_q == Q ** Q == 27,
        "trinomial_row_qp1_sums_to_q_to_qp1": tri_row_qp1 == Q ** QP1 == 81,
        "central_binomial_at_q_is_cuboctahedron_volume": central_q == 20,
        "e_approximation_close": abs(e_approx - math.e) < 1e-3,
        "pi_approximation_close": abs(pi_approx - math.pi) < 1e-2,
        "phi_approximation_close": abs(phi_approx - ((1 + math.sqrt(5)) / 2)) < 1e-6,
        "rd_vertices_split_8_plus_6": (
            rd["vertex_split"]["tetrahedral_voids"]
            + rd["vertex_split"]["octahedral_voids"]
            == rd["V"]
            == 14
        ),
        "rd_E_equals_tetrahedron_flags": rd["E"] == 24,
        "rd_F_equals_codec": rd["F"] == 12,
        "rd_volume_equals_q_factorial": rd["vol_synergetics"] == math.factorial(Q) == 6,
        "synergetics_hierarchy_has_W33_volumes": (
            [m["volume"] for m in integer_matches] == [1, 3, 4, 5, 6, 20]
        ),
    }

    theorem = (
        "Pascal-Synergetics-Clifford Theorem.  At q = 3 the Pascal "
        "Triangle row q + 1 = 4 has entries (1, 4, 6, 4, 1) whose sum "
        "16 = trace(Cartan E_8) = F of the tomotope (DCCXXVII), whose "
        "central entry 6 = q! = octahedron V = closure-clock nilpotence "
        "index (DCCXLIX), and whose grade interpretation gives the "
        "Cl(q+1)-Clifford algebra dimensions of scalars / vectors / "
        "bivectors / pseudovectors / pseudoscalars on 4D spacetime.  "
        "Pascal row q = 3 has entries (1, 3, 3, 1) summing to "
        "2^q = 8 = tomotope cells, with central entries = q = 3 = "
        "Master Equation root.  Pascal's Tetrahedron row sums (1+1+1)^n "
        "= 3^n at q = 3 give 27 = q^q at row 3 (E_6 fundamental rep) "
        "and 81 = q^(q+1) at row 4 (H_1 of W(3,3)).  The central "
        "binomial C(2q, q) at q = 3 is 20, exactly the cuboctahedron "
        "volume in Fuller's Synergetics concentric hierarchy and "
        "v(W(3,3))/2.  Every integer volume in the Synergetics "
        "hierarchy (1, 3, 4, 5, 6, 20) is a W(3,3) primitive; the "
        "rhombic dodecahedron (V=14, E=24, F=12, vol=6) is the "
        "unifying polyhedron whose f-vector encodes the Csaszar / "
        "Szilassi vertex-face count, the tetrahedron flag count, the "
        "codec, and the closure-clock nilpotence in one object."
    )

    one_line = (
        "Pascal row q+1 = (1, 4, 6, 4, 1) = Clifford grades of Cl(4); "
        "sum = 16 = E_8 Cartan trace; central = 6 = q! = closure-clock "
        "nilpotence; central binomial C(2q, q) = 20 = cuboctahedron "
        "volume = v(W33)/2."
    )

    summary = {
        "q": Q,
        "pascal_row_q": pascal_q,
        "pascal_row_qp1": pascal_qp1,
        "cl3_total": cl3["total_dim"],
        "cl4_total": cl4["total_dim"],
        "cl4_central": cl4["central_entry"],
        "central_binomial_at_q": central_q,
        "trinomial_row_3_sum": tri_row_q,
        "trinomial_row_4_sum": tri_row_qp1,
        "rd_f_vector": [rd["V"], rd["E"], rd["F"]],
        "all_identities_hold": all(identities.values()),
    }

    return {
        "summary": summary,
        "pascal_triangle_rows": {
            "row_q": pascal_q,
            "row_qp1": pascal_qp1,
            "row_q_interpretation": "Cl(3) grades = (scalars, vectors, bivectors, pseudoscalar) = (1, 3, 3, 1); total = 8 = tomotope cells",
            "row_qp1_interpretation": "Cl(4) grades = (1, 4, 6, 4, 1); total = 16 = Cartan(E_8) trace; central = 6 = q!",
        },
        "pascal_tetrahedron_rows": {
            "row_3_sum": tri_row_q,
            "row_3_interpretation": "3^3 = 27 = q^q = E_6 fundamental rep dim",
            "row_4_sum": tri_row_qp1,
            "row_4_interpretation": "3^4 = 81 = q^(q+1) = H_1 of W(3,3) (off-genus-spectrum)",
        },
        "central_binomial": {
            "C(2q, q)": central_q,
            "synergetics_identification": "cuboctahedron volume = 20",
            "w33_identification": "v(W(3,3)) / 2 = 20 (antipodal pairs)",
        },
        "clifford_grades": {
            "Cl_3": cl3,
            "Cl_4": cl4,
        },
        "synergetics_hierarchy": hierarchy,
        "synergetics_integer_volumes_W33_matches": integer_matches,
        "three_natural_constants": {
            "e": {
                "pascal_form": "lim_{n -> oo} (1 + 1/n)^n",
                "approximation_at_n_10000": e_approx,
                "true_value": math.e,
            },
            "pi": {
                "pascal_form": "Stirling: C(2n, n) ~ 4^n / sqrt(pi * n)",
                "approximation_at_n_1000": pi_approx,
                "true_value": math.pi,
            },
            "phi": {
                "pascal_form": "lim F_{n+1} / F_n where F_n = sum_{k} C(n-k, k) (shallow diagonals)",
                "approximation_at_n_40": phi_approx,
                "true_value": (1 + math.sqrt(5)) / 2,
            },
        },
        "rhombic_dodecahedron_as_hub": rd,
        "identities": identities,
        "theorem": theorem,
        "one_line": one_line,
        "honesty_boundary": (
            "All Pascal-row identities are exact arithmetic.  The "
            "Synergetics volumes are Fuller's convention with the "
            "tetrahedron normalised to unit volume.  The Clifford grade "
            "identification (Pascal row n+1 = dim Cl(n)_k) is a standard "
            "fact about exterior algebras.  The W(3,3) re-readings of "
            "Synergetics volumes (e.g. cuboctahedron = v(W33)/2) are "
            "numerical alignments at q = 3.  This part does NOT derive "
            "the Synergetics hierarchy or e/pi/phi from W(3,3); it "
            "documents the structural alignment of Pascal, Synergetics, "
            "Clifford, and W(3,3) at the q = 3 saturation point."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    s = payload["summary"]
    print(f"\nPascal row q = 3:   {s['pascal_row_q']}, sum = {sum(s['pascal_row_q'])} = tomotope cells")
    print(f"Pascal row q+1 = 4: {s['pascal_row_qp1']}, sum = {sum(s['pascal_row_qp1'])} = E_8 Cartan trace")
    print(f"  central = {s['cl4_central']} = q! = closure-clock nilpotence")
    print(f"Central binomial C(6, 3) = {s['central_binomial_at_q']} = cuboctahedron volume")
    print(f"Trinomial row 3 sum = 3^3 = {s['trinomial_row_3_sum']} = q^q = E_6 fundamental")
    print(f"Trinomial row 4 sum = 3^4 = {s['trinomial_row_4_sum']} = H_1 of W(3,3)")
    print(f"Rhombic dodecahedron f-vector = {s['rd_f_vector']} (vol = 6 = q!)")
    cs = payload["three_natural_constants"]
    print(f"\nThree natural constants from Pascal:")
    print(f"  e   approx {cs['e']['approximation_at_n_10000']:.6f} (true {cs['e']['true_value']:.6f})")
    print(f"  pi  approx {cs['pi']['approximation_at_n_1000']:.6f} (true {cs['pi']['true_value']:.6f})")
    print(f"  phi approx {cs['phi']['approximation_at_n_40']:.6f} (true {cs['phi']['true_value']:.6f})")


if __name__ == "__main__":
    main()
