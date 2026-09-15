#!/usr/bin/env python3
"""Support-level bridge: E8 order-3 root orbits vs two-qutrit Pauli grading of sl9.

This certificate deliberately stops at bracket SUPPORT.  It does not choose a
Chevalley cocycle/lift of the Weyl element, so it does not assert equality of
Lie structure constants.  It proves that root-addition among the 80 oriented
A2 orbits has exactly the same zero/nonzero and degree-addition law as the
standard F_3^4 tensor-Pauli grading of sl(9,C).
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_e8_a8_pauli_support_bridge.json'
import w33_e8_twisted_fibration_weld as base


def int_tuple(row):
    out=[]
    for x in list(row):
        x=sp.Rational(x); assert x.q==1; out.append(int(x))
    return tuple(out)


def main(write=True):
    roots=base.e8_roots(); rset=set(roots); ridx={r:i for i,r in enumerate(roots)}
    c=sp.eye(8)
    for r in base.SIMPLE_ROOTS: c=c*base.reflection(r)
    g=c**10
    B=sp.Matrix(base.SIMPLE_ROOTS); Binv=B.inv(); Gram=B*B.T/4
    G=B*g*Binv; M=sp.eye(8)-G; Minv=M.inv()
    Omega=G*Gram+2*(G**2)*Gram

    def act(i,A): return ridx[int_tuple(sp.Matrix([roots[i]])*A)]
    def coeff(r): return int_tuple(sp.Matrix([r])*Binv)
    def same_coset(a,b):
        row=sp.Matrix([[a[i]-b[i] for i in range(8)]])*Minv
        return all(sp.Rational(x).q==1 for x in row)
    def omega(a,b): return int((sp.Matrix([a])*Omega*sp.Matrix(b))[0])%3

    unseen=set(range(240)); orbits=[]
    while unseen:
        i=min(unseen); o=tuple(sorted({i,act(i,g),act(i,g**2)}))
        unseen.difference_update(o); orbits.append(o)
    assert len(orbits)==80
    reps=[coeff(roots[o[0]]) for o in orbits]
    orbit_of={i:k for k,o in enumerate(orbits) for i in o}

    def class_sum(a,b):
        s=tuple(a[i]+b[i] for i in range(8))
        if same_coset(s,(0,)*8): return None
        hits=[k for k,r in enumerate(reps) if same_coset(s,r)]
        assert len(hits)==1
        return hits[0]

    census=Counter(); target_ok=True
    for a,d in itertools.combinations(range(80),2):
        om=omega(reps[a],reps[d])
        hits=[]; targets=set()
        for i in orbits[a]:
            for j in orbits[d]:
                s=tuple(roots[i][k]+roots[j][k] for k in range(8))
                if s in rset:
                    h=ridx[s]; hits.append((i,j,h)); targets.add(orbit_of[h])
        census[(om,len(hits),len(targets))]+=1
        if om==0:
            assert len(hits)==0
        else:
            assert len(hits)==3 and len(targets)==1
            t=next(iter(targets))
            assert t==class_sum(reps[a],reps[d])
    assert census==Counter({(0,0,0):1000,(1,3,1):1080,(2,3,1):1080})

    V=[v for v in itertools.product(range(3),repeat=4) if any(v)]
    def symp(v,w): return (v[0]*w[1]-v[1]*w[0]+v[2]*w[3]-v[3]*w[2])%3
    pc=Counter(symp(v,w) for v,w in itertools.combinations(V,2))
    assert pc==Counter({0:1000,1:1080,2:1080})

    checks={
      '80_oriented_root_orbits':len(orbits)==80,
      'root_support_census_omega0_1000':census[(0,0,0)]==1000,
      'root_support_census_omega1_1080':census[(1,3,1)]==1080,
      'root_support_census_omega2_1080':census[(2,3,1)]==1080,
      'orthogonal_labels_have_no_root_sum':all(k[1]==0 for k in census if k[0]==0),
      'nonorthogonal_labels_have_three_root_sums_one_target':all(k[1:]==(3,1) for k in census if k[0]!=0),
      'root_sum_target_is_quotient_label_sum':target_ok,
      'two_qutrit_pauli_pair_census_matches':pc==Counter({0:1000,1:1080,2:1080}),
    }
    assert all(checks.values())
    result={
      'schema':'w33.e8_a8_pauli_support_bridge.v1',
      'status':'PASS',
      'headline':'The 80 E8 order-3 oriented-A2 orbit labels have exactly the bracket-support law of the F_3^4 tensor-Pauli grading of sl(9): Omega=0 iff no root sum, while Omega!=0 gives exactly three root sums in the unique degree v+w.',
      'root_orbit_pair_census':{
        'Omega_0_no_root_sum':1000,
        'Omega_1_three_root_sums_one_target':1080,
        'Omega_2_three_root_sums_one_target':1080,
        'total_unordered_pairs':3160,
      },
      'pauli_pair_census':{'commuting':1000,'phase_1':1080,'phase_2':1080},
      'grading_law':'[degree v, degree w] has support 0 iff Omega(v,w)=0; otherwise support lies in the unique degree v+w.',
      'literature_boundary':{
        'A8_fixed_algebra':'Classical order-3 E8 grading has fixed algebra sl(9).',
        'tensor_pauli_grading':'Pelantova-Svobodova-Tremblay, quant-ph/0510106: fine grading of sl(p^2,C) by tensor generalized Pauli matrices; normalizer quotient Sp(4,F_p) x Z2.',
        'new_corpus_piece':'Exact identification of the E8 root-orbit addition support with the same F_3^4 symplectic Pauli support law.',
      },
      'check_count':len(checks),'checks':checks,
      'scope':'Support-level Lie-grading bridge only. A Chevalley cocycle/lift is still required before claiming equality of structure constants or a canonical Lie-algebra isomorphism.',
    }
    if write: OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2)); return result

if __name__=='__main__': main(True)
