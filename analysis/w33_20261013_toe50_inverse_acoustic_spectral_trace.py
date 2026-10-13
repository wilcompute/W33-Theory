"""TOE50: a higher-band spectral moment resolves leading-cone flat directions.

W33 native 160-link Maxwell model: the six acoustic Gram components G(w)
have rank six Jacobian, but the trace of all Bloch k=0 nonzero generalized
magnetic eigenvalues may vary along the 154D G-level set. This calculates
a nonzero transverse derivative and two finite positive exactly-G-matched
weight sets. This is inverse homogenization, not gravity.
"""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import root
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_pass11956_local_electric_metric import prep,cycle_row,gradient
C=json.loads((R/"data/w33_pass11956_local_electric_metric.json").read_text())
w=np.array([float(x.split('/')[0])/float(x.split('/')[1]) if '/' in x else float(x) for x in C["electric_link_weights"]])
assert len(w)==160
ed,volts,lookup,zero,comm,*_=prep()
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(int)[:,1:]
P=np.array([cycle_row(z,ed,volts,lookup,np.zeros(3)) for z in zero+comm])
assert P.shape[1]==160
Kdiag=np.sum(abs(P)**2,axis=0).real
pairs=[(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
def gram(w):
 h=volts-B@np.linalg.solve(B.T@(w[:,None]*B),B.T@(w[:,None]*volts))
 return h.T@(w[:,None]*h),h
G,H=gram(w)
J=np.array([H[:,i]*H[:,j] for i,j in pairs])
assert np.linalg.matrix_rank(J,tol=1e-8)==6
gtrace=-Kdiag/(w*w)
normal=gtrace-J.T@np.linalg.solve(J@J.T,J@gtrace)
assert np.linalg.norm(J@normal)<1e-7
normal/=np.linalg.norm(normal)
base_T=float(np.sum(Kdiag/w))
slope=float(gtrace@normal)
rel_slope=float(slope/base_T)
assert abs(slope)>1e-5,(slope,rel_slope)
Gtarget=np.array([.5,.5,.5,0.,0.,0.])
def g6(w):
 GG,_=gram(w)
 return np.array([GG[i,j] for i,j in pairs])
assert np.max(abs(g6(w)-Gtarget))<5e-11
free=C["free_weight_indices"];free=np.asarray(free,dtype=int)
trials=[]
for t in [-.03,-.015,0.,.015,.03]:
 wt=w+t*normal
 if t:
  def corrected(x):
   ww=wt.copy();ww[free]=x
   return g6(ww)-Gtarget
  r=root(corrected,wt[free],tol=1e-11)
  assert r.success or np.linalg.norm(r.fun)<1e-11,r.message
  wt[free]=r.x
 assert np.min(wt)>.125
 residual=float(np.max(abs(g6(wt)-Gtarget)))
 assert residual<1e-11,(t,residual)
 # Sum of all finite generalized eigenvalues λ of K u = λ W u.
 # Similarity: trace(W^-1/2 K W^-1/2)=Σ K_ee / w_e.
 T=float(np.sum(Kdiag/wt))
 trials.append({"t":t,"min_weight":float(np.min(wt)),"acoustic_G_inf_err":residual,
                "gapped_spectral_trace":T,"fractional_trace_change":float(T/base_T-1),
                "leading_tangent_prediction":float(t*rel_slope)})
assert trials[-1]["gapped_spectral_trace"]!=trials[0]["gapped_spectral_trace"]
assert abs((trials[3]["gapped_spectral_trace"]-trials[1]["gapped_spectral_trace"])/(.03)-slope)<.05*abs(slope)
out={"status":"PASS_NATIVE_MAXWELL_HIDDEN_WEIGHTS_HAVE_GAPPED_SPECTRAL_FINGERPRINT",
"model":"TOE38 plaquette+commutator magnetic matrix P at k=0, 160 positive electric link weights W",
"leading_kinetic_G_target":"I3/2 six symmetric entries",
"initial_max_G_error":float(np.max(abs(g6(w)-Gtarget))),
"Jacobian_rank":6,"positive_weight_count":160,"fixed_leading_G_level_set_dimension":154,
"observable":"T(w)=Tr(W^-1 P(0)^dag P(0))=Σ_e (P^dag P)_ee/w_e, equal sum of all nonzero generalized magnetic band eigenvalues at k=0",
"exact_derivative_formula":"dT/dw_e= -(P^dag P)_ee /w_e²; dG_ij/dw_e=h_ei h_ej where h is W-harmonic representative",
"kernel_slope_dTdt":slope,"relative_kernel_slope":rel_slope,
"tangent_norm_J":float(np.linalg.norm(J@normal)),
"local_Gram_exact_relevel":"Keep 154 directions fixed except a chosen tangent and correct six free weights through nonlinear root to G=I/2 for every t",
"positive_equal_G_samples":trials,
"conclusion":"The 154 free electric-link directions are invisible to the leading twofold acoustic cone but NOT invisible to the total massive-band spectral trace. A finite-frequency/band-spectrum measurement can distinguish at least one independent microscopic direction while preserving exactly the same leading cone. Hence a single speed-of-light cone does not identify unique microgeometry.",
"scope":"Fixed choice of 160-edge marked finite Maxwell complex and fixed magnetic incidence matrix. This is a numerical local derivative + nonlinear correction certificate, not a globally rigid inverse spectral theorem, not selection of the 154 modes, and not a dynamical metric or gravity."}
(R/"data/w33_20261013_toe50_inverse_acoustic_spectral_trace.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"slope":slope,"relative":rel_slope,"samples":trials}))
