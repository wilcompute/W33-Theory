from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data'/'w33_pass548_552_nonlinear_semilinear_transfer.json').read_text(encoding="utf-8"))

def test_release_green():
    assert DATA['status']=='PASS'
    assert DATA['total_owner_checks']==45
    assert all(DATA['release_checks'].values())

def test_quartic_separator_and_quadratic_model():
    p548=DATA['parts']['pass548'];p549=DATA['parts']['pass549']
    assert p548['tensor_hierarchy']['target_prefix_fibres']['4']==80
    assert p548['tensor_hierarchy']['target_prefix_fibres']['5']==80
    assert p549['quadratic_model']['size']==80
    assert len(p549['quadratic_model']['core_patterns_y3_y4_y5_y6'])==5

def test_semilinear_covariance_boundary():
    p=DATA['parts']['pass550']
    assert p['global_law']['group_order']==480
    assert p['generator_covariance']['classification']['det4'].startswith('antiunitary')
    assert p['forced_fusions']['sigma2_fixed_in_fixed_profile']==0

def test_z9_transfer_growth_and_memory_obstruction():
    p=DATA['parts']['pass551']
    assert [x['sections'] for x in p['layers']]==[81,243,729,2187]
    assert [x['distinct_charpolys'] for x in p['layers']]==[13,26,96,336]
    assert [x['full_row_rank'] for x in p['transfers']]==[True,True,True]
    assert [x['spectral_markov'] for x in p['transfers']]==[True,False,False]

def test_constant_and_switch_all_m_results():
    p=DATA['parts']['pass552']
    assert p['odd_switch_family']['companion_order_mod_pi']==312
    assert [x['matrix_minus_identity_vpi'] for x in p['odd_switch_family']['order_lifting']]==[1,3,5,7]
    assert 'If 4|m' in p['constant_family']['all_m_formula']

def test_sources_and_owner_certificates_present():
    for n in range(548,553):
        assert list((ROOT/'analysis').glob(f'w33_pass{n}_*.py'))
        assert list((ROOT/'data').glob(f'w33_pass{n}_*.json'))
