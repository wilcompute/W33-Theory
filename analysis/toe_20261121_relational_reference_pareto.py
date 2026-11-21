"""Six finite Witting research fronts, with independent checkable geometry.

Reference-bath chart covariance, noisy 25-bin privacy/Fisher design,
cost-aware detector reference allocation, a minimal 10-mode Petz dilation,
all 45 conditional chart-gate identities, and conjugation-odd triangle phases.

NO physical chip, spacetime, force, TOE, QKD secrecy or quantum advantage claimed.
Run: python analysis/toe_20261121_relational_reference_pareto.py
"""
from __future__ import annotations
import itertools, json, math, sys
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.linalg import null_space

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_hermitian45_pauli_sic_bridge as source

OUT=ROOT/"data/toe_20261121_relational_reference_pareto.json"
LOW=[0,1,2,5,6,8,10,11,12,13,15,16,19,21,23,24,27,28,30,32,34,35,37,39]
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
BALANCED=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]
ROUTING=[0,22,14,19,6,7,2,11,33,38,35,40,23,31,10,32,8,43,29,36,27,44,
         9,15,21,16,12,25,3,37,13,41,20,5,34,26,30,17,42,24,18,39,28,1,4]

def geometry():
    rays,wf4=source.witting_rays()
    iso=sorted(z for z in {source.norm4(v)
         for v in itertools.product(range(4),repeat=4) if any(v)}
         if source.herm4(z,z)==0)
    H=np.array([[int(source.herm4(z,v)==0) for v in wf4] for z in iso],int)
    A=np.zeros((45,45),int)
    for a,b in itertools.combinations(range(45),2):
        A[a,b]=A[b,a]=int(not (H[a]&H[b]).any())
    J=np.ones((45,45),int)
    assert np.array_equal(H@H.T,6*np.eye(45,dtype=int)-2*A+2*J)
    assert np.array_equal(A@A,9*np.eye(45,dtype=int)+3*J)
    P1=J/45;P20=(9*np.eye(45)+3*A-J)/18;P24=(15*np.eye(45)-5*A+J)/30
    assert np.max(abs(P1+P20+P24-np.eye(45)))<1e-12
    return rays,H,A,(P1,P20,P24)

def calibration(H,P24):
    evals,U=np.linalg.eigh(P24);U=U[:,-24:]
    D=H.T@U/8
    eta=.75;probs=np.r_[np.full(40,eta/40),1-eta]
    JT=np.zeros((41,64));JR=JT.copy()
    JT[:40,:24]=eta*D;JT[:40,24:]=np.eye(40)/40
    JR[:40,24:]=np.eye(40)/40
    JT[40,24:]=JR[40,24:]=-1/40
    FT=JT.T@(JT/probs[:,None]);FR=JR.T@(JR/probs[:,None])
    scans=[]
    for f in (.1,.25,.5,.75,.9):
        F=(1-f)*FT+f*FR
        S=F[:24,:24]-F[:24,24:]@np.linalg.solve(F[24:,24:],F[24:,:24])
        eig=np.linalg.eigvalsh(S)
        assert max(abs(eig-7.5*eta*f*(1-f)))<1e-10
        scans.append([f,float(np.sum(1/eig))])
    assert abs(scans[2][1]-17.0666666666667)<1e-9
    c_ref=4.;c_target=1.
    spend_share=math.sqrt(c_ref)/(math.sqrt(c_ref)+math.sqrt(c_target))
    ref_launch_share=(spend_share/c_ref)/(spend_share/c_ref+(1-spend_share)/c_target)
    return dict(status="PASS",per_launch_Fisher_eigenvalue=7.5*eta/4,
        Cramer_Rao_coefficient=scans[2][1],fraction_scan=scans,
        reference_budget_fraction_if_reference_cost_4x=spend_share,
        reference_launch_fraction_if_reference_cost_4x=ref_launch_share,
        limitation="Local necessary Cramer-Rao bound; does not guarantee finite-shot risk.")

def privacy(H,P24):
    ev,U=np.linalg.eigh(P24);U=U[:,-24:]
    def score(labels,eps):
        C=np.c_[H[:,labels]/8,1-H[:,labels].sum(axis=1)/8]
        gamma=1-40*eps/39
        C=gamma*C+np.r_[np.full(24,eps/39),16*eps/39]
        p=C.mean(axis=0)
        def entropy(v):return -sum(float(z)*math.log2(float(z))for z in v if z>1e-13)
        info=entropy(p)-np.mean([entropy(c)for c in C])
        d=gamma*np.c_[U.T@H[:,labels]/8,-U.T@H[:,labels].sum(axis=1)/8]
        ev=np.linalg.eigvalsh((d/p)@d.T)
        assert ev.min()>0
        return [float(info),float(np.sum(1/ev))]
    arr=[]
    for eps in (0,.05,.15):
        arr.append(dict(wrong_label_probability=eps,old=score(OLD,eps),
                        new=score(BALANCED,eps),minimum_leakage=score(LOW,eps)))
        assert arr[-1]["new"][0]<arr[-1]["old"][0]
        assert arr[-1]["new"][1]<arr[-1]["old"][1]
    assert abs(arr[0]["new"][0]-1.412155394967)<1e-9
    assert abs(arr[0]["new"][1]-11.322222222222)<1e-9
    return dict(status="PASS",new_labels=BALANCED,
                previous_labels=OLD,previous_privacy_minimum_labels=LOW,
                noise_sweep=arr,
                optimization_claim="Verified discrete improvement, not global Pareto optimum.")

def relational_bath(P):
    P1,P20,P24=P
    n=45;u=np.ones(n)/np.sqrt(n);initial=np.outer(u,u)
    theta=math.pi;k=(43+2*math.cos(theta))/45
    def channel(rho):
        return k*rho+(1-k)*np.diag(np.diag(rho))
    rho=channel(initial)
    assert abs(np.trace(P24@rho)-96/2025)<1e-11
    pop=[]
    for t in (0,1,5,20,100):
        R=k**t*initial+(1-k**t)*np.eye(45)/45
        x=[float(np.trace(Q@R))for Q in P]
        assert abs(x[2]-24*(1-k**t)/45)<1e-11
        pop.append(dict(interactions=t,sector_populations=x))
    return dict(status="PASS",reference_state="I_45/45",
       joint_hamiltonian="Sum_r |r><r|_reference tensor |r><r|_chart",
       Kraus_formula="exp(-i pi |r><r|)/sqrt(45), r=0..44",
       exact_24D_population="(24/45)*(1-(41/45)^n)",
       reference_interaction_offdiagonal_factor=k,
       sector_populations=pop,
       caution="Open-system, fully S45-covariant mixing; not closed-system sector transitions or a fundamental gauge interaction.")

def cnot(c,t):
    M=np.zeros((16,16),complex)
    for i in range(16):
        b=[(i>>(3-j))&1 for j in range(4)]
        if b[c]:b[t]^=1
        M[sum(b[j]<<(3-j)for j in range(4)),i]=1
    return M

def chart_gate(rays,H):
    h=np.array([[1,1],[1,-1]],float)/np.sqrt(2)
    I=np.eye(2)
    prep=np.kron(np.kron(np.kron(I,h),I),I)@cnot(1,3)@cnot(0,2)
    phases=[]
    for i in range(16):
        b=[(i>>(3-j))&1 for j in range(4)]
        v=-1j if b[2]==0 else 1
        if b[2]==0 and b[1]==1 and b[3]==1:v*=1j
        phases.append(v)
    canonical=prep.conj().T@np.diag(phases)@prep
    O=abs(rays.conj()@rays.T)**2
    error=0.
    for row in H:
        ids=np.where(row)[0]
        idsL=[i for i in ids if O[i,ids[0]]>1e-10]
        idsR=sorted(set(ids)-set(idsL))
        assert len(idsL)==len(idsR)==4
        L=sum(np.outer(rays[i],rays[i].conj())for i in idsL)/2
        R=sum(np.outer(rays[i],rays[i].conj())for i in idsR)/2
        _,VL=np.linalg.eigh(L);_,VR=np.linalg.eigh(R)
        S=np.column_stack((VL[:,-2:],VR[:,-2:]))
        U=np.kron(S,S)@canonical@np.kron(S,S).conj().T
        Q=sum(np.kron(np.outer(rays[i],rays[i].conj()),
                      np.outer(rays[i],rays[i].conj()))for i in ids)
        error=max(error,float(np.max(abs(U-np.eye(16)-(-1-1j)*.75*Q))))
    assert error<1e-10
    return dict(status="PASS",charts=45,max_matrix_residual=error,
       canonical_CNOT_upper_bound=14,
       warning="Assumes native entangling gates and 4x4 basis rotations; not passive-only photon hardware.")

def petz_dilation(rays):
    B=np.zeros((45,4),complex);B[:40]=rays.conj()/np.sqrt(10)
    assert np.max(abs(B.conj().T@B-np.eye(4)))<1e-12
    K=B[ROUTING].reshape(9,5,4)
    def petz(T):
        d,e,k=T.shape
        sig=sum(T[:,j,:]@T[:,j,:].conj().T for j in range(e))/k
        ev,U=np.linalg.eigh(sig)
        inv=(U*np.where(ev>1e-12,1/np.sqrt(np.maximum(ev,1e-300)),0))@U.conj().T
        R=np.array([T[:,j,:].conj().T@inv/np.sqrt(k)for j in range(e)])
        Fe=sum(abs(np.trace(M@T[:,j,:]))**2 for M in R for j in range(e))/k**2
        return float(Fe),R
    rng=np.random.default_rng(20261121)
    best=(-1,None,None)
    for n in range(300):
        V,_=np.linalg.qr(rng.normal(size=(4,2))+1j*rng.normal(size=(4,2)))
        fidelity,R=petz(K@V)
        if fidelity>best[0]:best=(fidelity,n,V)
    fe,number,V=best
    fe,R=petz(K@V)
    iso=np.concatenate(R,axis=0)
    err=float(np.max(abs(iso.conj().T@iso-np.eye(9))))
    assert abs(fe-.9034972067200646)<1e-10 and number==261
    assert iso.shape==(10,9) and err<1e-11
    U=np.column_stack((iso,null_space(iso.conj().T)))
    assert U.shape==(10,10) and np.max(abs(U.conj().T@U-np.eye(10)))<1e-11
    return dict(status="PASS",best_seeded_subcode_index=number,
       entanglement_fidelity=fe,average_qubit_fidelity=(2*fe+1)/3,
       recovery_Kraus_count=5,recovery_dilation_shape=[10,9],
       isometry_error=err,unitary_extension_shape=[10,10],
       minimal_environment_dimension_by_dimension_count=5,
       caution="Petz decoder only; not the SDP-optimal decoder or a demonstrated physical interferometer.")

def phases(rays):
    G=rays.conj()@rays.T;counts=Counter();candidate=None
    for a,b,c in itertools.combinations(range(40),3):
        v=G[a,b]*G[b,c]*G[c,a]
        if abs(v)<1e-10:counts["zero"]+=1;continue
        ang=abs(np.angle(v))
        if abs(ang-math.pi/6)<1e-9:counts["pi_over_6"]+=1
        elif abs(ang-math.pi/2)<1e-9:counts["pi_over_2"]+=1
        else:raise AssertionError((a,b,c,v))
        if candidate is None or abs(v.imag)>abs(candidate[1]):candidate=([a,b,c],v.imag)
    assert dict(counts)==dict(zero=6640,pi_over_6=2880,pi_over_2=360)
    return dict(status="PASS",triangle_count=dict(counts),
       phase_sensitive_example_ray_ids=candidate[0],
       Im_Tr_PiPjPk=float(candidate[1]),
       conjugation_odd=True,
       warning="Requires phase-sensitive coherent interferometry; pairwise intensities cannot see handedness.")

def main():
    rays,H,A,P=geometry()
    d={"status":"PASS","date":"2026-11-21",
       "geometry":"Witting rays / isotropic GF4 Hermitian charts rebuilt from repo source",
       "front1_calibrated_reference":calibration(H,P[2]),
       "front2_privacy_Pareto":privacy(H,P[2]),
       "front3_covariant_quantum_reference":relational_bath(P),
       "front4_non_circular_chart_gate":chart_gate(rays,H),
       "front5_minimal_Petz_dilation":petz_dilation(rays),
       "front6_triangle_phase_witness":phases(rays),
       "scope":"Mathematical finite-mode models; no physical build or fundamental-theory proof."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS six independent fronts; certificate:",OUT,flush=True)
    return d

if __name__=="__main__":
    main()
