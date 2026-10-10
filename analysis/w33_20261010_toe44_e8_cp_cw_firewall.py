"""TOE44 front 5: generalized CP and missing-loop-input audit for SU9 84.

Exactly tests single I12 coupling generalized CP and relative 12/18
coupling rephasing invariant, while reusing independently calculated
SU(9) vector CW shape. Does NOT claim full scalar/ghost/fermion action.
"""
from pathlib import Path
import json,itertools,math
import numpy as np
R=Path(__file__).resolve().parents[1]
O=R/"data/w33_20261010_toe44_e8_cp_phase_firewall.json"
old=json.loads((R/"data/w33_20261010_toe43_e8_one_loop_audit.json").read_text())
rays=[old["cases"][f"witting_{j}"] for j in range(4)]
generics=[old["cases"][f"generic_{j}"] for j in range(8)]
assert all(r["unbroken_gauge_bosons"]==24 for r in rays)
assert all(g["unbroken_gauge_bosons"]==0 for g in generics)
assert all(abs(r["cw_vector_log_shape"]+6*np.log(3))<1e-11 for r in rays)
# Phase functional of a homogeneous degree-n real-coefficient invariant I_n.
# On a fixed Cartan ray I_n(r) is fixed complex A_n; absorb its phase
# into effective coupling angle alpha_n=Arg(kappa_n I_n(r)).
# Conjugation of all fields can be composed with x -> exp(i delta) x*
# when coefficients of all relevant invariants admit generalized CP.
def V12(phi,alpha):return math.cos(12*phi+alpha)
def V1218(phi,alpha,beta):return V12(phi,alpha)+.7*math.cos(18*phi+beta)
def cp_reflection_angle(alpha,n):return (-2*alpha/n)%(2*math.pi/n)
rng=np.random.default_rng(44005)
single_residuals=[]
for i in range(30):
 alpha=rng.uniform(-np.pi,np.pi)
 delta=cp_reflection_angle(alpha,12)
 res=max(abs(V12(phi,alpha)-V12(delta-phi,alpha))
         for phi in rng.uniform(-np.pi,np.pi,40))
 single_residuals.append(res)
 assert res<1e-12,res
# CP invariance for both terms exists iff Im(kappa12**3 * conj(kappa18)**2)=0
# with the REAL form convention for invariant tensors, absent other couplings.
# The condition 3 alpha - 2 beta == n*pi follows by eliminating delta.
alpha=.37;beta_aligned=1.5*alpha;beta_incompatible=.71
def gap(beta):
 phase=(3*alpha-2*beta)
 return abs(np.sin(phase))
assert gap(beta_aligned)<1e-12
assert gap(beta_incompatible)>.1
# Enumerate ALL branches solving invariance of I12 and test invariance
# of the I18 term. No CP reflection when incompatible.
branches=[(-2*alpha+2*np.pi*k)/12 for k in range(12)]
def best_cp_residual(beta):
 return min(max(abs(V1218(phi,alpha,beta)-V1218(delta-phi,alpha,beta))
   for phi in np.linspace(-1,1,111)) for delta in branches)
aligned=best_cp_residual(beta_aligned)
incompatible=best_cp_residual(beta_incompatible)
assert aligned<1e-12 and incompatible>.1,(aligned,incompatible)
# Unknown fermion Yukawas -> neither fermion masses nor the numerical
# full one-loop effective potential can be specified. Stress sensitivity:
# A wholly hypothetical fermion spectrum mF²=y² eA would contribute
# negative fermion supertrace weight to the same F; y=0 vs y=1
# can reverse direction preference for a sufficiently large degeneracy.
nferm=8;y=.9
positive_bosonic_weight=3
fermion_toy_weight=-4*nferm*y**4
assert positive_bosonic_weight+fermion_toy_weight<0
shape_w=rays[0]["cw_vector_log_shape"];shape_g=generics[0]["cw_vector_log_shape"]
assert (shape_g-shape_w)>0
assert (positive_bosonic_weight+fermion_toy_weight)*(shape_g-shape_w)<0
out={"status":"CP_COEFFICIENT_REPHASE_FIREWALL_AND_INCOMPLETE_CW_ACTION",
"generalized_CP_one_I12_theorem":"For scalar V=V0+2Re(kappa12 I12(x)), with V0 depending only on Hermitian x products and a REAL polynomial tensor I12, arbitrary Arg kappa12 can be removed by x->exp(-i Arg kappa12/12)x. Equivalently a generalized CP conjugation with delta=-2 Arg kappa12/12 leaves V invariant. This rules out explicit CP from the lone complex coefficient; spontaneous CP breaking remains possible.",
"max_single_invariant_cp_residual_30_trials":max(single_residuals),
"two_invariants":"With nonzero independent I12,I18 and otherwise real-form couplings, invariant relative coefficient phase is Arg(kappa12^3/conj-free-kappa18^2)=3 Arg(kappa12)-2 Arg(kappa18) modulo pi; two phases cannot generally both be made real under one field rephasing.",
"example_alpha_12":alpha,"example_beta18_CP_compatible":beta_aligned,
"example_beta18_CP_incompatible":beta_incompatible,
"CP_compatible_max_residual":aligned,
"CP_incompatible_min_residual_over_12_branches":incompatible,
"vector_witting_shape_F":shape_w,"vector_generic_example_shape_F":shape_g,
"toy_missing_fermion_weight":{"vector_only_shape_coefficient":positive_bosonic_weight,
"hypothetical_8_dirac_modes_with_mass_squared_y2_e":fermion_toy_weight,
"total_example":positive_bosonic_weight+fermion_toy_weight,
"this_is_not_a_consistent_complete_representation":True},
"cannot_calculate":"No Yukawa fermion representations, invariant contractions, gauge-fixing prescription, renormalization conditions and full scalar/ghost spectrum specified in this independent producer. A complete one-loop potential and actual CP-breaking vacuum cannot be reported.",
"physical_boundary":"Field rephasing is a Lagrangian basis redefinition not an SU(9) gauge rotation. Other complex Yukawas, theta angles or additional holomorphic terms can yield physical relative CP phases. Presence of a CP symmetry at the level of couplings does not rule out spontaneous CP breaking."
}
O.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:out[k] for k in ("status","max_single_invariant_cp_residual_30_trials","CP_compatible_max_residual","CP_incompatible_min_residual_over_12_branches","vector_witting_shape_F")}))
