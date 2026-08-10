import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
def load(name):return json.loads((DATA/name).read_text(encoding="utf-8"))

def test_release_total_and_status():
    files=['w33_pass1087_canonical_steinberg_parity.json','w33_pass1088_frame_adjacency_wedderburn.json','w33_pass1089_dual_hesse_triple_hyperplanes.json','w33_pass1090_controller_protocol_boundary.json','w33_pass1091_formal_orbital_intertwiner_lock.json']
    ds=[load(x) for x in files]
    assert all(d['status']=='PASS' for d in ds)
    assert sum(d['check_count'] for d in ds)==77
    assert all(all(d['checks'].values()) for d in ds)

def test_canonical_steinberg_parity():
    d=load('w33_pass1087_canonical_steinberg_parity.json')
    assert d['outer_action_matrix_mod_1000003']==[[1,1000002],[0,1000002]]
    assert d['canonical_maps']['Steinberg_plus']['outer_trace']==3
    assert d['canonical_maps']['Steinberg_minus']['outer_trace']==-3
    assert d['combined_image_rank']==162

def test_wedderburn_decomposition_and_kernel():
    d=load('w33_pass1088_frame_adjacency_wedderburn.json')
    assert d['inner']['rank']==32 and d['inner']['center_dimension']==9
    assert d['outer']['rank']==22 and d['outer']['center_dimension']==10
    assert d['inner']['sum_isotypic_dimensions']==540
    assert d['outer']['sum_multiplicity_squares']==22
    assert sum(x['module_localization_dimensions']['frame_kernel'] for x in d['inner']['components'])==504

def test_outer_splits_the_two_81s():
    d=load('w33_pass1088_frame_adjacency_wedderburn.json')
    c={x['label']:x for x in d['outer']['components']}
    assert c['81_plus']['module_localization_dimensions']['Steinberg_plus']==81
    assert c['81_plus']['module_localization_dimensions']['Steinberg_minus']==0
    assert c['81_minus']['module_localization_dimensions']['Steinberg_minus']==81
    assert c['81_minus']['module_localization_dimensions']['Steinberg_plus']==0

def test_dual_hesse_objectwise_identification():
    d=load('w33_pass1089_dual_hesse_triple_hyperplanes.json')
    assert d['arrangements']['extra9']['lines']==9
    assert d['arrangements']['extra9']['triple_points']==12
    assert d['duality']['extra_triple_points_equal_G25_line_normals']
    assert d['duality']['G25_quadruple_points_equal_extra_line_normals']
    assert d['group_action']['extra9']['projective_image_order']==216
    assert d['group_action']['extra9']['scalar_kernel_order']==3

def test_controller_protocol_boundary_fails_closed():
    d=load('w33_pass1090_controller_protocol_boundary.json')
    assert d['manifest']['protocol']=='W33-MZI-TCP/1.0'
    assert d['transcript_summary']['event_count']==240
    assert d['analysis']['decision']=='contextual_positive'
    assert d['analysis']['contextual_fraction_field'] is None
    assert d['negative_probes']['bad_crc']==[True,'crc_or_json_failure']
    assert d['negative_probes']['missing_calibration']==[True,'calibration_required']
    assert d['manifest']['real_hardware_connected'] is False

def test_formal_lock_and_hashes():
    d=load('w33_pass1091_formal_orbital_intertwiner_lock.json')
    lean=(ROOT/'formal/W33/Pass1091FrameOrbitalIntertwiner.lean').read_text(encoding="utf-8")
    assert d['counts']=={'inner_self_paired':12,'inner_nonself_paired':20,'inner_transpose_pairs':10,'outer_fusion_orbits':22,'outer_self_paired':14}
    assert d['tensor_hashes']['Steinberg_plus'] in lean
    assert d['tensor_hashes']['Steinberg_minus'] in lean
    assert 'theorem innerTranspose_involutive' in lean
    assert 'theorem column_mem_leftKernel' in lean
    assert 'theorem cycleEigen_entry' in lean
