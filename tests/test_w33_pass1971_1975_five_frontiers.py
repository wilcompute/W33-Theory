from analysis.w33_pass1971_1975_verify_frozen import main


def test_frozen_packet():
    out=main()
    assert out['n_checks']==out['n_verified']==45


def test_boundaries_and_corrections():
    import json
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    d71=json.loads((root/'data/w33_pass1971_spread_treatments_concordance.json').read_text(encoding="utf-8"))
    d72=json.loads((root/'data/w33_pass1972_scalable_constraint_audit.json').read_text(encoding="utf-8"))
    d73=json.loads((root/'data/w33_pass1973_solver_stagnation_diagnosis.json').read_text(encoding="utf-8"))
    d74=json.loads((root/'data/w33_pass1974_uniform_spread_proofs.json').read_text(encoding="utf-8"))
    d75=json.loads((root/'data/w33_pass1975_claim_ledger_physics_engineering.json').read_text(encoding="utf-8"))
    assert d71['status']=='PASS_WITH_FALSE_MAXIMALITY_WITHDRAWN'
    assert d72['boundary'].startswith('Witness and orbit audits')
    assert d73['comparisons']['combined40_over_spread_branches']>8
    assert d74['q3_correction']['completion_possible'] is False
    assert d75['physics']['withdrawn'][:2]==['electric charge','homological or Dirac flux']
