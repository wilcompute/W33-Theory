from __future__ import annotations
import json,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PASSES=range(468,473)
FILES={
  468:'semisimple_sheet_intertwiner',469:'galois_ring_conductor_tower',
  470:'integral_conductor_coupling',471:'uniform_cover_prime_power_witness',
  472:'hardware_custody_gate',
}

def test_certificates_regenerate():
    for n,name in FILES.items():
        subprocess.run([sys.executable,str(ROOT/'analysis'/f'w33_pass{n}_{name}.py'),'--check'],check=True)

def test_all_payloads_pass():
    for n,name in FILES.items():
        payload=json.loads((ROOT/'data'/f'w33_pass{n}_{name}.json').read_text(encoding="utf-8"))
        assert payload['status']=='PASS'
        assert all(payload['checks'].values())

def test_intertwiner_and_coupling_headlines():
    p468=json.loads((ROOT/'data'/'w33_pass468_semisimple_sheet_intertwiner.json').read_text(encoding="utf-8"))
    assert p468['central_character_quotient']['quotient_group']=='C2'
    p470=json.loads((ROOT/'data'/'w33_pass470_integral_conductor_coupling.json').read_text(encoding="utf-8"))
    assert [p470['exact_exponent_counts_including_units'][str(i)] for i in (6,7,8)]==[0,11,7]

def test_prime_power_and_hardware_boundaries():
    p471=json.loads((ROOT/'data'/'w33_pass471_uniform_cover_prime_power_witness.json').read_text(encoding="utf-8"))
    assert {x['q'] for x in p471['exact_witnesses']}=={3,5,7,9}
    p472=json.loads((ROOT/'data'/'w33_pass472_hardware_custody_gate.json').read_text(encoding="utf-8"))
    assert p472['physical_status']=='OPEN_NO_MEASURED_INPUTS'
    assert 'no laboratory score' in p472['boundary'].lower()
