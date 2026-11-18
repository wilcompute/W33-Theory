"""Explicit pairwise-classical gate decompositions with independent
depolarizing noise at times 2 and 3.

Strong-damping gamma=.96,p=.45,eta=.95: the published Beyer
three-time witness remains negative, and all three PAIRS have complete
classical-record realizations, checked on full 4x4 Choi matrices.
Not a hardware experiment; source theorem is Beyer et al (2026).
"""
import json,math,numpy as np
from pathlib import Path
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
L=np.array([[0,1],[0,0]],complex);U=L.conj().T
def app(K,rho):return sum((k@rho@k.conj().T for k in K),np.zeros((2,2),complex))
def choi(K):
    return np.block([[app(K,np.outer(I[i],I[j])) for j in range(2)] for i in range(2)])
def CPTP(K):return np.max(abs(sum((k.conj().T@k for k in K),np.zeros((2,2),complex))-I))<1e-13
def conditional(K,branches):
    assert len(K)==len(branches) and all(CPTP(P) for P in branches)
    return [p@k for k,ps in zip(K,branches) for p in ps]
def mix(D,K):return [d@k for d in D for k in K]
def run():
    g=.96;p=.45;eta=.95
    assert p>=(1-math.sqrt(1-g))/2
    E1=[math.sqrt(g)*L,np.diag([1.,math.sqrt(1-g)]).astype(complex)]
    E2=[math.sqrt(p)*Z,math.sqrt(1-p)*I]
    E3=[math.sqrt(p)*X,math.sqrt(1-p)*I]
    a=(1+3*eta)/4;b=(1-eta)/4
    Pauli=[I,X,Y,Z];D=[math.sqrt(a)*I]+[math.sqrt(b)*u for u in Pauli[1:]]
    assert CPTP(D)
    E2n=mix(D,E2);E3n=mix(D,E3)
    assert all(CPTP(k) for k in (E1,E2n,E3n))
    f=(math.sqrt(1-g)+2*p-1)/(2*math.sqrt(1-g))
    assert 0<=f<=.5
    phi1=[U,U@L]
    phi2=[math.sqrt(f)*Z,math.sqrt(1-f)*I]
    C12=conditional(E1,[mix(D,phi1),mix(D,phi2)])
    err12=float(np.max(abs(choi(C12)-choi(E2n))))
    phi=-math.asin(math.sqrt(g))
    R=[expm(sign*1j*phi*Y/2) for sign in (1,-1)]
    E1pm=[(E1[0]+E1[1])/math.sqrt(2),(E1[0]-E1[1])/math.sqrt(2)]
    Phi_pm=[[math.sqrt(f)*X@rr,math.sqrt(1-f)*rr] for rr in R]
    assert np.max(abs(choi(E1pm)-choi(E1)))<1e-12
    C13=conditional(E1pm,[mix(D,K) for K in Phi_pm])
    err13=float(np.max(abs(choi(C13)-choi(E3n))))
    # E2n itself is random unitary (two dephasing and four Pauli
    # branches). Record all 8 classical random-unitary outcomes,
    # invert the accumulated Pauli*Z^i unitary, then apply E3n.
    K2=[];branches=[]
    for d_j,p_j in enumerate(Pauli):
        for i in (0,1):
            z_i=Z if i==0 else I
            K2.append(D[d_j]@E2[i])
            unitary=p_j@z_i
            branches.append([e@unitary.conj().T for e in E3n])
    assert np.max(abs(choi(K2)-choi(E2n)))<1e-12
    C23=conditional(K2,branches)
    err23=float(np.max(abs(choi(C23)-choi(E3n))))
    errors=[err12,err13,err23]
    assert max(errors)<1e-12,errors
    gamma_z=float(np.trace(app(E1,I/2)@Z).real)
    eta2=float(np.trace(app(E2n,(I+Z)/2)@Z).real)
    eta3=float(np.trace(app(E3n,(I+X)/2)@X).real)
    assert max(abs(gamma_z-g),abs(eta2-eta),abs(eta3-eta))<1e-12
    upper=math.sqrt(1-eta2**2)+math.sqrt(1-eta3**2)-gamma_z
    assert upper<-.33
    out=dict(status="PASS",gamma=g,p=p,eta=eta,
        pairwise_classical_threshold=(1-math.sqrt(1-g))/2,
        pairwise_full_Choi_errors=errors,
        classical_record_branch_counts={"E1_to_E2_noisy":2,"E1_to_E3_noisy":2,"E2_noisy_to_E3_noisy":8},
        all_conditional_branch_maps_CPTP=True,
        measured_design_expectations={"first_z_displacement":gamma_z,
                                     "second_protected_z":eta2,"third_protected_x":eta3},
        genuine_three_time_fixed_axes_W3=upper,
        provenance="Full 3-time incompatibility theorem and original two-time Kraus decompositions are from Beyer et al arXiv:2611.17268v1; the depolarizing random-unitary branch extension and numeric .96/.45/.95 design are independently checked.",
        caveats="Proves existence of classical decompositions separately for each PAIR and violation of the theorem's triple compatibility witness for these ideal channels. Does not generate a joint CPTP process tensor or physical optical circuit; experimentally one must establish dynamical maps from a common valid process, calibrate noise and acceptance, and exclude drift.")
    dest=ROOT/"data/toe_20261118_three_time_096_depol_pairwise_classical_proof.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS complete 8-branch noisy pairwise-classical decomposition, full Choi residuals",errors,"and W3",upper)
    return out
if __name__=="__main__":run()
