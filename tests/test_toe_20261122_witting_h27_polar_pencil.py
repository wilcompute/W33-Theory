"""Exact regression of the Witting 1+4*3+27 Heisenberg polar decomposition."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261122_witting_h27_polar_pencil as polar

def test_fixed_ray_four_lines_and_regular_outer_orbit():
    d=polar.verify()
    assert d['fixed_witting_ray_zero_based']==25
    assert d['H27_orbit_sizes']==[1,3,3,3,3,27]
    assert d['four_three_ray_pencil_lines']==[
      [1,5,33],[8,23,26],[11,14,24],[28,35,38]]
    assert d['regular_H27_orbit_point_stabilizer']==1

def test_symplectic_quadrangle_exact_pair_counts():
    d=polar.verify()
    assert d['srg_parameters']==[40,12,2,4]
    assert d['pair_count_by_adjacency_and_common_neighbors']=={
      'adjacent_common2':240,'nonadjacent_common4':540}
    assert d['exterior_27_rays_all_nonorthogonal_to_fixed']
