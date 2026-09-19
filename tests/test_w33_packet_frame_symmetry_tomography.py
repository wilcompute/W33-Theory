import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run():
    subprocess.run([sys.executable,str(ROOT/'analysis/w33_packet_frame_symmetry_tomography.py')],cwd=ROOT,check=True)
    return json.loads((ROOT/'data/w33_packet_frame_symmetry_tomography.json').read_text())

def test_symmetry_tomography_replay():
    d=run()
    assert d['status']=='PASS_72_FRAME_TOMOGRAPHY_TWIRL'
    assert d['population_tomography']['decoder']=='p=(A(H(2,3))/2-J/5)y'
    assert d['population_tomography']['condition_number_2']=='5'
    assert d['population_tomography']['white_measurement_noise_average_variance_gain']=='14/25'
    assert d['twirl']['operator_invariant_dimension']==3
    assert d['twirl']['twirled_superoperator_commutant_dimension']==105
    assert d['twirl']['generic_superoperator_dimension_before']==6561

def test_runtime_fibers_are_9_by_8_with_phase_balance():
    d=run()
    fibers=d['runtime_frame']['center_fibers']
    assert len(fibers)==9
    assert sorted(x['hesse_bin'] for x in fibers)==list(range(9))
    for f in fibers:
        assert len(f['settings'])==8
        assert sum(x['phase_action']=='preserve' for x in f['settings'])==4
        assert sum(x['phase_action']=='invert' for x in f['settings'])==4
        assert len({x['slot'] for x in f['settings']})==8
