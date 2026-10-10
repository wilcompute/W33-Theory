"""TOE41: native W33 three-deck Maxwell polarizations and a locked isotropy null.

Uses ONLY the existing TOE38 Levi closed native plaquettes and Bloch gradient.
Pre-registers strict polarization degeneracy before numerical evaluation;
testing a hypothesis internal to the supplied Hamiltonian, not a physical
vacuum birefringence observation or measured light-speed prediction.
The prior TOE40 x-axis mode splitting was already known, so this is a
frozen regression null, not an independently blinded prospective forecast.
"""
import sys,json
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe36_incidence_relativistic_walk import gradient
OUT=ROOT/"data/w33_20261010_toe41_maxwell_anisotropy_null.json"
LOCKED_NULL={
 "units":"Dimensionless lattice/deck momentum, equal unit curl-edge weights and canonical kinetic energy",
 "strict_two_polarization_degeneracy":True,
 "isotropic_speed_across_each_unit_direction":True,
 "tolerance_for_exact_relativistic_null":1e-3,
 "precomparison_assumption":"The lattice eigenfrequencies omega_1,omega_2 should agree at the same |k| in a strictly isotropic continuum Maxwell candidate",
}
ed,volts,lookup,zero,comm,picked,fc=prep()
walks=zero+comm
r=.015
vectors={"x":(1.,0,0),"y":(0,1.,0),"z":(0,0,1),
         "xy":(1,1,0),"xz":(1,0,1),"xyz":(1,1,1)}
res={}
projector_stats={}
for name,vec in vectors.items():
 direction=np.asarray(vec,dtype=float);direction/=np.linalg.norm(direction)
 k=r*direction
 B=gradient(ed,volts,k)
 P=np.asarray([cycle_row(w,ed,volts,lookup,k) for w in walks])
 assert max(abs((P@B).ravel()))<1e-10
 U,s,Vh=np.linalg.svd(B,full_matrices=True)
 assert len(s)==80 and min(s)>1e-5
 T=U[:,80:]
 C=P@T
 K=C.conj().T@C
 eig=np.linalg.eigvalsh(K)
 assert min(eig)>-1e-8
 assert 0<eig[0]<eig[1]<.01 and eig[2]>1.
 speeds=np.sqrt(eig[:2])/r
 ratio=float(speeds[1]/speeds[0])
 res[name]=dict(direction=direction.tolist(),k_norm=r,
                two_curl_eigenvalues=eig[:2].tolist(),third_gap=float(eig[2]),
                two_low_speed_estimates=speeds.tolist(),polarization_ratio=ratio,
                fractional_birefringence=float((speeds[1]-speeds[0])/np.mean(speeds)))
 if name=="x":
  Q=T@T.conj().T
  projector_stats=dict(hermiticity_defect=float(np.max(abs(Q-Q.conj().T))),
   idempotence_defect=float(np.max(abs(Q@Q-Q))),
   gauss_projector_defect=float(np.max(abs(Q@B))),
   transverse_dimension=int(np.rint(np.trace(Q).real)),
   canonical_bracket="on the Gauss-reduced linear phase space, [A_i,E_j]=i Q_ij, Q=T T^dag; no Fock representation or matter coupling constructed")
  assert max(projector_stats[k] for k in ["hermiticity_defect","idempotence_defect","gauss_projector_defect"])<1e-10
  assert projector_stats["transverse_dimension"]==80
ratios=[x["polarization_ratio"] for x in res.values()]
speeds=np.asarray([x["two_low_speed_estimates"] for x in res.values()])
max_degeneracy=max(abs(1-z) for z in ratios)
max_direction_var=float(np.max(speeds)/np.min(speeds))
null_failed=max_degeneracy>LOCKED_NULL["tolerance_for_exact_relativistic_null"] or max_direction_var>1+LOCKED_NULL["tolerance_for_exact_relativistic_null"]
assert null_failed
out=dict(status="STRICT_ISOTROPIC_MAXWELL_NULL_REJECTED",
  prior_locked_null=LOCKED_NULL,directions=res,
  max_polarization_ratio_defect=float(max_degeneracy),
  all_speed_max_over_min=max_direction_var,
  constraint_projector=projector_stats,
  interpretation="For fixed deck marking and equal plaquette weights, lowest native W33 Maxwell Bloch branches are not strictly degenerate/isotropic. This falsifies a specific finite-lattice strict Maxwell identification; changing weights, taking an RG limit or physical coupling could change the result.",
  boundary="No translation of deck momentum into physical energy/length, no laboratory constraint, no universal c, no claim about astrophysical birefringence.")
OUT.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({k:v for k,v in out.items() if k!="directions"}))
for k,v in res.items():print("DIRECTION",k,v["two_low_speed_estimates"],v["polarization_ratio"],flush=True)
