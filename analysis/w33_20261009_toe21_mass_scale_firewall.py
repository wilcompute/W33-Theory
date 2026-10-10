"""Can 1/2 selected W33 stars + a single free mass coefficient predict
a physical hierarchy? Exact rational eigenratio firewall and
dimensional-transmutation parameter dependence (illustrative RG only).
"""
from pathlib import Path
import json,math
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
def analyze():
 frozen=json.loads((ROOT/'data/w33_20261009_toe_star_defect_spectra.json').read_text())
 R={}
 allvals=[]
 for k,v in frozen['all3160_distinct_vertex_pairs'].items():
  out=[]
  for x in v['nonzero_eigenvalues_of_two_star_harmonic_operator']:
   frac=s.Rational(str(x)).limit_denominator(10**6)
   assert abs(float(frac)-x)<1e-10
   out.append(frac)
  allvals+=out
  ratio=max(out)/min(out)
  R[k]=dict(nonzero_eigenvalues=[str(z) for z in out],largest_smallest_exact=str(ratio),
   distinct_positive=len(set(out)),rank=len(out))
 assert max(allvals)/min(allvals)==2
 assert max(s.Rational(x['largest_smallest_exact']) for x in R.values())==2
 # Fundamental dimensional analysis: H=lambda Q for dimensionless Q. Vary
 # lambda>0 preserves all normalized ratios, changes every energy scale.
 scales={}
 for b in (s.Rational(1,20),s.Rational(1,10)):
  for g0 in (.7,1.,1.3):
   ratio=math.exp(-1/(2*float(b)*g0*g0))
   scales[f'b={b},g0={g0}']=ratio
 # The scale is an initial-condition+beta coefficient, not geometric.
 out=dict(status='PASS',source='Round21 native star-selector full all-3160 exact eigenvalues and older Pass11313-11319 RG analysis',
   eigenratio_by_type=R,global_nonzero_min='9/20',global_nonzero_max='9/10',
   maximum_cross_type_nonzero_eigenratio='2',
   no_hierarchy_theorem='For the positive semidefinite single-star/two-star defect operators H=lambda P_H(P_S or P_S+P_T)P_H with lambda>0, every NONZERO eigenvalue is between (9/20)*lambda and (9/10)*lambda, so their entire available nonzero mass-squared ratio is at most 2; within one pair type the ratio is <=2. Zero eigenvalues remain protected by the low-rank assumption. This does not represent observed charged-particle hierarchies without extra operators, nonlinear effects, baseline cancellations or mixing.',
   mass_units_no_go='All matrices and graph data are dimensionless. If H(lambda)=lambda Q, then H(c lambda) has the same symmetry/eigenvectors/ratios, but every energy eigenvalue is multiplied by c. The W33 incidence data provide no unit, boundary calibration or external physical scale to determine c.',
   arbitrary_beta_example='A separately POSTULATED one-loop asymptotically-free beta dg/d(log mu)=-b*g^3 gives Lambda/mu0=exp[-1/(2*b*g0²)] for b>0. Neither b, g0 nor mu0 is fixed by W33 graph topology alone. Changing these freely changes the apparent hierarchy by orders of magnitude.',
   RG_scale_examples=scales,
   prior_scope='Repo passes 11313-11319 already tested independently supplied beta functions, radiative scales and portal dynamics; do not present textbook dimensional transmutation as new.',
   physically_falsifiable_gate='A predictive TOE must derive beta coefficient, normalizations, symmetry-breaking vacuum, physical scale and an independent measured hierarchy before fitting parameters. A geometric ratio not matching a Standard Model observable is not itself a prediction.')
 (ROOT/'data/w33_20261009_toe21_mass_scale_firewall.json').write_text(json.dumps(out,indent=2)+'\n')
 print('SCALES ratio<=2 exact; beta examples',scales,flush=True)
 return out
if __name__=='__main__':analyze()
