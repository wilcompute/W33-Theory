import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data'/'PART_W33_PASS7164_E8_FOURIER_ADDENDUM.json'

def test_pass7164_exact_cyclotomic_fourier():
    subprocess.run([sys.executable,str(ROOT/'analysis'/'w33_pass7164_e8_fourier_addendum.py')],check=True,cwd=ROOT)
    d=json.loads(CERT.read_text())
    assert d['status']=='PASS'
    assert d['k0_identity']=='M_0 = 2J - 2 A_W33'
    assert d['full_root_graph_spectrum']=={'-4':84,'-2':112,'8':35,'28':8,'56':1}
    assert d['sectors']['0']['spectrum']=={'-4':24,'8':15,'56':1}
    assert d['sectors']['1']['spectrum']=={'-2':36,'28':4}
    assert d['sectors']['2']['spectrum']=={'-4':30,'8':10}
    assert d['sectors']['3']['spectrum']=={'-2':40}
