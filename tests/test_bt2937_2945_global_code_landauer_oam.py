from __future__ import annotations
import importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'analysis'/'bt2937_2945_global_code_landauer_oam.py'
CERT=ROOT/'data'/'PART_BT2937_BT2945_GLOBAL_CODE_LANDAUER_OAM_results.json'
spec=importlib.util.spec_from_file_location('bt2937',SOURCE); assert spec and spec.loader
bt=importlib.util.module_from_spec(spec); spec.loader.exec_module(bt)
_RESULT=bt.build_result()
def result(): return _RESULT
def test_frozen(): assert json.loads(CERT.read_text(encoding="utf-8"))==result()
def test_global():
 d=result()['global_affine_support_code']; assert (d['global_lower_bound'],d['global_upper_bound'],d['binary_minimum_distance'])==(13,16,4)
def test_outer():
 d=result()['nonlinear_code_identification']; assert d['parameters']=='[8,4,4]_3'; assert d['isodual'] and not d['self_dual']; assert d['single_symbol_syndrome_count']==16; assert d['coordinate_automorphism_order']==24; assert d['monomial_automorphism_order']==48
def test_m36(): assert 0.072 < result()['m36_fault_envelope']['accepted_fault_budget'] < 0.074
def test_calibration():
 rows=result()['calibrated_active_observer']['rows']; assert [r['repetitions_per_support_bit'] for r in rows]==[5,9,13,18]; assert all(r['union_bound_16_observations']<=r['target_total_failure'] for r in rows)
def test_landauer(): assert abs(result()['landauer']['state_entropy_bits']-6.339850002884624)<1e-12
def test_oam():
 d=result()['oam']['group_theoretic_addressing_obstruction']; assert d['projective_similitude_actions']==51840 and d['maximum_single_orbit']==12 and not d['forty_cycle_exists']
def test_rtl_contract_files():
 rtl=(ROOT/'rtl'/'w33_pass2938_isodual_support_codec.sv').read_text(encoding="utf-8"); tb=(ROOT/'rtl'/'tb_w33_pass2938_isodual_support_codec.sv').read_text(encoding="utf-8"); assert 'module w33_pass2938_isodual_support_encoder' in rtl; assert 'module w33_pass2938_isodual_support_decoder' in rtl; assert '16-entry correction' in rtl; assert 'PASS 81 clean + 1296 one-bit corrections' in tb
