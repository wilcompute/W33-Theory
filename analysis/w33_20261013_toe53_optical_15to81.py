"""TOE53: native 15-to-81 real optical Givens decomposition and error budget.

This is a mathematical triangular linear-optics network, NOT a fabricated chip.
"""
from pathlib import Path
import numpy as np,runpy,json
R=Path(__file__).resolve().parents[1]
p=runpy.run_path(str(R/"analysis/w33_20261013_toe52_h27_bridge.py"))
val,U=np.linalg.eigh(p["P15"]);Q=U[:,val>.5]
W=p["reyn"][:81].astype(float)@Q
ev,V=np.linalg.eigh(W.T@W)
assert min(ev)>0
F=W@(V@np.diag(ev**-.5)@V.T)
assert np.max(abs(F.T@F-np.eye(15)))<2e-12
X=F.copy()
rot=[]
for col in range(15):
 for row in range(80,col,-1):
  a,b=float(X[row-1,col]),float(X[row,col])
  r=np.hypot(a,b)
  if r<1e-12:continue
  c,s=a/r,b/r
  old=X[row-1].copy();other=X[row].copy()
  X[row-1]=c*old+s*other
  X[row]=-s*old+c*other
  rot.append((row-1,row,float(np.arctan2(s,c))))
# Near identity diagonal signs, no other upper-triangular terms.
expected=np.zeros((81,15));diag=np.sign(np.diag(X[:15]))
expected[:15]=np.diag(diag)
res=float(np.max(abs(X-expected)))
assert res<1e-11,res
def restore(angular=0,loss_db=0,rng=None):
 z=expected.astype(float).copy()
 loss_amp=10**(-loss_db/20)
 for i,j,ang in reversed(rot):
  theta=ang+(rng.normal(0,angular) if rng is not None else 0.)
  co,si=np.cos(theta),np.sin(theta)
  a=z[i].copy();b=z[j].copy()
  z[i]=loss_amp*(co*a-si*b)
  z[j]=loss_amp*(si*a+co*b)
 return z
recreated=restore()
err=float(np.max(abs(F-recreated)))
assert err<3e-12,err
# Characterize loss from all beam splitters having an independent
# phenomenological amplitude transmittance, not measured device spec.
loss=[]
for dB in [0,.005,.01,.02,.05]:
 Y=restore(loss_db=dB)
 tr=np.linalg.norm(Y,axis=0)**2
 fidelity=np.abs(np.diag(F.T@Y))**2 / np.maximum(tr,1e-15)
 loss.append({"loss_db_per_2mode_operation":dB,
  "min_transmission":float(min(tr)),"mean_transmission":float(np.mean(tr)),
  "max_transmission":float(max(tr)),
  "min_mode_conditional_overlap":float(min(fidelity)),
  "max_orthonormality_error":float(max(abs(Y.T@Y-np.eye(15)).ravel()))})
rng=np.random.default_rng(5315)
phase=[]
for sigma in [0,.001,.003,.01]:
 overlaps=[]
 for _ in range(24):
  noisy=restore(angular=sigma,rng=rng)
  overlaps.append(float(np.mean(abs(np.diag(F.T@noisy))**2)))
 phase.append({"rms_Givens_angle_error_rad":sigma,
   "mean_target_column_overlap_24trials":float(np.mean(overlaps)),
   "sd_target_column_overlap_24trials":float(np.std(overlaps))})
cert={"status":"PASS_REAL_15_TO_81_TRIANGULAR_LINEAR_OPTICS_QR_COMPILER",
"source":"TOE52 integer Reynolds H27 spread15-to-K81 81D polar isometry",
"input_dimension":15,"output_modes":81,
"nontrivial_adjacent_two_mode_Givens_rotations":len(rot),
"universal_81x81_Clements_or_Reck_2mode_slot_count":81*80//2,
"triangular_partial_QR_slot_upper_bound":sum(80-j for j in range(15)),
"diagonal_pi_phase_flips":int(np.sum(diag<0)),
"exact_matrix_reconstruction_max_element_error":err,
"max_QR_elimination_residual":res,
"simulated_equal_per_Givens_attenuation_scenarios":loss,
"independent_Gaussian_Givens_phase_or_angle_noise":phase,
"specification":"Each elementary real Givens rotation corresponds to a tunable two-mode interference operation. Diagonal signs are π phases. To implement on 81 physical modes the network must route modes, calibrate couplers and account for propagation, insertion and detection loss.",
"prior_art":"Reck et al PRL73 58 (1994) and Clements et al Optica3 1460 (2016), DOI 10.1364/OPTICA.3.001460; triangular mesh here, not claimed loss-optimal Clements layout.",
"physical_scope":"A deterministic 81-mode partial orthogonal isometry with illustrative per-operation loss and Gaussian angle noise. No experimentally specified coupler, photon source, FI-clock implementation, fault-tolerant magic-state injection or fabricated photonic Holonet."}
(R/"data/w33_20261013_toe53_optical_15to81_compilation.json").write_text(json.dumps(cert,indent=2)+"\n")
print(json.dumps({"status":cert["status"],"rotations":len(rot),"error":err,"loss":loss,"phase":phase}))
