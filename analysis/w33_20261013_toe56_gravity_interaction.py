"""TOE56: explicit failure of a plausible native geometry constraint,
and finite-field nonlinear magnetic interaction / scaling audit.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
P=np.rint(np.array([cycle_row(z,ed,volts,look,np.zeros(3)) for z in octs+comm]).real)
B=np.rint(gradient(ed,volts,np.zeros(3)).real)
rng=np.random.default_rng(56031)
w=1+.2*rng.random(160);p=rng.normal(size=160)*.13
E=rng.normal(size=160)*.2
A=rng.normal(size=160)*.12
chi=rng.normal(size=80)*.5
a=B@chi
M,kappa,w0=2.,1.7,1.0
def metric_energy(w,p):
 return float(np.sum(E**2/(2*w)+p*p/(2*M)+kappa*(w-w0)**2/2))
def orbit(t):
 return metric_energy(w*np.exp(t*a),p*np.exp(-t*a))
# Candidate vertex "diffeomorphism" C_chi=sum_e (B chi)_e*w_e*p_e.
# It generates per-link canonical scaling, but is NOT a symmetry of H.
analytic=float(np.sum(a*(-E*E/(2*w)+kappa*w*(w-w0)-p*p/M)))
numerical=(orbit(1e-5)-orbit(-1e-5))/(2e-5)
assert abs(analytic-numerical)<1e-8,(analytic,numerical)
assert abs(analytic)>.001
# All proposed D_v=sum_e B_ev w_e p_e mutually commute, because
# each separate link density w_e p_e commutes with all w_f p_f.
# But {H,D_chi} is generally nonzero and not a sum of existing
# U(1) Gauss constraints on a Gauss-compatible state.
charge=np.zeros(80)
Egauss=E-B@np.linalg.lstsq(B.T@B,B.T@E,rcond=None)[0]
assert np.max(abs(B.T@Egauss))<1e-11
E=Egauss
analytic_on_gauss=float(np.sum(a*(-E*E/(2*w)+kappa*w*(w-w0)-p*p/M)))
assert abs(analytic_on_gauss)>.001
# Four proposed local grav constraints per W33 site would need 320
# independent first-class generators. This candidate rank<=79 and
# has no Hamiltonian constraint or correct hypersurface deformation.
# Coupling native Wilson compact plaquettes to A:
g=.43
f=P@A
def Hmag(lmbda):
 return float(np.sum(1-np.cos(g*lmbda*f))/(g*g))
quad=.5*np.dot(f,f)
quartic=-g*g*np.sum(f**4)/24
qerrs=[]
for x in (.5,.25,.125):
 inferred=(Hmag(x)-x*x*quad)/(x**4)
 rel=abs(inferred-quartic)/abs(quartic)
 qerrs.append({"A_amplitude":x,"effective_quartic_coefficient":float(inferred),
               "relative_error_vs_exact_taylor":float(rel)})
assert qerrs[2]["relative_error_vs_exact_taylor"]<.004
# Exact native background-dependent magnetic Hessian:
# ∂²H_B/∂A²=P.T diag(cos(gP A)) P;
# unlike the purely quadratic model, nonzero photon self-interaction.
cos=np.cos(g*f)
assert np.min(cos)>.5
perturb=cos-1
assert np.max(abs(perturb))>.01
# Gauge invariance of the new Hessian itself:
hessB= P.T@(cos[:,None]*P)
assert np.max(abs(hessB@B))<1e-10
# Conditional flux smoothness assumption theta=g a² F.
# Ratio Wilson/Maxwell magnetic deviation scales a^4 for fixed g,F.
F=.7
deviation=[]
for ascale in [1,.5,.25]:
 phi=g*(ascale**2)*F
 ratio=abs(2*(1-np.cos(phi))/(phi*phi)-1)
 deviation.append(ratio)
factors=[deviation[1]/deviation[0],deviation[2]/deviation[1]]
assert all(.04<r<.085 for r in factors),factors
out={"status":"PASS_TOE56_NATIVE_SCALING_CONSTRAINT_FAILURE_AND_COMPACT_INTERACTION",
"native_site_incidence_shape":[160,80],"native_plaq_rows":int(P.shape[0]),
"candidate_diffeo_generator":"D_chi=sum_e (B chi)_e w_e p_we, a canonical local multiplicative link-weight scaling.",
"candidate_diffeo_poisson":{"D_v_D_u":"0 exactly for all v,u, since D_v linear sums of commuting link densities w_e p_e",
"analytic_H_vs_D":analytic,"finite_difference_H_vs_D":numerical,
"H_vs_D_on_U1_Gauss_surface":analytic_on_gauss,
"verdict":"NOT_FIRST_CLASS_WITH_H; candidate is NOT a constraint symmetry, its bracket with H does not vanish even on the physical U1 Gauss surface, and D has no H_gravity partner."},
"compact_B_interaction":{"g":g,"small_amplitude_quadratic_coefficient":float(quad),
"exact_quartic_coefficient":float(quartic),
"quartic_finite_difference":qerrs,
"min_background_cos":float(min(cos)),
"max_background_hessian_multiplier_shift":float(max(abs(perturb))),
"max_background_hessian_times_gradient_residual":float(max(abs(hessB@B).ravel()))},
"conditional_a2_flux_scaling":{"hypothesis":"smooth physical field plaquette integral theta=g a² F; this is ASSUMED, not derived from W33 cover",
"a_values":[1.,.5,.25],"relative_magnetic_energy_deviation":deviation,
"error_halving_ratios":factors,"expected_leading_ratio":1/16,
"continuum_caveat":"Fixed local finite W33 plaquette action has no growing W33 cell sequence, no renormalized g(a), no interacting quantum Ward identities or actual scattering amplitude."},
"gravity_no_go_scope":"Only the natural tested canonical link-rescaling candidate fails. This does not exclude all W33 microscopic geometric constraints or emergent gravity.",
"physics_limits":"The Wilson quartic term is a finite-lattice nonlinear interaction and not observed light-by-light scattering; perturbative continuum suppression is conditional on an undemonstrated physical spacing and smooth flux scaling."}
(R/"data/w33_20261013_toe56_dynamical_gravity_and_interaction.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"bracket":analytic_on_gauss,"quartic":quartic,
"err":qerrs[-1]["relative_error_vs_exact_taylor"],"halving":factors}))
