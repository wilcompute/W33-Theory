from __future__ import annotations
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))

def test_pass573_c3_and_600cell():
 p=load('w33_pass573_hjelmslev_c3_600cell_apex.json')
 assert p['status']=='PASS'
 assert p['hjelmslev_symmetry']['dominant_size3_single_C3_orbits']==177377
 assert p['600cell_apex']['base_vertices']==12
 assert p['checks']['module_mismatch_falsifier']

def test_pass574_association_scheme():
 p=load('w33_pass574_singer_coherent_configuration.json')
 assert p['status']=='PASS'
 assert p['scheme']['rank']==9
 assert p['spectral']['multiplicities']==[1,7,20,28,45,45,56,64,70]
 assert p['automorphisms']['full_automorphism_upper_bound']==20160

def test_pass575_principal_kernel_source():
 p=load('w33_pass575_cyclotomic_dvr_kernel_formal.json')
 s=(ROOT/'formal/W33/Pass575CyclotomicDVRKernel.lean').read_text(encoding="utf-8")
 assert p['status']=='PASS'
 assert 'theorem residueIdeal_eq_lambda_span' in s
 assert not any(x in s for x in ('sorry','admit','axiom'))

def test_pass576_exact_central_idempotents():
 p=load('w33_pass576_exact_walsh_central_idempotents.json')
 assert p['status']=='PASS'
 assert p['group']['identification']=='D10 x C4'
 assert p['signed_Walsh_representation']['projector_ranks']==[104]*8+[408]*8
 assert len(p['formula_signatures'])==6

def test_pass577_dynamic_program():
 p=load('w33_pass577_bayesian_posterior_dynamic_program.json')
 assert p['status']=='PASS'
 assert p['results']['conservative']['absolute_gain']>0
 assert p['results']['nominal']['absolute_gain']>0
 assert abs(p['results']['aspirational']['absolute_gain'])<1e-8
 assert p['results']['aspirational']['states_strictly_improved']>0

def test_release_custody():
 p=load('w33_pass573_577_c3_600cell_scheme_dvr_idempotent_dp_release.json')
 assert p['status']=='PASS' and p['owner_check_total']==58
 for row in p['owner_custody'].values():
  assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
