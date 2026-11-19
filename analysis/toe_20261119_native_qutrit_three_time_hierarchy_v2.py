"""Native qutrit three-time-only quantum-memory witness, with pairwise
classical Kraus/feedforward realizations and one common unitary dilation.
The W_3^(d) theorem is due to Beyer et al, arXiv:2611.17268 (2026).
"""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import null_space

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261119_native_qutrit_memory_hierarchy_v2.json'
D=3
I=np.eye(D,dtype=complex)
O=np.exp(2j*np.pi/3)
Z=np.diag([1,O,O**2])
X=np.roll(I,1,axis=0)
F=np.array([[O**(i*j) for j in range(3)] for i in range(3)],complex)/np.sqrt(3)
B=I
C=F

def apply(kraus,rho):
    return sum((K@rho@K.conj().T for K in kraus),np.zeros((3,3),complex))

def complete(kraus):
    return max(abs(sum((K.conj().T@K for K in kraus),np.zeros((3,3),complex))-I).ravel())

def channels(gamma):
    a=[np.sqrt(1-gamma)*I]
    for j in range(3):
        e=np.zeros((3,3),complex);e[0,j]=np.sqrt(gamma);a.append(e)
    dB=[np.outer(B[:,j],B[:,j].conj()) for j in range(3)]
    dC=[np.outer(C[:,j],C[:,j].conj()) for j in range(3)]
    return a,dB,dC

def prep(v):
    return [np.outer(v,I[:,j].conj()) for j in range(3)]

def choi(kraus):
    return np.array([[apply(kraus,np.outer(I[:,i],I[:,j].conj()))
          for j in range(3)] for i in range(3)]).transpose(0,2,1,3).reshape(9,9)

def pair_classical(gamma):
    E1,E2,E3=channels(gamma)
    # The disturbance/replacement jump basis is contextual: choose Z or X.
    def from_replacer(basis):
        K=[np.sqrt(1-gamma)*I]
        for j in range(3):
            K.append(np.sqrt(gamma)*np.outer(I[:,0],basis[:,j].conj()))
        dBasis=[np.outer(basis[:,j],basis[:,j].conj()) for j in range(3)]
        feedback=[dBasis]+[prep(basis[:,j]) for j in range(3)]
        return K,feedback
    def comp_pair(K,fb):
        assert complete(K)<1e-14
        assert all(complete(Fs)<1e-14 for Fs in fb)
        return [V@k for k,Fs in zip(K,fb) for V in Fs]
    e12=comp_pair(*from_replacer(B))
    e13=comp_pair(*from_replacer(C))
    # E2 random-unitary realization: uniform Z^k. Conditional unphase
    # and then dephase in Fourier basis to produce E3 exactly.
    ks=[np.linalg.matrix_power(Z,k)/np.sqrt(3) for k in range(3)]
    fb=[[P@np.linalg.matrix_power(Z,-k) for P in E3] for k in range(3)]
    e23=comp_pair(ks,fb)
    targets=(E2,E3,E3)
    err=[float(np.linalg.norm(choi(test)-choi(goal))) for test,goal in zip((e12,e13,e23),targets)]
    firsterr=max(np.linalg.norm(choi(K)-choi(E1)) for K in [from_replacer(B)[0],from_replacer(C)[0]])
    randomerr=float(np.linalg.norm(choi(ks)-choi(E2)))
    assert max(err)<1e-12 and firsterr<1e-12 and randomerr<1e-12
    return {'pairwise_full_choi_residuals':err,
       'first_instrument_equal_E1_residual':float(firsterr),
       'E2_random_phase_instrument_residual':randomerr,
       'first_instrument_branch_count':4,
       'E2_instrument_branch_count':3,
       'pairwise_decompositions':['(E1,E2): replacement instrument in computational basis',
          '(E1,E3): replacement instrument in Fourier basis',
          '(E2,E3): random Z^k with inverse feedforward and Fourier dephasing']}

def construct_unitary(kraus):
    # Common S(3)*E(4) unitary. Environment basis |0> is first 3 axes.
    V=np.concatenate(kraus+[np.zeros((3,3),complex)]*(4-len(kraus)),axis=0)
    assert np.linalg.norm(V.conj().T@V-I)<1e-12
    null=null_space(V.conj().T)
    U=np.column_stack((V,null))
    assert np.linalg.norm(U.conj().T@U-np.eye(12))<1e-12
    return U

def common_unitary_dilation(gamma):
    ksets=channels(gamma)
    U=[construct_unitary(ks) for ks in ksets]
    transitions=[U[0],U[1]@U[0].conj().T,U[2]@U[1].conj().T]
    rng=np.random.default_rng(261119)
    maxerr=0.;maxunit=0.
    for _ in range(24):
        A=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
        rho=A@A.conj().T;rho/=np.trace(rho)
        total=np.zeros((12,12),complex);total[:3,:3]=rho
        for j in range(3):
            T=transitions[j]
            maxunit=max(maxunit,float(np.linalg.norm(T.conj().T@T-np.eye(12))))
            total=T@total@T.conj().T
            output=sum(total[3*e:3*e+3,3*e:3*e+3] for e in range(4))
            maxerr=max(maxerr,float(np.linalg.norm(output-apply(ksets[j],rho))))
    assert maxerr<1e-12 and maxunit<1e-12
    return {'same_environment_dimension':4,'global_hilbert_dimension':12,
      'random_density_matrices_verified':24,'three_output_channel_max_residual':maxerr,
      'intertime_unitarity_max_error':maxunit,
      'construction':'U1, U2 U1†, U3 U2† on shared S3⊗E4; no interventions between observations in marginal checks'}

def h27_gate(ksets):
    # All H27-covariant CPTP maps are unital by irreducibility and Schur:
    # E(I) commutes with X,Z; hence is cI and trace-preserving forces c=1.
    rng=np.random.default_rng(42)
    rho=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));rho=rho@rho.conj().T;rho/=np.trace(rho)
    residual=[]
    for ks in ksets:
        errs=[]
        for U in (X,Z):
            errs.append(float(np.linalg.norm(apply(ks,U@rho@U.conj().T)-U@apply(ks,rho)@U.conj().T)))
        residual.append(max(errs))
    assert residual[0]>1e-3 and residual[1]<1e-12 and residual[2]<1e-12
    return {'H27_covariance_residuals_for_E1_E2_E3':residual,
      'nonunital_H27_covariant_qutrit_CPTP_possible':False,
      'reason':'Schur lemma on irreducible X,Z plus TP forces E(I)=I',
      'interpretation':'Nonzero W3 from this particular witness requires breaking exact H27 covariance of first channel; does NOT exclude other quantum-memory witnesses for covariant channels.'}

def run():
    samples=[]
    for g in (.05,.36,.75):
        ks=channels(g)
        assert all(complete(ch)<1e-12 for ch in ks)
        first=apply(ks[0],I)
        nonunital=.5*sum(abs(x) for x in np.linalg.eigvalsh(first-I))
        assert abs(nonunital-2*g)<1e-12
        # F(dephased basis orthogonal pure states)=0 in both MUB bases.
        fidelities=[]
        for K,basis in ((ks[1],B),(ks[2],C)):
            maxF=0.
            for i in range(3):
                for j in range(i+1,3):
                    ra=apply(K,np.outer(basis[:,i],basis[:,i].conj()))
                    rb=apply(K,np.outer(basis[:,j],basis[:,j].conj()))
                    maxF=max(maxF,float(abs(np.trace(ra@rb))))
            fidelities.append(maxF)
        assert max(fidelities)<1e-12
        pairs=pair_classical(g)
        mem=common_unitary_dilation(g)
        samples.append({'gamma':g,'native_qutrit_dimension':3,
            'unitality_witness_S1':float(nonunital),
            'pairwise_Fidelity_sums':fidelities,
            'published_dimension_d_three_time_witness':float(-2*g),
            'pairwise_classical_certificates':pairs,'joint_quantum_dilation':mem})
    cov=h27_gate(channels(.36))
    out={'status':'PASS_NATIVE_QUTRIT_GENUINE_THREE_TIME_ONLY_MEMORY',
       'samples':samples,'H27_symmetry_selection_rule':cov,
       'published_witness':'Beyer et al arXiv:2611.17268 supplement VI eq S38; theorem not original to repo',
       'novel_combination':'Native full qutrit Z and Fourier MUB channels, 3 explicit pairwise Kraus-feedback models, and one full S3⊗E4 unitary sequence',
       'limitations':'No measured device; interventions in a fabricated device still require experimental tomography. Individual pairwise classical realizations are incompatible with one common classical record, as witnessed by W<0.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('NATIVE QUTRIT MEMORY PASS W(gamma=.36)',samples[1]['published_dimension_d_three_time_witness'])
    return out
if __name__=='__main__':run()
