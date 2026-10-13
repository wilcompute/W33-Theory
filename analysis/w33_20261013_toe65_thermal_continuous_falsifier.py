"""TOE65 front1: independent continuous U(1)^3 thermal free-energy falsifier.

Full 80x80 native Hermitian hopping matrix: multi-temperature Sobol search,
independently optimized at finite beta and zero temperature. NUMERICAL only.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.optimize import minimize
from scipy.stats import qmc
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,v,*_=prep();ed=np.asarray(ed,dtype=int);v=np.asarray(v,dtype=int)
assert ed.shape==(160,2) and v.shape==(160,3)
PI=np.ones(3)*np.pi

def thermo(theta,beta,weights=None):
    if weights is None:weights=np.ones(len(ed))
    p=weights*np.exp(1j*v@np.asarray(theta))
    H=np.zeros((80,80),complex)
    H[ed[:,0],ed[:,1]]=-p
    H[ed[:,1],ed[:,0]]=-p.conjugate()
    e=np.linalg.eigvalsh(H)
    if beta is None:
        return -float(np.sum(abs(e)))/2
    return float(-np.sum(np.logaddexp(beta*e/2,-beta*e/2))/beta)

def certificate():
    beta_cases=(.25,.5,2.,8.,None)
    sampler=qmc.Sobol(d=3,scramble=True,seed=6513)
    phases=2*np.pi*sampler.random_base2(8)
    # Compare the exact three-pi flux to the entire 256-point space-filling
    # sample and to independent optimization from 8 distinct seed phases.
    rows=[]
    for beta in beta_cases:
        fpi=thermo(PI,beta)
        fzero=thermo(np.zeros(3),beta)
        differences=[thermo(theta,beta)-fpi for theta in phases]
        lowest_index=int(np.argmin(differences))
        starts=[PI,np.zeros(3)]+list(phases[:6])
        minimizers=[]
        for start in starts:
            q=minimize(lambda t: thermo(t,beta),start,
                       method="BFGS",options={"gtol":2e-6,"maxiter":130})
            minimizers.append({"free_energy_diff_from_pi":float(q.fun-fpi),
                              "angles":((q.x+np.pi)%(2*np.pi)-np.pi).tolist(),
                              "converged":bool(q.success)})
        # Equalities only near modulo 2pi π are possible candidates.
        rows.append({"beta":str(beta),"Fpi":fpi,"Fzero":fzero,
            "pi_minus_zero":fpi-fzero,"sobol_points":len(phases),
            "smallest_sobol_gap":float(min(differences)),
            "best_sobol_angles":phases[lowest_index].tolist(),
            "best_minimizer_gap":float(min(m["free_energy_diff_from_pi"] for m in minimizers)),
            "optimizations":minimizers})
        print("TOE65 THERMAL",beta,"pi-minus-zero",fpi-fzero,
              "minSample",min(differences),"optmin",min(m["free_energy_diff_from_pi"] for m in minimizers),flush=True)
    assert all(r["smallest_sobol_gap"]>-1e-8 for r in rows)
    assert all(r["best_minimizer_gap"]>-1e-7 for r in rows)
    # Check complex-conjugate symmetry under theta --> -theta.
    for beta in beta_cases:
        for theta in phases[:8]:
            assert abs(thermo(theta,beta)-thermo(-theta,beta))<1e-10
    return {"status":"PASS_TOE65_NUMERIC_ALL_BETA_CONTINUOUS_FLUX_FALSIFIER",
            "native_sites":80,"native_edges":160,"phase_dimensions":3,
            "boltzmann_beta_cases":rows,
            "conjugation_check_samples":len(beta_cases)*8,
            "scope":"Finite numerical grid and local optimizations, not an analytic all-beta global U(1)^3 theorem; no gauge-field dynamics, full W33 interactions, CP breaking or measured physical constants."}
if __name__=="__main__":
    obj=certificate()
    (ROOT/"data/w33_20261013_toe65_thermal_continuous_falsifier.json").write_text(json.dumps(obj,indent=2)+"\n")
