#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(p): return json.loads((R/p).read_text())

def check():
    Z=J('data/PART_W33_PASS5254_5261_RESULTS.json')
    assert Z['range']==[5254,5261]
    assert Z['5254']['distinct_weight8_configurations']==25920
    assert Z['5254']['full_decoder'].startswith('all 25920 clear')
    assert Z['5255']['q5']['zero_blocks']=={'J1':2156,'J3':520}
    assert Z['5255']['q5']['one_blocks']=={'J1':804,'J2':1471,'J3':48,'J4':536}
    assert Z['5256']['shell4']=='(q-1)^2(q-4)^2'
    assert Z['5257']['binary_kernel']=='ker_F2(H8)=C_F direct-sum <1>'
    assert Z['5258']['parameters']=='[312,52,d_sh]_2'
    assert Z['5258']['distance_bounds']==[28,40]
    assert Z['5259']['states_enumerated']==33554432
    assert Z['5259']['low_even_shell']=={'40':180,'48':450,'64':3825}
    assert Z['5260']['dimensions']['zero_footprint_residual']==560
    assert Z['5260']['dimensions']['L_rank_even']==7240
    assert Z['5260']['strict_target'].startswith('Prove block distance')
    assert Z['5261']['centered_frame'].startswith('156 equal-norm vectors')
    assert Z['5261']['unit_inner_products']=={'collinear':'2/15','noncollinear':'-1/25'}

    # Original development certificates retained after numbering reconciliation.
    A=J('data/PART_W33_PASS5239_Q3_RADIUS8_FALSE_CENTER_ECHO.json')
    B=J('data/PART_W33_PASS5240_CONNECTEDL_MOD2_JORDAN_STRUCTURE.json')
    C=J('data/PART_W33_PASS5241_ROOT_OUTER_SHELL_TWO_ROOT_TORUS_FAMILY.json')
    D=J('data/PART_W33_PASS5242_Q5_WEIGHT8_FRAME_CONSTANT_MODE.json')
    E=J('data/PART_W33_PASS5243_HOFFMAN13_SHORTENED_DOUBLY_EVEN_CODE.json')
    F=J('data/PART_W33_PASS5244_Q5_ZERO_FOOTPRINT_EVEN_TENSOR_SHELL.json')
    G=J('data/PART_W33_PASS5245_ZERO_FOOTPRINT_PARITY_SYNDROME_EXACT_SEQUENCE.json')
    H=J('data/PART_W33_PASS5261_Q5_FOOTPRINT_MINIMUM_SHELL_TWO_DISTANCE_FRAME.json')
    assert A['distinct_weight8_configurations']==25920
    assert B['q5']['zero_primary_Jordan_blocks']=={'1':2156,'3':520}
    assert B['q5']['one_primary_Jordan_blocks']=={'1':804,'2':1471,'3':48,'4':536}
    assert C['shell4']=='(q-1)^2(q-4)^2'
    assert D['binary_rank']==259 and D['binary_nullity']==66
    assert E['shortened_dimension']==52 and E['distance_lower_bound']==28
    assert F['minimum_even_weight']==40 and F['minimum_even_count']==180
    assert F['active_P_components_max']==15
    assert G['zero_footprint_residual_dimension']==560 and G['syndrome_quotient_dimension']==260
    assert H['tight_frame_dimension']==90 and H['tight_frame_bound']==40

    # Reconcile against the authoritative preceding packet rather than replacing it.
    P=J('data/PART_W33_PASS5238_5245_RESULTS.json')
    assert P['5238']['code']=='C_F=[325,65,25]_2'
    assert '936 chamber stars' in P['5238']['equality_consequence']
    assert P['5243']['even_subcode_minimum']==40
    assert 'leader36' in P['strict_frontier']
    return True

if __name__=='__main__':
    check(); print('PASS5254-5261 reconciled regression: PASS')
