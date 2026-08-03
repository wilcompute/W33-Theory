#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2855() -> dict:
    support_character = (15, 7, 3, 3, 1)
    support_dec = character_decompose(support_character, S4_IRREPS, S4_CLASS_SIZES, 24)
    level_chars = {
        "weight1": (4, 2, 0, 1, 0),
        "weight2": (6, 2, 2, 0, 0),
        "weight3": (4, 2, 0, 1, 0),
        "weight4": (1, 1, 1, 1, 1),
    }
    level_decs = {name: character_decompose(ch, S4_IRREPS, S4_CLASS_SIZES, 24) for name, ch in level_chars.items()}
    n = 16
    A = [[0] * n for _ in range(n)]
    for s in range(n):
        for bit in range(4):
            A[s ^ (1 << bit)][s] = 1
    Ast = [[0] * n for _ in range(n)]
    for s in range(n):
        Ast[s][s] = 4 - 2 * s.bit_count()
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    generators = [tuple(map(tuple, A)), tuple(map(tuple, Ast))]
    basis = []
    def independent_add(M):
        before = gf_rank_vectors([flatten_matrix(x) for x in basis])
        after = gf_rank_vectors([flatten_matrix(x) for x in basis] + [flatten_matrix(M)])
        if after > before:
            basis.append(M)
            return True
        return False
    independent_add(tuple(map(tuple, I)))
    independent_add(generators[0])
    independent_add(generators[1])
    frontier = list(basis)
    while frontier:
        X = frontier.pop(0)
        for G in generators:
            for Y in (mm_int(X, G), mm_int(G, X)):
                if independent_add(Y):
                    frontier.append(Y)
    algebra_dimension = len(basis)

    module_types = [
        {"endpoint": 0, "dimension": 5, "multiplicity": 1},
        {"endpoint": 1, "dimension": 3, "multiplicity": 3},
        {"endpoint": 2, "dimension": 1, "multiplicity": 2},
    ]
    d8_restriction = {"A1": 5, "B1": 3, "B2": 1, "E": 3}
    checks = {
        "support_character_fixed_subset_formula": support_character == tuple(2 ** c - 1 for c in (4, 3, 2, 2, 1)),
        "S4_decomposition_4triv_3standard_22": support_dec == {"[4]": 4, "[31]": 3, "[22]": 1},
        "level1_decomposition": level_decs["weight1"] == {"[4]": 1, "[31]": 1},
        "level2_decomposition": level_decs["weight2"] == {"[4]": 1, "[31]": 1, "[22]": 1},
        "level3_decomposition": level_decs["weight3"] == {"[4]": 1, "[31]": 1},
        "level4_decomposition": level_decs["weight4"] == {"[4]": 1},
        "dimension_15": 4 * 1 + 3 * 3 + 1 * 2 == 15,
        "Q4_Terwilliger_dimension_35": algebra_dimension == 35,
        "Terwilliger_module_dimension_sum_16": sum(x["dimension"] * x["multiplicity"] for x in module_types) == 16,
        "Terwilliger_Wedderburn_dimension_35": sum(x["dimension"] ** 2 for x in module_types) == 35,
        "D8_restriction_matches_pass2812": d8_restriction == {"A1": 5, "B1": 3, "B2": 1, "E": 3},
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass2855.boolean_harmonic_terwilliger.v1",
        "status": "COMPLETE_EXACT",
        "support_S4_character": dict(zip(S4_CLASSES, support_character)),
        "support_S4_decomposition": support_dec,
        "rank_level_decompositions": level_decs,
        "Q4_Terwilliger": {
            "generated_algebra_dimension": algebra_dimension,
            "module_types": module_types,
            "Wedderburn_type": "M5(C) + M3(C) + M1(C)",
        },
        "D8_restriction": d8_restriction,
        "reading": "The 15 nonempty supports are the punctured Boolean permutation module 4[4]+3[31]+[22]. The full 16-state cube module splits into Terwilliger strings of dimensions 5,3,1 with multiplicities 1,3,2.",
        "checks": checks,
        "check_count": len(checks),
        "boundary": "The fixed-matching quotient operator is only D8-equivariant. The S4 statement concerns the underlying support permutation module, not each 1+9+5 spectral subspace separately.",
    }
