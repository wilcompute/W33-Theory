"""TOE51 independent three-front physics audit: color threshold, leptons, gravity.

Explicitly specified finite models; not a UV completion or derived TOE.
"""
import json,sys,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/"analysis"))
def freeze(name,out):
 (R/"data"/f"w33_20261013_toe51_{name}.json").write_text(json.dumps(out,indent=2)+"\n")
 return out
def color_threshold():
 # The stated Pass11957 n=0 holomorphic matching: Lambda3^9 =
 # m0 z Lambda5^12/(v0^4 z^4) = C/z^3.
 v0,m0,Lambda5=100.,50.,1.
 C=m0*Lambda5**12/v0**4
 # Lambda_IR(z)=C^(1/9)/|z|^(1/3).
 c=C**(1/9)
 zcrit=(c/min(v0,m0))**(.75)
 trials=[]
 for z in [.5,.1,.03,zcrit,.01,.001]:
  L=c*z**(-1/3)
  heavy=min(v0,m0)*z
  trials.append(dict(z=z,ir_scale=L,min_heavy_threshold=heavy,
                     heavy_over_strong=heavy/L,controlled_threshold=heavy>L))
 assert trials[0]["controlled_threshold"]
 assert not trials[-1]["controlled_threshold"]
 assert abs(trials[3]["heavy_over_strong"]-1)<1e-12
 # Anomaly/winding pole holds formally independent of beta flavour n.
 exponents={str(n):[12-n,10-n,8-n,9-n] for n in (0,3,6)}
 out=dict(status="PASS",front="strong_CP_color_threshold_decoupling",
   holomorphic_identity="Lambda3^(9-n)=m0*Lambda5^(12-n)/(v0^4 z^3)",
   benchmark=dict(v0=v0,m0=m0,Lambda5=Lambda5,light_spectators=0,
                  min_heavy_over_strong_equals_1_at_abs_z=zcrit),
   beta_coefficients=exponents,trials=trials,
   universal_nonuniform_limit="As |z|->0, Lambda3 scales |z|^-1/3 while all m,v thresholds scale |z|; threshold/strong ratio tends zero as |z|^(4/3). The pole formal series cannot be extrapolated to the separating divisor using the same weakly coupled SU3 EFT.",
   status_of_local_pole="Pass11957 local holomorphic pole is valid at scales with heavy thresholds above strong dynamics; this independently checks its restricted domain, not its global theta phase or modular completion.",
   quality="Does not solve strong CP, predict the vectorlike spectrum, or bound full loop theta.")
 return freeze("color_threshold_domain",out)
def leptonic_branches():
 from w33_pass11960_11961_clebsch_and_shared_cone import quark_kernel,charged_ratios
 d=json.loads((R/"data/w33_pass11960_11961_clebsch_and_shared_cone.json").read_text())["11960"]
 m,A=quark_kernel()
 # Normalize each computed ν matrix so Δm31²=2.5e-3 eV²,
 # with the fixed dimensionless ratio .0296; this introduces a scale.
 spl31=.0025
 cases=[]
 for f in d["two_real_diagonal_45_coefficients_fits"]:
  _,e=charged_ratios(f["coefficients"],m,A)
  _,ue=np.linalg.eigh(e.conj()@e.T)
  for root in f["two_real_offdiagonal_neutrino_roots"]:
   n=np.asarray(root["real_bare_Majorana"],float)
   nu=A.T@n@A
   mass=np.sort(np.linalg.svd(nu,compute_uv=False))
   scale=math.sqrt(spl31/(mass[2]**2-mass[0]**2))
   abs_m=mass*scale
   nu_e=ue.T@nu@ue
   m_bb=float(abs(nu_e[0,0])*scale)
   elec=np.asarray(root["PMNS_abs_squared"])[0]
   # Unknown free phases envelope given masses and U_e magnitudes:
   lengths=elec*abs_m
   lower=max(0.,2*max(lengths)-sum(lengths))
   upper=sum(lengths)
   # Phase choices in fitted matrix fix a specific m_bb inside envelope.
   # Takagi phases may depend on basis conventions; check within envelope.
   cases.append(dict(clebsch=f["coefficients"],delta_deg=root["delta_deg"],
     m_ee_eV=m_bb,total_masses_eV=float(sum(abs_m)),
     lightest_mass_eV=float(abs_m[0]),
     mass_ratios=(mass/mass[2]).tolist(),
     conservative_Majorana_free_interval_eV=[float(lower),float(upper)],
     within_free_phase_envelope=bool(lower-1e-10 <=m_bb<=upper+1e-10)))
 assert len(cases)>=3
 assert all(z["within_free_phase_envelope"] for z in cases)
 # Even where all four mixing targets fit exactly, the different roots
 # demonstrate that delta was NOT a unique output.
 deltas=[z["delta_deg"] for z in cases]
 assert max(deltas)-min(deltas)>100
 out=dict(status="PASS",front="leptonic_CP_branch_predictions",
    supplied_absolute_scale="Delta m31 squared =0.0025 eV² as illustrative comparator; not a derived W33 prediction",
    n_branches=len(cases),branches=cases,
    observed_issue="All fitted branches reproduce four supplied PMNS angle/splitting ratios but give different Dirac delta. They additionally predict distinct m_bb at imposed Δm31, conditional on their specific fitted real Majorana matrices and charged basis; none of the texture coefficients or absolute scale is dynamically selected.",
    limits="m_bb depends on charged-lepton Takagi convention and Majorana phases. A lepton-number-violating amplitude prediction requires the full Majorana phase convention, RG, nuclear matrix elements and a stable vacuum. Values are model-input consequences, not phenomenological evidence.")
 return freeze("lepton_branch_observables",out)
def gravity_scalar_completion():
 # One-link canonical Hamiltonian (a,W; E,pi_W):
 # H= E^2/(2W)+ magnetic(Pa)^2/2 + pi^2/(2M)+k(W-W0)^2/2
 # It retains canonical, unconstrained W but supplies no diff gauge.
 from w33_20261013_toe50_inverse_acoustic_spectral_trace import B,P,w
 import scipy.linalg as la
 rng=np.random.default_rng(51005)
 A=rng.normal(size=len(w))
 E=rng.normal(size=len(w))
 # Gauge-invariant Gauss solution: B^T E=0 (Euclidean kernel);
 # may use QR basis to avoid ill-conditioning.
 E-=B@la.solve(B.T@B,B.T@E,assume_a="pos")
 E_dot=-(P.conj().T@P@A).real
 gauss0=float(np.max(abs(B.T@E)))
 gaussdot=float(np.max(abs(B.T@E_dot)))
 magnetic_gauge_err=float(np.max(abs(P@B)))
 assert max(gauss0,gaussdot,magnetic_gauge_err)<1e-8
 M,k,w0=2.,3.,1.
 eq=[]
 for esq in [0.,1.,4.,16.]:
  # monotonic derivative of V=E²/(2w)+k(w-w0)^2/2
  from scipy.optimize import brentq
  z=brentq(lambda z:k*(z-w0)-esq/(2*z*z),w0,max(w0+20,1+esq))
  curvature=k+esq/(z**3)
  eq.append(dict(E_squared=esq,equilibrium_weight=z,
                 scalar_omega2=curvature/M,
                 physical_positive_mass=curvature>0))
 assert all(z["physical_positive_mass"] for z in eq)
 out=dict(status="PASS",front="native_dynamical_link_metric_constraint_gate",
  full_native_links=160,gauss_initial_inf_error=gauss0,
  gauss_time_derivative_inf_error=gaussdot,
  magnetic_gauge_identity_inf_error=magnetic_gauge_err,
  canonical_extension="H=Σ E_e²/(2w_e)+||P A||²/2+Σ p_w,e²/(2M)+k(w_e-w0)²/2, with w_e>0. Gauss B^T E=0 and P B=0 are unchanged and first class.",
  canonical_equations="dot w=p_w/M; dot p_w=E²/(2w²)-k(w-w0); dot A=E/w; dot E=-P^T P A",
  test_single_link_equilibria=eq,
  gravity_gate="Adding canonical metric scalars avoids pi_w=0 and its E=0 secondary but introduces 160 physical scalar oscillators; it supplies zero Hamiltonian/diffeomorphism constraints and cannot be identified as general relativity. A genuine spatial metric requires additional first-class constraints, closure and continuum diffeomorphism symmetry.",
  prior_art="Bonzom Dittrich 2013 arxiv:1304.5983 derives discrete Dirac hypersurface algebra in restricted gravity sectors; not implied by a gauge-invariant W33 Maxwell-scalar extension.")
 return freeze("dynamic_metric_gauss",out)
if __name__=="__main__":
 for fn in (color_threshold,leptonic_branches,gravity_scalar_completion):
  z=fn();print(z["front"],z["status"],flush=True)
