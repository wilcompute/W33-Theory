"""TOE59 Lorentz/interacting-front identifiability audit.

Use actual TOE54 photon and Pass11970 native Wilson low-k controls.
The temporal electric normalization epsilon and Dirac velocity v are
independent bare choices; static fermion Ward data cannot select them.
"""
from pathlib import Path
import numpy as np,json
R=Path(__file__).resolve().parents[1]
ph=json.loads((R/"data/w33_20261013_toe54_finite_lorentz_dispersion.json").read_text())
di=json.loads((R/"data/w33_pass11970_native_wilson_dirac.json").read_text())
assert ph["squared_continuum_speed_target"]==2.
assert di["origin_zero_modes"]==4
# Extract measured finite-k control instead of inferring from arbitrary
# symbolic speeds; below has 6 directions radius .02.
photon=[s for s in ph["samples"] if s["radius"]==.02]
assert len(photon)==6
ph_v2=float(np.mean([x["mean_light_phase_velocity_sq"] for x in photon]))
# Pass11970 free Dirac is H = v alpha K + r beta L.
# Its low-p slope is v to first order; v is externally supplied.
rows=[]
for eps in (1.,2.,4.):
 for v in (.5,1.,np.sqrt(2)):
  photon_speed=np.sqrt(2/eps)
  fermion_speed=v
  rows.append({"electric_epsilon":eps,"bare_Dirac_velocity":v,
    "photon_leading_speed":photon_speed,
    "fermion_leading_speed":fermion_speed,
    "photon_to_fermion_speed_ratio":photon_speed/v,
    "finite_k_photon_speed_estimate":np.sqrt(ph_v2/eps)})
matched=[x for x in rows if abs(x["photon_to_fermion_speed_ratio"]-1)<1e-12]
assert len(matched)==2,(rows,matched)
assert matched[0]["electric_epsilon"]!=matched[1]["electric_epsilon"]
# Actual static fermionic determinant from TOE58 is entirely magnetic
# spatial hopping; independent of eps or the four-spinor v above.
static=json.loads((R/"data/w33_20261013_toe58_fermion_polarization.json").read_text())
assert static["max_two_pure_gauge_rows_or_columns"]<1e-8
out={"status":"PASS_TOE59_PHOTON_SPINOR_COMMON_CONE_UNDERDETERMINATION",
"source_photon":"TOE54 native photon dispersion with Pass11956 electric weights; six low-k directions at |k|=.02",
"photon_low_k_mean_speed_squared":ph_v2,
"source_fermion":"Pass11970 320-band native single free vectorlike Dirac with externally supplied v",
"spinor_origin_massless":di["origin_zero_modes"],
"rows":rows,"matched_bare_parameter_pairs":matched,
"static_one_loop_gauge_Ward_residual":static["max_two_pure_gauge_rows_or_columns"],
"theorem":"For the stated separate free W33 photon/Dirac sectors, multiplying temporal electric kinetic term by 1/epsilon rescales the photon squared cone speed 2/epsilon, while the freely supplied native Wilson-Dirac velocity v rescales fermion cone speed v. Matching cones v²=2/epsilon leaves a continuous one-parameter choice: relative-speed coincidence alone does not predict physical c or renormalized interaction. The existing TOE58 static one-loop spinless fermion determinant has no temporal kinetic normalization and cannot fix epsilon or the 4-spinor v.",
"limitation":"Uses two separate previously established FREE low-energy models and an independent STATIC fermion susceptibility; not a new interacting 4D common action, RG beta function, finite-size relativistic scattering amplitude or phenomenological Lorentz bound.",
"prior_art":"Independent photon and fermion velocities on emergent lattice cones and velocity matching by tuning are familiar in lattice quantum field theory; this is an explicit W33 proof-obligation/identifiability control, not a novel universal theorem."}
(R/"data/w33_20261013_toe59_lorentz_velocity_gate.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE59 Lorentz",[(x["electric_epsilon"],x["bare_Dirac_velocity"]) for x in matched],ph_v2)
