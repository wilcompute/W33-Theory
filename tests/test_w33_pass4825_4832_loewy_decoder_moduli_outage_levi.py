import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def J(name):return json.loads((ROOT/'data'/name).read_text())

def test_pass4826_code399_decoder():
    x=J('PART_W33_PASS4826_CODE399_DECODER.json')
    assert x['code']=='[2025,399,14]_2'
    assert x['parity_check']['rank']==1626
    assert x['parity_check']['global_rows']==6
    assert x['explicit_schedule']['global_conflict_chromatic_number']==6
    assert x['bounded_distance_decoder']['guaranteed_arbitrary_error_radius']==6
    assert x['bounded_distance_decoder']['raw_candidate_bound']==262144

def test_pass4829_levi_code():
    x=J('PART_W33_PASS4829_LEVI_HOMOLOGY_CODE.json')
    assert x['code']=='[2025,64,96]_2'
    assert x['effective_punctured_code']=='[1620,64,96]_2'
    assert x['physical']['hot_zero_coordinates']==405
    assert x['physical']['cold_repetition_blocks']==135
    assert x['physical']['coordinates_per_block']==12
    assert x['Levi']['minimum_8_cycle_count']==1080
    assert x['dual']['dimension']==1961 and x['dual']['minimum_distance']==1
    assert x['dual']['weight1_dual_words']==405
    assert x['dual']['weight2_dual_words']==90720
    assert x['decoder']['guaranteed_arbitrary_error_radius']==47

def test_pass4831_twelve_is_not_twelve():
    x=J('PART_W33_PASS4831_DEEPHOLE_RESIDUE_12X12_FALSIFIER.json')
    assert x['H10_deep_hole_orbits']['count']==12
    assert x['residue_ordered_pair_orbitals']['count']==12
    assert x['componentwise_PSp_Gset_identification_exists'] is False

def test_pass4832_intrinsic_dual_shell():
    x=J('PART_W33_PASS4832_CODE399_DUAL_SHELL_GEOMETRY.json')
    assert x['weight2_shell']['class_size_profile']=={'3':135,'4':405}
    assert x['weight2_shell']['weight2_dual_words']==2835
    assert x['weight2_shell']['weight2_span_dimension']==1485
    q=x['quotient_by_weight2_span']
    assert q['length']==540 and q['dimension']==141 and q['minimum_weight']==4
    assert q['weight4_dependency_count']==135
    assert q['minimum_dependencies_partition_all_540_classes'] is True
    assert x['intrinsic_reconstruction']['K6_cells_recovered']==135

def test_optional_heavy_certificates_if_materialized():
    optional=[
      'PART_W33_PASS4825_BRAUER_LOEWY_CLOSURE.json',
      'PART_W33_PASS4827_PGSP_SIGN_BURNSIDE.json',
      'PART_W33_PASS4828_PARAMETRIC_OUTAGE_FLOW.json',
      'PART_W33_PASS4830_SIGN_LEVI_MODULE_INTERTWINER.json']
    for f in optional:
        p=ROOT/'data'/f
        if not p.exists():continue
        x=json.loads(p.read_text())
        assert 4825<=int(x['pass'])<=4830
