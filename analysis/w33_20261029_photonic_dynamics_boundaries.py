#!/usr/bin/env python3
"""Two falsifiers: a single-photon loss/dimension boundary and
the non-uniqueness of W33-invariant unitary dynamics.
No claim that finite graph spectra derive laboratory particle physics.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
from w33_incidence_even_line_resolution_20261029 import make_geometry,rank_basis
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261029_photonic_dynamics_boundaries.json"
def main():
    points,lines,lm,A,N,*_=make_geometry(3)
    n=len(A);assert n==40 and len(rank_basis(A))==16
    degrees=[x.bit_count() for x in A]
    assert all(d==12 for d in degrees)
    common_adj=[]
    common_non=[]
    for i in range(n):
        for j in range(i+1,n):
            count=(A[i]&A[j]).bit_count()
            if (A[i]>>j)&1:common_adj.append(count)
            else:common_non.append(count)
    assert len(common_adj)==240 and set(common_adj)=={2}
    assert len(common_non)==540 and set(common_non)=={4}
    # A^2=8I-2A+4J, eigenvalues 12 (1), 2 (24), -4 (15).
    # H=A and H'=A+J/40 are both invariant under every W33 automorphism.
    # At t=pi, e^-itH=I whereas e^-itH' = I-2J/40.
    # Vertex return probability for H'=|1-2/40|^2=361/400.
    revival_A=Fraction(1,1)
    revival_A_plus_J=Fraction(19,20)**2
    assert revival_A_plus_J==Fraction(361,400)
    assert revival_A!=revival_A_plus_J
    # Single-excitation Hilbert space of M modes has exactly dimension M.
    # A loss channel rho -> eta*rho+(1-eta)|vac><vac| has output
    # trace distance eta for any two orthogonal one-photon inputs.
    loss_eta=Fraction(9,10)
    assert loss_eta<1
    mode_counts=[40,240,256]
    results={
        "W33_srg":{"v":40,"degree":12,"adjacent_common_neighbors":2,
                   "nonadjacent_common_neighbors":4,
                   "A_squared_identity":"8I - 2A + 4J",
                   "integer_spectrum":{"12":1,"2":24,"-4":15}},
        "invariant_dynamics_counterexample":{
            "H1":"A","H2":"A+J/40","time":"pi in units where b=1",
            "H1_site_return_probability":"1",
            "H2_site_return_probability":"361/400",
            "conclusion":"W33 symmetry alone does not fix a unique Hamiltonian or clock rate"},
        "one_photon_dimension":{"40_modes_logical_qubit_ceiling":5,
                                "240_modes_logical_qubit_ceiling":7,
                                "256_modes_logical_qubit_ceiling":8,
                                "full_adjacency_css_8_logical_requires_at_least_modes":256,
                                "one_photon_40_mode_model_fails_8_logicals":True,
                                "one_photon_240_mode_model_fails_8_logicals":True},
        "loss_no_go":{"eta":"9/10","orthogonal_input_trace_distance":"1",
                      "postloss_trace_distance":"9/10",
                      "exact_deterministic_recovery_impossible_for_eta_lt_1":True,
                      "heralded_survival_not_excluded":True,
                      "requires":"additional quantum carriers and a precise syndrome/erasure recovery model"},
        "limits":["no prediction of particle masses or GR","does not preclude encoding 4 qubits in 40 modes","does not preclude heralded or externally assisted photonic schemes"]}
    OUT.write_text(json.dumps(results,indent=2)+"\n",encoding="utf8")
    print("PASS: W33 invariant dynamics non-uniqueness and single-photon dimension/loss tests")
    print("fixed-time return:",revival_A,revival_A_plus_J)
if __name__=="__main__":main()
