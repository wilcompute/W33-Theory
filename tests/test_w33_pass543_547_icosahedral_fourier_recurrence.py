from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 sys.path.insert(0,str(ROOT/'analysis'))
 p=ROOT/'analysis'/name;s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def test_pass543_association_image():
 p=load('w33_pass543_q5_icosahedral_association_image.py').payload()
 assert p['status']=='PASS'
 assert p['association_scheme']['permutation_module']=='1 + 3 + 3prime + 5'
 assert p['linearized_block_map']['gram']=='-10 I_12'
def test_pass544_switch_fibre():
 p=load('w33_pass544_binary_switch_spectral_fibre.py').payload()
 assert p['status']=='PASS'
 assert p['scan']['distinct_exact_charpolys']==98
 assert p['scan']['target_fibre']==80
 assert not p['scan']['linear_code']
def test_pass545_antiunitary_lift():
 p=load('w33_pass545_triality_antiunitary_lift.py').payload()
 assert p['status']=='PASS'
 assert p['checks']['exact_antiunitary_intertwiner']
 assert p['checks']['vector_charpoly_distinct']
def test_pass546_z9_fourier():
 p=load('w33_pass546_z9_kernel_fourier_image.py').payload()
 assert p['status']=='PASS'
 assert p['kernel_fourier']['dimension_check']==40
 assert p['nonlinear_base_slice']['distinct_exact_charpolys']==13
def test_pass547_recurrence():
 p=load('w33_pass547_q5_recurrence_families.py').payload()
 assert p['status']=='PASS'
 assert p['checks']['sparse_valuation_law_1000']
 assert p['checks']['constant_families_galois_conjugate']
 assert p['checks']['odd_switch_recurrences_identical']
def test_static_release_certificate_present_and_pass():
 import json
 p=ROOT/'data'/'w33_pass543_547_icosahedral_fourier_recurrence.json'
 d=json.loads(p.read_text(encoding="utf-8"))
 assert d['status']=='PASS'
 assert d['total_exact_checks']==46
