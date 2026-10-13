"""TOE57 gravity: exact no-go for repairing tested w*p local-rescaling
constraint by adding ANY potential U(w) independent of electric field.

The theorem is conditional on w-only correction and this D generator;
it does not exclude electromagnetic-dependent constraints or true gravity.
"""
from pathlib import Path
import sys,json
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
ed,volts,look,octs,comm,*_=prep()
B=np.rint(gradient(ed,volts,np.zeros(3)).real).astype(int)
c=np.rint(cycle_row(octs[0],ed,volts,look,np.zeros(3)).real).astype(int)
assert np.array_equal(B.T@c,np.zeros(80,dtype=int))
rng=np.random.default_rng(57003)
w=.7+.6*rng.random(160)
p=rng.normal(size=160)*.12
K=2.;kappa=1.5;w0=1.
# For a fixed arbitrary chi, D_chi=Σ a_e w_e p_e,
# {H,D} = Σ a_e [-E_e²/(2 w_e)+ κ w_e(w_e-w0)-p_e²/K] + δ_D U(w).
# For any U(w), the last term is independent of E. Evaluate on
# Gauss-compatible E=t*c, t=0,1,2 and finite difference in t².
bsource=B.T@(c*c/w)
v=int(np.argmax(abs(bsource)));chi=np.zeros(80);chi[v]=1
a=B@chi
C=float(-.5*np.dot(a,c*c/w))
assert abs(C)>1e-3
def kinetic_bracket(t):
 E=t*c.astype(float)
 assert max(abs(B.T@E))==0
 return float(np.dot(a, -E*E/(2*w) + kappa*w*(w-w0)-p*p/K))
v0=kinetic_bracket(0.);v1=kinetic_bracket(1.);v2=kinetic_bracket(2.)
assert abs(v1-v0-C)<1e-12
assert abs(v2-v0-4*C)<1e-12
# Any w-only U contributes same D(U) for all these distinct E.
# Therefore first-class H vs D can't hold for all on-shell E, since
# differences cancel arbitrary unknown U but yield C != 0.
# Gauge energy of flux E=t c is classically allowed for charged-neutral
# matter, so this is a genuinely Gauss-surface theorem.
out={"status":"PASS_TOE57_LINK_RESCALING_UW_ONLY_REPAIR_NO_GO",
"native_edges":160,"native_vertices":80,
"chosen_closed_native_flux":"boundary vector c of one native 8-edge octagon with B.T c=0",
"chosen_vertex":v,
"test_chi_chosen_by":"maximize |(B.T (c_e²/w_e))_v| among native vertices",
"nonzero_no_go_coefficient_C":C,
"Gauss_E_scales":[0,1,2],
"native_H_vs_D_for_three_electric_scales":[v0,v1,v2],
"zero_one_bracket_difference":v1-v0,
"zero_two_bracket_difference":v2-v0,
"theorem":"For fixed positive nonuniform weights w, native incidence B, and D_chi=Σ_e(Bχ)_e w_e p_we, the bracket of H_E+w+U(w) with D_chi on Gauss-compatible E=t c has a t² term C=-1/2 Σ_e(Bχ)_e c_e²/w_e. Every potential U(w) independent of E shifts the bracket by a t-independent amount. If C!=0, no such U can enforce {H,D_chi}=0 on all Gauss-compatible E. Native c from a closed 8-cycle and an explicitly constructed χ give C!=0.",
"scope":"Conditional exact no-go for this local rescaling D and correction potentials U(w) independent of E. It does not exclude modified D involving E/A, nontrivial gravitational canonical pairs, nonlocal corrections, special constrained weights, or Einstein gravity emerging in other limits.",
"prior_art":"Canonical Dirac first-class constraint requirement standard. TOE56 previously exhibited nonzero bracket at one state; this pass strengthens to an entire family and arbitrary potential U(w)."}
(R/"data/w33_20261013_toe57_gravity_potential_no_go.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"C":C,"H_D":out["native_H_vs_D_for_three_electric_scales"]}))
