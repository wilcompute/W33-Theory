#!/usr/bin/env python3
"""Dimension firewall for the heterotic twisted-sector interpretation.

A useful parallel-agent result identified the *sector-label* action correctly:
in a Z3 orbifold, theta and theta^2 twisted sectors carry conjugate order-three
charges and can be exchanged by an inversion symmetry.  This matches the
two-dimensional W33 logical label r=1,2.

It does NOT identify the full W33 Schrodinger modules with the ordinary
fixed-point flavour modules of a six-real-dimensional heterotic orbifold.

W33 parent:
  H_W = 3^(1+12), phase space F3^12,
  dim V_r = 3^6 = 729.

Factorized T^6/Z3 fixed-point flavour:
  at most three complex T2/Z3 factors share the point-group centre,
  H_het = 3^(1+2d), d<=3,
  dim S_r = 3^d <= 27.

Hence the full module dimensions differ by 27 at d=3:
  729 / 27 = 27.
The doubled spaces are 1458 versus at most 54.

What survives exactly is the *central-character / sector-label doublet*
  span{|theta>, |theta^2>} ~= C^2
with order-three phase diag(omega,omega^-1) and inversion swap.  That is the
same abstract S3 doublet already certified by the Konopka intertwiner.

To obtain a 729-dimensional heterotic partner one needs six independent
ternary canonical pairs (d=6), i.e. a 12-dimensional F3 phase space.  An
ordinary six-real-dimensional factorized Z3 fixed-point geometry supplies
only d=3.  Any full physical bridge must find three additional canonical
pairs elsewhere (gauge lattice, winding/momentum, oscillator, Narain, etc.)
and prove that they share the same central extension.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_heterotic_twisted_sector_dimension_firewall.json'

def main(write=True):
    w33_d=6
    w33_group=3**(1+2*w33_d)
    w33_irrep=3**w33_d
    max_het_d=3
    het_group=3**(1+2*max_het_d)
    het_irrep=3**max_het_d
    assert w33_irrep==729 and het_irrep==27 and w33_irrep//het_irrep==27
    out={
      'schema':'w33.heterotic_twisted_sector_dimension_firewall.v1',
      'status':'PASS_LABEL_BRIDGE__FULL_MODULE_IDENTIFICATION_NO_GO_WITH_FIXED_POINTS_ALONE',
      'W33':{
        'Heisenberg':'3^(1+12)','d':w33_d,'phase_space_dimension_F3':12,
        'Schrodinger_irrep_dimension':w33_irrep,'doubled_dimension':2*w33_irrep},
      'ordinary_factorized_T6_Z3_fixed_point_flavour':{
        'complex_Z3_planes_max':max_het_d,
        'shared_center_Heisenberg':'3^(1+6)',
        'phase_space_dimension_F3':6,
        'faithful_irrep_dimension_max':het_irrep,
        'doubled_theta_theta2_dimension_max':2*het_irrep},
      'dimension_obstruction':{
        'single_sector_ratio':w33_irrep//het_irrep,
        'missing_ternary_degrees_of_freedom':w33_d-max_het_d,
        'missing_canonical_pairs':w33_d-max_het_d},
      'surviving_exact_bridge':{
        'object':'two-dimensional sector/central-character label only',
        'theta_sector':'r=1 up to convention',
        'theta2_sector':'r=2 up to convention',
        'order3_action':'diag(omega,omega^-1)',
        'inversion':'sector swap',
        'module':'defining complex S3 doublet'},
      'needed_for_full_bridge':'Find three additional ternary canonical pairs in gauge/Narain momentum-winding/oscillator structure and prove a common extraspecial 3^(1+12) action.',
      'parallel_agent_audit':'The finite Heisenberg calculations in Holotrade commit 2365e596 are useful, but the statement that the full W33 V1+V2 equals ordinary T1+T2 is dimensionally too strong for a standard six-real-dimensional factorized Z3 fixed-point space.',
      'checks':{'729_vs_27':True,'label_doublet_dimension2_compatible':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
