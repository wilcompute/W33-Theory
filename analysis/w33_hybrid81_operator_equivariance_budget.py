#!/usr/bin/env python3
"""Quantify the exact equivariance budget between the completed address chart
and the trinification operator chart.

Abstractly identify the scheduler group as
    K = H27 x C3_external.

Source/address module:
    Reg(K).

Operator module:
    (9 V_omega) tensor Reg(C3)
  = 9 V_(omega,0) + 9 V_(omega,1) + 9 V_(omega,2).

The completed root chart splits as visible73 + dark8.  The dark theorem gives
    dark8 = chi_ext + chi_ext^2 + V_(omega,0) + V_(omega^2,0).

Subtracting this from Reg(K) gives the exact visible73 profile.

The maximum ranks of K-equivariant maps to the operator module are:
    visible73 -> operator81 : 24
    dark8     -> operator81 :  3
    full81    -> operator81 : 27.

Thus an invertible 81-state compiler necessarily crosses a 54-dimensional
representation mismatch.  The hybrid 81x81 basis solves coordinate
completeness, but cannot solve this representation mismatch by any basis
change that preserves K.

Boundary: "54-dimensional equivariance deficit" means 54 target dimensions
lie outside the image of every K-equivariant source->operator map.  It is not
an identification with the separate 54 fiber cubic instructions.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_hybrid81_operator_equivariance_budget.json"


def rank_overlap(source, target, degrees):
    return sum(
        degrees[label] * min(source.get(label, 0), target.get(label, 0))
        for label in degrees
    )


def hom_dimension(source, target):
    return sum(
        source.get(label, 0) * target.get(label, 0)
        for label in set(source) | set(target)
    )


def module_dimension(profile, degrees):
    return sum(degrees[label] * mult for label, mult in profile.items())


def main(write=True):
    # Labels: L_u_v_t are 1D H27-abelian characters times external chi_t.
    # S_s_t are 3D Schrodinger central character omega^s times external chi_t.
    degrees = {}
    source = {}

    for u in range(3):
        for v in range(3):
            for t in range(3):
                label = f"L_{u}_{v}_{t}"
                degrees[label] = 1
                source[label] = 1

    for s in (1, 2):
        for t in range(3):
            label = f"S_{s}_{t}"
            degrees[label] = 3
            source[label] = 3  # regular multiplicity = degree

    assert module_dimension(source, degrees) == 81

    target = {label: 0 for label in degrees}
    for t in range(3):
        target[f"S_1_{t}"] = 9
    assert module_dimension(target, degrees) == 81

    dark = {label: 0 for label in degrees}
    dark["L_0_0_1"] = 1
    dark["L_0_0_2"] = 1
    dark["S_1_0"] = 1
    dark["S_2_0"] = 1
    assert module_dimension(dark, degrees) == 8

    visible = {
        label: source.get(label, 0) - dark.get(label, 0)
        for label in degrees
    }
    assert all(mult >= 0 for mult in visible.values())
    assert module_dimension(visible, degrees) == 73

    rank_visible = rank_overlap(visible, target, degrees)
    rank_dark = rank_overlap(dark, target, degrees)
    rank_full = rank_overlap(source, target, degrees)
    assert (rank_visible, rank_dark, rank_full) == (24, 3, 27)

    hom_visible = hom_dimension(visible, target)
    hom_dark = hom_dimension(dark, target)
    hom_full = hom_dimension(source, target)
    assert (hom_visible, hom_dark, hom_full) == (72, 9, 81)

    target_deficits = {
        "visible73": 81 - rank_visible,
        "dark8": 81 - rank_dark,
        "full81": 81 - rank_full,
    }
    source_kernels = {
        "visible73": 73 - rank_visible,
        "dark8": 8 - rank_dark,
        "full81": 81 - rank_full,
    }
    assert target_deficits == {"visible73": 57, "dark8": 78, "full81": 54}
    assert source_kernels == {"visible73": 49, "dark8": 5, "full81": 54}

    # Which dark summands can meet the operator module equivariantly?
    dark_common = [
        label
        for label, mult in dark.items()
        if mult and target.get(label, 0)
    ]
    dark_incompatible = [
        label
        for label, mult in dark.items()
        if mult and not target.get(label, 0)
    ]
    assert dark_common == ["S_1_0"]
    assert set(dark_incompatible) == {"L_0_0_1", "L_0_0_2", "S_2_0"}

    obstruction = json.loads(
        (ROOT / "data/w33_scheduler_operator_k81_intertwiner_obstruction.json").read_text()
    )
    dark_cert = json.loads(
        (ROOT / "data/w33_hesse36_e8_matter81_dark8_decomposition.json").read_text()
    )
    hybrid = json.loads(
        (ROOT / "data/w33_e8_matter81_hybrid_cubic_dark_basis.json").read_text()
    )
    operator = json.loads(
        (ROOT / "data/w33_e8_matter81_pauli243_restriction.json").read_text()
    )

    assert obstruction["intertwiner"]["maximum_rank"] == 27
    assert dark_cert["irreducible_decomposition"]["formula"] == (
        "chi_ext + chi_ext^2 + V_omega + V_omega^2"
    )
    assert hybrid["hybrid_basis"]["rank"] == 81
    assert operator["matter_representation"]["multiplicity"] == 9

    out = {
        "schema": "w33.hybrid81_operator_equivariance_budget.v1",
        "status": "PASS_COMPLETE_81D_CHART_HAS_EXACT_54D_EQUIVARIANCE_DEFICIT_TO_OPERATOR_MODULE",
        "headline": (
            "The new 73+8 hybrid chart solves linear coordinate completeness but "
            "not the address/operator representation mismatch. Under the abstract "
            "K=H27 x C3 identification, the visible73 sector can map equivariantly "
            "to at most 24 operator dimensions and the dark8 sector to at most 3. "
            "The full maximum is therefore 27, leaving an exact 54-dimensional "
            "target equivariance deficit. Of the dark eight, only V_(omega,0) is "
            "operator-compatible; chi_ext, chi_ext^2 and V_(omega^2,0) are outside "
            "the operator irrep support in the frozen central orientation."
        ),
        "modules": {
            "source_address": {
                "description": "Reg(H27 x C3)",
                "dimension": 81,
                "one_dimensional_irreps": 27,
                "three_dimensional_irreps": 6,
                "three_dimensional_regular_multiplicity_each": 3,
            },
            "operator": {
                "description": "9 V_omega tensor Reg(C3)",
                "dimension": 81,
                "nonzero_irrep_multiplicities": {
                    "S_1_0": 9,
                    "S_1_1": 9,
                    "S_1_2": 9,
                },
            },
            "visible73": {
                "dimension": 73,
                "operator_common_S1_multiplicities": {
                    "S_1_0": visible["S_1_0"],
                    "S_1_1": visible["S_1_1"],
                    "S_1_2": visible["S_1_2"],
                },
            },
            "dark8": {
                "dimension": 8,
                "profile": {
                    "L_0_0_1": 1,
                    "L_0_0_2": 1,
                    "S_1_0": 1,
                    "S_2_0": 1,
                },
                "operator_compatible": dark_common,
                "operator_incompatible": dark_incompatible,
            },
        },
        "equivariant_map_budget": {
            "Hom_dimensions": {
                "visible73_to_operator81": hom_visible,
                "dark8_to_operator81": hom_dark,
                "full81_to_operator81": hom_full,
            },
            "maximum_ranks": {
                "visible73_to_operator81": rank_visible,
                "dark8_to_operator81": rank_dark,
                "full81_to_operator81": rank_full,
            },
            "target_dimensions_outside_any_equivariant_image": target_deficits,
            "source_dimensions_forced_into_kernel": source_kernels,
            "full_equivariance_deficit": 54,
        },
        "compiler_consequence": (
            "The remaining compiler problem is now quantitatively a representation "
            "conversion problem. At least 54 target dimensions cannot be reached "
            "by any K-equivariant map. Any invertible address-to-operator compiler "
            "must therefore use the Hesse/Fourier character twist, a changed group "
            "action, or another explicitly symmetry-changing mechanism on that "
            "deficit rather than searching for a hidden equivariant basis change."
        ),
        "count_collision_firewall": (
            "The number 54 also occurs as the phase-decorated fiber-instruction "
            "sector in the 270 compiler. No objectwise identification between that "
            "instruction carrier and this representation-theoretic deficit is "
            "asserted here."
        ),
        "boundary": (
            "This is an exact finite representation budget under the abstract "
            "identification of the two K factors. It does not construct the final "
            "symmetry-changing 81x81 address-to-operator matrix or assign particle "
            "families, masses, or a vacuum."
        ),
        "parents": [
            "data/w33_scheduler_operator_k81_intertwiner_obstruction.json",
            "data/w33_hesse36_e8_matter81_dark8_decomposition.json",
            "data/w33_e8_matter81_hybrid_cubic_dark_basis.json",
            "data/w33_e8_matter81_pauli243_restriction.json",
        ],
        "checks": {
            "source_dimension81": True,
            "operator_dimension81": True,
            "visible_dimension73": True,
            "dark_dimension8": True,
            "visible_max_rank24": True,
            "dark_max_rank3": True,
            "full_max_rank27_reproduced": True,
            "full_equivariance_deficit54": True,
            "dark_common_only_Vomega_t0": True,
            "fiber54_count_collision_firewalled": True,
        },
    }

    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
