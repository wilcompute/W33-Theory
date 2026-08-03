#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2854() -> dict:
    js = tuple(j_matrix(m) for m in MATCHINGS)
    perms = tuple(permutations(range(4)))
    hom = defaultdict(set)
    affine_arrow_count = 0
    lambda_profile = Counter()
    permutation_projection = defaultdict(set)

    for source in range(3):
        for p in perms:
            target = matching_index(matching_image(p, MATCHINGS[source]))
            P = permutation_matrix(p)
            for signs in product((1, 2), repeat=4):
                A = matmul_mod(diagonal(signs), P)
                left = matmul_mod(matmul_mod(transpose(A), js[target]), A)
                for lam in (1, 2):
                    if left == scalar_mod(lam, js[source]):
                        affine_arrow_count += 1
                        lambda_profile[lam] += 1
                        hom[(source, target)].add(projective_matrix(A))
                        permutation_projection[(source, target)].add(p)
                        break

    fixed_projection_sizes = []
    fixed_hom_sizes = []
    for source in range(3):
        fixed_projection_sizes.append(len(permutation_projection[(source, source)]))
        fixed_hom_sizes.append(len(hom[(source, source)]))

    composition_closed = True
    for source in range(3):
        for middle in range(3):
            for target in range(3):
                for a in hom[(source, middle)]:
                    for b in hom[(middle, target)]:
                        c = projective_matrix(matmul_mod(b, a))
                        if c not in hom[(source, target)]:
                            composition_closed = False
                            break
                    if not composition_closed:
                        break

    vectors = tuple(product(range(3), repeat=4))
    nonzero = tuple(v for v in vectors if any(v))
    def form(x, J, y):
        return sum(x[i] * J[i][j] * y[j] for i in range(4) for j in range(4)) % 3
    def mv(A, x):
        return tuple(sum(A[i][j] * x[j] for j in range(4)) % 3 for i in range(4))
    zero_relation_preserved = True
    for (source, target), arrows in hom.items():
        for A in arrows:
            for x, y in combinations(nonzero, 2):
                if (form(x, js[source], y) == 0) != (form(mv(A, x), js[target], mv(A, y)) == 0):
                    zero_relation_preserved = False
                    break
            if not zero_relation_preserved:
                break

    checks = {
        "three_polarizations": len(MATCHINGS) == 3,
        "all_homsets_projective_size_32": all(len(hom[(s, t)]) == 32 for s in range(3) for t in range(3)),
        "all_homset_permutation_projections_size_8": all(len(permutation_projection[(s, t)]) == 8 for s in range(3) for t in range(3)),
        "fixed_form_only_D8_projection": fixed_projection_sizes == [8, 8, 8],
        "fixed_form_projective_isotropy_32": fixed_hom_sizes == [32, 32, 32],
        "affine_arrow_count_576": affine_arrow_count == 576,
        "projective_arrow_count_288": sum(len(v) for v in hom.values()) == 288,
        "lambda_split_288_288": lambda_profile == Counter({1: 288, 2: 288}),
        "composition_closed": composition_closed,
        "zero_relation_preserved": zero_relation_preserved,
        "full_S4_fixed_form_obstructed": all(size < 24 for size in fixed_projection_sizes),
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass2854.polarization_groupoid.v1",
        "status": "COMPLETE_EXACT_WITH_FIXED_FORM_OBSTRUCTION",
        "theorem": "Full S4 does not lift inside one fixed W(3,3) polarization. It lifts exactly as a three-object signed-monomial polarization groupoid.",
        "fixed_polarization": {
            "permutation_projection_order": 8,
            "projective_signed_monomial_isotropy_order": 32,
            "affine_signed_monomial_isotropy_order": 64,
            "reading": "The fixed-form coordinate projection is D8, not S4.",
        },
        "groupoid": {
            "objects": 3,
            "projective_homset_order": 32,
            "projective_arrows": 288,
            "affine_arrows": affine_arrow_count,
            "similitude_multiplier_profile": {str(k): v for k, v in sorted(lambda_profile.items())},
        },
        "checks": checks,
        "check_count": len(checks),
        "boundary": "This closes the signed-monomial lift as a polarization groupoid. It does not turn the checked-in lexicographic residual-channel selector into an S4-equivariant atlas; an intrinsic channel gauge is still required for that stronger statement.",
    }
