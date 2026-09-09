#!/usr/bin/env python3
"""Explicit GF(4)->GF(2) trace gauges for the Marcelis/Witting atlas.

Source-faithful layer
---------------------
Marcelis' Penrose/Witting page fixes the Pauli/GF(4) alphabet

    I -> 0,  Y -> 1,  X -> omega,  Z -> omega^2,

and his E8 four-qubit page then applies Tr(x)=x+x^2.  Since

    Tr(0)=Tr(1)=0,  Tr(omega)=Tr(omega^2)=1,

the induced word map is simply I,Y -> 0 and X,Z -> 1.  A Pauli word is a
chosen representative, so this map is perfectly well-defined on the word.
It is NOT invariant under arbitrary GF(4)^* rescaling of a homogeneous vector,
which is why coordinatewise trace alone is not a map PG(3,4)->PG(3,2).

Source audit
------------
The E8 four-qubit page has an internal two-entry transcription mismatch in the
complement row.  For the listed words ... ZYZZ, YZZZ, ZYYZ, YYYZ ... it prints
binary ... 1011, 1001, 0111, 0001 ... but immediately gives decimal
... 11, 7, 9, 1 ....  The declared trace rule gives binary
... 1011, 0111, 1001, 0001 ..., whose decimals are exactly 11,7,9,1.
Thus the algebra and the source decimal list agree; the printed binary entries
for YZZZ and ZYYZ are transposed.  This certificate records rather than hides
that source inconsistency.

Projective completion added here
--------------------------------
To make a total projective map, choose an explicit section of each homogeneous
class: scale the first nonzero coordinate to omega.  Its trace is then 1, so
the traced binary vector is never zero.  Therefore

    tau_omega : PG(3,4) -> PG(3,2)
    [v] |-> Tr(g_omega(v))

is a well-defined total map once the ordered-coordinate gauge is declared.
It is invariant under changing the input representative, but it is a gauge-
fixed coordinate map, not a PGL(4,4)-canonical construction.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_marcelis_gf4_trace_gauge.json"

GF4_MUL = (
    (0, 0, 0, 0),
    (0, 1, 2, 3),
    (0, 2, 3, 1),
    (0, 3, 1, 2),
)
PAULI_TO_GF4 = {"I": 0, "Y": 1, "X": 2, "Z": 3}


def gf4_add(a: int, b: int) -> int:
    return a ^ b


def gf4_mul(a: int, b: int) -> int:
    return GF4_MUL[a][b]


def gf4_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError
    for b in (1, 2, 3):
        if gf4_mul(a, b) == 1:
            return b
    raise AssertionError(a)


def gf4_trace(a: int) -> int:
    return gf4_add(a, gf4_mul(a, a))


def scale(v, scalar):
    return tuple(gf4_mul(scalar, x) for x in v)


def trace_vector(v):
    return tuple(gf4_trace(x) for x in v)


def word_to_gf4(word: str):
    if len(word) != 4 or any(ch not in PAULI_TO_GF4 for ch in word):
        raise ValueError("four-letter Pauli word over IXYZ required")
    return tuple(PAULI_TO_GF4[ch] for ch in word)


def marcelis_word_trace(word: str):
    return trace_vector(word_to_gf4(word))


def bits_text(bits):
    return "".join(str(x) for x in bits)


def canon_first_one(v):
    for x in v:
        if x:
            return scale(v, gf4_inv(x))
    raise ValueError("zero vector")


def projective_points_pg34():
    return tuple(sorted({
        canon_first_one(v)
        for v in product(range(4), repeat=4)
        if any(v)
    }))


def omega_gauge(v):
    for x in v:
        if x:
            return scale(v, gf4_mul(2, gf4_inv(x)))
    raise ValueError("zero vector")


def projective_trace_gauge(v):
    traced = trace_vector(omega_gauge(v))
    assert any(traced), "first nonzero omega has trace one"
    return traced


def first_one_index(bits):
    return next(i for i, x in enumerate(bits) if x)


def bits_decimal(bitstring: str) -> int:
    return int(bitstring, 2)


def source_examples():
    plane_words = ["YYYY", "ZZYY", "YZYY", "ZYYY", "YZZY", "ZZZY", "YYZY", "ZYZY"]
    plane_bits = ["0000", "1100", "0100", "1000", "0110", "1110", "0010", "1010"]
    complement_words = ["ZZZZ", "YYZZ", "ZYZZ", "YZZZ", "ZYYZ", "YYYZ", "ZZYZ", "YZYZ"]
    # Printed binary sequence on the source page; entries 4 and 5 conflict
    # with both the declared trace rule and the page's following decimal list.
    complement_printed_bits = ["1111", "0011", "1011", "1001", "0111", "0001", "1101", "0101"]
    complement_printed_decimals = [15, 3, 11, 7, 9, 1, 13, 5]
    return (
        plane_words,
        plane_bits,
        complement_words,
        complement_printed_bits,
        complement_printed_decimals,
    )


def build_result():
    trace_table = [gf4_trace(x) for x in range(4)]
    points = projective_points_pg34()
    assert len(points) == 85

    representative_checks = 0
    for p in points:
        target = projective_trace_gauge(p)
        for scalar in (1, 2, 3):
            assert projective_trace_gauge(scale(p, scalar)) == target
            representative_checks += 1

    fibres = Counter(projective_trace_gauge(p) for p in points)
    assert len(fibres) == 15
    fibre_size_histogram = Counter(fibres.values())
    first_one_law = {}
    for binary, size in sorted(fibres.items()):
        j = first_one_index(binary)
        expected = 2 ** (3 - j)
        assert size == expected
        first_one_law[bits_text(binary)] = {
            "first_one_index": j,
            "fibre_size": size,
        }

    (
        plane_words,
        plane_bits,
        comp_words,
        comp_printed_bits,
        comp_printed_decimals,
    ) = source_examples()
    reproduced_plane = [bits_text(marcelis_word_trace(w)) for w in plane_words]
    reproduced_comp = [bits_text(marcelis_word_trace(w)) for w in comp_words]
    reproduced_comp_decimals = [bits_decimal(x) for x in reproduced_comp]
    mismatch_positions = [
        i for i, (a, b) in enumerate(zip(reproduced_comp, comp_printed_bits))
        if a != b
    ]

    raw_counterexample = {
        "representative": [1, 0, 0, 0],
        "scaled_same_projective_point": [2, 0, 0, 0],
        "raw_trace_representative": bits_text(trace_vector((1, 0, 0, 0))),
        "raw_trace_scaled": bits_text(trace_vector((2, 0, 0, 0))),
    }

    checks = {
        "trace_table_is_0_0_1_1": trace_table == [0, 0, 1, 1],
        "marcelis_plane_examples_reproduced": reproduced_plane == plane_bits,
        "complement_algebra_matches_source_decimal_list": (
            reproduced_comp_decimals == comp_printed_decimals
        ),
        "source_complement_binary_has_exact_two_entry_transposition": (
            mismatch_positions == [3, 4]
            and reproduced_comp[3] == comp_printed_bits[4]
            and reproduced_comp[4] == comp_printed_bits[3]
        ),
        "raw_coordinate_trace_fails_projective_invariance": (
            raw_counterexample["raw_trace_representative"] != raw_counterexample["raw_trace_scaled"]
        ),
        "pg34_has_85_points": len(points) == 85,
        "omega_gauge_is_representative_invariant": representative_checks == 85 * 3,
        "omega_gauge_hits_all_15_pg32_points": len(fibres) == 15,
        "omega_gauge_fibre_histogram_is_1_2_4_8_staircase": (
            dict(sorted(fibre_size_histogram.items())) == {1: 1, 2: 2, 4: 4, 8: 8}
        ),
        "all_fibre_sizes_obey_first_one_law": all(
            row["fibre_size"] == 2 ** (3 - row["first_one_index"])
            for row in first_one_law.values()
        ),
    }

    return {
        "schema": "w33.marcelis-gf4-trace-gauge.v2",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "marcelis_source_gauge": {
            "pauli_to_gf4": {"I": "0", "Y": "1", "X": "omega", "Z": "omega^2"},
            "trace_table": {"0": 0, "1": 0, "omega": 1, "omega^2": 1},
            "word_rule": "I,Y -> 0; X,Z -> 1 coordinatewise",
            "plane_example_words": plane_words,
            "plane_example_bits": reproduced_plane,
            "complement_example_words": comp_words,
            "complement_algebraic_bits": reproduced_comp,
            "complement_source_printed_bits": comp_printed_bits,
            "complement_source_printed_decimals": comp_printed_decimals,
            "complement_algebraic_decimals": reproduced_comp_decimals,
            "source_binary_mismatch_positions_zero_based": mismatch_positions,
            "source_audit": (
                "The source binary list swaps YZZZ/ZYYZ outputs (positions 3 and 4). "
                "Its following decimal list agrees exactly with the declared GF(4) "
                "trace algebra, so the binary pair is recorded as a source "
                "transcription mismatch rather than imported as mathematics."
            ),
            "interpretation": (
                "The Pauli word fixes a representative before trace. This is why "
                "Marcelis can use the trace consistently in operator tables even "
                "though raw trace does not descend from homogeneous GF4 vectors."
            ),
        },
        "raw_projective_trace_firewall": raw_counterexample,
        "projective_completion": {
            "definition": (
                "For [v] in PG(3,4), scale the first nonzero coordinate to omega, "
                "then apply coordinatewise GF4/F2 trace."
            ),
            "domain_points": 85,
            "image_points": 15,
            "image": "all nonzero vectors of F2^4 = PG(3,2) points",
            "fibre_size_histogram": {
                str(size): count for size, count in sorted(fibre_size_histogram.items())
            },
            "fibre_mass_identity": "1*1 + 2*2 + 4*4 + 8*8 = 85",
            "first_one_fibre_law": "|tau_omega^{-1}(b)| = 2^(3-j), j = index of first 1 in b",
            "first_one_rows": first_one_law,
        },
        "relation_to_marcelis": (
            "The source-faithful Pauli-word trace is Marcelis' operator-table "
            "construction. The omega-normalized PG(3,4)->PG(3,2) map is a new "
            "explicit gauge completion introduced here to remove homogeneous-"
            "representative ambiguity; it is not claimed to be Marcelis' original "
            "implicit normalization."
        ),
        "claim_boundary": [
            "The projective completion depends on the ordered-coordinate/first-nonzero gauge and is not PGL(4,4)-canonical.",
            "The trace map is a coordinate/label bridge, not an isomorphism between PG(3,4) and PG(3,2).",
            "The complement-row source mismatch is textual; the declared trace algebra and the source decimal list agree.",
            "No physical cryptographic security follows from the fibre sizes alone.",
        ],
        "sources": [
            "https://fgmarcelis.wordpress.com/2018/02/21/penrose-dodecahedron-witting-polytope/",
            "https://fgmarcelis.wordpress.com/e8-%C2%A714-four-qubits/",
        ],
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "plane_examples": result["checks"]["marcelis_plane_examples_reproduced"],
        "complement_decimal_audit": result["checks"]["complement_algebra_matches_source_decimal_list"],
        "source_binary_transposition_detected": result["checks"]["source_complement_binary_has_exact_two_entry_transposition"],
        "pg34_points": result["projective_completion"]["domain_points"],
        "pg32_image_points": result["projective_completion"]["image_points"],
        "fibre_histogram": result["projective_completion"]["fibre_size_histogram"],
    }, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
