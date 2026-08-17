from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def rd(p): return (ROOT/p).read_text()


def test_anchor23_not_closed():
    s=rd('scripts/w33_ce2_anchor23_full_orbit.py')
    assert 'OPEN_BEYOND_FIVE_SEED_ROWS__NOT_CLOSED' in s
    assert 'orbit_action_constructed' in s
    assert 'family_counts' not in s


def test_anchor24_25_are_hypotheses_only():
    for p in ('scripts/w33_ce2_anchor24_orbit.py','scripts/w33_ce2_anchor25_orbit.py'):
        s=rd(p)
        assert 'UNVERIFIED_ANALOGY_SEEDS_ONLY__NOT_CLOSED' in s
        assert 'source_certificate' in s
        assert 'family_counts =' not in s


def test_batches_have_no_fake_covered_counts():
    for p in ('scripts/w33_ce2_anchor26_31_batch.py','scripts/w33_ce2_anchor32_39_final.py'):
        s=rd(p)
        assert 'OPEN__NO_ROWS_OR_ACTION_CERTIFICATE' in s
        assert "'actual_rows_loaded':0" in s
        assert 'covered = sum' not in s


def test_global_verifier_fail_closed():
    s=rd('scripts/w33_ce2_global_closure_verify.py')
    assert 'GLOBAL STATUS: OPEN / NOT VERIFIED COMPLETE' in s
    assert 'coverage_denominator=20' in s
    assert 'actual_rows_loaded' in s
    assert 'VERIFIED COMPLETE' not in s


def test_k3_scan_requires_real_object():
    s=rd('scripts/w33_k3_curvature_witness_scan.py')
    assert 'NO_OBJECT_LOADED__WITNESS_SCAN_NOT_RUN' in s
    assert 'loaded_matrix_hash' in s
    assert 'coordinate_map_certificate' in s
    assert 'np.zeros' not in s


def test_summaries_corrected():
    assert 'CORRECTED BY PASS6137–6144' in rd('docs/pass_6041_6064_summary.md')
    assert 'CORRECTED BY PASS6137–6144' in rd('docs/pass_6065_6136_summary.md')
