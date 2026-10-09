"""Symmetry-selective full-H spectral measure inclusion using the exact
full current-square Gaussian residual from parallel Pass11800.

The reference Gaussian is PSp invariant since its covariance and
quadratic phase are polynomials in the PSp-invariant point-line
association blocks. Thus its exact full-H spectral measure is
supported ONLY in the invariant (trivial-isotypic) subspace.

Finite Wick residual variance makes its spectral measure broad;
Chebyshev produces certified spectral probability in specified
trivial-sector intervals. It cannot tell whether the true ground
state is PSp invariant.
"""
import json,math,sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
def ceil_sqrt_grid(x,den=10**9):
 n=(x.numerator*den*den)//x.denominator
 z=math.isqrt(n)
 if F(z*z,den*den)<x:z+=1
 assert F(z*z,den*den)>=x
 return F(z,den)
def certificate():
 prior=json.load(open(ROOT/'data/w33_pass11797_11801_five_physical_fronts.json'))['pass11800']
 mlo,mhi=map(F,prior['trial_energy_interval'])
 vlo,vhi=map(F,prior['full_residual_variance_interval'])
 assert vlo>1000 and vhi<1200
 sig=ceil_sqrt_grid(vhi)
 assert F(33)<sig<F(34)
 windows=[]
 for k in (1,2,3,4):
  left=mlo-k*sig;right=mhi+k*sig
  windows.append(dict(k=k,lower_endpoint=str(left),upper_endpoint=str(right),
    approximate_lower=float(left),approximate_upper=float(right),
    guaranteed_spectral_weight_at_least=str(F(1)-F(1,k*k)),
    interpretation='With k=1, at least one spectral point exists in the interval; k>=2 gives >=1-1/k² of the Gaussian spectral measure inside.'))
 assert windows[0]['approximate_lower']>95 and windows[0]['approximate_upper']<163
 return dict(status='PASS',fullH_Gaussian_energy_interval=prior['trial_energy_interval'],
   fullH_Gaussian_residual_variance_interval=prior['full_residual_variance_interval'],
   outward_sigma_upper=str(sig),
   gaussian_exact_eigenstate=False,
   spectral_windows=windows,
   proof='The full L² spectral measure mu_psi of normalized PSp-invariant Gaussian psi has mean E and variance sigma² from Pass11800 160² exact Wick integrals. As psi is PSp invariant and H commutes with PSp, mu_psi is supported only on true eigenvalues in the trivial PSp representation. Chebyshev ensures mass |lambda-E|<=k*sigma at least 1-1/k². A strictly positive variance excludes this Gaussian itself being an exact eigenstate.',
   provenance='Pass11800 already certified the full-H Gaussian second moment, mean and total-spectrum spectral inclusion. New check isolates the PSp-trivial spectral measure, gives outward rational k=2..4 weight windows, and explicitly distinguishes trial vector from true eigenstate.',
   limit='Does not establish the first ground representation or any actual eigenvalue lower enclosure or gap: even a trivial-sector eigenvalue below 163 can coexist with lower nontrivial-sector states.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_PSp_trivial_spectral_measure.json').write_text(json.dumps(d,indent=2)+'\n')
 print('TRIVIAL SPECTRAL',[(w['k'],w['approximate_lower'],w['approximate_upper']) for w in d['spectral_windows']])
