"""TOE51 front 1: higher Bloch spectral moments and local inverse rank."""
from pathlib import Path
import sys,json
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261013_toe50_inverse_acoustic_spectral_trace import B,P,w,J,ed,volts,lookup,zero,comm,cycle_row
points=[(0.,0.,0.),(.83,0.,0.),(0.,.91,0.),(0.,0.,1.01)]
columns=[]
frames=[]
D=1/np.sqrt(w)
for k in points:
 Z=P if k==points[0] else np.array([cycle_row(z,ed,volts,lookup,np.array(k)) for z in zero+comm])
 H=(Z.conj().T@Z)*D[:,None]*D[None,:]
 assert max(abs(H-H.conj().T).ravel())<1e-10
 Hpower=np.eye(160,dtype=complex)
 for n in (1,2,3):
  Hpower=Hpower@H
  moments=float(np.trace(Hpower).real)
  grad=-n*Hpower.diagonal().real/w
  assert np.isfinite(grad).all() and np.linalg.norm(grad)>0
  columns.append(grad)
  frames.append(dict(k=list(k),moment_order=n,trace=moments,gradient_norm=float(np.linalg.norm(grad))))
gradients=np.vstack([J]+columns)
normalized=gradients/np.linalg.norm(gradients,axis=1)[:,None]
singular=np.linalg.svd(normalized,compute_uv=False)
rank=int(sum(singular>singular[0]*1e-8))
acoustic_rank=int(np.linalg.matrix_rank(J,tol=1e-8))
assert acoustic_rank==6
assert rank>acoustic_rank,(rank,singular)
# Gradient finite difference on selected coordinates at nonzero k.
k=(.83,0.,0.)
Z=np.array([cycle_row(z,ed,volts,lookup,np.array(k)) for z in zero+comm])
K=Z.conj().T@Z
chosen=[5,34,113]
checks=[]
for n in (1,2,3):
 for e in chosen:
  def tr(wt):
   dd=1/np.sqrt(wt)
   H=(K*dd[:,None])*dd[None,:]
   return float(np.trace(np.linalg.matrix_power(H,n)).real)
  dw=1e-4
  wp=w.copy();wm=w.copy();wp[e]+=dw;wm[e]-=dw
  empirical=(tr(wp)-tr(wm))/(2*dw)
  g=columns[3+n-1][e]
  rel=abs(empirical-g)/max(1,abs(g))
  checks.append(dict(moment=n,edge=e,analytic=float(g),finite_difference=float(empirical),relative_error=float(rel)))
assert max(q["relative_error"] for q in checks)<1e-5
out=dict(status="PASS",front="higher_Bloch_spectral_moment_inverse_rank",
 model="Fixed TOE38 160-link Maxwell graph at TOE50 positive isotropic weight center.",
 acoustic_rank=acoustic_rank,
 spectral_moment_count=len(frames),
 n_observables=int(gradients.shape[0]),
 joint_local_gradient_rank_1e_minus8=rank,
 singular_values_normalized_rows=singular.tolist(),
 rank_by_relative_SVD_tolerance={str(t):int(sum(singular>singular[0]*t)) for t in (1e-3,1e-4,1e-5,1e-6,1e-8)},
 normalized_observable_condition_number=float(singular[0]/singular[-1]),
 moment_data=frames,
 derivative_n="d Tr[(W^-1/2 K(k) W^-1/2)^n] / dw_e = -n [M(k)^n]_ee / w_e",
 finite_difference_checks=checks,
 max_relative_check_error=max(q["relative_error"] for q in checks),
 nullity_after_local_linear_probes=160-rank,
 qualification="Ranks are floating-point local Jacobian counts at selected isotropic root, not exact full-rank theorem nor actual independent noisy spectroscopy. Bloch momentum directions, magnetic tensor and all 160 w are supplied. Further gauge equivalence and measurement costs remain open.")
(R/"data/w33_20261013_toe51_spectral_moment_rank.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ("status","acoustic_rank","spectral_moment_count","joint_local_gradient_rank_1e_minus8","nullity_after_local_linear_probes","max_relative_check_error")}))
