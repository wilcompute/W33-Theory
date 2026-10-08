"""Experiment-facing 27-port Trotter coupler calibration sensitivity simulation.

Plausible but user-chosen phase disorder, port efficiency mismatches.
Exact unitarity checked. Sampled perturbations do not certify robustness
outside sampled devices. Surrogate unitary model is NOT an optical chip.
"""
import sys,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_photon_likelihood_information import design,unitary
OUT=ROOT/"data/w33_20261008_photon_calibrated_coupler_mc.json"
def imperfect(layers,r,seed,sigma,efferr):
 rng=np.random.default_rng(seed)
 u=np.eye(27,dtype=complex);t=.78;theta=t/r
 for step in range(r):
  for matching in layers:
   m=np.eye(27,dtype=complex)
   for i,j in matching:
    phase=float(theta+rng.normal(0,sigma))
    co=np.cos(phase);si=np.sin(phase)
    m[i,i]=co;m[j,j]=co;m[i,j]=-1j*si;m[j,i]=-1j*si
   u=m@u
 assert np.max(np.abs(u.conj().T@u-np.eye(27)))<3e-12
 p=np.abs(u)**2
 efficiency=1+rng.uniform(-efferr,efferr,size=27)
 p=p*efficiency[:,None]
 p=p/p.sum(axis=0)
 assert np.max(np.abs(p.sum(axis=0)-1))<1e-12
 return p
def margin(a,b):
 return min(float(np.max(np.abs(x-y))) for x in a.T for y in b.T)
def main():
 g=build_graphs()
 records=[]
 for reps in (4,8,16):
  nominal={k:np.sort(np.abs(unitary(a,design[k]["nine_layer_schedule"],.78,reps))**2,axis=0)
   for k,a in g.items()}
  names=sorted(g)
  baseline=margin(nominal[names[0]],nominal[names[1]])
  for sigma,deterr in ((0,0),(.0001,.002),(.0005,.005),(.001,.01)):
   empirical=[]
   for seed in range(12):
    pert={k:np.sort(imperfect(design[k]["nine_layer_schedule"],reps,seed+1000*(j+1)+173*reps,sigma,deterr),axis=0)
      for j,k in enumerate(names)}
    # Sampled separation is the nearest pair of sorted source distributions
    mi=margin(pert[names[0]],pert[names[1]])
    drift=max(float(np.max(np.abs(pert[k]-nominal[k]))) for k in names)
    empirical.append({"seed":seed,"perturbed_model_separation":mi,"maximum_template_drift_vs_nominal":drift})
   records.append({"stages":9*reps,"phase_noise_std_rad_per_coupler":sigma,
     "final_detector_efficiency_max_fractional_error":deterr,
     "nominal_sorted_min_margin":baseline,
     "sampled_min_calibrated_margin":min(s["perturbed_model_separation"] for s in empirical),
     "sampled_max_template_drift":max(s["maximum_template_drift_vs_nominal"] for s in empirical),
     "sampled_unconditioned_nominal_margin_minus_twice_max_drift":baseline-2*max(s["maximum_template_drift_vs_nominal"] for s in empirical),
     "calibration_samples":empirical})
 return {"random_seed_policy":"independent reproducible numpy PCG64 per hypothesis and per depth",
   "couplers":"two-mode reciprocal 27x27 unitary with normal-distributed phase perturbations; nine nonoverlapping matching layers per Trotter repetition",
   "detectors":"random uniform efficiency from 1-r to 1+r then renormalize conditional successes",
   "samples_per_scenario":12,"scenarios":records,
   "no_physical_device_measurements":True,
   "no_worst_case_guarantee_from_monte_carlo":True,
   "quantitative_error_bounds_use_prior_analytic_telescope_guard":True}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 for r in x["scenarios"]:
  print(r["stages"],r["phase_noise_std_rad_per_coupler"],r["final_detector_efficiency_max_fractional_error"],
    round(r["sampled_min_calibrated_margin"],6),round(r["sampled_max_template_drift"],6),flush=True)
 print("PHOTON_COHERENT_UNITARY_MC_PASS")
