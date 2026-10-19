"""Full correlated 19-outcome shot covariance for 36-setting complex
W33 trace tomography, propagated through W=R^-1 S analytically.
Compare with photon-count multinomial Monte Carlo.
"""
from __future__ import annotations
import json,numpy as np
from pathlib import Path
from w33_20261019_round9_photon_tomography_shots import Uref,echo,transfer,probabilities,shot_tomography
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round11_photon_covariance.json"
rng=np.random.default_rng(113119)
def analytic_cov(W,R,S,n):
    inv=np.linalg.inv(R)
    total=0.0
    terms=[]
    for target,T in (("R",R),("S",S)):
        # δd=+1/9 ReTr(W R^-1 δR) -1/9 ReTr(R^-1 δS)
        G=(W@inv if target=="R" else -inv)/9
        for j in range(9):
            for axis,phi in enumerate((0.,np.pi/2)):
                p=probabilities(T,j,phi)
                dk=p[:9]-p[9:18]
                cov=(np.diag(p[:9]+p[9:18])-np.outer(dk,dk))/n
                factor=1 if axis==0 else -1j
                coef=np.real(G[j,:]*factor/np.conj(Uref[:,j]))
                variance=float(coef@cov@coef)
                assert variance>=-1e-15
                total+=variance
                terms.append({"condition":target,"input":j,"phase":phi,"contribution_to_deficit_variance":variance})
    return total,terms
def measure(T,n,local):
    obs=np.zeros((9,9,2))
    for j in range(9):
        for k,phi in enumerate((0,np.pi/2)):
            p=probabilities(T,j,phi)
            c=local.multinomial(n,p)
            obs[:,j,k]=(c[:9]-c[9:18])/n
    return (obs[:,:,0]-1j*obs[:,:,1])/Uref.conj()
def run():
    M=transfer(.16);W=echo();R=M;S=M@W
    ideal=float(1-np.trace(W).real/9)
    groups=[]
    for n in (5000,20000,80000):
        var,terms=analytic_cov(W,R,S,n)
        shots=[]
        for _ in range(130):
            rr=measure(R,n,rng);ss=measure(S,n,rng)
            est=np.linalg.solve(rr,ss)
            shots.append(float(1-np.trace(est).real/9))
        arr=np.array(shots)
        groups.append({"N_per_setting":n,"total_input_photons":36*n,
             "delta_method_sigma":float(np.sqrt(var)),
             "MonteCarlo_sigma":float(np.std(arr,ddof=1)),
             "MonteCarlo_mean":float(np.mean(arr)),
             "delta_method_vs_sample_std_ratio":float(np.sqrt(var)/np.std(arr,ddof=1)),
             "MonteCarlo_bias":float(np.mean(arr)-ideal),
             "variance_detailed_36_settings":terms if n==20000 else None})
    checks={"all_36_setting_covariance_terms":len(groups[1]["variance_detailed_36_settings"])==36,
      "delta_method_variance_scales_exactly_1_over_N":abs(groups[0]["delta_method_sigma"]/groups[1]["delta_method_sigma"]-2)<1e-12 and abs(groups[1]["delta_method_sigma"]/groups[2]["delta_method_sigma"]-2)<1e-12,
      "MonteCarlo_matches_correlated_covariance_within_25pct":all(.75<x["delta_method_vs_sample_std_ratio"]<1.25 for x in groups),
      "MonteCarlo_low_bias":all(abs(x["MonteCarlo_bias"])<.01 for x in groups),
      "ideal_deficit_8_over_27":abs(ideal-8/27)<1e-12}
    out={"schema":"w33.round11.full_multinomial_delta_method_tomography_covariance.v1",
     "formula":"D_k=(N_+k-N_-k)/N. For each phase/input, Cov(D_k,D_l)=[(p_+k+p_-k)delta_kl - D_k D_l]/N, INCLUDING anti-correlations between simultaneous output-mode counts. Transfer entries T_kj=(D0_kj-i D90_kj)/conj(Uref_kj). With W=R^-1 S, first-order δW=R^-1(δS-δR W); δ(trace deficit)=-ReTr δW/9. Sum all 36 setting contributions using exact Jacobian and multinomial covariances.",
     "ideal_trace_deficit":ideal,"settings_per_run":36,"tested":groups,
     "scope":"This is leading-order covariance of an unbiased transfer inversion under a known ideal Fourier reference, independent photon multinomial outcomes and STATIONARY lossy/crosstalk R, S. Finite-count nonlinear inversion bias, correlated drift, readout detector darks and non-Poisson photon source are not included. No actual device or detector measured.",
     "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"sigma":[x["delta_method_sigma"] for x in groups],"ratio":[x["delta_method_vs_sample_std_ratio"] for x in groups]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
