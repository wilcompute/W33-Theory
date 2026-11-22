#!/usr/bin/env python3
"""Exact 24-order causal C4 stochastic quantization and reversible time-arrow obstruction.

Quantum Hamiltonian is the symmetric similarity transform of the prior
reversible Metropolis chain, NOT the gravitational Hamiltonian constraint.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
import toe_20261122_next5_causal_dynamics as C

OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_further_quantum_causal_arrow.json'

EDGE={(0,1),(0,2),(1,3),(2,3)}
ORDERS=list(itertools.permutations(range(4)))
INDEX={o:i for i,o in enumerate(ORDERS)}

def model(theta=C.THETA):
    energies=np.array([C.energy(C.causal_stats(o,EDGE),theta) for o in ORDERS])
    weights=np.exp(-energies-np.max(-energies));weights/=sum(weights)
    P=np.zeros((24,24))
    for i,o in enumerate(ORDERS):
        for k in range(3):
            q=list(o);q[k],q[k+1]=q[k+1],q[k]
            j=INDEX[tuple(q)]
            a=min(1.,math.exp(energies[i]-energies[j]))/3
            P[i,j]+=a
            P[i,i]-=a
        P[i,i]+=1
    assert np.max(abs(P.sum(axis=1)-1))<1e-14
    assert np.max(abs(weights[:,None]*P-weights[None,:]*P.T))<1e-14
    S=np.sqrt(weights[:,None]/weights[None,:])*P
    assert np.max(abs(S-S.T))<1e-14
    H=np.eye(24)-S
    eig=np.linalg.eigvalsh(H)
    assert abs(eig[0])<1e-13 and eig[1]>0
    gs=np.sqrt(weights)
    assert np.linalg.norm(H@gs)<1e-13
    return H,eig,weights,P

def permutation_rep(phi):
    Q=np.zeros((24,24),dtype=np.int64)
    for k,o in enumerate(ORDERS):
        to=phi(o)
        Q[INDEX[to],k]=1
    assert np.array_equal(Q.T@Q,np.eye(24))
    return Q

def graph_automorphisms():
    good=[]
    for p in itertools.permutations(range(4)):
        if {tuple(sorted((p[a],p[b]))) for a,b in EDGE}==EDGE:
            good.append(p)
    assert len(good)==8
    return good

def verify():
    H,eig,weights,P=model()
    H0,eig0,weights0,P0=model(theta=(0,0,0))
    assert np.allclose(weights0,1/24)
    assert eig0[1]>0
    R=permutation_rep(lambda o:o[::-1])
    assert np.max(abs(H@R-R@H))<1e-13
    assert np.max(abs(R@np.sqrt(weights)-np.sqrt(weights)))<1e-13
    for p in graph_automorphisms():
        U=permutation_rep(lambda o:tuple(p[x] for x in o))
        assert np.max(abs(H@U-U@H))<1e-13
    # A fabricated time-odd local orientation charge has zero GS expectation.
    sign=np.array([1 if o.index(0)<o.index(3) else -1 for o in ORDERS],dtype=np.int64)
    assert np.array_equal(R@(sign*np.sqrt(weights)),-sign*np.sqrt(weights))
    expect=float(np.sum(weights*sign))
    assert abs(expect)<1e-13
    return dict(status='PASS_QUANTUM_CAUSAL_C4_HAMILTONIAN_AND_ARROW_NO_GO',date='2026-11-22',
         state_count=24,undirected_C4_edge_count=4,graph_automorphism_group_order=8,
         exact_detailed_balance=True,real_symmetric_quantum_H=True,
         construction='S=diag(sqrt(pi)) P diag(1/sqrt(pi)), H=I-S, pi~exp(-S_causal)',
         quantum_ground_state='sqrt(pi), unique, reversal-even',
         spectral_gap=float(eig[1]),flat_action_spectral_gap=float(eig0[1]),
         gap_positive=True,reversal_commutator_norm=float(np.linalg.norm(H@R-R@H)),
         reversal_odd_order_parameter_expectation=expect,
         theorem='A finite irreducible reversible causal-order Metropolis chain induces a stoquastic Hermitian H with unique strictly positive sqrt(pi) ground state. If its interval action is time-reversal symmetric, the ground state is time-reversal-even. There is no preferred history arrow in this finite stationary ground state.',
         boundary='Quantization-by-similarity is an illustrative quantum walk, not Lorentzian gravitational Hamiltonian dynamics or a measured spin-2 propagator. Thermodynamic limits, boundary conditions or explicit time-odd terms can evade the no-arrow conclusion.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(d,indent=2)+'\n');print(d['status'], 'gap',d['spectral_gap'])
if __name__=='__main__':main()
