#!/usr/bin/env python3
"""Trinification E6 cubic on the exact sparse Witting/H27 address interface.

Exact mod-p H27 covariance and a 54-dimensional radical of the cubic
pulled back along the existing 27x81 coisometry. This is not a physical
E6-representation lift of the 81 address coordinates.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import toe_20261122_next5_h27_exact_matrix as W
import toe_20261122_witting_minimal_lie_control as L

OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_further_e6_cubic_pullback.json'
PRIMES=(7,13,19,31,37,43)

def action_chart():
    """Canonical 9x3 Schr basis to raw (A,B,C) 3x3 matrix entries."""
    raw=[]
    for block in range(3):
        def xp(p):
            i,j=p
            if block==0:return (i+1)%3,(j+1)%3
            if block==1:return (i+1)%3,j
            return i,(j+1)%3
        def q(p):
            i,j=p
            return ((2*i-j) if block==0 else (i if block==1 else j))%3
        unseen={(i,j) for i in range(3) for j in range(3)}
        seeds=[]
        while unseen:
            s=min(t for t in unseen if q(t)==0)
            orb=[s,xp(s),xp(xp(s))]
            assert [q(t) for t in orb]==[0,1,2]
            unseen-=set(orb)
            seeds.append(orb)
        assert len(seeds)==3
        raw.extend([9*block+3*i+j for orb in seeds for i,j in orb])
    assert len(raw)==len(set(raw))==27
    return raw

def cubic_raw(v,p):
    A,B,C=[np.asarray(v[9*i:9*(i+1)],dtype=np.int64).reshape(3,3)%p for i in range(3)]
    def det(M):
        a,b,c=M
        return int((a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%p)
    return int((det(A)+det(B)+det(C)-np.trace(A@B@C))%p)

def canonical_to_raw(v,chart):
    x=np.zeros(27,dtype=np.int64)
    x[chart]=v
    return x

def source_perm(g,orbit):
    index={int(v):i for i,v in enumerate(orbit)}
    P=np.zeros((27,27),dtype=np.int64)
    for j,v in enumerate(orbit):P[index[int(g(v))],j]=1
    return P

def verify():
    chart=action_chart()
    expo,_,_,orbit,x,y,z=W.exact_exponent_matrix()
    fibers=[]
    for p in PRIMES:
        T9,T9d,w=W.evaluate_mod(expo,p)
        T=np.kron(np.eye(3,dtype=np.int64),T9)%p
        Tdag=np.kron(np.eye(3,dtype=np.int64),T9d)%p
        assert np.array_equal(T@Tdag%p,np.eye(27,dtype=np.int64))
        Z=np.diag([pow(w,q,p) for _ in range(9) for q in range(3)]).astype(np.int64)
        X=np.kron(np.eye(9,dtype=np.int64),np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=np.int64))
        Px=np.kron(np.eye(3,dtype=np.int64),source_perm(x,orbit))
        Py=np.kron(np.eye(3,dtype=np.int64),source_perm(y**-1,orbit))
        assert np.array_equal(T@Px%p,Z@T%p)
        assert np.array_equal(T@Py%p,X@T%p)
        rng=np.random.default_rng(246810+p)
        for j in range(40):
            source=rng.integers(0,p,size=81,dtype=np.int64)
            u=T@source%p
            f=cubic_raw(canonical_to_raw(u,chart),p)
            fclock=cubic_raw(canonical_to_raw(Z@u%p,chart),p)
            fshift=cubic_raw(canonical_to_raw(X@u%p,chart),p)
            assert f==fclock==fshift,(p,j)
            # Surjectivity gives an explicit source lift of each target.
            assert np.array_equal(T@(Tdag@u%p)%p,u)
            assert cubic_raw(canonical_to_raw(T@(Tdag@u%p)%p,chart),p)==f
        # The pulled-back cubic has zero first derivative along ker(T).
        source=rng.integers(0,p,size=81,dtype=np.int64)
        P=Tdag@T%p
        null=(np.eye(81,dtype=np.int64)-P)@source%p
        assert np.all(T@null%p==0)
        base=rng.integers(0,p,size=81,dtype=np.int64)
        for t in range(3):
            assert cubic_raw(canonical_to_raw(T@(base+t*null)%p,chart),p)==cubic_raw(canonical_to_raw(T@base%p,chart),p)
        # Witness: A=I_3, B=C=0 => determinant A=1.
        target=np.zeros(27,dtype=np.int64)
        for i in range(3):target[chart.index(3*i+i)]=1
        assert cubic_raw(canonical_to_raw(target,chart),p)==1
        lifted=Tdag@target%p
        assert np.array_equal(T@lifted%p,target)
        fibers.append(dict(prime=p,omega=w,samples_checked=40,
                           source_rank=27,source_kernel_dimension=54,
                           H27_cubic_covariant=True,nonzero_determinant_witness=1))
    return dict(status='PASS_EXACT_WITTING_E6_TRINIFICATION_CUBIC_PULLBACK_WITH_RADICAL54',
      date='2026-11-22',H27_input_dimension=81,output_E6_trinification_dimension=27,
      sparse_matrix_nonzeros=243,output_chart_canonical_to_raw=chart,
      cubic='det(A)+det(B)+det(C)-tr(A*B*C) for A,B,C in Mat3',
      X_internal_SU3_triple='(X,X,I); X standard cyclic shift',
      Z_internal_SU3_triple='(Z^2,Z,I); Z standard qutrit clock',
      center='commutator acts by omega on all 27 target coordinates',
      exact_modular_cubic_checks=fibers,
      cubic_radical_dimension=54,
      cubic_radical_proof='The target cubic has zero linear polar radical: choose two matrix-unit partners completing a determinant to isolate each target coordinate. For C(Tu), its polar radical is exactly ker T, dim 81-rank27=54.',
      theorem='The 27x81 Witting coisometry transports a nonzero, H27-invariant E6-trinification cubic to the formal 81D address module. The transported cubic is necessarily degenerate along a 54-dimensional kernel.',
      limitation='Does not construct a faithful E6 action on the 81 formal address modes, a nondegenerate E6 cubic on 81D, a physical photon interface, or a gauge-invariant vacuum. E6 cubic formula is standard; construction is a Witting-basis transport and radical certificate.')

def main():
    out=verify();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
