#!/usr/bin/env python3
"""Pass5609: old s12/Weyl-Heisenberg phase unlocks a rich Segre event spectrum.

Pass5607 proves that a fully projective-invariant untwisted operator on
P1(3)xP1(3) is spectrally too small. The old s12 program says the missing
algebraic ingredient is a Heisenberg 2-cocycle/phase. Use the exact W33
symplectic form B on Segre events and weight every rook-complement edge by
omega^B(s,t), omega^3=1. Alternation makes the matrix Hermitian.

The untwisted rook-complement adjacency has only 3 eigenvalues. The magnetic
matrix has an exact degree-16 integer characteristic polynomial with 15 distinct
real roots (only -2 is double), and 60 of 96 event triangles carry nonzero Z3
Wilson flux. Thus the phase is not a removable gauge and genuinely breaks the
flat spectral degeneracy.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5609_S12_HEISENBERG_PHASE_SEGRE_SPECTRUM.json'

def norm(v,q=3):
    v=tuple(x%q for x in v)
    for a in v:
      if a:
        z=pow(a,-1,q); return tuple(z*x%q for x in v)
    raise ValueError
def p1(): return [(1,t) for t in range(3)]+[(0,1)]
def segre(u,v): return norm((u[0]*v[0],u[1]*v[1],u[0]*v[1],-u[1]*v[0]))
def B(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    a,b=x;c,d=y
    return (a*c-b*d,a*d+b*c-b*d) # omega^2=-1-omega
def wpow(e): return ((1,0),(0,1),(-1,-1))[e%3]
def matmul(A,Bm):
    n=len(A); C=[[(0,0) for _ in range(n)] for __ in range(n)]
    for i in range(n):
      for k in range(n):
        aik=A[i][k]
        if aik==(0,0): continue
        for j in range(n):
          b=Bm[k][j]
          if b!=(0,0): C[i][j]=add(C[i][j],mul(aik,b))
    return C
def trace(A):
    s=(0,0)
    for i in range(len(A)): s=add(s,A[i][i])
    return s

def exact_charpoly(A):
    # Newton identities in Z[omega]. All traces/coefs collapse to Z here.
    n=len(A); cur=[row[:] for row in A]; traces=[]
    for _ in range(1,n+1):
      traces.append(trace(cur)); cur=matmul(cur,A)
    coeff=[(1,0)]
    for k in range(1,n+1):
      s=(0,0)
      for i in range(1,k+1): s=add(s,mul(coeff[k-i],traces[i-1]))
      assert s[0]%k==0 and s[1]%k==0
      coeff.append((-s[0]//k,-s[1]//k))
    assert all(b==0 for a,b in coeff)
    return [a for a,b in coeff],[a for a,b in traces]

def main():
    P=p1(); events=[segre(u,v) for u in P for v in P]; n=16
    A=[[(0,0) for _ in range(n)] for __ in range(n)]
    An=np.zeros((n,n),complex); U=np.zeros((n,n),int)
    omega=np.exp(2j*np.pi/3)
    for i in range(n):
      ri,ci=divmod(i,4)
      for j in range(n):
        rj,cj=divmod(j,4)
        if i!=j and ri!=rj and ci!=cj:
          e=B(events[i],events[j]); A[i][j]=wpow(e); An[i,j]=omega**e; U[i,j]=1
    assert np.allclose(An,An.conj().T)
    cp,traces=exact_charpoly(A)
    expected=[1,0,-72,-12,2028,627,-29112,-12660,230793,122822,-1017204,-587478,2380932,1278288,-2663712,-1003104,1041984]
    assert cp==expected
    eig=np.linalg.eigvalsh(An); uniq=len(np.unique(np.round(eig,8))); assert uniq==15
    ue=np.linalg.eigvalsh(U.astype(float)); uuniq=sorted((round(x,8),int(sum(abs(ue-x)<1e-7))) for x in np.unique(np.round(ue,8)))
    assert len(uuniq)==3

    flux=Counter(); triangles=0
    for i,j,k in itertools.combinations(range(n),3):
      if U[i,j] and U[j,k] and U[k,i]:
        triangles+=1; flux[(B(events[i],events[j])+B(events[j],events[k])+B(events[k],events[i]))%3]+=1
    assert triangles==96 and flux[0]==36 and flux[1]+flux[2]==60

    quotient=[1,-4,-60,244,1292,-5517,-12212,58256,46617,-296670,-16992,667170,-219780,-511272,260496]
    out={
      'pass':5609,'status':'EXACT_HEISENBERG_MAGNETIC_SPECTRAL_SPLITTING',
      'events':16,'rook_complement_degree':9,
      'untwisted_spectrum':'9^1 + 1^9 + (-3)^6',
      'magnetic_eigenvalues':[float(x) for x in eig],
      'magnetic_distinct_eigenvalues_numeric':uniq,
      'exact_characteristic_polynomial_coefficients_descending':cp,
      'exact_factorization':'(x+2)^2 * (x^14-4x^13-60x^12+244x^11+1292x^10-5517x^9-12212x^8+58256x^7+46617x^6-296670x^5-16992x^4+667170x^3-219780x^2-511272x+260496)',
      'exact_degree14_factor_coefficients_descending':quotient,
      'trace_moments_1_to_16':traces,
      'triangle_flux_counts_oriented_by_sorted_vertex_order':{str(k):v for k,v in sorted(flux.items())},
      'nonzero_flux_triangles':flux[1]+flux[2],
      'theorem':'The Z3 Heisenberg phase is not gauge-trivial on the Segre rook-complement event graph: 60/96 triangles have nonzero Wilson flux, and the 3-band untwisted spectrum splits to 15 distinct magnetic eigenvalues.',
      's12_bridge':'The phase exponent is the same type of symplectic 2-cocycle used by the old s12 -> 3-qutrit Weyl-Heisenberg closure. Pass5610 records an explicit chosen embedding of the W33 four-coordinate symplectic space into that F3^6 phase space.',
      'physics_firewall':'This is an exact finite magnetic/holonomy operator, not yet a Lorentzian continuum Hamiltonian or measured physical dispersion law.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
