#!/usr/bin/env python3
"""Constructive pure-state control with compact USp8, not SU8.

Every unit vector in C8 is the first column of a symplectic unitary
built by explicit quaternionic Gram-Schmidt, with an exact formula.
The 36 repo Pauli usp8 generators span the full 15D tangent to the
unit sphere at |000>. Numerical compilation to 45 continuously
tunable Pauli rotations supplies an independent finite-depth demo.
One fixed irrational-angle gate plus Clifford conjugates gives a
DENSE rather than finite exact approximation of these rotations.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_USp8_constructive_pure_state_compiler.json"

def main():
    pauli,quad,nonquad,terms=E.pauli_data()
    J=pauli[9];I=np.eye(8,dtype=complex)
    def quat_gram_schmidt(target):
        target=target/np.linalg.norm(target)
        bases=[target]
        eye=np.eye(8,dtype=complex)
        for k in range(1,4):
            remainders=[]
            for seed in eye.T:
                r=seed.copy()
                for v in bases:
                    w=J@v.conj()
                    r-=v*np.vdot(v,r)+w*np.vdot(w,r)
                remainders.append(r)
            r=max(remainders,key=np.linalg.norm)
            assert np.linalg.norm(r)>1e-6
            bases.append(r/np.linalg.norm(r))
        U=np.zeros((8,8),complex)
        for k,v in enumerate(bases):
            U[:,k]=v
            U[:,k+4]=-1j*(J@v.conj())
        return U
    rng=np.random.default_rng(20261114)
    symplectic_residual=0
    for n in range(60):
        target=rng.normal(size=8)+1j*rng.normal(size=8)
        target/=np.linalg.norm(target)
        U=quat_gram_schmidt(target)
        symplectic_residual=max(symplectic_residual,float(np.max(abs(U.T@J@U-J))))
        assert symplectic_residual<1e-12
        assert np.max(abs(U.conj().T@U-I))<1e-12
        assert np.max(abs(U[:,0]-target))<1e-12
        assert abs(np.linalg.det(U)-1)<1e-12
    e0=I[:,0]
    vs=[1j*pauli[a]@e0 for a in nonquad]
    M=np.stack([np.concatenate((v.real,v.imag)) for v in vs],axis=1)
    rank=int(np.linalg.matrix_rank(M,tol=1e-10))
    assert rank==15
    # Greedy independent tangent directions, deterministic.
    ids=[];columns=[]
    for j,a in enumerate(nonquad):
        trial=M[:,[nonquad.index(z) for z in ids]+[j]]
        if np.linalg.matrix_rank(trial,tol=1e-10)>len(ids):
            ids.append(a)
    assert len(ids)==15
    labels=ids*3;P=[pauli[a] for a in labels];N=len(labels)
    def compile(target):
        def both(theta):
            state=e0.copy();states=[]
            for ang,p in zip(theta,P):
                state=np.cos(ang)*state+1j*np.sin(ang)*(p@state)
                states.append(state)
            overlap=np.vdot(target,state)
            cost=1-abs(overlap)**2
            grad=np.empty(N)
            bra=target.conj().copy()
            for j in range(N-1,-1,-1):
                dz=bra@(1j*P[j]@states[j])
                grad[j]=-2*np.real(np.conj(overlap)*dz)
                ang=theta[j]
                bra=np.cos(ang)*bra+1j*np.sin(ang)*(bra@P[j])
            return float(cost),grad
        trials=[]
        for seed in range(3):
            initial=rng.normal(0,.25,size=N) if seed else np.zeros(N)
            res=minimize(both,initial,jac=True,method="L-BFGS-B",
                options={"maxiter":1000,"ftol":5e-14,"gtol":1e-9})
            trials.append((res.fun,res.x,res.nit))
            if res.fun<1e-9:break
        val,ang,it=min(trials,key=lambda x:x[0])
        return val,ang,int(it)
    fidelities=[];iters=[];angles=[]
    for j in range(5):
        target=rng.normal(size=8)+1j*rng.normal(size=8)
        target/=np.linalg.norm(target)
        err,theta,it=compile(target)
        assert err<1e-7,(j,err,it)
        fidelities.append(1-err);iters.append(it);angles.append(theta.tolist())
    out=dict(status="PASS_CONSTRUCTIVE_USP8_TRANSITIVE_PURE_STATE_PREPARATION",
       pure_state_dimension="CP7 real dimension14; normalized S15 real dimension15",
       usp8_dimension=36,symplectic_householder_like_qr_samples=60,
       quaternionic_GramSchmidt_residual_max=symplectic_residual,
       generator_tangent_rank_at_e0=rank,
       minimal_independent_tangent_axes=ids,
       compiled_gate_count_per_target=N,
       continuous_angle_compiled_random_targets=5,
       random_target_state_fidelities=fidelities,
       minimum_fidelity=min(fidelities),
       L_BFGS_iterations=iters,
       continuous_angle_vectors=angles,
       group_dynamics="Sp4 acts transitively on S15, stabilizer Sp3; 36 continuous iP_a generate its Lie algebra",
       discrete_gate_firewall="One irrational fixed rotation plus Clifford W(E6) is dense USp8, so these gates can approximate arbitrary pure states with no uniform finite exact compilation bound. Not full SU8 unitary controllability.",
       physical_scope="Mathematical unitary eight-level/3qubit control; no optical noise or hardware fidelity claimed.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","quaternionic_GramSchmidt_residual_max","generator_tangent_rank_at_e0","compiled_gate_count_per_target","continuous_angle_compiled_random_targets","minimum_fidelity","L_BFGS_iterations"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
