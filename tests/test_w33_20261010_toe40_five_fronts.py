"""Focused TOE40 standalone/actual W33 Maxwell replay."""
import subprocess,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def launch(name,certificate):
    p=subprocess.run([sys.executable,str(ROOT/'analysis'/name)],cwd=ROOT,check=True,capture_output=True,text=True,timeout=180)
    assert p.returncode==0
    return json.loads((ROOT/'data'/certificate).read_text())
def test_four_independent_controls():
    d=launch('w33_20261010_toe40_four_controls.py','w33_20261010_toe40_four_controls.json')
    assert d['chirality']['Dirac_index']==0
    assert d['modular']['S_modular_generator_defect']>.01
    assert d['ccz']['nonzero_third_mixed_difference']==1
    assert d['falsifiers']['conditional_sigma_discrepancy']>200
def test_native_W33_maxwell_canonical_gauge():
    d=launch('w33_20261010_toe40_native_maxwell_hamiltonian.py','w33_20261010_toe40_native_maxwell_hamiltonian.json')
    assert d['status']=='PASS'
    assert all(abs(q-4)<.01 for q in d['linear_dispersion_eigenvalue_ratio_double_k'])
    assert all(x['curl_rank']==80 and x['gradient_rank']==80 for x in d['k_samples'])
