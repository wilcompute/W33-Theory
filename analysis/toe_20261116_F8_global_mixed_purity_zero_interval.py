#!/usr/bin/env python3
"""Exact global MIXED-state zero-certainty interval for the nine F8
regulus MUBs, plus two explicit preparation upper-bound families.

C(rho)=sum_{567 covered nonidentity Paulis} Tr(rho P)^2 >=0.
An uncovered 5-dimensional commuting Pauli subspace gives a rank-two
projector rho_code whose covered moments are ALL zero. Mixing it with
I/64 realizes every purity in [1/64,1/2] at C=0, so the global
minimum C_min(purity)=0 THROUGHOUT THAT ENTIRE INTERVAL.
No statement of optimality is made for purity >1/2.
"""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"toe_20261115_F8_mixed_uncovered_stabilizer.json"
OUT=ROOT/"data"/"toe_20261116_F8_exact_mixed_purity_zero_interval.json"

def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if (a>>3)&1:a^=0b1011
    return r
def trace(a):
    s=0;y=a
    for _ in range(3):
        s^=y;y=mul(y,y)
    assert s in (0,1)
    return s
def q(w):
    x1=w&7;x2=(w>>3)&7;z1=(w>>6)&7;z2=(w>>9)&7
    return mul(x1,z1)^mul(x2,z2)
def comm(w,v):
    x1=w&7;x2=(w>>3)&7;z1=(w>>6)&7;z2=(w>>9)&7
    y1=v&7;y2=(v>>3)&7;t1=(v>>6)&7;t2=(v>>9)&7
    return trace(mul(x1,t1)^mul(x2,t2)^mul(y1,z1)^mul(y2,z2))==0

def run():
    prev=json.loads(SOURCE.read_text())
    basis=[int(x) for x in prev["basis"]]
    assert len(basis)==5 and all(0<w<4096 for w in basis)
    span={0}
    for b in basis:span|={w^b for w in list(span)}
    assert len(span)==32
    assert all(q(w)!=0 for w in span if w)
    assert all(comm(x,y) for x in basis for y in basis)
    assert sum(q(w)==0 for w in range(1,4096))==567
    central=[w for w in range(4096) if all(comm(w,b) for b in basis)]
    assert len(central)==128
    todo=set(central)
    logical=[]
    while todo:
        rep=min(todo)
        coset={rep^s for s in span}
        assert coset<=todo
        todo-=coset
        if rep not in span:logical.append((rep,sum(q(w)==0 for w in coset)))
    assert len(logical)==3
    assert sorted(v for w,v in logical)==[3,3,3]
    # Group orthogonality of Pauli operators: Tr(P_g P_h)=64 δgh.
    # The code projector = (1/32) sum_g P_g (up to generator sign),
    # normalized rho0=Pi/2=(1/64) sum_g P_g.
    # Covered labels do not occur in this span; moments vanish exactly.
    sample=[]
    for t in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
        purity=F(1+31*t*t,64)
        sample.append({
          "codeweight_t":str(t),
          "state":"rho_t=(1-t) I_64/64 + t Pi_rank2/2",
          "Tr_rho_squared":str(purity),
          "covered_certainty_exact":0})
    assert sample[0]["Tr_rho_squared"]=="1/64"
    assert sample[-1]["Tr_rho_squared"]=="1/2"
    # Beyond p=1/2 an encoded logical Bloch state has
    # purity (1+r²)/2, certainty 3r²=6p-3.
    # An independently known exact pure torus witness admits standard
    # depolarization C=(64p-1) c8 /63, p in [1/64,1].
    c8=(47-32*math.cos(2*math.pi/9))/9
    crossing=(189-c8)/(378-64*c8)
    assert .85<crossing<.86
    for p in [F(1,2),F(3,4),F(9,10),F(1)]:
        logical_C=6*p-3
        torus_C=(64*float(p)-1)*c8/63
        assert logical_C>=0 and torus_C>=0
    result={
      "status":"EXACT_F8_GLOBAL_MIXED_STATE_ZERO_CERTAINTY_FOR_PURITY_LE_HALF",
      "source_stabilizer_basis_integer_labels":basis,
      "uncovered_subgroup_nonidentity_count":31,
      "symplectically_isotropic_rank":5,
      "stabilizer_code_projector_rank":2,
      "covered_Pauli_observables":567,
      "centralizer_size":128,
      "logical_coset_covered_counts":[x[1] for x in logical],
      "global_mixed_state_exact_min_zero_purity_interval":["1/64","1/2"],
      "exact_zero_state_family":"rho_t=(1-t)I_64/64 + t Pi_rank2/2, 0<=t<=1; purity=(1+31t²)/64; C=0",
      "global_lower_bound_C_nonnegative":True,
      "exact_sample_families":sample,
      "rank2_code_purity_upper_preparation":"For 1/2<=p<=1, exists pure-encoded-qubit Bloch mixture with C=6p-3",
      "depolarized_torus_witness_upper_preparation":"For 1/64<=p<=1, C<=c8*(64p-1)/63, c8=(47-32cos(2pi/9))/9",
      "two_explicit_upper_family_numeric_cross_purity":crossing,
      "two_explicit_upper_family_cross_certainty":6*crossing-3,
      "scope":"C_min(p)=0 is proven for 1/64<=p<=1/2 because the functional is nonnegative and an explicit rank-two-code mixture attains zero. No claim of maximal attainable zero-certainty purity or global minimum for p>1/2; known c8 is an exact pure-state UPPER witness, not a proven global lower bound."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result

if __name__=="__main__":
    r=run()
    print("PASS",r["status"],"interval",r["global_mixed_state_exact_min_zero_purity_interval"],flush=True)
