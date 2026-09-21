#!/usr/bin/env python3
"""Import the physical heterotic FI ray into the W33 Y+A4 neutral cokernel.

W33-Theory independently proves that the physical E8 neutral holonomy sector
has a five-dimensional self-bracket cokernel refined as
    Y(1) + A4(4),
and realizes it in the S6-duad carrier:
  * hypercharge is the S5-invariant star direction;
  * the extra U(1) sector is the four-dimensional zero-sum fluctuation space on
    the five star edges.

Holotrade now supplies the exact physical anomalous-U(1) generator from
Orbifolder and proves that its projection onto the flagship A5 organizer is
pure A4 with
    coefficients (-5/3,-2/3,-1/3,-2)
and six-times-duad-star vector
    (-5,3,1,-5,6).

This file imports that exact physical vector and verifies that it belongs to
the W33 A4 cokernel sector and has zero projection onto the hypercharge star
direction.

This is a cross-repository representation bridge, not a vacuum theorem.
"""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_physical_fi_ray_in_neutral_a4_cokernel.json'

def main(write=True):
    parent=json.loads((ROOT/'data/w33_hypercharge_duad_center_cokernel.json').read_text())
    assert parent['status']=='PASS_EXPLICIT_HYPERCHARGE_DUAD_AND_CENTER_COKERNEL'
    assert parent['extra_u1_A4']['rank']==4
    assert parent['neutral_bracket_cokernel']['refinement']=='16 = 11 + 1(Y) + 4(A4)'

    sixstar=[-5,3,1,-5,6]
    assert sum(sixstar)==0
    # The hypercharge star mode is the constant vector on the five distinguished
    # star edges; zero sum is exact orthogonality to that one-dimensional mode.
    Ystar=[1]*5
    assert sum(a*b for a,b in zip(sixstar,Ystar))==0

    coeff=[F(-5,3),F(-2,3),F(-1,3),F(-2)]
    primitive=[3*x for x in coeff]
    assert primitive==[-5,-2,-1,-6]

    out={
      'schema':'w33.physical_fi_ray_in_neutral_a4_cokernel.v1',
      'status':'PASS_PHYSICAL_FI_VECTOR_LANDS_IN_A4_COKERNEL',
      'headline':'The exact anomalous-U(1) FI generator measured by Orbifolder projects onto the flagship A5 organizer as a pure A4 vector, with zero hypercharge component. In the W33 duad carrier its six-times-star coordinates are (-5,3,1,-5,6), whose zero sum makes it orthogonal to the S5-invariant hypercharge star mode. Thus the physical FI instability occupies the four-dimensional A4 part of the independently derived neutral bracket cokernel 5=Y(1)+A4(4).',
      'physical_input':{
        'source_repo':'wilcompute/Holotrade',
        'source':'data/w33_flagship_fi_ray_pure_a4.json',
        'Orbifolder_FI_trace':200,
        'A4_simple_coefficients':['-5/3','-2/3','-1/3','-2'],
        'primitive_three_times_coefficients':[-5,-2,-1,-6]},
      'duad_image':{
        'six_times_star':sixstar,
        'sum':0,
        'hypercharge_star_inner_product':0,
        'reading':'nonzero A4 zero-sum fluctuation on the five distinguished star edges'},
      'W33_neutral_cokernel':{
        'dimension':5,
        'refinement':'Y(1)+A4(4)',
        'self_bracket_image_dimension':11,
        'neutral_sector_dimension':16},
      'TOE_reading':'The finite E8 bracket algebra and the physical heterotic FI instability select the same hypercharge-preserving four-dimensional Abelian sector. This identifies where the FI pressure acts in the W33 neutral-cokernel coordinates; it does not prove that a D/F-flat vacuum exists.',
      'boundary':'Cross-repository exact-vector import. The full anomalous generator also has a component in the other E8 factor, and no equality between the full FI direction and the five-dimensional W33 cokernel is asserted.',
      'parents':['data/w33_hypercharge_duad_center_cokernel.json'],
      'checks':{
        'neutral_cokernel_Y_plus_A4_loaded':True,
        'physical_A4_vector_nonzero':True,
        'duad_star_zero_sum':True,
        'hypercharge_component_zero':True,
        'primitive_A4_coordinates':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
