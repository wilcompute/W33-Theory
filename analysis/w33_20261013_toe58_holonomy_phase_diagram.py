"""TOE58 front5: physical-vacuum predictivity gate using W33 harmonic pi corners.

Eight conjugation-fixed flat U1 Wilson holonomies are evaluated for a
spinless fermion at different chemical potentials and temperatures.
External thermodynamic parameters remain free: no TOE constant predicted.
"""
from pathlib import Path
from itertools import product
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,volts,lookup,octs,comm,*_=prep()
e=np.asarray(ed,dtype=int);v=np.asarray(volts,dtype=int)
assert e.shape==(160,2) and v.shape==(160,3)
# For phi in {0,pi}^3, link U=exp(i vol_e dot phi) is real ±1,
# hence conjugation-invariant even before quotient by vertex gauge.
corners=list(product((0,1),repeat=3))
mats=[]
for c in corners:
 p=np.array(c,dtype=int);s=(-1.)**(v@p)
 H=np.zeros((80,80))
 for j,(a,b) in enumerate(e):H[a,b]-=s[j];H[b,a]-=s[j]
 spec=np.linalg.eigvalsh(H)
 assert np.max(abs(spec+spec[::-1]))<1e-10
 mats.append(spec)
all_ev=np.array(mats)
def F(E,mu,beta):
 return float(-np.logaddexp(0.,-beta*(E-mu)).sum()/beta)
samples=[]
for beta in (.5,2.,4.,12.):
 for mu in (-4.5,-3.,-1.,0.,1.,3.,4.5):
  fs=[F(x,mu,beta) for x in all_ev]
  idx=int(np.argmin(fs))
  samples.append(dict(inverse_temperature=beta,chemical_potential=mu,
      minimizing_pi_corner=list(corners[idx]),free_energy_min=float(fs[idx]),
      zero_minus_min=float(fs[0]-fs[idx]),
      full_three_pi_energy=float(fs[-1]),trivial_energy=float(fs[0]),
      lowest_corner_degeneracy=int(sum(abs(x-fs[idx])<1e-8 for x in fs))))
# For free μ=0 at beta4 reproduces prior11964 (π,π,π), but no
# all-holonomy global minimization is claimed here.
middle=[s for s in samples if s["inverse_temperature"]==4. and s["chemical_potential"]==0.][0]
assert middle["minimizing_pi_corner"]==[1,1,1] and middle["zero_minus_min"]>.7
# Phi reversal maps pi->-pi modulo 2pi, so all corners are
# exactly CP/conjugation-fixed under chosen static spinless model.
# At every mu, beta this subset cannot spontaneously break conjugation.
# Inspect if thermodynamic choices change the selected corner.
unique=sorted({tuple(x["minimizing_pi_corner"]) for x in samples})
out={"status":"PASS_TOE58_HOLONOMY_PARAMETER_PHASE_DIAGRAM_NO_UNIQUE_VACUUM",
"native_sites":80,"native_links":160,"three_deck_voltages":True,
"corners":[list(x) for x in corners],"corner_symmetry":"All static pi-corner connections exp(i volts·phi) have real ±1 link phases, and are exactly invariant under link complex conjugation; no corner by itself signals spontaneous physical CP.",
"fixed_external_mu_and_temperature_grid":samples,
"number_distinct_selected_pi_corners":len(unique),"selected_pi_corners":[list(x) for x in unique],
"half_filling_beta4_reproduces_prior11964":middle,
"limitation":"Grand-canonical finite spinless fermions, selected deck marking, externally supplied filling and temperature, no dynamical gauge ground state. Other generic flat holonomies may beat the eight corners; this grid is NOT a certified global phase diagram. It predicts neither the observed CP phase nor alpha, physical mu, beta, mass, Newton G or cosmology.",
"physics_gate":"Vacuum selection depends on supplied matter filling, T, charges and representation; even at a selected corner it is conjugation-fixed. A TOE must dynamically determine those parameters and generate a nonzero gauge-invariant CP-odd observable, not infer CP from nonzero Wilson angles."}
(R/"data/w33_20261013_toe58_holonomy_phase_diagram.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE58 holonomy",len(unique),unique,"half",middle["zero_minus_min"])
