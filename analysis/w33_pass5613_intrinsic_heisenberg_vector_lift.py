#!/usr/bin/env python3
"""Pass5613: correct the projective-section phase and construct the intrinsic q=3 lift.

Pass5609 is exact for its chosen normalized projective representatives, but the
edge phase omega^B(s,t) is not invariant under rescaling representatives.  This
file demonstrates the dependence and replaces the projective-point operator by
the natural vector/Heisenberg lift.

For q=3 every projective point has exactly two nonzero vector lifts +/-v.  There
cannot be an Sp(4,3)-equivariant section: central -I fixes every projective point
but swaps the two nonzero lifts.  On the 32 lifted Segre events we use the
alternating Heisenberg cocycle psi(v,w)=B(v,w)/2=2B(v,w) mod 3.  It is intrinsic
to vectors and is compatible with the old s12/Weil phase mechanism.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5613_INTRINSIC_HEISENBERG_VECTOR_LIFT.json'

def norm(v,q=3):
    v=tuple(x%q for x in v)
    for a in v:
        if a:
            z=pow(a,-1,q);return tuple(z*x%q for x in v)
    raise ValueError

def p1(): return [(1,t) for t in range(3)]+[(0,1)]
def segre(u,v): return norm((u[0]*v[0],u[1]*v[1],u[0]*v[1],-u[1]*v[0]))
def B(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3

def projective_matrix(reps):
    n=16;w=np.exp(2j*np.pi/3);A=np.zeros((n,n),complex)
    for i in range(n):
        ri,ci=divmod(i,4)
        for j in range(i+1,n):
            rj,cj=divmod(j,4)
            if ri!=rj and ci!=cj:
                z=w**B(reps[i],reps[j]);A[i,j]=z;A[j,i]=np.conj(z)
    return A

def tr_power(A,k): return float(np.trace(np.linalg.matrix_power(A,k)).real)

def lifted_matrix(reps):
    vecs=[];base=[]
    for i,v in enumerate(reps):
        for a in (1,2): vecs.append(tuple(a*x%3 for x in v));base.append(i)
    w=np.exp(2j*np.pi/3);N=32;A=np.zeros((N,N),complex)
    for i in range(N):
        ri,ci=divmod(base[i],4)
        for j in range(i+1,N):
            rj,cj=divmod(base[j],4)
            if ri!=rj and ci!=cj:
                e=(2*B(vecs[i],vecs[j]))%3
                z=w**e;A[i,j]=z;A[j,i]=np.conj(z)
    return A

def main():
    P=p1();reps=[segre(u,v) for u in P for v in P]
    A0=projective_matrix(reps)
    reps2=list(reps);reps2[0]=tuple(2*x%3 for x in reps2[0])
    A1=projective_matrix(reps2)
    moments0=[round(tr_power(A0,k)) for k in range(2,7)]
    moments1=[round(tr_power(A1,k)) for k in range(2,7)]
    assert moments0[:2]==moments1[:2] and moments0[2:]!=moments1[2:]
    assert moments0[2]==2256 and moments1[2]==2400

    L=lifted_matrix(reps)
    ev=np.linalg.eigvalsh(L);cnt=Counter(float(x) for x in np.round(ev,8))
    expected={-6.0:6,-3.0:7,-1.0:3,2.0:6,3.0:5,6.0:4,9.0:1}
    assert dict(sorted(cnt.items()))==dict(sorted(expected.items()))
    moments=[round(tr_power(L,k)) for k in range(1,9)]
    assert moments==[0,576,288,20592,43200,1007136,4219488,59923152]

    out={
      'pass':5613,'status':'CORRECTION_PLUS_INTRINSIC_Q3_VECTOR_HEISENBERG_LIFT',
      'pass5609_correction':{
        'statement':'the 16-point normalized-section magnetic operator is exact for that section but is not projectively intrinsic',
        'base_trace_moments_k2_to_k6':moments0,
        'one_representative_sign_flip_moments_k2_to_k6':moments1,
        'first_changed_moment':'tr(A^4): 2256 -> 2400'
      },
      'no_equivariant_section_proof':'central -I in Sp(4,3) fixes every projective point but sends every nonzero lift v to -v, so an Sp(4,3)-equivariant choice of one lift per point is impossible',
      'q3_scalar_fiber':{'projective_scalar_fiber_size':'q-1','at_q3':2,'unique_odd_q_double_cover':'q-1=2 iff q=3'},
      'intrinsic_lift':{
        'events':32,'description':'all +/- vector lifts of the 16 Segre projective events',
        'phase':'omega^(B(v,w)/2)=omega^(2B(v,w))',
        'spectrum':{str(k):v for k,v in sorted(expected.items())},
        'trace_moments_k1_to_k8':moments
      },
      'old_repo_bridge':'scripts/grade_weil_phase.py separates section-dependent Heisenberg cocycles from the invariant alternating cocycle and supplies the Weil 1-cochain correction; tools/toe_heisenberg_connection_model.py independently identifies the E6/firewall Z3 curvature with the same Heisenberg commutator form',
      'physics_reading':'phase/holonomy naturally lives on a vector/frame line bundle above projective events. At q=3 that bundle is literally a two-sheeted sign cover, making a spin-like interpretation structurally available but not yet a derivation of physical spinors.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
