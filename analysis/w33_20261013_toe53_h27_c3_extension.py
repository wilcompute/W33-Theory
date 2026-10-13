"""TOE53: clock compatibility of H27 W33 lines and K81 regular slices.

Two distinct source-clock assignments are *not* interchangeable.
"""
from pathlib import Path
import json,runpy
import numpy as np
R=Path(__file__).resolve().parents[1]
p=runpy.run_path(str(R/"analysis/w33_20261013_toe52_h27_bridge.py"))
perms=p["perms"]; mult=p["mult"]; orbits=p["orbit"]
assert len(orbits)==8 and sorted(map(len,orbits))==[1]*4+[9]*4
omega=np.exp(2j*np.pi/3)
# Regular(H27)xRegular(C3) has 3 copies of Regular(H27),
# one copy for each external C3 eigencharacter.
# Under a scalar source phase omega, the image occupies one
# Reg(H27) per 81D K81, carrying *one* invariant H27 vector.
fixed={k:len(orbits) for k in ("full40",)}
E=p["E"]; projector={"spread15":p["P15"],"cusp25":p["P0"]+p["P24"],"line40":np.eye(40)}
source_invariants={k:int(round(np.trace(E@Q))) for k,Q in projector.items()}
scalar_minimum={k:v for k,v in source_invariants.items()}
assert scalar_minimum=={"spread15":3,"cusp25":5,"line40":8}
# Construct an explicit 40->243 H27xC3 isometry for an ASSIGNED graded
# C3 clock. Each W33 orbit is its own transitive permutation module.
# Map to normalized indicator of stabilizer coset in a single H27 regular
# sector. Eight orbits require eight of the nine available regular sectors.
# Regular-sector index b=3*carrier+character, so ext phase=omega^character.
iso=np.zeros((243,40),dtype=np.complex128)
charge=np.zeros(40,dtype=np.int64)
orbit_assignments=[]
identity=p["identity"]
for b,O in enumerate(orbits):
 i=O[0]; stabilizer=[g for g in range(27) if perms[g][i]==i]
 assert len(stabilizer)*len(O)==27
 # One regular target sector for this orbit.
 for col in O:
  preimage=[g for g in range(27) if perms[g][i]==col]
  assert len(preimage)==len(stabilizer)
  iso[27*b+np.array(preimage),col]=1/np.sqrt(len(stabilizer))
 charge[O]=b%3
 orbit_assignments.append({"orbit_size":len(O),"target_carrier":b//3,
   "external_C3_eigencharacter":b%3,"stabilizer_size":len(stabilizer)})
assert np.linalg.norm(iso.conj().T@iso-np.eye(40))<1e-12
# One H27 action on 27D regular target copies.
max_H=0.
for g in range(27):
 Q=np.zeros((40,40))
 Q[perms[g],np.arange(40)]=1
 moved=iso[27*np.arange(9)[:,None]+mult[g][None,:],:].copy()
 # indexing moved with row g*h gives T_g action, using inverse push.
 L=np.zeros_like(iso)
 for b in range(9):
  L[27*b+mult[g],:]=iso[27*b:27*(b+1),:]
 max_H=max(max_H,float(np.max(abs(L-iso@Q))))
assert max_H<1e-12
# C3 eigenbasis target and graded source phases.
K=np.repeat(np.array([0,1,2]*3),27)
source=omega**charge
target=omega**K
max_clock=float(np.max(abs(target[:,None]*iso-iso*source[None,:])))
assert max_clock<1e-12
# If the physical FI clock is scalar omega on ALL 40 source lines,
# a 243D three-carrier target has only 3 H27-invariant vectors in
# that selected eigenvalue and cannot contain 8 source invariants.
# The 8-orbit assignment changes the source clock; it does not
# demonstrate FI compatibility of the actual 40 W33 lines.
out={"status":"PASS_EXACT_H27_X_C3_CLOCK_EXTENSION_WITH_CHARGE_ASSIGNMENT_FIREWALL",
"H27_orbits":sorted(map(len,orbits)),
"scalar_FI_char_omega_minimum_number_of_81D_K81_slices":scalar_minimum,
"TOE52_H27_only_minimum_slices":{"spread15":1,"cusp25":2,"line40":3},
"proof_scalar_no_go":"Each K81=Reg(H27)xReg(C3) contains exactly ONE trivial H27 character in the fixed external C3 eigenspace omega; source FI scalar omega forces all its H27-invariants into this eigenspace. Hence >=3,5,8 K81 copies for the spread15,cusp25,line40 sectors. A 3-K81 H27-only embedding of line40 cannot be scalar-FI equivariant.",
"graded_source_clock_isometry":{"source_dimension":40,"target_dimension":243,
 "orbit_charge_assignment":orbit_assignments,
 "orbit_charges_per_line":charge.tolist(),
 "max_H27_equivariance_error":max_H,
 "max_C3_equivariance_error":max_clock,
 "isometry_inf_norm_error":float(np.max(abs(iso.conj().T@iso-np.eye(40))))},
"graded_source_clock_interpretation":"A non-scalar C3 clock assigning eigenspaces by W33 H27 orbits admits an explicit 40->243 H27xC3 isometry in the three preexisting K81 carriers; this is a constructed mathematical extension. No Holotrade Qpsi charge rule on W33 40 lines has been derived. Distinguish this arbitrary graded clock from the physical FI clock scalar on the 27 frame addresses.",
"physical_gate":"The exact action of external C3 on physical W33 40 line observables and the ordering of each Holotrade K81 carrier must be derived from the model. Do NOT claim graded assignment matches FI D12^4 or a compiled optical Hamiltonian."}
(R/"data/w33_20261013_toe53_h27_c3_extension.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":out["status"],"scalar":scalar_minimum,
  "H_err":max_H,"C3_err":max_clock,"iso_err":out["graded_source_clock_isometry"]["isometry_inf_norm_error"]}))
