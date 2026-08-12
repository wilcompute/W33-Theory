import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())
def test_pass4984_residual_a4():
 d=J('PART_W33_PASS4984_RESIDUAL_A4_CHORDLESS_ORBIT.json');assert d['sigma_even_4cycle_split_by_chords']=={'0':810,'1':6480,'2':3240};assert d['residual_810']['single_WE6_orbit'];assert d['residual_810']['stabilizer_order']==64
def test_pass4985_audit():
 d=J('PART_W33_PASS4985_COLLISION_PACKET_AUDIT.json');assert d['ihara_nontrivial_root_fields']==['Q(i sqrt(10))','Q(i sqrt(7))'];assert d['critical_group']['structure']=='(Z/10)^8 (+) Z/40 (+) (Z/160)^14'
def test_pass4986_twin_dark15():
 d=J('PART_W33_PASS4986_TWIN_DARK15_LEVI_OBSTRUCTION.json');assert d['Levi']['nullity']==30;assert d['nonisomorphism_certificate']['GF2_adjacency_rank_point']==16;assert d['nonisomorphism_certificate']['GF2_adjacency_rank_line']==10
def test_pass4987_decoder():
 d=J('PART_W33_PASS4987_40_45_EXACT_DECODER.json');assert d['reader']['rank']==36;assert d['frame_operator']=='R^T R = 18 I_36 + 22 J_36';assert d['minimal_sensor_count']==36;assert d['erasure']['exact_failure_size_interval']==[5,12]
def test_pass4988_gauge_survives():
 d=J('PART_W33_PASS4988_AG23_INTRINSIC_GAUGE_SURVIVES.json');assert d['AG23_completions']==12;assert d['PSp_local_group']['action']=='transitive';assert d['PSp_local_group']['completion_stabilizer']==54
def test_pass4989_octahedral_bundle():
 d=J('PART_W33_PASS4989_A4_TRITANGENT_OCTAHEDRAL_BUNDLE.json');assert d['residual_A4']==810;assert d['base_intersecting_tritangent_pairs']==270;assert d['fiber_multiplicity']==3;assert d['per_intersecting_pair']['induced_H36_graph'].startswith('K6 minus 3K2')
def test_pass4990_tight_frame():
 d=J('PART_W33_PASS4990_CENTERED_85_TIGHT_FRAME.json');assert d['line_centered_frame_operator']=='18 P_15';assert d['tritangent_centered_frame_operator']=='18 P_20';assert d['dimensions']=={'mean_zero':35,'line_sector':15,'tritangent_sector':20}
def test_pass4991_point_packets():
 d=J('PART_W33_PASS4991_AG23_12_TO_4_POINT_PACKETS.json');assert d['disjointness_graph_on_12']=='4 K3';assert d['canonical_packets']=={'count':4,'size_each':3};assert d['unique_full_group_equivariant_packet_to_point_bijection']
def test_public_and_manifest_wiring():
 manifest=(ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex').read_text();assert 'PASS4984_4991_shell_decoder_gauge_insert' in manifest
 page=(ROOT/'docs/pass4984-4991-shell-decoder-gauge.html').read_text();assert 'R^T R = 18 I_36 + 22 J_36' not in page or 'Passes 4984' in page
