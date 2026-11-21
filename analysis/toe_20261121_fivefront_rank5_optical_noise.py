"""Five independently falsifiable Witting physics/computation fronts.

1 rank-5 CPTP SDP decoder with primal/dual feasible bounds and 10-mode unitary;
2 phase-noise decoder witness and output-replacement affine control;
3 passive 16-rail versus two-physical-photon encoding resources;
4 covariant partial-SWAP with 24D resource bookkeeping;
5 25-bin calibrated Fisher Schur complement with unknown raw-ray efficiencies.

Mathematical models ONLY. Requires NumPy/SciPy plus committed Witting geometry.
Run from repo: python analysis/toe_20261121_fivefront_rank5_optical_noise.py
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import numpy as np
from scipy.linalg import null_space
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parent))
import toe_20261121_relational_reference_pareto as prior
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_fivefront_rank5_optical_noise.json"
PERM=[0,22,14,19,6,7,2,11,33,38,35,40,23,31,10,32,8,43,29,36,27,44,
      9,15,21,16,12,25,3,37,13,41,20,5,34,26,30,17,42,24,18,39,28,1,4]
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
NEW=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]

def routed_qubit(rays):
    B=np.zeros((45,4),complex);B[:40]=rays.conj()/np.sqrt(10)
    assert np.max(abs(B.conj().T@B-np.eye(4)))<1e-11
    K=B[PERM].reshape(9,5,4)
    rng=np.random.default_rng(20261121)
    best=(-1,None,None)
    for i in range(300):
        V,_=np.linalg.qr(rng.normal(size=(4,2))+1j*rng.normal(size=(4,2)))
        T=K@V
        sig=sum(T[:,j,:]@T[:,j,:].conj().T for j in range(5))/2
        ev,U=np.linalg.eigh(sig)
        inv=(U*np.where(ev>1e-12,1/np.sqrt(np.maximum(ev,1e-300)),0))@U.conj().T
        R=np.array([T[:,j,:].conj().T@inv/math.sqrt(2) for j in range(5)])
        Fe=sum(abs(np.trace(r@T[:,j,:]))**2 for r in R for j in range(5))/4
        if Fe>best[0]:best=(float(Fe),V,R)
    assert abs(best[0]-.9034972067200646)<1e-9
    return K,best

def optimize_decoder(rays):
    K,(petz,V,Rpetz)=routed_qubit(rays)
    T=K@V
    M=np.zeros((18,18),complex)
    for j in range(5):
        v=T[:,j,:].T.conj().reshape(18)
        M+=np.outer(v,v.conj())/4
    Jpetz=sum(np.outer(r.reshape(18),r.reshape(18).conj()) for r in Rpetz)
    assert abs(np.trace(M@Jpetz).real-petz)<1e-10
    H=[]
    for i in range(9):
        e=np.zeros((9,9),complex);e[i,i]=1;H.append(e)
    for i in range(9):
        for j in range(i+1,9):
            e=np.zeros((9,9),complex);e[i,j]=e[j,i]=1/math.sqrt(2);H.append(e)
            e=np.zeros((9,9),complex);e[i,j]=1j/math.sqrt(2);e[j,i]=-1j/math.sqrt(2);H.append(e)
    H=np.asarray(H)
    assert len(H)==81
    basis=np.array([np.kron(np.eye(2),h)for h in H])
    def toY(x):return np.einsum("a,aij->ij",x,H,optimize=True)
    def toX(y):return np.einsum("aij,ji->a",H,y,optimize=True).real
    def fg(x,mu):
        y=toY(x);S=np.kron(np.eye(2),y)-M
        eig,U=np.linalg.eigh(S)
        if eig.min()<1e-13:return 1e6+abs(min(eig.min(),0))*1e6,np.ones(81)*1e3
        inv=(U*(1/eig))@U.conj().T
        grad=np.eye(9)-mu*(inv[:9,:9]+inv[9:,9:])
        return float(np.trace(y).real-mu*np.log(eig).sum()),toX(grad)
    x=toX((max(np.linalg.eigvalsh(M)).real+.4)*np.eye(9))
    for mu in (.08,.015,.003,.0006,.0001,.00002,.000004,.0000008):
        res=minimize(lambda z:fg(z,mu),x,jac=True,method="BFGS",
                     options={"maxiter":300,"gtol":1e-8})
        x=res.x
    # A damped Newton step resolves the small-barrier ill conditioning.
    for mu in (1.6e-7,3.2e-8,6.4e-9):
        for _ in range(35):
            val,g=fg(x,mu)
            if np.linalg.norm(g)<1e-8:break
            S=np.kron(np.eye(2),toY(x))-M
            ev,U=np.linalg.eigh(S)
            inv=(U*(1/ev))@U.conj().T
            A=np.einsum("ij,ajk->aik",inv,basis,optimize=True)
            hess=mu*np.einsum("aij,bji->ab",A,A,optimize=True).real
            step=np.linalg.solve(hess,g)
            desc=float(g@step);scale=1.0
            for _ in range(35):
                nextx=x-scale*step
                fv,_=fg(nextx,mu)
                if fv<val-1e-4*scale*desc:break
                scale*=.5
            x=nextx
            if scale<1e-10:break
    Y=toY(x);Slack=np.kron(np.eye(2),Y)-M
    assert np.linalg.eigvalsh(Slack)[0]>0
    # Central-path primal followed by an exact CPTP Choi rank-five truncation
    J=mu*np.linalg.inv(Slack)
    ev,U=np.linalg.eigh((J+J.conj().T)/2)
    L=U[:,-5:]@np.diag(np.sqrt(ev[-5:]))
    J5=L@L.conj().T
    block=J5[:9,:9]+J5[9:,9:]
    lam,V9=np.linalg.eigh(block)
    assert lam.min()>0
    Nin=(V9*(1/np.sqrt(lam)))@V9.conj().T
    J5=np.kron(np.eye(2),Nin)@J5@np.kron(np.eye(2),Nin)
    vals,Sv=np.linalg.eigh((J5+J5.conj().T)/2)
    Kraus=np.array([(Sv[:,-5+i]*np.sqrt(vals[-5+i])).reshape(2,9)
                    for i in range(5)])
    iso=Kraus.reshape(10,9)
    tp=np.max(abs(iso.conj().T@iso-np.eye(9)))
    assert tp<1e-9
    U10=np.column_stack((iso,null_space(iso.conj().T)))
    assert U10.shape==(10,10) and np.max(abs(U10.conj().T@U10-np.eye(10)))<1e-9
    f_primal=float(np.trace(M@J5).real)
    f_dual=float(np.trace(Y).real)
    assert abs(f_primal-.9165859735)<2e-6
    assert f_dual-f_primal>0 and f_dual-f_primal<2e-6
    return dict(status="PASS",petz_entanglement_fidelity=petz,
        rank5_CPTP_fidelity=f_primal,dual_upper_bound=f_dual,
        upper_lower_gap=f_dual-f_primal,Stinespring_shape=[10,9],
        decoder_unitary_shape=[10,10],TP_residual=float(tp),
        Choi_rank=5),Kraus,Rpetz,T,U10,V

def phase_noise(Ropt,Rpetz,T):
    def compute(R):
        c=np.einsum("rai,iza->rzi",R,T)
        F0=float((abs(c.sum(axis=2))**2).sum()/4)
        Fdeph=float((abs(c)**2).sum()/4)
        return {"clean":F0,"fully_output_dephased":Fdeph,
                "gaussian_std_scan":[{"sigma_rad":sig,
                "average_F_e":float(math.exp(-sig**2)*F0+
                     (1-math.exp(-sig**2))*Fdeph)}
                for sig in (0,.03,.1,.2,.5,1.)]}
    a=compute(Ropt);b=compute(Rpetz)
    assert a["clean"]>b["clean"] and a["fully_output_dephased"]>b["fully_output_dephased"]
    # Independently: output replacement is affine *for every CPTP decoder*
    # F_e[(1-p)N + p Tr(.)I_9/9]=(1-p) F_e(N)+p/4.
    return {"status":"PASS","SDP":a,"Petz":b,
        "output_replacement_affine_fidelity":"(1-p)*F_e(0)+p/4, all CPTP decoders",
        "critical_control":"The replacement model cannot change which decoder is optimal; phase noise can."}

def optical_cost(rays,H):
    Olap=abs(rays.conj()@rays.T)**2
    def mesh_count(U):
        Q=U.copy();n=Q.shape[0];count=0
        for col in range(n-1):
            for i in range(n-1,col,-1):
                a,b=Q[i-1,col],Q[i,col];norm=np.hypot(abs(a),abs(b))
                if norm<1e-13:continue
                c=np.conj(a)/norm;s=np.conj(b)/norm
                g=np.array([[c,s],[-np.conj(s),np.conj(c)]])
                Q[[i-1,i]]=g@Q[[i-1,i]]
                count+=1
        assert np.max(abs(Q-np.diag(np.diag(Q))))<1e-10
        return count
    full=[];local=[]
    for row in H:
        ids=np.where(row)[0]
        L=[i for i in ids if Olap[i,ids[0]]>1e-10]
        R=sorted(set(ids)-set(L))
        l=sum(np.outer(rays[i],rays[i].conj())for i in L)/2
        r=sum(np.outer(rays[i],rays[i].conj())for i in R)/2
        _,vl=np.linalg.eigh(l);_,vr=np.linalg.eigh(r)
        S=np.column_stack((vl[:,-2:],vr[:,-2:]))
        local.append(mesh_count(S))
        Q=sum(np.kron(np.outer(rays[i],rays[i].conj()),
                       np.outer(rays[i],rays[i].conj()))for i in ids)
        U=np.eye(16)+(-1-1j)*.75*Q
        full.append(mesh_count(U))
    assert len(full)==len(local)==45
    return {"status":"PASS","single_photon_16rail_Reck_gate_count":
        {"min":min(full),"mean":float(np.mean(full)),"max":max(full)},
        "local_4rail_SIC_basis_Reck_gate_count":
        {"min":min(local),"mean":float(np.mean(local)),"max":max(local)},
        "logical_multi_ququart_single_photon_modes":"4^n",
        "warning":"One photon in 16 paths simulates two logical ququarts, not two interacting photons. Two-photon photonic entanglers remain required for two independently occupied ququarts."}

def covariant_resource(A,P):
    P1,P20,P24=P
    # Coordinates swapped in the *actual* GF4 45-chart geometry.
    assert np.max(abs(A@P24-P24@A))<1e-11
    rho=P1;sig=P24/24
    assert np.max(abs(rho@sig))<1e-11
    res=[]
    for theta in (0,math.pi/8,math.pi/4,math.pi/2):
        c,s=math.cos(theta),math.sin(theta)
        R=c*c*rho+s*s*sig+1j*c*s*(rho@sig-sig@rho)
        a=[float(np.trace(Q@R).real)for Q in P]
        assert abs(a[2]-s*s)<1e-11
        res.append({"theta":theta,"sector_populations":a})
    return {"status":"PASS","partial_swap_sector_populations":res,
        "joint_symmetry":"SWAP commutes with U(g) tensor U(g) for any Witting chart permutation g",
        "resource":"Reference initially prepared as P24/24; no spontaneous creation of 24D charge"}

def calibrated_bins(H,P):
    ev,U=np.linalg.eigh(P);U=U[:,-24:]
    D=H.T@U/8;eta=.75;f=.5
    arr=[]
    for name,labels in (("old25",OLD),("new25",NEW),("all40",list(range(40)))):
        n=len(labels)+(len(labels)<40)
        C=np.zeros((n,40))
        for j,i in enumerate(labels):C[j,i]=1
        if n>len(labels):C[-1,[i for i in range(40)if i not in labels]]=1
        p=np.r_[C@(np.ones(40)*eta/40),1-eta]
        Jx=np.vstack((eta*C@D,np.zeros((1,24))))
        Je=np.vstack((C/40,-np.ones((1,40))/40))
        Jt=np.column_stack((Jx,Je));Jr=np.column_stack((np.zeros_like(Jx),Je))
        F=(1-f)*(Jt.T/p)@Jt+f*(Jr.T/p)@Jr
        Sch=F[:24,:24]-F[:24,24:]@np.linalg.pinv(F[24:,24:],rcond=1e-11)@F[24:,:24]
        lamb=np.linalg.eigvalsh(Sch)
        assert min(lamb)>1e-9
        arr.append({"layout":name,"profile_Fisher_inverse_trace":float(sum(1/lamb)),
                    "minimum_launches_RMS_0p001_CramerRao":int(math.ceil(sum(1/lamb)/1e-6)),
                    "rank_identifiable_efficiency_combinations":int(np.linalg.matrix_rank(Je))})
    assert abs(arr[1]["profile_Fisher_inverse_trace"]-60.385185185)<1e-6
    assert arr[1]["profile_Fisher_inverse_trace"]<arr[0]["profile_Fisher_inverse_trace"]
    return {"status":"PASS","eta":eta,"reference_launch_fraction":f,
        "unknown_raw_efficiencies":40,"layouts":arr,
        "model_limits":"Unknown raw efficiencies individually unidentifiable in pooled bin, yet 24 chart-bias coordinates remain locally identifiable from reference and resolved labels."}

def main():
    rays,H,A,P=prior.geometry()
    decoder,R,Petz,T,U10,V=optimize_decoder(rays)
    obj={"status":"PASS","date":"2026-11-21",
        "front1_rank5_optimal_decoder":decoder,
        "front2_phase_noise_and_depolarizing_control":phase_noise(R,Petz,T),
        "front3_optical_encoding_gate_cost":optical_cost(rays,H),
        "front4_covariant_reference_sector_transfer":covariant_resource(A,P),
        "front5_calibrated_25bin_detector":calibrated_bins(H,P[2]),
        "scope":"Finite mathematical model; no hardware demonstration or TOE."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
    print("PASS five fronts, feasible 5-Kraus decoder, 10-mode dilation",OUT)
    return obj
if __name__=="__main__":main()
