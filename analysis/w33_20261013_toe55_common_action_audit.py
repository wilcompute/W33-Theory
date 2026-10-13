"""TOE55 inverse-alpha and unified-action predictivity/constraint audit.

Comparing a bare W33 fraction to NIST is an explicit FALSE-positive gate,
not a new alpha theory or a measurement-derived model.
"""
import json,math
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name):
 return json.loads((R/"data"/f"w33_20261013_toe55_{name}.json").read_text())
gauge=load("native_matter_gauge")
grav=load("linear_spin2_constraints")
matter=load("anomaly_deformation")
proposal=Fraction(137)+Fraction(40,1111)
codata=Fraction(137035999177,10**9)
uncertainty=Fraction(21,10**9)
delta=proposal-codata
nsigma=delta/uncertainty
assert nsigma>200
# This repeats TOE40 prior negative-control comparison, NOT a fresh fit.
families={}
for g in (.1,.3,.7):
  families[str(g)]={"illustrative_tree_inverse_alpha_if_canonical_QED_normalization":4*math.pi/(g*g),
    "native_hopping_energy":gauge["free_gauge_coupling_values_hopping_energy"][str(g)]}
assert len(set(round(v["native_hopping_energy"],5) for v in families.values()))==3
# Explicit nondegeneracy of link-weight momentum Hessian:
# H contains sum pw_e²/(2M), M=2; Hessian=I_160/M.
# 160 weights are independent dynamical scalar degrees, no primary
# constraints pi_w=0 and no native gravitational H_i/H_0 exist.
nlink=gauge["w33_native_links"];nsite=gauge["w33_native_sites"]
configuration=nlink+2*nsite+nlink # A links + (Re z,Im z) + w links
first_class_U1=nsite
physical_config=configuration-first_class_U1
assert (configuration,first_class_U1,physical_config)==(480,80,400)
assert grav["TT_projector_rank_at_k_1_2_3"]==2
assert matter["SU2_Witten_even"] and matter["U1_cubed_anomaly"]=="0"
out={"status":"PASS_TOE55_FIVE_FRONT_UNIFIED_CLASSICAL_ACTION_EVIDENCE_LEDGER",
"prior_repo_owner_alpha":"TOE40 precomputed W33 137+40/1111 vs 2022 CODATA error >210 sigma. This repetition is a regression; no independent new physical inference.",
"bare_W33_inverse_alpha_fraction":str(proposal),
"bare_W33_inverse_alpha_decimal":float(proposal),
"CODATA2022_NIST_inverse_alpha":float(codata),
"CODATA2022_inverse_alpha_std_uncertainty":float(uncertainty),
"uncorrected_delta_alpha_inverse":float(delta),
"uncorrected_discrepancy_sigma_if_treated_as_exact":float(nsigma),
"important_scope":"Neither a missing renormalization correction nor a physical uncertainty budget is computed; sigma comparison invalidates the claim of an exact uncorrected bare prediction, NOT an entire W33 UV completion.",
"native_action_gauge_coupling_families":families,
"lattice_to_QED_normalization_warning":"Illustrative alpha=g²/4pi only in canonical continuum U1 normalization and with fixed matter charge, and not established for this dimensionless native lattice. Photon spectrum and gauge closure do not select any g.",
"shared_native_action":"Classical W33 Hamiltonian H(E,A,w,pw,z,p;g,kappa,m²,M,kw,w0) built in native_matter_gauge producer. Its U1 constraints form an Abelian first-class algebra; the same action contains dynamical link weights and charged scalar matter.",
"canonical_configuration_variables":{"Maxwell_links":nlink,"complex_scalar_site_real_components":2*nsite,"metric_link_scalar_variables":nlink,
 "total":configuration},
"constraints":{"charged_local_U1_first_class":first_class_U1,
 "native_gravitational_Hamiltonian_and_spatial_diffeomorphism":0,
 "physical_configuration_count_at_generic_scalar_configuration_after_U1_reduction":physical_config},
"link_weight_momentum_Hessian":{"dimension":nlink,"M":2.0,"full_rank":nlink,
 "eigenvalue_all":0.5,"meaning":"No primary constraints for w, and all 160 link-weight scalar momenta are dynamical"},
"not_spin2":"The constrained 480-config scalar+Maxwell finite theory still has 400 classical physical configuration dimensions, including 160 dynamical weight scalar modes. It is NOT Einstein gravity, nor a demonstrated spin-two field. Comparing different lattices' mode counts is not physical degree matching.",
"anomaly_gate":"Anomaly cancellation was checked for a *supplied* SM+nu_c generation, with a continuum Y+t(B-L) family. Native action contains only complex scalars, not those Weyl fermions.",
"five_front_gate_status":{
  "dynamical_gravity":"FAIL_NATIVE: only known continuum Fierz-Pauli spin2 benchmark passes",
  "electromagnetism":"PASS_CLASSICAL_NATIVE_LOCAL_U1: photon QED and continuum Lorentz unproved",
  "standard_model":"PASS_ANOMALY_BENCHMARK: actual W33-derived chiral spectrum unproved",
  "fundamental_constants":"FAIL_UNIQUE: g remains continuous; historical rational alpha differs from precise CODATA",
  "one_common_action":"PASS_FINITE_CLASSICAL_U1_SCALAR_WEIGHT_ONLY: fails quantum chiral SM and gravity"},
"does_not_prove":"This is a rigorous consistency/evidence partition, not a positive Theory of Everything or a no-go theorem for all possible W33 extensions."}
(R/"data/w33_20261013_toe55_five_front_physical_gate.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"sigma":float(nsigma),"config":physical_config,"couplings":families}))
