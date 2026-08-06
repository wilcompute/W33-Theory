from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODULE=ROOT/'analysis/w33_pass4033_4040_physics_continuation.py'
spec=importlib.util.spec_from_file_location('pass4033_4040',MODULE)
module=importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)
RESULT=module.main()

def test_all_checks_hold():
 assert RESULT['all_checks_hold']

def test_full_h1_swap_compiler():
 x=RESULT['pass4033_full_H1_swap_compiler']
 assert x['basis_shape']==[160,81]
 assert x['columns']==list(range(81))
 assert x['isometry_error']<1e-10
 assert x['projector_error']<1e-10

def test_projected_disorder_and_control():
 x=RESULT['pass4034_projected_disorder_algebra']
 assert (x['onsite_span'],x['coupling_span'],x['combined_span'])==(160,320,320)
 assert x['commutant']=='scalars'
 assert x['generated_lie_algebra'].startswith('u(81)')

def test_literal_algebra_gate_is_fail_closed():
 x=RESULT['pass4035_literal_algebra_gate']
 assert x['status'] in {'COMPLETE','BLOCKED_ENGINE_OUTPUTS_MISSING'}
 if x['status']=='BLOCKED_ENGINE_OUTPUTS_MISSING':
  assert not (x['relation_output'] and x['monster_output'])

def test_compressed_tomography():
 x=RESULT['pass4036_compressed_sector_tomography']
 assert [x[k]['minimal_nontrivial_probes'] for k in ['mode_H2','signed_Levi','line_graph']]==[2,4,4]
 assert max(v['chebyshev_condition_2'] for v in x.values())<2

def test_fabrication_and_bonkers_physics():
 assert RESULT['pass4037_fabrication_contract']['gap_over_J']>1.5
 assert RESULT['pass4038_bonkers_dissipative_Hodge_refrigerator']['decay_spectrum']['0']==81
 assert RESULT['pass4039_bonkers_disorder_as_universal_control']['hamiltonian_lie_closure']=='u(81)'
 assert RESULT['pass4040_bonkers_Levi_Coulomb_law']['resistance_by_distance']['4']['resistance']=='7/10'
