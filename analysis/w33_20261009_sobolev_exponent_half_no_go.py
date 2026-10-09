"""Upper limit s<=1/2 on ANY homogeneous global Sobolev coercivity
of the full 160-current W33 Hamiltonian, via the exact normalized
oscillatory Gaussian packets proved in round7.

If H>=c*(1+P²)^s-C in quadratic forms with c>0 and s>1/2,
the LHS is O(L) while RHS is Omega(L^(2s)).
An explicit probabilistic lower estimate for the Gaussian momentum
measure makes the asymptotics independent of hand-waving.
This is a quantitative NO-GO, NOT a positive lower spectral bound.
"""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from fractions import Fraction as F
from w33_20261009_no_uniform_ellipticity_packet import certificate as old
def certificate():
  prev=old()
  A,B,C=(F(prev[k]) for k in ['A','B','C'])
  # Gaussian packet Fourier momentum has mean L*k, variance L/2 per
  # physical coordinate, and |k|²=2. Markov gives
  # P(|P-Lk| >= (1/2)L|k|) <= (78L/2) / (L²*2/4) =78/L.
  rows=[]
  for exponent in (F(1,2),F(3,5),F(3,4),F(1)):
    r=[]
    for Lam in (100,1000,10000,100000):
      H=float(A*Lam+B+C/F(Lam))
      # rigorous finite-L lower bound for <(1+P²)^s>
      Sob=max(0,1-78/Lam)*(1+Lam**2/2)**float(exponent)
      r.append(dict(Lambda=Lam,energy=H,sobolev_expectation_lower=Sob,
                    upper_ratio_H_over_Sobolev_lower=H/Sob))
    rows.append(dict(s=str(exponent),threshold_asymptotic='H/Sobolev -> 0 for s>1/2' if exponent>F(1,2) else 'possible finite limit',samples=r))
  for a in rows[1:]:
    assert a['samples'][-1]['upper_ratio_H_over_Sobolev_lower']<a['samples'][0]['upper_ratio_H_over_Sobolev_lower']
  return dict(status='PASS',dimension=78,
      gaussian_packet_exact_H=['1599/5','1681/10','39/5'],
      all_s_strictly_greater_than_half_excluded=True,
      markov_lower='For Lambda>78: <(1+P²)^s> >= (1-78/Lambda)(1+Lambda²/2)^s for the normalized explicit packet.',
      no_go='For every s>1/2 and every c>0,C finite, H>=c*(1+P²)^s-C is false as a quadratic-form inequality on Schwartz vectors of the 78D W33 system.',
      powers=rows,
      boundary='s=1/2 is not established. In particular no positive full-H ground-energy lower bound, numerical spectral gap, or uniform global subelliptic inequality derived.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_sobolev_exponent_half_no_go.json').write_text(json.dumps(d,indent=2)+'\n')
  print('SOBOLEV EXPONENT',d['no_go'])
