"""Five-qubit perfect CODE photonic erasure protection and concatenation cost.

Builds on the repository's verified [[5,1,3]] Knill-Laflamme code.
Physical source/decoder/transversal-gate overhead NOT established.
"""
from pathlib import Path
from math import comb
import json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_five_qubit_photon_erasure_resources.json"

def logical_failure(p):
    return sum(comb(5,k)*p**k*(1-p)**(5-k) for k in range(3,6))

def run():
    import sys
    sys.path.insert(0,str(ROOT/"analysis"))
    from importlib import import_module
    verified=import_module("2026_11_03_five_qubit_algebraic_locality")
    assert len(verified.GEN)==4
    # Exact KL property verified separately by existing 32x32 matrices;
    # re-enumerate three-qubit representatives to prove each 3-erasure
    # subset supports a logical operator and hence cannot be corrected.
    group={"IIIII"}
    for gene in verified.GEN:
        group|={verified.mulword(word,gene) for word in tuple(group)}
    assert len(group)==16
    from itertools import combinations
    for erased in combinations(range(5),3):
        E=frozenset(erased)
        has_logical_X=any(verified.support(verified.mulword(verified.LX,g))<=E for g in group)
        has_logical_Z=any(verified.support(verified.mulword(verified.LZ,g))<=E for g in group)
        assert has_logical_X and has_logical_Z
    p=s.symbols("p")
    f=s.expand(sum(comb(5,k)*p**k*(1-p)**(5-k) for k in range(3,6)))
    assert s.factor(f-p)==p*(p-1)*(2*p-1)*(3*p*p-3*p-1)
    assert s.expand(f-(10*p**3-15*p**4+6*p**5))==0
    cases=[]
    for eta in (.9,.75,.55,.49):
        initial=1-eta; levels=[initial]
        for j in range(7):levels.append(logical_failure(levels[-1]))
        cases.append({"physical_photon_survival_eta":eta,
                      "physical_erasure_probability":initial,
                      "logical_erasure_probabilities_level_0_to_7":levels})
    scenarios=[]
    for n,target,eta in [(50,1e-3,.9),(1000,1e-6,.9),
                         (100000,1e-6,.9),(1000,1e-6,.75),
                         (1000,1e-6,.49)]:
        p0=1-eta
        vals=[p0]
        for level in range(1,8):
            vals.append(logical_failure(vals[-1]))
        feasible=[l for l,pfail in enumerate(vals) if n*pfail<=target]
        L=feasible[0] if feasible else None
        scenarios.append({"logical_qubits":n,"target_total_erasure_failure_upper_bound":target,
                          "single_photon_eta":eta,"levels_search_max":7,
                          "minimal_levels_certified_by_union_bound":L,
                          "physical_photonic_qubits_per_logical":5**L if L is not None else None,
                          "total_physical_photonic_qubits":n*(5**L) if L is not None else None,
                          "total_error_union_upper_bound":n*vals[L] if L is not None else None,
                          "logical_error_after_levels_0_to_7":vals})
    assert abs(logical_failure(.1)-.00856)<1e-13
    assert cases[0]["logical_erasure_probabilities_level_0_to_7"][3]<1e-12
    assert cases[-1]["logical_erasure_probabilities_level_0_to_7"][1]>.51
    return_value={
      "source_5qubit_code":"analysis/2026_11_03_five_qubit_algebraic_locality.py; 4 generators exact full 32x32 KL test in existing repo",
      "independent_all_ten_three_erasure_logical_support_failures_verified":True,
      "exact_level_map":"p_next=10p^3-15p^4+6p^5 = Pr[at least three of five photons erased]",
      "exact_fixed_points_factorization":str(s.factor(f-p)),
      "nontrivial_erasure_threshold":.5,
      "same_threshold_as_positive_unassisted_qubit_erasure_capacity":True,
      "per_level_cases":cases,
      "resource_scenarios":scenarios,
      "no_ft_gate_escape":"Even if storage erasure is suppressed by 5-qubit concatenation, an independently successful 75% heralded entangling gate required on N physical operations would give 0.75^N without active fault-tolerant feedforward. A protected universal logical gate set and nondemolition erasure flags are not derived.",
      "scope":"Independent erasure events, known locations, ideal encoding/decoding/ancillas and no gate or source errors. A 5-qubit QECC is not an optical implementation by itself. No better-than-QM prediction or TOE test; only standard quantum loss-resource engineering."
    }
    OUT.write_text(json.dumps(return_value,indent=2)+"\n",encoding="utf8")
    for z in scenarios:print("RESOURCE",z["logical_qubits"],z["single_photon_eta"],"L",z["minimal_levels_certified_by_union_bound"],"photons",z["total_physical_photonic_qubits"],"fail_bound",z["total_error_union_upper_bound"])
    print("PASS full [[5,1,3]] erasure subset proof, threshold 50% & concatenation resources")
    print(OUT)
    return return_value
if __name__=="__main__":run()
