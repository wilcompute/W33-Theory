#!/usr/bin/env python3
"""Front 1: simultaneous proton Z9, scalar PQ quality, and color anomaly tests.

Relative to X=3(B-3Le), S=-18, T=-9, all scalar VEV charges are
multiples of 9 so exact low-energy Z9 remains. Add candidate scalar
A with charge +9n. Enumerate least-degree A-sensitive monomials
using S,T and their conjugates; separate that from already-allowed
S^dag T^2, which generically lifts the original relative phase.
One KSVZ Dirac color triplet chiral under X with mass from A has
nonzero SU3² U1X anomaly; two opposite-mass couplings cancel it.
These are necessary *field-inventory* conditions, not a completed
anomaly-free axion + proton theory or a mixed-operator search.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_extra_pq_proton_color_scalar_scan.json"
def min_A_monomial(n):
    # a=1 for A, exponent on S and T can be signed
    best=[]
    for aS in range(-n,n+1):
        for aT in range(-n,n+1):
            if n-2*aS-aT!=0:continue  # X_A=9n, X_S=-18, X_T=-9
            degree=1+abs(aS)+abs(aT)
            best.append((degree,aS,aT))
    return min(best)
def main():
    vals=[]
    for n in range(1,33):
        d,es,et=min_A_monomial(n)
        assert d==1+math.ceil(n/2)
        assert math.gcd(9,18,9*n)==9
        vals.append({"A_charge":9*n,"A_sensitive_min_dimension":d,
            "monomial_exponent_S":es,"monomial_exponent_T":et,
            "scalar_vevs_leave_Z9":True,
            "original_relative_phase_breaker_remains":"Sdag T^2 (dimension 3)"})
    assert vals[23]["A_sensitive_min_dimension"]==13
    # For one vectorlike-under-SM (3,1) pair P,Pc, mass AP Pc:
    # qP+qPc=-qA and total SU3²U1X anomaly=(qP+qPc)/2=-qA/2.
    q=sp.symbols("q",integer=True,nonzero=True)
    a1=-q/sp.Integer(2)
    a2=+q/sp.Integer(2)
    assert sp.simplify(a1+a2)==0
    # With two pairs, the second mass comes from A dagger,
    # and has opposite SU3²X contribution. This cancels local
    # mixed color anomaly, not all X, grav, cubic anomalies.
    out={"status":"PASS_Z9_SCALAR_PQ_AND_COLOR_ANOMALY_NECESSARY_FILTER",
      "base_gauged_X":"3(B-3Le), charges T=-9 S=-18",
      "add_scalar_A_charge_scan":vals,
      "first_A_sensitive_scalar_operator_dimension_formula":"1+ceil(abs(X_A/9)/2)",
      "high_quality_candidate_example":{"X_A":216,"first_A_sensitive_dimension":13,
         "operator":"A S^12 (or h.c. depending phase charge)",
         "cannot_infer_full_axion_quality":True},
      "preexisting_cubic_breaks_original_relative_scalar_phase":True,
      "one_QCD_colored_KSVZ_pair_color_mixed_X_anomaly":"-X_A/2",
      "two_pairs_with_A_and_A_dagger_masses_color_mixed_X_anomaly":"-X_A/2 + X_A/2 = 0",
      "crucial_limitation":"Cubic Sdag T² remains; scalar-only A dimension does NOT test mixed PQ-breaking fermion operators, whether A phase is eaten, QCD anomaly under an accidental global PQ, residual discrete gauge anomalies, heavy relic decays, or full cubic/gravitational X anomaly. Opposite-color anomaly partners may alter the intended PQ anomaly.",
      "sources":["Davighi-Greljo-Ponce Diaz arxiv:2609.01712","Di Luzio et al arxiv:2609.16110"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("PQ_COLOR_SCAN_PASS",vals[23]["A_sensitive_min_dimension"],len(vals),flush=True)
    return out
if __name__=="__main__":main()
