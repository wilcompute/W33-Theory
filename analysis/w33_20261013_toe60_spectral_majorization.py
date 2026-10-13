"""TOE60 front1: singular-square spectral majorization and free-energy tests.
Searches for strong spectral ordering, with counterexamples reported.
"""
from pathlib import Path
import json,sys,numpy as np
from itertools import product
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,volts,*_=prep();E=np.asarray(ed,int);V=np.asarray(volts,int)
def H(c):
 h=np.zeros((80,80),dtype=np.float64)
 for (a,b),q in zip(E,V):
  s=(-1)**int(q@np.asarray(c))
  h[a,b]=h[b,a]=-s
 return h
s0=np.sort(np.linalg.eigvalsh(H((0,0,0)))**2)[::-1]
out=[]
for c in product([0,1],repeat=3):
 eig=np.linalg.eigvalsh(H(c))
 squares=np.sort(eig*eig)[::-1]
 major=np.cumsum(s0-squares)
 # Include both negative and positive controls
 out.append({"corner":c,"min_partial_majorization_margin":float(min(major)),
             "min_proper_partial_margin":float(min(major[:-1])),
             "k_with_min_margin":int(np.argmin(major[:-1])+1),
             "max_spectral_radius":float(max(abs(eig))),
             "sum_squares":float(sum(squares)),
             "passes_majorization_to_numerical_tol":bool(np.min(major)>-1e-8)})
print(json.dumps(out,indent=2),flush=True)
(R/"data/w33_20261013_toe60_spectral_majorization.json").write_text(json.dumps({"results":out,"scope":"Numerical Ky-Fan partial sum comparisons of squared single-particle energies for eight real Z2 flat holonomies. Strong majorization is not a theorem absent exact eigenvalue control; if violated report the explicit failing partial sum."},indent=2)+"\n")
