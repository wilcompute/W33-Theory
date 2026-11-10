#!/usr/bin/env python3
"""Four optical designs: full noncommuting lossy component POVMs, Fisher test.

Model physical 2/3/9 mode Givens, local U3⊗U3 stages, finite crossing
SWAPs, diagonal phase masks. Inject attenuation *between* noncommuting
mixing stages and independent phase drift. Use all nine click AND no-click
outcomes per launched trial, not a scalar throughput multiplier.
"""
import json,sys,math,hashlib
from pathlib import Path
import numpy as np
from w33_20261109_optical_fisher_competition import designs,two_cz,fourier
from w33_20261109_shallow_cz_complete import candidate,qutrit_haar,entangler
from w33_20261109_q8_structured_fourier_readout import L,LI,IL,F3
from w33_20261109_q8_ten_context_tomography import projection_design
from w33_20261109_q8_five_extensions import horodecki_state
from w33_20261109_q8_horodecki_ccnr_exact import realign
from w33_20261109_q8_perm_fourier_phases_27 import make
from w33_20261109_q8_12setting_completion import product_mub

def qr_lossy(U,t=1.,phase=0.,rng=None):
    """Exact U† when t=1,phase=0. Loss after each QR elimination gate."""
    rng=np.random.default_rng(1) if rng is None else rng
    n=len(U);R=U.copy();gates=[]
    for col in range(n-1):
        for row in range(n-1,col,-1):
            a,b=R[row-1,col],R[row,col]
            nn=np.hypot(abs(a),abs(b))
            if nn<1e-12:continue
            G=np.eye(n,dtype=complex)
            G[row-1,row-1]=a.conjugate()/nn
            G[row-1,row]=b.conjugate()/nn
            G[row,row-1]=-b/nn
            G[row,row]=a/nn
            R=G@R;gates.append((G,row-1,row))
    K=np.eye(n,dtype=complex)
    for G,i,j in gates:
        drift=np.eye(n,dtype=complex)
        drift[i,i]=np.exp(1j*rng.normal(0,phase))
        drift[j,j]=np.exp(1j*rng.normal(0,phase))
        att=np.eye(n,dtype=complex);att[i,i]=math.sqrt(t);att[j,j]=math.sqrt(t)
        K=att@drift@G@K
    K=np.diag(np.diag(R).conjugate())@K
    if t==1 and phase==0:assert np.max(abs(K-U.conj().T))<2e-12
    return K,len(gates)

def local_transfer(A,B,t,phase,rng):
    # Three-mode local transforms repeated on 3 spectator blocks:
    # 2 x 9 Givens (18 total for generic U3 tensor U3)
    K1,n1=qr_lossy(A,t,phase,rng)
    K2,n2=qr_lossy(B,t,phase,rng)
    return np.kron(K1,K2),3*(n1+n2)

def phase_transfer(phases,tphase,phase,rng):
    return math.sqrt(tphase)*np.diag(np.exp(-1j*np.array(phases)
                                   +1j*rng.normal(0,phase,size=9)))

def perm_transfer(p,tcross):
    P=np.eye(9)[p,:]
    target=list(np.argmax(P.T,axis=1))
    current=list(range(9));K=np.eye(9,dtype=complex);swaps=0
    for i,desired in enumerate(target):
        j=current.index(desired)
        while j>i:
            S=np.eye(9,dtype=complex)
            S[[j-1,j],:]=S[[j,j-1],:]
            loss=np.eye(9,dtype=complex)
            loss[j-1,j-1]=math.sqrt(tcross)
            loss[j,j]=math.sqrt(tcross)
            K=loss@S@K
            current[j-1],current[j]=current[j],current[j-1]
            swaps+=1;j-=1
    assert current==target
    if tcross==1:assert np.max(abs(K-P.T))<1e-12
    return K,swaps

def cz_factors():
    saved=json.loads((Path(__file__).resolve().parents[1]/
               "data/w33_20261109_shallow_cz_complete.json").read_text())
    rng=np.random.default_rng(20261109673)
    for _ in range(20):candidate(rng,False);candidate(rng,False)
    for _ in range(950):candidate(rng,True);candidate(rng,True)
    idx=saved["best_candidate_index"]
    selected=None
    for k in range(idx+1):
        stack=[]
        for _ in range(2):
            A,B,C,D=(qutrit_haar(rng) for q in range(4))
            stack.append((A,B,C,D))
        selected=stack
    target=two_cz()
    CZ=entangler()
    for x,U in zip(selected,target):
        A,B,C,D=x
        assert np.max(abs(CZ@np.kron(A,B)@CZ@np.kron(C,D)-U))<1e-12
    return selected

def all_physical(settings,t,tc,tp,phase,rng,fac):
    matrices={}
    generics=settings["generic_9mode"][0]
    fourier_design=settings["permutation_Fourier"][0]
    two_cz_design=settings["two_CZ_local"][0]
    products=settings["matched_12_product"][0]
    common=generics[:8]
    matrices["generic_9mode"]=[B.conj().T for B in common]
    matrices["permutation_Fourier"]=[B.conj().T for B in common]
    matrices["two_CZ_local"]=[B.conj().T for B in common]
    matrices["matched_12_product"]=[B.conj().T for B in common]
    counters={k:0 for k in matrices}
    for U in generics[8:]:
        K,n=qr_lossy(U,t,phase,rng)
        matrices["generic_9mode"].append(K);counters["generic_9mode"]+=n
    data=json.loads((Path(__file__).resolve().parents[1]/
               "data/w33_20261109_q8_perm_fourier_phases_27.json").read_text())
    for side,(p,ph,U) in enumerate(zip(
        [data["first_permutation"],data["second_permutation"]],
        data["programmed_diagonal_phase_masks"],fourier_design[8:])):
        X=LI if side==0 else IL
        # U=X D P L -> U†=L† P† D† X†
        # The full left product is ordered from final transfer to input.
        Kx,nx=(local_transfer(F3,np.eye(3),t,phase,rng)
               if side==0 else local_transfer(np.eye(3),F3,t,phase,rng))
        F=F3
        Kl,nl=local_transfer(F,F,t,phase,rng)
        Kp,ns=perm_transfer(p,tc)
        Kd=phase_transfer(ph,tp,phase,rng)
        K=Kl@Kp@Kd@Kx
        if t==tc==tp==1 and phase==0:
            assert np.max(abs(K-U.conj().T))<3e-12
        matrices["permutation_Fourier"].append(K)
        counters["permutation_Fourier"]+=nx+nl+ns
    for (A,B,C,D),U in zip(fac,two_cz_design[8:]):
        # U=CZ(A⊗B)CZ(C⊗D)
        Ka,na=local_transfer(A,B,t,phase,rng)
        Kc,nc=local_transfer(C,D,t,phase,rng)
        CZ=entangler()
        mask_left=math.sqrt(tp)*np.diag(np.exp(1j*rng.normal(0,phase,size=9)))@CZ.conj().T
        mask_right=math.sqrt(tp)*np.diag(np.exp(1j*rng.normal(0,phase,size=9)))@CZ.conj().T
        K=Kc@mask_left@Ka@mask_right
        if t==tc==tp==1 and phase==0:
            assert np.max(abs(K-U.conj().T))<3e-12
        matrices["two_CZ_local"].append(K)
        counters["two_CZ_local"]+=na+nc
    product,_=product_mub()
    for U3,U in zip(product,products[8:]):
        K,n=local_transfer(U3,U3,t,phase,rng)
        if t==tc==tp==1 and phase==0:assert np.max(abs(K-U.conj().T))<3e-12
        matrices["matched_12_product"].append(K)
        counters["matched_12_product"]+=n
    return matrices,counters

def fisher(Ks,rho,ops,h):
    F=np.zeros((80,80),float)
    minp=1
    p_surv=[]
    for K in Ks:
        A=np.einsum("ji,kil,jl->jk",K,ops,K.conj()).real
        p=np.diag(K@rho@K.conj().T).real
        lost=max(0.,1-sum(p))
        b=-A.sum(axis=0)
        if lost>1e-10:
            A=np.vstack([A,b]);p=np.r_[p,lost]
        assert min(p)>1e-14,(min(p),lost)
        F+=(A.T/p)@A
        p_surv.append(1-lost)
        minp=min(minp,min(p))
    F/=len(Ks)
    s=np.linalg.eigvalsh(F)
    assert min(s)>1e-9,min(s)
    vari=float(h@np.linalg.solve(F,h))
    return {"per_launch_CCNR_CRLB_coefficient":vari,
            "per_launch_Fisher_min_eigenvalue":float(min(s)),
            "mean_click_survival_fraction":float(np.mean(p_surv)),
            "min_click_outcome_prob":float(minp),
            "total_settings":len(Ks)}

def main(path=None):
    settings,ops=designs()
    fac=cz_factors()
    rho=horodecki_state(.236)
    r=realign(rho);u,_,vh=np.linalg.svd(r);W=u@vh
    h=np.array([float(np.vdot(W,realign(H)).real) for H in ops])
    cases={"ideal":(1.,1.,1.,0.),
      "moderate":(.995,.99,.999,.003),
      "harsh":(.98,.97,.995,.010)}
    outcases={}
    for name,(t,tc,tp,phase) in cases.items():
        reps=1 if name=="ideal" else 7
        result={k:[] for k in settings}
        counts=[]
        for j in range(reps):
            rng=np.random.default_rng(202611092500+j)
            Ks,ctr=all_physical(settings,t,tc,tp,phase,rng,fac)
            counts.append(ctr)
            for k in Ks:result[k].append(fisher(Ks[k],rho,ops,h))
        outcases[name]={}
        for key,arr in result.items():
            vals=[r["per_launch_CCNR_CRLB_coefficient"] for r in arr]
            outcases[name][key]={
              "replicates":len(vals),
              "mean_true_full_POVM_CCNR_CRLB":float(np.mean(vals)),
              "std_true_full_POVM_CCNR_CRLB":float(np.std(vals)),
              "min_and_max_true_full_POVM_CCNR_CRLB":[float(min(vals)),float(max(vals))],
              "mean_full_POVM_min_Fisher_eig":float(np.mean([q["per_launch_Fisher_min_eigenvalue"] for q in arr])),
              "mean_click_survival":float(np.mean([q["mean_click_survival_fraction"] for q in arr])),
              "average_programmed_two_mode_gates_and_crossings":float(np.mean([q[key] for q in counts]))}
    out={"status":"PASS_FOUR_STRUCTURED_TRUE_NONCOMMUTING_LOSS_POVM_FISHER",
      "benchmark_state":"Horodecki PPT a=0.236",
      "settings_compared":["generic_9mode","permutation_Fourier","two_CZ_local","matched_12_product"],
      "scenarios":{"ideal":{"gate_intensity":1,"cross_intensity":1,"mask_intensity":1,"rms_phase":0},
                   "moderate":{"gate_intensity":.995,"cross_intensity":.99,"mask_intensity":.999,"rms_phase":.003},
                   "harsh":{"gate_intensity":.98,"cross_intensity":.97,"mask_intensity":.995,"rms_phase":.01}},
      "full_POVM_results":outcases,
      "difference_from_prior_proxy":"Each stage is composed as a potentially nonunitary matrix K, with real mode-dependent transmission between noncommuting Givens, crossing SWAP and mask elements, and all nine clicks PLUS no-click FIM terms. The prior scalar-throughput test did not model these effects.",
      "scope":"Physically explicit toy circuits, not actual fabricated optical hardware. Stage decomposition, independent Gaussian phases and per-gate fixed intensity assumptions are synthetic, and the Bell eight bases are lossless controls. Full POVMs assumed known; no finite calibration uncertainty, source drift, mode-dependent detector error or certification power is included. CRLB is asymptotic at one fixed state."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("FULL_LOSS_FISHER",json.dumps({k:{u:round(v["mean_true_full_POVM_CCNR_CRLB"],4) for u,v in x.items()}
      for k,x in outcases.items()}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
