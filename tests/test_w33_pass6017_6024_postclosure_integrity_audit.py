from pathlib import Path
import math

ROOT=Path(__file__).resolve().parents[1]

def rd(p): return (ROOT/p).read_text()


def test_ce2_anchor22_live_status_is_open():
    s=rd('scripts/w33_ce2_anchor22_closure.py')
    assert 'OPEN_BEYOND_THREE_IMPORTED_WITNESSES' in s
    assert "'full_orbit_enumerated':False" in s
    assert 'def ce2_triple_weight' not in s


def test_yukawa_real_spectra_and_flag_refutation():
    A=((367,-55),(-55,175)); B=((323,275),(275,659))
    for M,tr,det,disc in [(A,542,61200,48964),(B,982,137232,415396)]:
        assert M[0][0]+M[1][1]==tr
        assert M[0][0]*M[1][1]-M[0][1]*M[1][0]==det
        assert tr*tr-4*det==disc and disc>0
        assert sum(M[0]) != sum(M[1])
    s=rd('scripts/w33_yukawa_radical_pair_closure.py')
    assert 'Refuted: equal-coordinate/generation-flag eigenvector alignment.' in s


def test_k3_formal_avatar_corrects_false_gcd():
    xs=[780,7944,62600,53979]
    g=0
    for x in xs:g=math.gcd(g,x)
    assert g==1
    s=rd('scripts/w33_k3_glue_slot_realization.py')
    assert 'assert g==1' in s
    assert "'status':'FORMAL_AVATAR_ONLY'" in s
    assert "'genuine_K3_glue_witness':'OPEN'" in s


def test_closure_ledger_propagates_physics_downgrade():
    s=rd('scripts/w33_bridge_full_closure_theorem.py')
    assert 'ANSATZ/COMPARISON-ONLY per Pass5957-5964' in s
    assert 'actual_gcd_of_780_7944_62600_53979' in s
    assert 'CE2 anchor-22 is NOT globally closed' in s


def test_qiskit_file_is_scaffold_not_oracle():
    s=rd('tools/qiskit/toe_bridge_completed_avatar_oracle.py')
    assert 'SEARCH SCAFFOLD' in s
    assert 'No phase oracle or computed predicate is implemented.' in s
    assert 'MARKED_CE2' not in s


def test_corrected_summary_is_live():
    s=rd('docs/pass_5957_6016_summary.md')
    assert 'CORRECTED BY PASS6017–6024' in s
    assert 'actual gcd **1**, not 217' in s
