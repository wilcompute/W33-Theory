#!/usr/bin/env python3
"""Single-photon spatial Bell test: displaced on/off POVMs with realistic loss.

Unlike hypothetical perfect local sigma_X/Y, a displacement+on/off
detector implements a nonprojective observable, with calibrated
efficiency, dark counts and LO phase. Numerically maximize 4
complex displacements and compare to CHSH=2 under *all-trial* scoring.
Not a real Bell experiment; no spacelike hardware was measured.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution

def no_click(alpha,eta,dark):
    # Exact |0>,|1> block for D(alpha) followed by no-click on/off
    # with Bernoulli efficiency eta and independent Poisson dark events
    pref=np.exp(-eta*abs(alpha)**2-dark)
    return pref*np.array([[1,-eta*alpha.conjugate()],
                          [-eta*alpha,1-eta+(eta*abs(alpha))**2]],complex)

def observable(alpha,eta,dark):
    E=no_click(alpha,eta,dark)
    assert min(np.linalg.eigvalsh(E))>-1e-10
    assert max(np.linalg.eigvalsh(E))<1+1e-10
    return 2*E-np.eye(2)

def rho(source,coh):
    # Global source loss to vacuum, then relative dephasing of path
    x=np.zeros((4,4),complex)
    x[0,0]=1-source
    x[1,1]=x[2,2]=source/2
    x[1,2]=x[2,1]=source*coh/2
    return x

def corr(A,B,source,coh):
    a,b=A[0,0].real,A[1,1].real
    c=A[0,1]
    x,y=B[0,0].real,B[1,1].real
    z=B[0,1]
    return float((1-source)*a*x+(source/2)*(a*y+b*x+
                  2*coh*np.real(c*np.conj(z))))

def CHSH(z,det,src,coh,dark):
    aa=[z[0]+1j*z[1],z[2]+1j*z[3]]
    bb=[z[4]+1j*z[5],z[6]+1j*z[7]]
    As=[observable(a,det,dark) for a in aa]
    Bs=[observable(b,det,dark) for b in bb]
    v=[corr(As[x],Bs[y],src,coh) for x,y in ((0,0),(0,1),(1,0),(1,1))]
    return v[0]+v[1]+v[2]-v[3],v

def optimize(det,src,coh,dark,seed=202611091,maxiter=120):
    bounds=[(-1.4,1.4)]*8
    def obj(z):
        val,_=CHSH(z,det,src,coh,dark)
        return -abs(val)
    r=differential_evolution(obj,bounds,seed=seed,tol=.0001,
       maxiter=maxiter,popsize=9,polish=True,updating="immediate",workers=1)
    val,corrs=CHSH(r.x,det,src,coh,dark)
    return {"CHSH":float(abs(val)),"signed_CHSH":float(val),"correlations":corrs,
       "displacements_real_imag":r.x.tolist(),
       "mean_displaced_photons_per_local_setting":[float(abs(r.x[2*j]+1j*r.x[2*j+1])**2) for j in range(4)],
       "optimizer_objective":float(r.fun),
       "converged":bool(r.success)}

def joint_probs(z,settings,det,source,coh,dark):
    rho0=rho(source,coh)
    a,b=z[2*settings[0]]+1j*z[2*settings[0]+1],z[4+2*settings[1]]+1j*z[5+2*settings[1]]
    E=no_click(a,det,dark);F=no_click(b,det,dark)
    I=np.eye(2)
    AB=[E,I-E];BB=[F,I-F]
    probs=np.array([np.trace(rho0@np.kron(AB[i],BB[j])).real
              for i in range(2) for j in range(2)])
    assert abs(sum(probs)-1)<1e-11
    assert min(probs)>-1e-11
    return np.clip(probs,0,1)/sum(np.clip(probs,0,1))

def iid_score(settings,N,det,src,coh,dark,seed):
    rng=np.random.default_rng(seed)
    probs={(x,y):joint_probs(settings["displacements_real_imag"],(x,y),det,src,coh,dark)
           for x in range(2) for y in range(2)}
    xs=rng.integers(0,2,size=N)
    ys=rng.integers(0,2,size=N)
    scores=np.empty(N)
    for x in range(2):
        for y in range(2):
            where=np.where((xs==x)&(ys==y))[0]
            outcomes=rng.choice(4,size=len(where),p=probs[x,y])
            ab=np.where((outcomes==0)|(outcomes==3),1.,-1.)
            scores[where]=4*((-1)**(x*y))*ab
    orientation=np.sign(settings["signed_CHSH"])
    point=float(np.mean(orientation*scores))
    eps=math.sqrt(32*math.log(20)/N)
    return {"trials":N,"observed_all_trials_CHSH":point,
            "one_sided_95pct_Hoeffding_halfwidth":eps,
            "confidence_lower":point-eps,
            "certificate_passes_no_postselection":bool(point-eps>2),
            "detector_model":"on/off with dark events: four joint outcomes including both no-click"}
def main(path=None):
    # Cases distinguish perfect ideal, high/low real detector efficiency,
    # local reference coherence and global source loss.
    cases=[
        ("ideal",1.,1.,1.,0.),
        ("high_eff",.95,1.,1.,1e-5),
        ("realistic_2026_telecom_proxy",.86,1.,.92,1e-4),
        ("source_and_detector_loss",.86,.9,.95,1e-4),
        ("phase_randomized",.95,1.,0.,1e-5)]
    outcases={}
    for j,(name,eta,src,coh,dark) in enumerate(cases):
        fit=optimize(eta,src,coh,dark,2026110920+j,maxiter=95)
        outcases[name]={"detector_efficiency":eta,
            "global_source_survival":src,
            "relative_phase_or_mode_coherence":coh,
            "mean_dark_counts_per_trial":dark,
            **fit}
    # Standard local settings optimization can only ever reach 2 if the
    # relative-path coherence is completely lost (separable mixture).
    print("OPT_ABS_CHSH", {k:round(v["CHSH"],6) for k,v in outcases.items()},flush=True)
    assert outcases["ideal"]["CHSH"]>2.3
    assert outcases["phase_randomized"]["CHSH"]<=2+1e-8
    # 2026 practical overlap was NOT measured by our source; numerical
    # placeholders intentionally reveal whether a violation is robust.
    iid=iid_score(outcases["ideal"],150000,1.,1.,1.,0.,2026110937)
    assert iid["certificate_passes_no_postselection"]
    low=iid_score(outcases["phase_randomized"],150000,.95,1.,0.,1e-5,2026110938)
    assert not low["certificate_passes_no_postselection"]
    # A coherent displacement of amplitude alpha requires a phase
    # reference, with at least |alpha|² photons in the displaced mode;
    # actual LO pre-split photon budget is ~|alpha|²/R for reflectivity R.
    R=.01
    out={"status":"PASS_SINGLE_PHOTON_DISPLACEMENT_ONOFF_DETECTOR_LOSS_CHSH",
      "povm_formula":"E_no_click=exp(-dark-eta|alpha|²)*[[1,-eta alpha*],[-eta alpha,1-eta+eta²|alpha|²]] on local Fock span{|0>,|1>}, O=2E-I",
      "source_model":"rho=(1-src)|00><00|+src/2(|01><01|+|10><10|+coh(|01><10|+h.c.))",
      "optimized_cases":outcases,
      "one_realized_all_trial_ideal_case":iid,
      "phase_randomized_negative_control":low,
      "reference_beamsplitter_reflectivity_toy":R,
      "minimum_local_oscillator_mean_photons_for_displacement_at_each_setting":{
          name:[float(n/R) for n in dat["mean_displaced_photons_per_local_setting"]]
                for name,dat in outcases.items()},
      "literature_and_scope":["https://arxiv.org/abs/2607.29012",
         "https://doi.org/10.1103/PhysRevA.88.012111",
         "https://dakic.univie.ac.at/details/news/testing-single-photon-entanglement-using-self-referential-measurements/"],
      "caveats":"Numerical optimizers are locally validated only; no global CHSH optimum theorem. Phase coherence lumps source and LO mode overlap. Detector efficiency is *local* on/off detection, src is independent source loss. No event-ready heralding implementation, independently calibrated time windows, causal spacelike device, measured dark counts or finite local-oscillator technical noise. No laboratory Bell claim."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("ONOFF_BELL",json.dumps({
      "CHSH":{k:round(v["CHSH"],5) for k,v in outcases.items()},
      "ideal_all_trial_lower95":iid["confidence_lower"],
      "phase_random_lower":low["confidence_lower"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
