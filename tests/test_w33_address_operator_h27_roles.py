from __future__ import annotations
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load():
    p=ROOT/"analysis/w33_address_operator_h27_roles.py"
    s=importlib.util.spec_from_file_location("addr_op_h27",p); assert s and s.loader
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def test_address_operator_h27_roles():
    o=load().main(False)
    assert o["status"]=="PASS_ADDRESS_AND_OPERATOR_H27_ROLES_SEPARATED_AND_EXECUTABLE"
    assert o["address"]["right_cosets"]==45
    assert o["address"]["lifted_cosets"]==270
    assert o["address"]["line_orbit_sizes"]==[9,36]
    assert o["address"]["phase_fixed_instruction_orbit_sizes"]==[27,27,216]
    assert o["address"]["anchored_incidence_isomorphism_count"]==1920
    assert o["operator"]["two_qutrit_Pauli_span_rank"]==81
    assert o["operator"]["Pauli_span_field"]=="Q(omega), omega^2+omega+1=0, exact Fraction pairs"
    assert o["operator"]["Pauli_Hilbert_Schmidt_Gram"]=="9 I_81 exactly"
    assert o["operator"]["generated_algebra_dimension"]==81
    assert o["operator"]["commutant_dimension"]==81
    assert o["operator"]["multiplicity_noiseless_subsystem_dimension"]==9
    assert o["operator"]["center_fixed_internal_ray_count"]==27
    assert o["operator"]["center_fixed_matter_ray_count"]==81
    assert o["nonidentification"]["same_permutation_action"] is False
    assert all(o["checks"].values())
    stored=json.loads((ROOT/"data/w33_address_operator_h27_roles.json").read_text())
    assert stored==o
