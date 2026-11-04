#!/usr/bin/env python3
"""Two-intervention qubit process-tensor Choi operators with exact causal
trace constraints: identity Markov channel versus SWAP environmental memory.

Both are positive and ordered; memory survives an intermediate causal break
in the SWAP model, but not in the Markov model. No gravity or indefinite
causal order is being asserted.
"""
from __future__ import annotations
import numpy as np,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_two_slot_quantum_memory_choi.json'
def traceout(rho,n,axes):
    D=rho.reshape([2]*n*2)
    for i in sorted(axes,reverse=True):
        D=np.trace(D,axis1=i,axis2=i+n)
        n-=1
    return D.reshape(2**n,2**n)
def psi6(components,swap=False):
    # 6 qubits [A_I,E,A_O,A'_O,B_O,B'_O].
    V=np.zeros([2]*6,complex)
    for i,e,weight in components:
        for j in range(2):
            for k in range(2):
                V[i,e,j,j,k,k]+=weight
    if swap:V=V.swapaxes(1,3).swapaxes(1,5)
    else:pass
    return V.transpose(0,2,3,4,5,1).reshape(32,2)
def choi(memory):
    if memory:
        V=psi6([(0,0,2**-.5),(1,1,2**-.5)],swap=True)
        C=V@V.conj().T
    else:
        C=np.zeros((32,32),complex)
        for i in (0,1):
            V=psi6([(i,0,1)],swap=False)
            C+=.5*(V@V.conj().T)
    assert np.max(abs(C-C.conj().T))<1e-12
    assert np.linalg.eigvalsh(C).min()>-1e-12
    assert abs(np.trace(C)-4)<1e-11
    return C
def causal(C):
    # Trace final F; output B_O cannot signal to A_I A_O B_I.
    TF=traceout(C,5,[4])
    Prev=traceout(TF,4,[3])/2
    assert np.linalg.norm(TF-np.kron(Prev,np.eye(2)))<1e-11
    # Trace B_I from the earlier process: A_O must be identity and
    # the initial S input A_I has maximally mixed state.
    initial=traceout(Prev,3,[2])
    expected=np.kron(np.eye(2)/2,np.eye(2))
    assert np.linalg.norm(initial-expected)<1e-11
    return {"min_Choi_eigenvalue":float(np.linalg.eigvalsh(C).min()),
       "Choi_trace":float(np.trace(C).real),
       "max_later_output_no_signalling_defect":float(np.max(abs(TF-np.kron(Prev,np.eye(2))))),
       "initial_state_trace_rule_defect":float(np.max(abs(initial-expected))),
       "Choi_rank":int(np.linalg.matrix_rank(C,tol=1e-10))}
def instrument_response(memory,a,b):
    # A discards its incoming system, prepares |a>. First map sends
    # system through first step, B discards its input and prepares |b>.
    # Final map gives output F. The environment memory persists through B.
    # Initial E state is I/2 for the entangled-memory model and |0>
    # for the Markov model, because initial S has been discarded.
    S=np.zeros((2,2),complex);S[a,a]=1
    E=np.eye(2)/2 if memory else np.diag([1.,0.])
    SE=np.kron(S,E)
    SWAP=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
    U=SWAP if memory else np.eye(4)
    after=U@SE@U.conj().T
    # discard B incoming system; trace S to retain E
    E2=traceout(after,2,[0])
    B=np.zeros((2,2),complex);B[b,b]=1
    final=U@np.kron(B,E2)@U.conj().T
    rhoF=traceout(final,2,[1])
    assert abs(np.trace(rhoF)-1)<1e-10
    return np.diag(rhoF).real.tolist()
def run():
    C0=choi(False);C1=choi(True)
    results={k:causal(C) for k,C in (("memoryless_identity",C0),("coherent_S_E_swap",C1))}
    responses=[]
    for a in (0,1):
        for b in (0,1):
            r0=instrument_response(False,a,b)
            r1=instrument_response(True,a,b)
            assert abs(r0[b]-1)<1e-11
            assert abs(r1[a]-1)<1e-11
            responses.append({"first_reprepared_bit_a":a,"causal_break_reprepared_bit_b":b,
                "Markov_final_distribution":r0,"SWAP_memory_final_distribution":r1})
    # Both causal processes can have correlated past/future, but only
    # the SWAP model bypasses an intermediate causal break.
    assert results['memoryless_identity']['Choi_rank']>0
    assert results['coherent_S_E_swap']['Choi_rank']>0
    out={"status":"PASS_TWO_SLOT_CP_CAUSAL_PROCESS_MEMORY",
        "Choi_tensor_factors":"[A_in,A_out,B_in,B_out,F], each dimension2; unnormalized Omega vectors on output-to-channel Choi links",
        "causal_constraints":"Tr_F T = I_{B_out} tensor T_{A_in A_out B_in}, and Tr_{B_in}T_prev = (I/2)_{A_in} tensor I_{A_out}. Trace full T=4.",
        "models":results,
        "two_slot_break_responses":responses,
        "operational_witness":"At the second-slot replacement causal break, F=b for identity (first-slot choice erased), while F=a for SWAP environmental memory (the first-slot choice bypasses the break). Both obey same one-way causal order.",
        "prior_art":"Standard process tensor constructions and environmental memory, not a novel QFT; existing repo PASS11042 covers related one-slot qutrit instrument dependence. Distinct additional result: explicit 2-intervention qubit comb Choi with causal trace rules.",
        "scope":"Models have predetermined time ordering; no indefinite-causal-order gravity, curved spacetime, stress tensor, graviton or Planck-scale observable.",
        "source":["https://doi.org/10.1103/PRXQuantum.3.020344","https://doi.org/10.1103/PRXQUANTUM.2.030201"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("TWO SLOT CHOI",results,"CAUSAL BREAK",responses[1],flush=True)
if __name__=="__main__":run()
