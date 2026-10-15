"""TOE86 track III: falsifiable qutrit clock-channel memory witness.

Constructs a CPTP qutrit coherence-preserving channel and its explicitly
entanglement-breaking clock-dephasing null. This is a designed quantum
temporal transfer experiment, NOT spacetime emergence or non-Markovianity.
"""
from __future__ import annotations
import json
import numpy as np
from scipy.stats import binom
from analysis.w33_20261015_toe85_h2_relation_module import ROOT

DIM=3
A=[(0,b,c) for b in range(3) for c in range(3)]
OMEGA=np.exp(2j*np.pi/3)

def clock_basis():
    # Eigenbasis of qutrit cyclic shift X; its projectors define the
    # non-central (0,b,c) commuting direction of H27.
    F=np.array([[OMEGA**(j*k)/np.sqrt(DIM)
                 for k in range(DIM)] for j in range(DIM)],complex)
    X=np.zeros((3,3),complex)
    for j in range(3):X[(j+1)%3,j]=1
    assert np.allclose(F.conj().T@F,np.eye(3))
    assert np.allclose(abs(np.diag(F.conj().T@X@F)),np.ones(3))
    return F,X

def kraus_visibility(v,F):
    assert 0 <= v <= 1
    out=[np.sqrt(v)*np.eye(3,dtype=complex)]
    out += [np.sqrt(1-v)*np.outer(F[:,i],F[:,i].conj())
            for i in range(3)]
    assert np.allclose(sum(k.conj().T@k for k in out),np.eye(3))
    return out

def apply(rho,K):
    return sum(k@rho@k.conj().T for k in K)

def normalized_choi(K):
    phi=np.zeros(9,complex)
    for i in range(3): phi[i*3+i]=1/np.sqrt(3)
    rho=np.outer(phi,phi.conj())
    return sum(np.kron(np.eye(3),k)@rho@
               np.kron(np.eye(3),k.conj().T) for k in K)

def partial_transpose_output(J):
    return J.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)

def witness(v):
    F,X=clock_basis()
    K=kraus_visibility(v,F)
    # Equal superposition of all clock eigenstates; more precisely the
    # computational |0> basis state under the chosen Fourier convention.
    probe=sum(F[:,j] for j in range(3))/np.sqrt(3)
    assert np.isclose(np.linalg.norm(probe),1)
    rho=np.outer(probe,probe.conj())
    p=float(np.real(np.vdot(probe,apply(rho,K)@probe)))
    J=normalized_choi(K)
    eig=np.linalg.eigvalsh(partial_transpose_output(J))
    neg=float(sum(abs(x) for x in eig if x < -1e-10))
    assert np.allclose(J,J.conj().T)
    assert np.all(np.linalg.eigvalsh(J)>-1e-10)
    assert np.isclose(np.trace(J),1)
    assert abs(p-(1+2*v)/3)<1e-12
    assert abs(neg-v)<1e-12
    # Only eigenbasis states are uninformative: identity and EB null
    # yield exactly the same transition probability 1 on them.
    for i in range(3):
        ket=F[:,i]; r=np.outer(ket,ket.conj())
        assert np.allclose(apply(r,K),r)
    return {"visibility":v,"clock_superposition_revival_probability":p,
            "normalized_Choi_partial_transpose_negativity":neg,
            "clock_basis_states_all_preserved":True,
            "partial_transpose_negative_eigenvalues":
                [float(x) for x in eig if x<-1e-10]}

def certificate():
    null=witness(0)
    trial=witness(0.25)
    perfect=witness(1)
    n=256
    p0=1/3
    p1=trial["clock_superposition_revival_probability"]
    alpha=1e-3
    k=next(k for k in range(n+1) if binom.sf(k-1,n,p0)<=alpha)
    fp=float(binom.sf(k-1,n,p0))
    power=float(binom.sf(k-1,n,p1))
    assert fp<=alpha and power>0.95
    assert null["normalized_Choi_partial_transpose_negativity"]==0
    assert np.isclose(perfect["normalized_Choi_partial_transpose_negativity"],1)
    return {"selected_H27_clock_subgroup":[list(x) for x in A],
            "system":"single qutrit transferred between preparation and measurement",
            "null":"entanglement-breaking measurement-and-repreparation in the selected clock eigenbasis",
            "alternative":"coherent identity memory mixed with clock-basis dephasing with visibility v",
            "null_and_alternative_classical_transition_tests":
                "identical on each of the three clock eigenbasis inputs",
            "Choi_PPT_NPT_witness":"normalized Choi partial-transpose negativity; zero for null, positive for this coherent alternative",
            "settings":[null,trial,perfect],
            "pre_registered_binomial_design":
                {"n_shots":n,"false_positive_target":alpha,
                 "success_threshold_inclusive":k,
                 "null_success_probability":p0,
                 "alternative_success_probability":p1,
                 "exact_null_tail_probability":fp,
                 "exact_alternative_detection_power":power,
                 "electronics_sham_expected_probability":p0},
            "limitations":"Synthetic ideal CPTP channels and trusted preparations/measurements only. Does not establish device implementation, non-Markovianity, indefinite causal order, or an arrow of time."}

if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe86_qutrit_temporal_null.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("witness",d["settings"])
    print("binomial design",d["pre_registered_binomial_design"])
    print("WROTE",p)
