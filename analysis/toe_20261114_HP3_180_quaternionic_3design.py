#!/usr/bin/env python3
"""Exact HP3 projective 3-design from the 180 minimal signed E6 charges.

The 27 J-even Pauli coordinates z of a random complex 8D pure state
are uniform on HP3 under the twistor map CP7 -> HP3. Haar first,
second, and third moments are computed from the exact cycle trace
formula, and tested against the complete 180-charge census. The
fourth moment of a coordinate is 1/9 on the finite set but 1/33 for
Haar: rigorous failure of projective 4-design.
"""
from itertools import permutations,product
from fractions import Fraction
from collections import Counter
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_HP3_180_quaternionic_projective_3design.json"

def main():
    _,source,_,_,_=R.load()
    cert=json.loads((ROOT/"data/toe_20261114_exact_gaussian_integer_USp8_pauli_Albert_intertwiner.json").read_text())
    signflip=set(cert["coordinate_negative_sign_indices"])
    mp={int(i):v for i,v in cert["coordinate_to_pauli_label"].items()}
    pauli,quad,nonquad,_=E.pauli_data()
    assert set(mp.values())==set(quad)
    P=[(-1 if i in signflip else 1)*pauli[mp[i]] for i in range(27)]
    charges=[]
    for (i,j,k),s in source.items():
        for a,b,c in product((-1,1),repeat=3):
            if a*b*c!=s:continue
            z=[0]*27;z[i]=a;z[j]=b;z[k]=c
            charges.append(tuple(z))
    assert len(charges)==180 and len(set(charges))==180
    # Direct exact moment tensors up to order 3 in native E6 27
    m1=[sum(z[i] for z in charges) for i in range(27)]
    m2={(i,j):sum(z[i]*z[j] for z in charges)
        for i in range(27) for j in range(27)}
    m3=Counter()
    for z in charges:
        supp=[(i,int(v)) for i,v in enumerate(z) if v]
        for i,a in supp:
            for j,b in supp:
                for k,c in supp:m3[i,j,k]+=a*b*c
    assert m1==[0]*27
    assert all(m2[i,j]==(20 if i==j else 0) for i in range(27) for j in range(27))
    expected={}
    for tri,s in source.items():
        for perm in permutations(tri):expected[perm]=4*s
    assert {k:v for k,v in m3.items() if v}==expected
    # Haar random CP7 pure-state expectation moment formula:
    # E[(psi†Apsi)(psi†Bpsi)(psi†Cpsi)]
    #  = [Tr(A)Tr(B)Tr(C)+Tr(AB)Tr(C)+...+
    #     Tr(ABC)+Tr(ACB)]/(d(d+1)(d+2)), d=8.
    # For distinct Pauli basis elements only the last two remain.
    # For repeated indices those traces are 0 (Pauli traceless).
    tested=0
    for i in range(27):
        for j in range(27):
            for k in range(27):
                trace_sum=int(round(((np.trace(P[i]@P[j]@P[k])+
                    np.trace(P[i]@P[k]@P[j]))/8).real))
                assert abs((np.trace(P[i]@P[j]@P[k])+
                    np.trace(P[i]@P[k]@P[j])).imag)<1e-10
                # two traces each ±8 or both zero; integer numerator
                assert trace_sum in (-2,0,2)
                haar=Fraction(trace_sum,90) # numerator=8*sum ± => /720
                fin=Fraction(m3.get((i,j,k),0),180)
                assert fin==haar,(i,j,k,fin,haar)
                tested+=1
    # Strong fourth-order counterexample, exact:
    # A=P_i has eigenvalues +1 (mult 4), -1 (mult4).
    # For random complex psi the plus weight p~Beta(4,4),
    # z_i=2p-1. Hence E z_i^4=3/[(8+1)(8+3)]=1/33.
    finite4=Fraction(sum(z[0]**4 for z in charges),180)
    haar4=Fraction(3,9*11)
    assert finite4==Fraction(1,9) and haar4==Fraction(1,33)
    assert finite4!=haar4
    # Independent arithmetic contraction for an exact third-moment
    # observable; reconstruct N from a finite HP3 Haar cubature.
    import random
    random.seed(20261114)
    for _ in range(30):
        x=[random.randrange(-3,4) for i in range(27)]
        Ns=sum(s*x[i]*x[j]*x[k] for (i,j,k),s in source.items())
        sum3=sum(sum(z[i]*x[i] for i in range(27))**3 for z in charges)
        assert sum3==24*Ns
    result=dict(status="PASS_EXACT_180_POINT_HP3_PROJECTIVE_3_DESIGN_NOT_4",
        basis="Native 27 signed E6 cubic mapped exactly to J-even 3-qubit Pauli observables",
        cardinality=180,HP3_base_real_dim=12,complex_total_CP7_real_dim=14,
        exact_first_moment="0",exact_second_moment="I_27/9",
        exact_third_moment="s_ijk/45 for every ordered tritangent triple; 0 otherwise",
        independently_compared_Haar_third_moment_entries=tested,
        Haar_formula="sum_{sigma in S3} product_cycle_traces / (8*9*10)",
        exact_cubature="(1/180) sum_z (z dot x)^3 = (2/15) N(x) for all x",
        projective_design_strength=3,not_4_design=True,
        fourth_counterexample={"finite_E_z0_4":"1/9","HP3_Haar_E_z0_4":"1/33",
                               "Haar_distribution":"2 Beta(4,4) - 1"},
        literature="Kueng & Gross 2015 show 1080 3qubit stabilizer states form complex projective 3-design; this script independently verifies the projected HP3 design in signed cubic native basis.",
        proof_scope="Full finite first/second/third tensors plus exact Haar trace formula; fourth disproval. Not a physical spacetime design or dynamics.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    return result
if __name__=="__main__":main()
