"""TOE56: compact W33 common-action parameter identifiability and physics gates.

Quantized flux plus classical scalar matter forms compatible *scaffolds*,
not a fully quantized gauge+matter+metric lattice Hamiltonian.
"""
from pathlib import Path
import json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
P=np.array([cycle_row(z,ed,volts,look,np.zeros(3)) for z in octs+comm]).real
B=gradient(ed,volts,np.zeros(3)).real
assert P.shape==(1385,160) and B.shape==(160,80)
w=np.ones(160)
# Define compact magnetic term H=beta/g² sum(1-cos(g P A)).
# For A=0 the FULL quadratic Hessian equals beta P.T P EXACTLY,
# independently of g. Hence no measurement of free-photon eigenvalues
# can determine g; nonlinear interaction has O(g²) dependence.
f=np.random.default_rng(56074).normal(size=160)*.25
def magnetic(A,g,beta):
 return float(beta*np.sum(1-np.cos(g*(P@A)))/(g*g))
sig={}
for g in [.25,.5,1.]:
 for beta in [.7,1.3]:
  # Analytic Hessian at vacuum: beta P.T P.
  h=beta*P.T@P
  assert np.max(abs(h@B))<1e-11
  # finite-direction curvature vs exact quadratic
  delta=.008
  centered=(magnetic(delta*f,g,beta)+magnetic(-delta*f,g,beta)-2*magnetic(np.zeros(160),g,beta))/(delta*delta)
  analytic=beta*sum((P@f)**2)
  err=abs(centered-analytic)/analytic
  assert err<2e-5,(g,beta,err)
  q=-beta*g*g*np.sum((P@f)**4)/24.
  assert q<0
  sig[f"{g},{beta}"]={"analytic_bare_quadratic_Hessian_direction":float(analytic),
    "finite_diff_relative_error":float(err),
    "quartic_compact_self_interaction_amplitude":float(q)}
# One g-independent free-sector spectrum at each beta;
# avoids calculating 6 full spectra for an analytically trivial identity.
v=np.linalg.eigvalsh(P.T@P)
positive=v[v>1e-6]
assert len(positive)==78
free_eigen={"first_3":positive[:3].tolist(),"number_positive":len(positive)}
assert np.allclose([sig[f"{g},0.7"]["analytic_bare_quadratic_Hessian_direction"] for g in (.25,.5,1.)],
                   [sig["0.25,0.7"]["analytic_bare_quadratic_Hessian_direction"]]*3)
# Effective physical electric charge in compact formulation is INTEGER
# relative link phase; continuous g remains in energy cost g² n² / 2w.
# Common action has >=7 *external* scalar parameters:
# g, beta, charged scalar hopping kappa, m², M, kw, w0.
# Additional 160 local scalar w initial values; no dynamical vacuum fixed.
c= json.loads((R/"data/w33_20261013_toe56_compact_u1.json").read_text())
q= json.loads((R/"data/w33_20261013_toe56_rotor_chirality.json").read_text())
z= json.loads((R/"data/w33_20261013_toe56_dynamical_gravity_and_interaction.json").read_text())
assert c["native_W33_dimensions"]["first_cohomology"]==3
assert q["native_bloch_chiral_index"][1]["index"]==-80
assert z["candidate_diffeo_poisson"]["verdict"].startswith("NOT_FIRST_CLASS")
gates=[
 {"requirement":"compact local gauge invariance","met":True,
 "evidence":"Native Wilson cos(gP A) is periodic under 2pi/g link shifts, PB=0, and covariant charged scalar hopping"},
 {"requirement":"full gauge+charged-matter quantum Hilbert dynamics","met":False,
 "evidence":"One-plaquette truncated electric rotor block only; scalar field/metric momenta remain classical"},
 {"requirement":"4D chiral anomaly-free SM from W33","met":False,
 "evidence":"Native incidence block index=-80 from orbital imbalance; no Weyl spinors or lattice overlap regulator"},
 {"requirement":"interacting Lorentz-invariant continuum","met":False,
 "evidence":"Formal smooth flux suppresses a^4 Wilson quartic and TOE55 free a² dispersion, no actual coupled scaling limit"},
 {"requirement":"Einstein gravity two spin2 polarizations","met":False,
 "evidence":"Candidate link-scaling constraints do NOT Poisson commute with native Hamiltonian even on U1 Gauss surface"},
 {"requirement":"first-principles coupling and scale prediction","met":False,
 "evidence":"Vacuum free photon Hessian is exactly independent of g; beta and at least 6 additional bare parameters unspecified"}]
out={"status":"PASS_TOE56_PHYSICS_FIRST_FIVE_FRONTS_PARAM_IDENTIFIABILITY",
"native_free_photon_hessian":"For H_B=beta/g² Σ[1-cos(gP A)], ∂²H_B/∂A² at A=0=beta P.T P, completely independent of bare g, with all 3 harmonic and 79 pure gauge zero directions at k=0.",
"beta_1_compatible_nonzero_spectrum":free_eigen,
"bare_parameter_grid":sig,
"gauge_coupling_not_identified":"All tested positive g values yield exactly the same classical free photon quadratic operator for fixed beta,w, but different compact nonlinear magnetic quartic coefficients proportional to -beta*g² and different quantized rotor electric energies proportional to g². A predicted alpha requires physical matter-charge normalization and QFT matching; neither is supplied.",
"couplings_unfixed_by_geometry":["g","beta","kappa_charged_hopping","mass_squared","M_metric","kappa_weight","w0"],
"minimum_number_of_external_bare_scalar_parameters":7,
"n_common_physics_gates_met":sum(int(t["met"]) for t in gates),
"required_gates":gates,
"important_scope":"Front1 compact repairs prior TOE55 classical magnetic term; Front2 finite rotor+chirality diagnostic; Front3 native candidate gravity bracket failure; Front4 formal nonlinear Wilson continuum error; Front5 explicit parameter identifiability and common-action evidence ledger. No physical TOE or renormalized SI observable claimed.",
"prior_work":"TOE38 native chain; TOE40 classical Maxwell; TOE51 weighted dynamics; TOE54 fixed Bloch lattice no exact Lorentz; TOE55 charged scalar local U1. New TOE56 correction respects full compact-link periodicity."}
(R/"data/w33_20261013_toe56_five_physics_gates.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"gates_met":out["n_common_physics_gates_met"],
 "g_direction_curvatures":[sig[f"{g},0.7"]["analytic_bare_quadratic_Hessian_direction"] for g in (.25,.5,1.)],
 "quartic":{g:sig[f"{g},0.7"]["quartic_compact_self_interaction_amplitude"] for g in (.25,.5,1.)}}))
