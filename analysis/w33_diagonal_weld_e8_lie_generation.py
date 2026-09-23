#!/usr/bin/env python3
"""Certify the diagonal H27 phase weld as a two-generator E8 switch.

The preceding cubic certificate singled out four integer matter backgrounds on
K = H27 x C3_ext:

    center    = 1 + c,
    external  = 1 + p,
    plus      = 1 + (c+p mod 3),
    minus     = 1 + (c-p mod 3).

Lift one background to the signed grade-one root chart and a second background
to the paired signed grade-two chart in the frozen W33-discrete Chevalley E8.
For generators x,y, the Lie algebra they generate is the smallest vector space
containing x,y and stable under ad_x and ad_y.  This gives a finite Krylov-style
closure calculation: every inserted vector is bracketed only with x and y.

All 16 grade-one/grade-two choices are tested modulo 103.  Every pair with a
diagonal background on either side reaches dimension 248.  Reduction modulo a
prime can only decrease rational rank, so dimension 248 modulo 103 proves that
the corresponding rational Chevalley Lie closure is all E8.  Four orientation
representatives are independently replayed modulo 109.

The four pairs using only center/external backgrounds are closed exactly over Q
with Fraction arithmetic.  They all give the same 24-dimensional subalgebra,
with grading dimensions 6+9+9.  Its possible relation to a trinification A2^3
subalgebra is deliberately left open pending an explicit ideal/root audit.

Internal ownership and rediscovery checks are documented in
analysis/2026-09-23_diagonal_weld_e8_lie_generation.md and its paper surface
analysis/PASS20260923_diagonal_weld_e8_lie_generation_insert.tex.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_diagonal_weld_e8_lie_generation.json"


def load_inputs():
    compiler = json.loads((ROOT / "data/w33_e8_full_hybrid_chevalley_compiler.json").read_text())
    source = json.loads((ROOT / "artifacts/e8_structure_constants_w33_discrete.json").read_text())
    bridge = json.loads((ROOT / "data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    weld = json.loads((ROOT / "data/w33_e6_cubic_diagonal_phase_weld.json").read_text())
    assert compiler["checks"]["all_2511496_source_Jacobi_triples_zero"] is True
    assert compiler["source"]["dimension"] == 248
    assert compiler["source"]["grading_dimensions"] == [86, 81, 81]
    assert bridge["incidence"]["mapped_full45_equal"] is True
    assert weld["checks"]["both_diagonal_welds_cover_full_retyped_quotient"] is True
    table = {
        tuple(map(int, key.split(","))): [(int(k), int(c)) for k, c in terms]
        for key, terms in source["brackets"].items()
    }
    return compiler, bridge, table


def backgrounds(bridge):
    e6_to_h = {
        int(i): tuple(map(int, h))
        for i, h in bridge["maps"]["e6id_to_current_H27_address"].items()
    }
    coords = [(e6_to_h[eid], p) for eid in range(27) for p in range(3)]
    out = {
        "center": [1 + h[2] for h, p in coords],
        "external": [1 + p for h, p in coords],
        "plus": [1 + ((h[2] + p) % 3) for h, p in coords],
        "minus": [1 + ((h[2] - p) % 3) for h, p in coords],
    }
    assert all(Counter(v) == Counter({1: 27, 2: 27, 3: 27}) for v in out.values())
    return out


def source_generators(compiler, amplitudes):
    maps = compiler["coordinate_maps"]
    out = {}
    for grade in (1, 2):
        indices = maps[f"grade{grade}_source_indices"]
        signs = maps[f"grade{grade}_signs"]
        for name, values in amplitudes.items():
            vector = [0] * 248
            for value, sign, index in zip(values, signs, indices):
                vector[index] = int(value) * int(sign)
            assert sum(x != 0 for x in vector) == 81
            out[(grade, name)] = vector
    return out


def bracket(left, right, table, modulus=None):
    out = [0] * 248
    ls = [(i, x) for i, x in enumerate(left) if x]
    rs = [(i, x) for i, x in enumerate(right) if x]
    for i, x in ls:
        for j, y in rs:
            if i == j:
                continue
            sign = 1 if i < j else -1
            for k, coefficient in table.get((min(i, j), max(i, j)), ()):
                out[k] += sign * x * y * coefficient
                if modulus is not None:
                    out[k] %= modulus
    return out


class ModularBasis:
    def __init__(self, modulus):
        self.modulus = modulus
        self.rows = {}
        self.vectors = []
        self.depths = []

    def add(self, vector, depth):
        p = self.modulus
        vector = [int(x) % p for x in vector]
        for pivot in sorted(self.rows):
            if vector[pivot]:
                factor = vector[pivot]
                row = self.rows[pivot]
                vector = [(x - factor * y) % p for x, y in zip(vector, row)]
        pivot = next((i for i, x in enumerate(vector) if x), None)
        if pivot is None:
            return False
        inverse = pow(vector[pivot], -1, p)
        vector = [(x * inverse) % p for x in vector]
        self.rows[pivot] = vector
        self.vectors.append(vector)
        self.depths.append(depth)
        return True


class RationalBasis:
    def __init__(self):
        self.rows = {}
        self.vectors = []
        self.depths = []

    def add(self, vector, depth):
        vector = list(map(Fraction, vector))
        for pivot in sorted(self.rows):
            if vector[pivot]:
                factor = vector[pivot]
                row = self.rows[pivot]
                vector = [x - factor * y for x, y in zip(vector, row)]
        pivot = next((i for i, x in enumerate(vector) if x), None)
        if pivot is None:
            return False
        inverse = 1 / vector[pivot]
        vector = [x * inverse for x in vector]
        self.rows[pivot] = vector
        self.vectors.append(vector)
        self.depths.append(depth)
        return True


def closure(generators, table, basis, modulus=None):
    queue = deque()
    for vector in generators:
        if basis.add(vector, 0):
            queue.append((basis.vectors[-1], 0))
    evaluations = 0
    while queue:
        vector, depth = queue.popleft()
        for generator in generators:
            evaluations += 1
            image = bracket(generator, vector, table, modulus)
            if basis.add(image, depth + 1):
                queue.append((basis.vectors[-1], depth + 1))
    return basis, evaluations


def grade_counts(pivots, compiler):
    maps = compiler["coordinate_maps"]
    sets = {
        "g0": set(maps["neutral_source_indices"]),
        "g1": set(maps["grade1_source_indices"]),
        "g2": set(maps["grade2_source_indices"]),
    }
    return {grade: sum(pivot in indices for pivot in pivots) for grade, indices in sets.items()}


def summarize(basis, evaluations, compiler):
    pivots = sorted(basis.rows)
    return {
        "dimension": len(pivots),
        "grading_dimensions": grade_counts(pivots, compiler),
        "adjoint_generator_evaluations": evaluations,
        "maximum_recorded_bracket_depth": max(basis.depths),
        "insertion_depth_histogram": {
            str(k): v for k, v in sorted(Counter(basis.depths).items())
        },
        "pivot_digest": hashlib.sha256(",".join(map(str, pivots)).encode()).hexdigest(),
    }


def main(write=True):
    compiler, bridge, table = load_inputs()
    amplitudes = backgrounds(bridge)
    vectors = source_generators(compiler, amplitudes)
    names = ("center", "external", "plus", "minus")

    mod103 = {}
    for left, right in itertools.product(names, repeat=2):
        basis, evaluations = closure(
            (vectors[(1, left)], vectors[(2, right)]),
            table,
            ModularBasis(103),
            103,
        )
        mod103[f"{left}|{right}"] = summarize(basis, evaluations, compiler)

    representatives = (
        ("plus", "plus"),
        ("plus", "center"),
        ("center", "plus"),
        ("center", "center"),
    )
    mod109 = {}
    for left, right in representatives:
        basis, evaluations = closure(
            (vectors[(1, left)], vectors[(2, right)]),
            table,
            ModularBasis(109),
            109,
        )
        mod109[f"{left}|{right}"] = summarize(basis, evaluations, compiler)

    rational_controls = {}
    for left, right in itertools.product(("center", "external"), repeat=2):
        basis, evaluations = closure(
            (vectors[(1, left)], vectors[(2, right)]),
            table,
            RationalBasis(),
        )
        summary = summarize(basis, evaluations, compiler)
        summary["pivots"] = sorted(basis.rows)
        rational_controls[f"{left}|{right}"] = summary

    diagonal_names = {"plus", "minus"}
    for left, right in itertools.product(names, repeat=2):
        expected = 248 if left in diagonal_names or right in diagonal_names else 24
        assert mod103[f"{left}|{right}"]["dimension"] == expected
    assert {row["dimension"] for row in mod109.values()} == {24, 248}
    assert all(row["dimension"] == 24 for row in rational_controls.values())
    assert len({row["pivot_digest"] for row in rational_controls.values()}) == 1
    assert all(row["grading_dimensions"] == {"g0": 6, "g1": 9, "g2": 9}
               for row in rational_controls.values())

    grid = {
        left: {right: mod103[f"{left}|{right}"]["dimension"] for right in names}
        for left in names
    }
    out = {
        "schema": "w33.diagonal_weld_e8_lie_generation.v1",
        "status": "PASS_ONE_DIAGONAL_H27_PHASE_WELD_SWITCHES_PAIRED_MATTER_GENERATORS_FROM_COMMON_24D_CLOSURE_TO_ALL_E8",
        "headline": "The diagonal H27-center/external-qutrit correlation is an exact Lie-generation switch. Lift any one of the four three-level backgrounds to signed grade one and any one to paired signed grade two in the frozen W33 Chevalley E8. If neither side is diagonal, all four center/external pairs generate the same exact 24-dimensional subalgebra, graded 6+9+9. If either side uses c+p or c-p, every one of the remaining twelve pairs generates all 248 dimensions, graded 86+81+81. Full generation is certified modulo 103 for all twelve pairs and independently modulo 109 for both one-sided orientations and a matched pair; dimension 248 after reduction proves dimension 248 over Q.",
        "generators": {
            "grade1": "signed current-H27 root lift of one three-level background",
            "grade2": "paired signed current-H27 root lift of one three-level background",
            "backgrounds": {
                "center": "1+c",
                "external": "1+p",
                "plus": "1+((c+p) mod 3)",
                "minus": "1+((c-p) mod 3)",
            },
            "amplitude_multiplicities_each": {"1": 27, "2": 27, "3": 27},
        },
        "generation_method": {
            "identity": "Lie<x,y> is the smallest vector space containing x,y and invariant under ad_x and ad_y",
            "algorithm": "incremental row basis closed under the two adjoint generators",
            "source_bracket": "artifacts/e8_structure_constants_w33_discrete.json",
            "source_jacobi_basis_triples": 2511496,
            "rational_full_rank_logic": "248 independent reductions modulo a prime lift to 248 rationally independent iterated Lie words; the ambient rational algebra has dimension 248",
        },
        "dimension_grid_mod_103": grid,
        "all_cases_mod_103": mod103,
        "orientation_replay_mod_109": mod109,
        "exact_rational_nondiagonal_controls": rational_controls,
        "theorem": {
            "no_diagonal_background_dimension": 24,
            "no_diagonal_background_grading": [6, 9, 9],
            "all_nondiagonal_pairs_same_subspace": True,
            "diagonal_on_either_grade_dimension": 248,
            "diagonal_on_either_grade_grading": [86, 81, 81],
            "matched_diagonal_orientation_required": False,
            "one_diagonal_correlation_is_sufficient": True,
        },
        "external_context": {
            "two_generation_prior_art": "Two-generation is a general theorem for simple Lie algebras; the new finite statement here is that these highly structured current-H27 diagonal backgrounds are explicit generating pairs.",
            "e8_grading_prior_art": "The E8 decomposition 248=(8,1)+(1,78)+(3,27)+(3bar,27bar) under SL3 x E6 is standard; this certificate resolves generation for the repository's explicit signed address backgrounds.",
        },
        "boundary": "This is exact generation of the rational/complex Chevalley Lie algebra by two structured algebra elements. It is not a compact-real-form controllability theorem, a pair of anti-Hermitian laboratory Hamiltonians, a vacuum-selection mechanism, an energy scale, a coupling strength, or a claim that the residual 24-dimensional algebra is SU(3)^3. The 24=A2^3 dimension match remains a hypothesis until its ideals or roots are explicitly identified.",
        "parents": [
            "data/w33_e6_cubic_diagonal_phase_weld.json",
            "data/w33_e8_full_hybrid_chevalley_compiler.json",
            "data/w33_e6id_current_h27_gauge_bridge.json",
            "artifacts/e8_structure_constants_w33_discrete.json",
        ],
        "checks": {
            "all_16_background_pairs_tested_mod103": True,
            "all_12_pairs_with_a_diagonal_side_generate_248": True,
            "both_one_sided_diagonal_orientations_replayed_mod109": True,
            "matched_diagonal_pair_replayed_mod109": True,
            "all_4_nondiagonal_pairs_closed_exactly_over_Q": True,
            "all_4_nondiagonal_pairs_equal_same_24D_subspace": True,
            "nondiagonal_grading_is_6_9_9": True,
            "matching_plus_or_minus_orientation_not_required": True,
            "physical_controllability_not_claimed": True,
            "trinification_identification_not_claimed": True,
        },
    }
    assert all(out["checks"].values())
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
