from functools import lru_cache
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))

import w33_levi_next5_v2 as subject

@lru_cache(maxsize=1)
def result():
    return subject.analyze()

def test_all_five_tracks_pass():
    data=result()
    assert data['status']=='PASS'
    assert data['all_five_pass']
    assert all(data['checks'].values())

def test_symbolic_rank_certificate_closes_jordan_law():
    track=result()['tracks']['1_formal_odd_q_rank_certificate']
    assert track['status']=='PROVED'
    assert track['checks']['J2_absent']
    assert track['checks']['J4_two']
    assert len(track['certificate']['sha256'])==64

def test_sentinel_combined_theorem():
    track=result()['tracks']['2_sentinel_authenticated_admission']
    assert track['code']['parameters']=='[40,15,8]_2'
    assert track['checks']['all_sampled_weight_1_to_7_errors_rejected_at_sentinel']
    assert track['checks']['sentinel_dark_weight8_still_rejected_by_provenance']
    assert track['checks']['authenticated_raw_type_confusion_rejected']

def test_mod8_lift_is_fixed_line_plus_U14_minus():
    track=result()['tracks']['3_mod8_U14_lift']
    assert track['two_part']=='A_2(L_-4) = (Z/2)^14 + Z/8'
    assert track['canonical_filtration']['q_h']=='11/8 mod 2Z'
    assert track['canonical_filtration']['U14_isotropic_nonzero']==8127
    assert track['brown_invariants']=={'Z8_depth_block':7,'U14_minus':4,'full_2_part':3}

def test_native_runtime_is_WE6_regular_action():
    track=result()['tracks']['4_native_51840_action']
    assert track['orbit_structure']['PSp']==[25920,25920]
    assert track['orbit_structure']['full_extension']==[51840]
    assert track['stabilizers']['point_stabilizer_mod_center_Clifford']==216
    assert track['stabilizers']['noncollinear_pair']==48
    assert track['checks']['coordinate_bijection_2x40x3x216']

def test_photonic_compiler_reduces_to_eight_bins():
    track=result()['tracks']['5_photonic_E8_compiler']
    assert track['active_time_bins']==[0,4,7,13,40,41,44,45]
    assert track['active_determinant']==-1
    assert track['compiler_options']['exact_coherent_dilation']['total_modes']==16
    assert track['compiler_options']['exact_coherent_dilation']['Clements_MZIs']==120
    assert track['compiler_options']['sparse_weighted_readout']['tunable_couplers']==86

def test_photonic_loss_dark_model_is_guarded():
    track=result()['tracks']['5_photonic_E8_compiler']
    sim=track['hardware_fault_simulation']
    assert sim['loss_retries']>0
    assert sim['dark_events_admitted']==0
    assert track['checks']['dark_faults_never_admitted']

def test_cli_dispatches_new_commands(capsys):
    sys.path.insert(0, str(ROOT))
    import holonet_cmd
    import pytest
    for command in ('packet-sentinel-stack','photonic-e8-compile'):
        with pytest.raises(SystemExit) as exc:
            holonet_cmd.main([command])
        assert exc.value.code==0
        assert '"status": "PROVED"' in capsys.readouterr().out
