from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
R=json.loads((ROOT/'data/PART_W33_PASS5300_5307_RESULTS.json').read_text())

def test_status_and_closed_boundaries():
    assert R['status']=='EXECUTED_WITH_ALLODD_Q11_AND_HOFFMAN_DISTANCE_OPEN'
    assert R['5300']['hoffman_order']==576
    assert R['5300']['klein_V4_autoparatopy_order']==576
    assert 'not isomorphic' in R['5300']['negative']

def test_576_affine_quotient_bridge():
    assert R['5300']['latin_even_parastrophe_order']==288
    assert 'H/Z(H)' in R['5300']['exact_bridge']
    assert R['5301']['hoffman_latin_even_direction_orbits']==[9,6]
    assert R['5301']['toroidal_knight'].startswith('Q4')

def test_hoffman_fourcell_reduction():
    assert R['5302']['four_subsets']==715 and R['5302']['orbits']==10
    assert sum(a for a,b in R['5302']['orbit_size_rank'])==715
    assert set(b for a,b in R['5302']['orbit_size_rank'])=={33,35,38,39,40}

def test_rank_and_q11_firewall():
    assert R['5303']['q13']['rank_F2']==1105==R['5303']['q13']['target_g']
    assert R['5304']['necessary_edge_lower_bound']==120
    assert 'remain open' in R['5304']['boundary']

def test_k0_orbitals_and_64_no_go():
    assert R['5305']['vertices']==2340 and R['5305']['orbital_rank']==21
    assert R['5306']['relation_fixed_dimension_under_transvection']==4
    assert R['5306']['footprint_hull_fixed_dimension_under_transvection']==24

def test_latin_mols_spread():
    assert R['5307']['latin_total']==576
    assert R['5307']['V4_isotopy_class']+R['5307']['C4_isotopy_class']==576
    assert R['5307']['PG3_2_spreads']==56
    assert R['5307']['GL4_2_spread_stabilizer']==360
