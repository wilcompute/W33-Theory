from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))

def test_frozen_packet():
 from w33_pass2050_2053_2064_verify_frozen import main
 out=main();assert out['n_checks']==out['n_verified']==77

def test_full_group_fusion_replay():
 from w33_pass2050_full_group_orbit_cover_fusion import main
 out=main();assert out['full_group_subgroup_types']==14

def test_integrated_reference_prototype():
 from w33_pass2052_integrated_geometry_hardware_prototype import main
 out=main();assert out['d8']['frames']==60 and out['d8']['edge_profile']=={'1':240}

def test_literal_spread_graph_identification():
 from w33_pass2053_identify_spread_graph import main
 out=main();assert out['identification'].startswith('NO_6^-(2)')

def test_q357_certificate_replay():
 from w33_pass2064_regular_spread_rank3_family import main
 out=main(False);assert [out['q'][q]['spreads'] for q in ('3','5','7')]==[36,300,1176]
