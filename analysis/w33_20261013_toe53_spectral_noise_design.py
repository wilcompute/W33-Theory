"""TOE53: whitened non-redundant finite-Bloch spectral design.

A proxy statistical model; not measured shot noise or physical bandwidth.
"""
import json,runpy,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
p=runpy.run_path(str(R/"analysis/w33_20261013_toe50_inverse_acoustic_spectral_trace.py"))
w=p["w"]; P0=p["P"]; J=p["J"]; E=p["ed"]; V=p["volts"]; L=p["lookup"]; B=p["zero"]+p["comm"]; row=p["cycle_row"]
# Real positive W, 3D Bloch momentum candidates (not just opposite pairs).
base=[(0.,0.,0.),(.83,0.,0.),(0.,.91,0.),(0.,0.,1.01)]
candidates=base[1:]+[(0.37,0.29,0.14),(0.49,0.20,0.55),(.73,.61,.16),
(.18,.79,.62),(.41,.44,.47),(.95,.29,.69),(.32,.91,.52),(.71,.17,1.03),
(.13,.23,.97),(.88,.86,.81),(.27,1.06,.43),(.52,.77,.96)]
W_inv=1/np.sqrt(w)
def moments(k):
 P=P0 if k==base[0] else np.asarray([row(z,E,V,L,np.array(k)) for z in B])
 H=(P.conj().T@P)*W_inv[:,None]*W_inv[None,:]
 powers=[];g=[];T=[];M=H.copy()
 for n in (1,2,3):
  if n>1:M=M@H
  val=float(np.trace(M).real)
  assert val>0
  powers.append(val)
  g.append((-n*M.diagonal().real/w)/val)
 return np.asarray(g),powers
G=np.asarray(J)/.5
fixed,m0=moments(base[0])
store={k:moments(k) for k in candidates}
# Equal % noise for each moment and 0.5-normalized acoustic entries,
# normalized gradient row for the geometric rank conditioning metric.
def stack(sel):
 return np.vstack([G,fixed]+[store[k][0] for k in sel])
def condition(D):
 L=D/np.linalg.norm(D,axis=1)[:,None]
 lam=np.linalg.eigvalsh(L@L.T)
 return float(np.sqrt(max(lam[0],0))),float(np.sqrt(max(lam[-1],0))),int(sum(lam>lam[-1]*1e-8))
original=condition(stack(base[1:]))
best=None
for choice in itertools.combinations(candidates,3):
 score=condition(stack(choice))
 if best is None or score[0]>best[0][0]:
  best=(score,choice)
assert best[0][0]>=original[0]-1e-12
selected=stack(best[1])
# noise oracle: 3 known link locations and their small perturbations;
# this does not solve sparsity or unknown-support identification.
support=[5,34,113]
D=selected[:,support]
sv=np.linalg.svd(D,compute_uv=False)
delta=np.array([.04,-.03,.05])
rng=np.random.default_rng(534)
outcomes=[]
for sigma in [.0001,.001,.005]:
 errs=[]
 for _ in range(300):
  obs=D@delta+rng.normal(0,sigma,len(D))
  fit=np.linalg.lstsq(D,obs,rcond=None)[0]
  errs.append(float(np.linalg.norm(fit-delta)))
 exact_cov=sigma**2*np.linalg.inv(D.T@D)
 outcomes.append({"relative_moment_noise_sigma":sigma,
   "oracle_known_3link_L2_error_mean_300":float(np.mean(errs)),
   "oracle_known_3link_L2_error_rms_300":float(np.sqrt(np.mean(np.square(errs)))),
   "expected_oracle_L2_error_rms":float(np.sqrt(np.trace(exact_cov)))})
certificate={"status":"PASS_WHITENED_NONOPPOSITE_BLOCH_SPECTRAL_DESIGN",
"positive_weights":len(w),"candidate_k_count":len(candidates),
"n_three_k_designs_evaluated":len(list(itertools.combinations(candidates,3))),
"whitened_model":"Each spectral moment T_n receives independent noise σ*T_n; six leading metric entries noise σ*.5. Physical photon/sample variance not derived.",
"original_three_nonzero_k":[list(k) for k in base[1:]],
"original_row_normalized_smallest_sv":original[0],
"selected_three_nonzero_k":[list(k) for k in best[1]],
"optimized_row_normalized_smallest_sv":best[0][0],
"improvement_factor":best[0][0]/max(original[0],1e-20),
"original_relative_rank_1e_minus4":original[2],
"optimized_relative_rank_1e_minus4":best[0][2],
"assumed_3known_weight_support":support,
"restricted_support_smallest_whitened_sv":float(min(sv)),
"oracle_3link_inversion_with_gaussian_measurement_noise":outcomes,
"limitations":"Finite Bloch trace moments, not a calibrated device. The operator gradients are exact finite-model derivatives, but scale-proxy noise is assumed, the 3 defect locations are given to the estimator, and all 160 weights remain underdetermined. Covariance assumes independent equal fractional errors; optimality only within the finite enumerated candidate pool."}
(R/"data/w33_20261013_toe53_spectral_noise_design.json").write_text(json.dumps(certificate,indent=2)+"\n")
print(json.dumps({"status":certificate["status"],"orig":original,"best":best,"oracle":outcomes}))
