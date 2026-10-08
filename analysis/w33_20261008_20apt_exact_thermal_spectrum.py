"""Exact full Hilbert-space energy degeneracies for 20-apartment CSS Hamiltonian.

Two independent check-product constraints select even star and even-face
violation counts. Each compatible eigenvalue sector carries 4-dimensional
logical degeneracy. This is a solved finite commuting-projector model,
not 3+1 GR or a thermodynamic transition.
"""
import sys,json,math,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_20apt_Hamiltonian_Z6 import main as baseline
OUT=ROOT/"data/w33_20261008_20apt_exact_thermal_spectrum.json"
def spectrum():
 old=baseline();assert old["ground_space_dimension_exact"]==4
 deg=collections.Counter()
 for k in range(0,41,2):
  for j in range(0,21,2):
   E=-60+2*(k+j)
   deg[E]+=4*math.comb(40,k)*math.comb(20,j)
 assert sum(deg.values())==2**60
 assert deg[-60]==4
 assert deg[-56]==4*(math.comb(40,2)+math.comb(20,2))==3880
 # The normalized polynomial in x=e^-2beta exactly gives partition function:
 # e^(60beta) *4 * E40(x)*E20(x), where E_m is even binomial.
 E40=lambda x:sum(math.comb(40,k)*x**k for k in range(0,41,2))
 E20=lambda x:sum(math.comb(20,k)*x**k for k in range(0,21,2))
 observations=[]
 for beta in (0,.2,.5,1,2):
  zz=sum(v*math.exp(-beta*(e+60)) for e,v in deg.items())
  zz2=4*E40(math.exp(-2*beta))*E20(math.exp(-2*beta))
  assert math.isclose(zz,zz2,rel_tol=1e-12)
  en=sum((e+60)*v*math.exp(-beta*(e+60)) for e,v in deg.items())/zz-60
  observations.append({"beta":beta,"partition_rescaled_exp_minus_60beta":zz,
    "average_energy":en,"ground_state_fraction":4/zz})
 return {"qubits":60,"Hilbert_dimension_exact":2**60,
  "E_to_degeneracy":{str(k):v for k,v in sorted(deg.items())},
  "energy_levels":len(deg),"lowest_energy":-60,"ground_degeneracy":4,
  "first_excited_energy":-56,"first_excited_degeneracy":3880,
  "gap":4,"all_spectrum_accounted_for":True,
  "partition_exact":"Z(beta) = 4 exp(60 beta) E_40(exp(-2 beta)) E_20(exp(-2 beta)); E_n(t)=((1+t)^n+(1-t)^n)/2",
  "temperature_points":observations,
  "finite_system_free_energy_analytic_for_all_finite_real_beta":True,
  "no_finite_size_thermodynamic_phase_transition":True,
  "no_Einstein_hypersurface_deformation_algebra_derived":True,
  "fault_tolerance_not_inferred_from_energy_gap":True}
if __name__=="__main__":
 x=spectrum();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print({k:v for k,v in x.items() if k not in ("E_to_degeneracy","temperature_points")},flush=True)
 print("EXACT_THERMAL_SPECTRUM_PASS")
