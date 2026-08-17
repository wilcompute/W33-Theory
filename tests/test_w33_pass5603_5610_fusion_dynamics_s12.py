from __future__ import annotations
import importlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))


def test_5603_symbolic_bose_mesner():
    m=importlib.import_module('w33_pass5603_psl2_fixedpoint_fusion_symbolic')
    out=m.symbolic_packet()
    assert out['status']=='THEOREM_SYMBOLIC_BOSE_MESNER_CLOSURE'
    assert out['multiplicities'][2]=='q^2'
    assert out['q3_structural_collapse']['two_fixed_relation_valency']==0


def test_5604_distance_formula():
    m=importlib.import_module('w33_pass5604_isodual_minimum_distance')
    for q in (3,5,7,9,11,25):
        x=m.theory(q)
        assert x['distance']==q+1
        assert x['lower_bound_at_s_eq_q']>0


def test_5605_hodge_hashimoto_counts():
    m=importlib.import_module('w33_pass5605_hodge_hashimoto_scaling_firewall')
    for q in (3,5,9,25):
        h=m.hodge(q)
        assert sum(x['multiplicity'] for x in h['spectrum'])==h['dimension']
        b=m.hashimoto(q)
        assert sum(x['multiplicity'] for x in b['BBt_singular_bands'])==b['directed_edges']


def test_5607_box_spectrum_dimension():
    m=importlib.import_module('w33_pass5607_segre_dalembertian_no_go')
    for q in (3,5,9,25):
        x=m.packet(q)
        assert sum(a['multiplicity'] for a in x['box_spectrum'])==x['events']


def test_5609_exact_phase_certificate_exists_after_replay():
    p=ROOT/'data/PART_W33_PASS5609_S12_HEISENBERG_PHASE_SEGRE_SPECTRUM.json'
    if not p.exists():
        m=importlib.import_module('w33_pass5609_s12_heisenberg_phase_segre_spectrum'); m.main()
    x=json.loads(p.read_text())
    assert x['magnetic_distinct_eigenvalues_numeric']==15
    assert x['nonzero_flux_triangles']==60
    assert x['exact_characteristic_polynomial_coefficients_descending'][0]==1


def test_5610_explicit_embedding_exists_after_replay():
    p=ROOT/'data/PART_W33_PASS5610_S12_W33_SYMPLECTIC_EMBEDDING_FIREWALL.json'
    if not p.exists():
        m=importlib.import_module('w33_pass5610_s12_w33_symplectic_embedding_firewall'); m.main()
    x=json.loads(p.read_text())
    assert x['forms_match_exactly'] is True
    assert x['all_pair_checks']==6561


def test_5608_m12_shell_after_replay():
    p=ROOT/'data/PART_W33_PASS5608_S12_GOLAY_WEIGHT12_M12_ACTION.json'
    if p.exists():
        x=json.loads(p.read_text())
        assert x['induced_group_order']==95040
        assert x['orbital_sizes']==[12,132]


def test_5606_cover_to_f4_object_bijection_is_frozen():
    gate = json.loads(
        (ROOT / 'data/PART_W33_PASS5606_COVER12_EXPLICIT_CONJUGATOR.json').read_text()
    )
    bridge = json.loads(
        (ROOT / 'data/PART_W33_PASS5606_COVER_TO_F4_ROOTPAIR_MAP.json').read_text()
    )
    assert gate['conjugate_in_S12'] is True
    assert gate['cover12_order'] == gate['latin12_order'] == 576
    assert gate['conjugator_cover12_to_latin12_one_based'] == [
        1, 9, 4, 8, 12, 7, 10, 2, 5, 3, 6, 11
    ]
    rows = bridge['map']
    assert len(rows) == 12
    assert sorted(row['cover_action_position_one_based'] for row in rows) == list(range(1, 13))
    assert sorted(row['latin_symbol_zero_based'] for row in rows) == list(range(12))
    assert sorted(row['F4_short_rootpair_index_zero_based'] for row in rows) == list(range(12))
