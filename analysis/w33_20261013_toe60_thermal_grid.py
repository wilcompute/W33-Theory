"""TOE60 supplemental: test thermal flux signs beyond failed spectral majorization.

No all-temperature theorem; 8 corners and finite beta grid only.
"""
from pathlib import Path
import numpy as np,json,sys
from itertools import product
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep
ed,vs,*_=prep();E=np.asarray(ed,int);V=np.asarray(vs,int)
def evals(c):
 H=np.zeros((80,80))
 for (a,b),w in zip(E,V):
  H[a,b]=H[b,a]=-(-1)**int(w@np.asarray(c))
 return np.linalg.eigvalsh(H)
corners=list(product((0,1),repeat=3))
bands=[evals(c) for c in corners];bs=[.1,.2,.4,.8,1.,2.,4.,8.,20.,50.]
def F(vals,beta):
 return float(-np.logaddexp(0.,-beta*vals).sum()/beta)
rows=[]
for k,c in enumerate(corners):
 tab=[{"beta":b,"DeltaF":F(bands[k],b)-F(bands[0],b)} for b in bs]
 EZ=float(-.5*(np.abs(bands[k]).sum()-np.abs(bands[0]).sum()))
 rows.append({"corner":list(c),"values":tab,
              "zero_temperature_fermion_filled_sea_shift":EZ,
              "strict_lower_at_all_sampled_beta":bool(all(t["DeltaF"]<-1e-11 for t in tab)) if k else None})
 print("TOE60 thermal",c,"zeroT",EZ,"at beta .1",tab[0]["DeltaF"],flush=True)
assert all(r["strict_lower_at_all_sampled_beta"] for r in rows[1:])
out={"status":"PASS_TOE60_NUMERIC_ALL_SAMPLED_HALF_FILLED_FLUX",
"reference":"One finite static 80-site nearest-neighbor spinless fermion at chemical potential mu=0 with actual W33 three-deck Z2 characters.",
"tested_inverse_temperatures":bs,"rows":rows,
"exact_zero_temperature_formula":"For bipartite hopping H the spectrum is ± paired, so at mu=0 the spinless grand ground energy is F_infinity(H)=-(1/2) Tr|H|. This does not establish an all-beta free-energy inequality; the seven nontrivial pi corners are preferred numerically at listed finite betas and at zero temperature.",
"majorization_caveat":"The strong Ky-Fan majorization of squared energies needed for a simple convexity theorem was explicitly numerically FALSE in the separate TOE60 majorization probe. Numerical sampling across positive betas is not a continuum proof and does not show these corners are global minimizers among all U1 connections.",
"prior_work":"Pass11964 already identified three-pi holonomy at beta4. Lieb flux-phase theorem for planar bipartite periodic graph does not transfer to this nonplanar W33 Levi cover without checking hypotheses."}
(R/"data/w33_20261013_toe60_thermal_grid.json").write_text(json.dumps(out,indent=2)+"\n")
