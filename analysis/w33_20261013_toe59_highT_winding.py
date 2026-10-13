"""TOE59: exact W33 high-temperature coefficient of fermionic holonomy free energy.

Lowest nontrivial closed-walk order is n=8; the analytic logcosh
series derives the first flux-dependent thermal coefficient without fits.
"""
from pathlib import Path
from itertools import product
import sympy as sp,numpy as np,json,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/"analysis"))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
ed,volts,lk,octs,comm,*_=prep()
E=np.asarray(ed,int);V=np.asarray(volts,int)
P=np.rint(np.asarray([cycle_row(z,ed,volts,lk,np.zeros(3)).real for z in octs+comm])).astype(int)
assert np.max(abs(P@V))==0
prev=json.loads((R/"data/w33_20261013_toe59_wilson_girth_moments.json").read_text())
x=sp.Symbol('x')
series=sp.series(-sp.log(2*sp.cosh(x/2)),x,0,10).removeO()
coeff=sp.expand(series).coeff(x,8)
assert coeff==sp.Rational(17,645120),coeff
def mat(c):
 s=(-1.)**(V@np.asarray(c,int))
 h=np.zeros((80,80))
 for (a,b),u in zip(E,s):h[a,b]=h[b,a]=-u
 return h
eps0=np.linalg.eigvalsh(mat((0,0,0)))
def F(e,beta):
 return float(-np.logaddexp(0.,-beta*e).sum()/beta)
rows=[]
for row in prev["tested_corners"]:
 c=row["pi_corner"];delta=row["trace_moment_difference"]
 h=mat(c);e=np.linalg.eigvalsh(h)
 leading=float(coeff*delta)
 beta_rows=[]
 for beta in (.1,.15,.2,.3,.5):
  df=F(e,beta)-F(eps0,beta)
  normalized=df/(beta**7)
  beta_rows.append({"beta":beta,"free_energy_difference":df,
                    "quotient_over_beta_seven":normalized,
                    "fractional_deviation_from_leading":abs(normalized-leading)/abs(leading) if leading else 0.})
 if c!=[0,0,0]:
  assert abs(beta_rows[0]["quotient_over_beta_seven"]-leading)/abs(leading)<.04
  assert beta_rows[0]["free_energy_difference"]<0
 rows.append({"pi_corner":c,"delta_trace_H8":delta,"exact_leading_coefficient":str(coeff*delta),
              "leading_coefficient_float":leading,"temperature_checks":beta_rows})
 print("TOE59",c,"lead",leading,"beta.15",beta_rows[0]["quotient_over_beta_seven"],flush=True)
out={"status":"PASS_TOE59_GIRTH8_HIGH_T_FERMION_FLUX_COEFFICIENT",
"native_P_times_deck_voltages_max":int(max(abs(P@V).ravel())),
"exact_fermion_free_energy_series_coeff_of_beta7_traceH8":str(coeff),
"high_temperature_free_energy_series":"At mu=0 on an 80-site bipartite model, F_beta(H)=-beta^-1 Tr log[2 cosh(beta H/2)]. The expansion has -beta Tr H²/8 + beta³ Tr H4/192 - beta⁵ Tr H6/2880 + 17 beta7 Tr H8/645120+... . All twisted trace differences first appear at H8; hence DeltaF=17 beta7 DeltaTrH8/645120+O(beta9).",
"winding_moment_rows":rows,
"convergence_caveat":"The displayed asymptotic series has finite radius from cosh complex zeros; beta=.15 approximates the asymptotic coefficient better than beta=.5. This is a fixed finite graph static spinless fermion, not physical thermodynamics.",
"prior_art":"Trace closed-walk magnetic flux expansions and finite-temperature half-filled flux phases are established techniques; compare Lieb Phys Rev Lett 73,2158 (1994), whose planar hypotheses do not apply automatically to the W33 three-deck graph.",
"physical_limit":"This is a parameter-independent coefficient WITHIN a supplied 80-site hopping Hamiltonian, not a fundamental coupling, spacetime vacuum or experimental prediction."}
(R/"data/w33_20261013_toe59_highT_winding.json").write_text(json.dumps(out,indent=2)+"\n")
