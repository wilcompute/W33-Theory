#!/usr/bin/env python3
"""Construct an explicit Cartan-weight bridge from cubic 27 to
the symplectic-traceless wedge^2 representation of USp(8).

The result is a *weight/character-level intertwiner*, not yet a global
36-generator Lie-algebra intertwiner; it supplies exact separate
integer characteristic polynomial controls.
"""
import json,sys,itertools
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261113_usp8_27_weight_character_bridge.json"

def weights(Ks,indices,hadamard):
    h=[Ks[i] for i in indices]
    multipliers=[1,10,100,1000]
    A=sum((w*H for w,H in zip(multipliers,h)),np.zeros((27,27),dtype=np.int64))
    eig,V=np.linalg.eig(A.astype(float))
    rows=[]
    for lam,v in zip(eig,V.T):
        if abs(lam)<1e-8:
            rows.append((0,0,0,0))
            continue
        assert abs(lam.real)<1e-7
        w=[]
        for H in h:
            x=np.vdot(v,H@v)/np.vdot(v,v)
            assert abs(x.real)<1e-7 and abs(x.imag-round(x.imag))<1e-7,(x,lam)
            w.append(round(x.imag))
        assert abs(sum(p*q for p,q in zip(multipliers,w))-lam.imag)<1e-6
        rows.append(tuple(w))
    original=Counter(rows)
    assert original[(0,0,0,0)]==3 and len(original)==25,original
    canonical=[]
    for w in rows:
        dots=[sum(x*y for x,y in zip(w,H)) for H in hadamard]
        assert all(x%2==0 for x in dots)
        canonical.append(tuple(x//2 for x in dots))
    return A,original,Counter(canonical)

def standard_wedge():
    h=[]
    for i in range(4):
        p=[0]*4;p[i]=1;h.append(tuple(p))
    for i in range(4):
        p=[0]*4;p[i]=-1;h.append(tuple(p))
    wedge=[tuple(v[j]+u[j] for j in range(4)) for v,u in itertools.combinations(h,2)]
    assert len(wedge)==28
    assert wedge.count((0,0,0,0))==4
    wedge.remove((0,0,0,0)) # quotient the invariant symplectic form
    assert len(wedge)==27
    return Counter(wedge)

def main():
    data=json.loads((ROOT/"data/toe_20261113_e6_c4_compact_translation_holography.json").read_text())
    compact=data["lie_type"]
    assert compact["root_system"]=="C4"
    long=[tuple(x) for x in compact["root_weight_vectors"] if sum(abs(t) for t in x)==4]
    had=[w for w in long if w[0]==1]
    assert len(had)==4
    cert,terms,D,mapi,roots=R.load()
    keys,Ks=R.pack_roots(roots)
    A,initial,canonical=weights(Ks,compact["Cartan_commuting_basis_indices"],had)
    expected=standard_wedge()
    assert canonical==expected,{"actual":canonical,"expected":expected}
    t=sp.Symbol("t")
    # The spectral frequencies are integers. Coefficientwise exact
    # characteristic polynomial of a real integer skew matrix.
    coeff=[1,10,100,1000]
    # Original frequency is dot(w, original coefficients), not dot on
    # canonically rotated coordinates; compute independently from
    # inverse Hadamard map: w_orig = H^T w_canon / 2.
    poly=t**3
    hz=Counter()
    for w,n in canonical.items():
        if w==(0,0,0,0):continue
        original_weight=tuple(sum(w[j]*had[j][k] for j in range(4))//2 for k in range(4))
        f=abs(sum(original_weight[k]*coeff[k] for k in range(4)))
        hz[f]+=n
    assert all(x%2==0 for x in hz.values()),hz
    for f,n in hz.items():
        poly*=(t*t+f*f)**(n//2)
    direct=sp.Matrix(A.tolist()).charpoly(t).as_expr()
    assert sp.expand(poly-direct)==0
    returnable={
       "status":"PASS_EXACT_C4_27_CHARACTER_EQUALS_USP8_SYMPLECTIC_TRACELESS_WEDGE2",
       "compact_Cartan_indices":compact["Cartan_commuting_basis_indices"],
       "Hadamard_root_basis_rotation":[list(x) for x in had],
       "original_weight_counts":{str(k):v for k,v in initial.items()},
       "canonical_27_weight_counts":{str(k):v for k,v in canonical.items()},
       "canonical_pattern":"24 weights {±e_i±e_j, i<j} and zero with multiplicity 3",
       "Lambda2_8_weights":28,
       "Lambda2_0_8_weights":27,
       "character_equal_to_USp8_omega2":True,
       "full_integer_charpoly_equal":True,
       "global_intertwiner_not_yet_constructed":True,
       "scope":"Identifies the 27D compact Cartan character with the irreducible ω2 representation Λ²_0 of USp(8), and verifies a generic exact characteristic polynomial. A simultaneous 36-generator 27x27 intertwiner and its normalization remain separate construction work."
    }
    OUT.write_text(json.dumps(returnable,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":returnable["status"],
          "weight_count":sum(canonical.values()),
          "nonzero_weight_count":sum(v for k,v in canonical.items() if any(k)),
          "zero_weight_multiplicity":canonical[(0,0,0,0)],
          "charpoly_equal":returnable["full_integer_charpoly_equal"]},indent=2),flush=True)
    return returnable

if __name__=="__main__":main()
