#!/usr/bin/env python3
"""Generalized Pascal beta-base discriminants and selection-bias controls.

For m>=2, f_m(X)=X^m-X^(m-1)-1 has discriminant:
(-1)^(m(m-1)/2+m+1) * (m^m+(m-1)^(m-1)).
The primes dividing this *polynomial* discriminant are precisely where
f_m has repeated roots mod p. For nonmaximal Z[beta] orders, this does
not by itself determine ramification in the maximal number field order.

m=5 factors 3381=3*7^2*23, coinciding with three sampled Levi primes.
Prime43 is another Levi-family prime not dividing 3381: this apparent
coincidence is NOT a global correspondence or evidence for classical RH.
"""
from __future__ import annotations
import json
from pathlib import Path
from sympy import symbols, discriminant, factorint, Poly

def certificate():
    x=symbols("x");cases=[]
    for m in range(2,11):
        expected=(-1)**(m*(m-1)//2+m+1)*(m**m+(m-1)**(m-1))
        obtained=int(discriminant(x**m-x**(m-1)-1,x))
        assert obtained==expected
        factors={str(k):int(v) for k,v in factorint(abs(expected)).items()}
        # discriminant primes must make polynomial not square-free mod p
        f=Poly(x**m-x**(m-1)-1,x)
        for prime in factors:
            p=int(prime)
            fmod=Poly(f.as_expr(),x,modulus=p)
            assert fmod.gcd(fmod.diff()).degree()>0
        cases.append({"m":m,"discriminant":expected,"prime_factorization":factors})
    assert cases[0]["discriminant"]==5
    assert cases[1]["discriminant"]==-31
    assert cases[2]["discriminant"]==-283
    assert cases[3]["discriminant"]==3381
    assert cases[3]["prime_factorization"]=={"3":1,"7":2,"23":1}
    assert 43%20==3 and 3381%43!=0
    return {"status":"PASS_EXACT_SYMBOLIC","classical_RH_proved":False,
        "m_range":[2,10],"formula":"Disc(f_m)=(-1)^[m(m-1)/2+m+1]*(m^m+(m-1)^(m-1))",
        "proof":"f'(x)=x^(m-2)(m x-(m-1)); use resultant Res(f,f')=f(0)^(m-2)*m^m*f((m-1)/m), then standard discriminant sign.",
        "candidate_exceptional_characteristics":cases,
        "m5_sample_overlap":{"discriminant":3381,"divisors":[3,7,23],
            "Levi_family_nondivisor_control":43,
            "warning":"Three selected sample primes are divisors, but infinitely many other Levi primes are not; overlap is not an Euler-factor or motive identity."},
        "number_field_boundary":"Polynomial discriminant zero mod p gives repeated-root reduction of this order; field discriminant/actual ramification may require index-of-Z[beta] analysis."}

if __name__=="__main__":
    d=certificate()
    p=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_pascal_beta_discriminants.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print([(a["m"],a["discriminant"]) for a in d["candidate_exceptional_characteristics"]])
