from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rd(p): return (ROOT/p).read_text()

def test_status_fail_closed():
    s=rd('scripts/w33_ce2_k3_evidence_repair_status.py')
    assert "ce2_global_closure='OPEN'" in s
    assert 'k3_curvature_object_loaded=False' in s
    assert 'REFUTED_FOR_DISPLAYED_BLOCKS' in s

def test_transport_scaffold_conditional_only():
    s=rd('scripts/w33_transport_cocycle_scaffold.py')
    assert 'CONDITIONAL_SCAFFOLD_ONLY' in s
    assert 'No actual family-flag identification' in s
    assert 'rho =' not in s

def test_k3_count_is_ambient_upper_bound():
    s=rd('scripts/w33_k3_witness_search_scaffold.py')
    assert 'AMBIENT_UPPER_BOUND_SCAFFOLD_ONLY' in s
    assert 'admissible_candidate_count' in s
    assert 'None' in s
    assert '174816' in s

def test_summary_corrected():
    s=rd('docs/pass_6189_6232_summary.md')
    assert 'CORRECTED BY PASS6233–6240' in s
    assert 'CE2 global orbit closure: **OPEN**' in s
