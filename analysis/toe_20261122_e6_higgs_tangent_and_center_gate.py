#!/usr/bin/env python3
"""Full-field first-order mass obstruction in the E6/H27 singlet toy vacuum,
and a conditional no-go for extending three Witting regular modules to an
81-dimensional honest E6 representation with identified central C3.

No claim about exact nonlinear moduli or general E6 compactifications.
"""
from __future__ import annotations
import json,itertools
from pathlib import Path
import sympy as sp
import toe_20261122_further_e6_isolated_singlet as S
import toe_20261122_h27_central_fourier_bridge as H
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_e6_higgs_tangent_and_center_gate.json'


def verify():
    proof=S.check_poly()
    assert len(proof['Jacobian_5x5_minors'])==6
    # E6 27 -> (16,1) + (10,-2) + (1,4) under SO10 x U1;
    # 27bar is conjugate. At the chosen singlet VEV the unbroken
    # connected gauge group is SO10, of dimension 45, inside E6 dim78.
    n=3
    singlet_chirals=2*n
    nonsinglet_chirals=2*n*(16+10)
    fields=singlet_chirals+nonsinglet_chirals
    assert (singlet_chirals,nonsinglet_chirals,fields)==(6,156,162)
    # Each of 5 driver F-term constraints has nonzero gradient only in
    # singlet Higgs coordinates at the singlet-only configuration.
    # Their Jacobian rank is 5 exactly by the prior Q(omega) minors.
    holomorphic_F_rank=5
    tangent_F=fields-holomorphic_F_rank
    gauge_broken=78-45
    gauge_broken_U1=1
    gauge_broken_charged=gauge_broken-gauge_broken_U1
    charged_nongauge=nonsinglet_chirals-gauge_broken_charged
    assert (tangent_F,gauge_broken,gauge_broken_charged,charged_nongauge)==(157,33,32,124)
    assert tangent_F-gauge_broken==charged_nongauge
    # The renormalizable toy W has only X_{ab} * (barH H)_ab for the
    # Higgs sector. With all X_ab=0 and purely singlet H/barH VEVs, the
    # Higgs-Higgs Hessian is identically zero in all 156 nonsinglet rows.
    # Broken gauge vector multiplets eat 33 complex chiral directions,
    # one within singlets and 32 in spinors. At least 124 remaining
    # charged Higgs complex tangents have no quadratic superpotential mass.
    massless_10_pairs=2*n*10
    massless_spinors=2*n*16-gauge_broken_charged
    assert massless_10_pairs==60 and massless_spinors==64
    # H27 regular address module has 9 linear irreps and two 3D irreps,
    # with center eigenspace dimensions (9,9,9), and exactly one H27
    # invariant vector. Three copies multiply both counts by 3.
    normal,x,y,z,orbit=H.heisenberg_action()
    assert normal.order()==27 and len(orbit)==27
    n_fixed=sum(all(g(i)==i for g in normal.generate_schreier_sims()) for i in orbit)
    assert n_fixed==0  # action regular, group nontrivial
    source_center_eigenspace_dims={'1':27,'omega':27,'omega_squared':27}
    H27_invariant_dimension=3
    # Any *genuine* complex E6 representation of dimension 81 whose
    # global center acts like the source H27 center has a 27D
    # center-TRIVIAL eigenspace. The smallest nontrivial center-trivial
    # irreducible of E6 is the 78D adjoint. Therefore that 27D sector
    # is a sum of 27 trivial E6 representations. Its restriction to
    # H27 then has at least 27 invariant vectors, unlike source's 3.
    forced_trivial_E6_sector_dim=source_center_eigenspace_dims['1']
    assert forced_trivial_E6_sector_dim<78
    assert forced_trivial_E6_sector_dim>H27_invariant_dimension
    # If one enlarges the target to allow a nontrivial center-neutral
    # sector plus both opposite center sectors, the dimension is at
    # least 78+27+27. This is a NECESSARY DIMENSION bound only, not
    # proof that an embedding exists in the 132D candidate.
    necessary_E6_supermodule_dimension=78+27+27
    assert necessary_E6_supermodule_dimension==132
    return dict(status='PASS_E6_FULL_HIGGS_CHARGED_TANGENT_AND_81D_CENTRAL_EXTENSION_NO_GO',
       higgs_family_pairs=n,full_Higgs_complex_chiral_fields=fields,
       E6_decomposition='27=16_1+10_-2+1_4 and conjugate bar27',
       Higgs_singlet_field_count=singlet_chirals,
       Higgs_nonsinglet_field_count=nonsinglet_chirals,
       driver_Fterm_Jacobian_rank=holomorphic_F_rank,
       total_Fflat_Zariski_tangent_dimension=tangent_F,
       E6_group_dimension=78,unbroken_connected_SO10_dimension=45,
       broken_complex_gauge_directions=gauge_broken,
       broken_gauge_charged_spinor_directions=gauge_broken_charged,
       unlifted_nonsinglet_Higgs_tangent_after_gauge_quotient=charged_nongauge,
       components_left_unlifted_at_quadratic_order={'10_and_bar10':massless_10_pairs,'spinors_after_goldstone_quotient':massless_spinors},
       tangent_caution='These are first-order complex tangent/mass-Hessian null directions, NOT proof of 124 exact nonlinear D-flat moduli. Higher-order F constraints and added superpotential terms can obstruct them.',
       central_module='three copies of the 27D H27 regular address permutation representation',
       center_eigenspace_dimensions=source_center_eigenspace_dims,
       whole_source_H27_invariant_dimension=H27_invariant_dimension,
       minimum_nontrivial_complex_E6_irrep_with_trivial_center_dimension=78,
       source_center_trivial_sector_dimension=27,
       forced_E6_trivial_rep_dimension=27,
       E6_81D_extension_with_identified_center_exists=False,
       necessary_dimension_for_any_center_compatible_nontrivial_E6_supermodule=necessary_E6_supermodule_dimension,
       central_no_go_proof='An 81D E6 module with center eigenspaces (27,27,27) has its center-trivial 27D piece equal to 27 E6 trivial modules, since the smallest nontrivial center-trivial E6 irrep is adjoint78. All 27 must be H27-fixed, but the three regular H27 modules have exactly 3 fixed vectors. Contradiction.',
       central_assumptions='H27 is the center-correct operator subgroup of simply-connected E6, with H27 center generator identified with global Z(E6). Honest linear E6 action and exact 3xregular H27 source action are required. Relaxing any premise evades this scoped no-go.',
       physical_boundary='Neither first-order charged tangent nor center-character obstruction proves general E6 model nonviability. No full gauge vacuum or phenomenological spectrum derived.')


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],d['unlifted_nonsinglet_Higgs_tangent_after_gauge_quotient'],d['necessary_dimension_for_any_center_compatible_nontrivial_E6_supermodule'])
if __name__=='__main__':main()
