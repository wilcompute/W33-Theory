from analysis.w33_pass1966_1970_verify_frozen import main

def test_frozen_packet():
    out=main()
    assert out['n_checks']==out['n_verified']==37

def test_boundaries_and_key_values():
    import json
    from pathlib import Path
    r=Path(__file__).resolve().parents[1]
    d66=json.loads((r/'data/w33_pass1966_combined_spread_signature_geometry.json').read_text(encoding="utf-8"))
    d68=json.loads((r/'data/w33_pass1968_internal_mu6_structural_role.json').read_text(encoding="utf-8"))
    d69=json.loads((r/'data/w33_pass1969_backward_constraint_audit.json').read_text(encoding="utf-8"))
    assert d66['bounded_9color_highs']['conclusion']=='UNKNOWN'
    assert d66['exact_nonvacuity_witness']['survivors_after_40_cuts']==807
    assert d68['sector_action']['eisenstein_rotated_sector']==90
    assert d68['boundary'].startswith('Cyclotomic sector marker')
    assert d69['status']=='PASS_WITH_TWO_LEGACY_REPLAYS_UNLOCATED'
