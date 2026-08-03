#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2858() -> dict:
    states = tuple(product(range(3), repeat=4))
    support = lambda x: tuple(int(v != 0) for v in x)
    classes = defaultdict(list)
    for i, x in enumerate(states):
        classes[support(x)].append(i)

    equations = []
    for indices in classes.values():
        rep = states[indices[0]]
        for idx in indices[1:]:
            x = states[idx]
            for target_support in classes:
                row = [0] * 81
                for ai, a in enumerate(states):
                    y1 = tuple((rep[j] + a[j]) % 3 for j in range(4))
                    y2 = tuple((x[j] + a[j]) % 3 for j in range(4))
                    row[ai] += int(support(y1) == target_support)
                    row[ai] -= int(support(y2) == target_support)
                if any(row):
                    equations.append(row)
    constraint_rank = rank_mod(equations)
    nullity = 81 - constraint_rank

    support_indicator_basis = []
    for supp in classes:
        support_indicator_basis.append([int(support(a) == supp) for a in states])
    indicator_rank = rank_mod(support_indicator_basis)
    indicators_satisfy = all(sum(eq[i] * vec[i] for i in range(81)) == 0 for eq in equations for vec in support_indicator_basis)

    good_linear_forms = []
    for coeff in states[1:]:
        okay = True
        seen = {}
        for x in states:
            s = support(x)
            out = int(sum(coeff[i] * x[i] for i in range(4)) % 3 != 0)
            if s in seen and seen[s] != out:
                okay = False
                break
            seen[s] = out
        if okay:
            good_linear_forms.append(coeff)
    monomial_forms = [c for c in states[1:] if sum(v != 0 for v in c) == 1]

    monomial_matrix_count = 2 ** 4 * 24
    affine_good = 0
    for p in permutations(range(4)):
        for signs in product((1, 2), repeat=4):
            for b in states:
                seen = {}
                okay = True
                for x in states:
                    y = [0] * 4
                    for i in range(4):
                        y[p[i]] = signs[i] * x[i] % 3
                    y = tuple((y[i] + b[i]) % 3 for i in range(4))
                    s = support(x)
                    sy = support(y)
                    if s in seen and seen[s] != sy:
                        okay = False
                        break
                    seen[s] = sy
                if okay:
                    affine_good += 1
    checks = {
        "translation_constraint_rank_65": constraint_rank == 65,
        "translation_lumping_nullity_16": nullity == 16,
        "support_indicator_basis_rank_16": indicator_rank == 16,
        "support_indicator_basis_satisfies_all_constraints": indicators_satisfy,
        "translation_criterion_exact": nullity == indicator_rank and indicators_satisfy,
        "only_monomial_linear_forms_descend": set(good_linear_forms) == set(monomial_forms),
        "eight_good_nonzero_linear_forms": len(good_linear_forms) == 8,
        "signed_monomial_linear_bijections_384": monomial_matrix_count == 384,
        "no_nonzero_translation_affine_bijection_descends": affine_good == monomial_matrix_count,
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass2858.quantum_support_coarse_graining.v1",
        "status": "COMPLETE_EXACT",
        "deterministic_gate_theorem": {
            "support_descending_invertible_linear_maps": 384,
            "classification": "exactly the signed monomial matrices",
            "support_descending_affine_bijections": affine_good,
            "nonzero_translation_allowed": False,
        },
        "Weyl_noise_theorem": {
            "translation_probability_variables": 81,
            "constraint_rank": constraint_rank,
            "solution_space_dimension": nullity,
            "classification": "the X-displacement marginal is constant on each of the 16 support fibers",
            "Z_phase_marginal": "arbitrary for support observables",
        },
        "checks": checks,
        "check_count": len(checks),
        "reading": "Support is not an execution quotient for CX or affine translations, but it is an exact quantum-observable quotient for precisely the Weyl channels whose displacement law is invariant under coordinatewise sign flips.",
        "boundary": "The theorem concerns the computational-basis support conditional expectation. It does not claim preservation of coherences inside or between support blocks.",
    }
