#!/usr/bin/env python3
"""All 2^t theorem for the *C module* under one projective transvection.

For p=2, C_q is the Frobenius-twisted tensor product of t natural four
dimensional modules. One transvection acts on each factor J2+2*J1.
Over F2[C2], J2 tensor W is projective with dim(W) copies J2/2.
Only all-J1 choices survive as J1, giving C|<T> = J1^q + J2^{q(q-1)/2}.
This does NOT prove any general law for the nonsplit/split K extension.
"""
import json,sys
from pathlib import Path

def tensor_jordan_u2(left,right):
    # indecomposable J1 has dimension1; J2 is free rank1.
    a,b=left["J1"],left["J2"]
    c,d=right["J1"],right["J2"]
    return {"J1":a*c,
            "J2":a*d+b*c+2*b*d}

def run():
    state={"J1":1,"J2":0}
    cases=[]
    for t in range(1,11):
        state=tensor_jordan_u2(state,{"J1":2,"J2":1})
        q=2**t
        assert state=={"J1":q,"J2":q*(q-1)//2}
        cases.append({"q":q,"t":t,"Cdim":q*q,"J1":state["J1"],"J2":state["J2"],
                      "rank_D_on_C":state["J2"]})
    return {"status":"ALL_CHARACTERISTIC_TWO_TRANSVECTION_C_JORDAN_THEOREM",
      "theorem":"For q=2^t, C_q=row(B) as a C2-module is J1^q plus J2^[q(q-1)/2].",
      "representation_input":"C_q tensor decomposition ⊗_{i=0}^{t-1} (natural 4D module)^(2^i), from Lucas surviving monomials of degree q-1.",
      "factor_structure":"Natural 4D module restricted to a transvection has J1^2 + J2^1; Frobenius twisting preserves that structure in characteristic two.",
      "tensor_rule":"J1⊗J1=J1, J2⊗J1=J2, J2⊗J2=2J2; hence only choosing 2 trivial lines from every digit contributes J1, namely 2^t=q.",
      "derived_rank_formula":"rank(T-I on C_q)=q(q-1)/2 for all t>=1",
      "sample_q":cases,
      "extension_boundary":"No all-t result for K or connecting delta1 inferred. Verified delta1=0 only q=4,8,16; GF9 delta1=4.",
      "priority":"The p-rank/C tensor theorem and all-prime Jordan ingredients are classical/appear elsewhere in W33 repository; the specific char2 corollary is algebraic bookkeeping, not a claimed fundamentally new field theorem."}

if __name__=="__main__":
 output=json.dumps(run(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(output,encoding="utf8")
 else:print(output)
