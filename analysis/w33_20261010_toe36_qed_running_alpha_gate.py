"""TOE36/5 QED running and independent W33 bare alpha validation.

Thomson alpha(0) CODATA22 vs exact W33 137+40/1111.
One-loop on-shell renormalized spacelike vacuum polarization:
alpha^-1(Q²) = alpha^-1(0) - (2/pi) int_0^1
 x(1-x) log(1 + Q²*x*(1-x)/m_e²) dx .
This function is monotone DECREASING in spacelike Q².
Solving for fictitious Q if W33 is treated as alpha^-1(0)
illustrates an arbitrary comparison scale, NOT a repair of
CODATA Thomson alpha(0).
"""
from pathlib import Path
from fractions import Fraction
import json,math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe36_qed_running_alpha_gate.json'
def vacuum_shift(x):
 integrand=lambda z: z*(1-z)*math.log1p(x*x*z*(1-z))
 return 2/math.pi * quad(integrand,0,1,epsabs=1e-15)[0]
def run():
 graph=Fraction(137)+Fraction(40,1111)
 pred=float(graph)
 alpha0=137.035999177
 sigma=.000000021
 discrepancy=pred-alpha0
 assert discrepancy>0
 # all Q² >=0 shift positive, alpha_inv(Q)<alpha_inv(0)
 for x in (.0001,.001,.01,.1,1,10):
  assert vacuum_shift(x)>0
  assert vacuum_shift(x/2)<vacuum_shift(x)
 hypothetical=brentq(lambda x:vacuum_shift(x)-discrepancy,0,1)
 implied_keV=hypothetical*.51099895069*1000
 assert .013<hypothetical<.016
 source_wrong_if_assigned_Thomson=(pred-alpha0)/sigma
 # independent low energy expansion Δ=(Q/me)^2/(15π)+O(Q4)
 smallq_est=math.sqrt(15*math.pi*discrepancy)
 assert abs(smallq_est/hypothetical-1)<.0001
 result=dict(status='PASS',
  W33_alpha_inv_exact=str(graph),
  W33_alpha_inv=pred,CODATA22_Thomson_alpha_inv=alpha0,
  CODATA22_sigma=sigma,naive_discrepancy_in_sigma=source_wrong_if_assigned_Thomson,
  photon_one_loop_momentum_scheme='On-shell-subtracted QED spacelike vacuum polarization, electron loop, Q²>0',
  exact_one_loop_formula='alpha_inv(Q²) = alpha_inv(0) - (2/pi) integral_0^1 dx x(1-x) log[1 + (Q²/m_e²)x(1-x)]',
  sign='Spacelike QED running ALWAYS makes alpha_inv(Q²) smaller than alpha_inv(0).',
  inferred_arbitrary_Q_over_me_to_match_CODATA_if_W33_is_Thomson_baseline=hypothetical,
  inferred_arbitrary_Q_keV=implied_keV,
  smallQ_approximation_sqrt_15piDelta=smallq_est,
  independent_physics='CODATA inverse alpha is Thomson/zero-momentum coupling, Q=0. Comparing W33 at Q=0 to CODATA at Q=0 leaves 210.6 sigma discrepancy. Selecting nonzero spacelike momentum Q merely to fit the number introduces an external unfixed parameter and changes the observable; it is NOT a parameter-free validation.',
  leading_beta_sign='One-loop screening gives alpha running toward stronger coupling for spacelike Q, so positive delta alpha_inv from Q=0 is impossible. Any alternative scheme/electron-mass/UV boundary condition must be separately specified and derived before comparison, and tested on independent observables.',
  sources=['https://physics.nist.gov/cuu/pdf/RevModPhys.97.025002.pdf','https://qft.org/gauge-theories-standard-model/quantum-electrodynamics/vacuum-polarization-running-charge/'],
  scope='One-loop only, electron contribution, fixed physical m_e and QED on-shell scheme. No derivation of photon gauge field, e, beta function or renormalization from W33 graph has been provided.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('TOE36 QED correction fake scale Q/me',hypothetical,'keV',implied_keV,'zero-momentum sigma',source_wrong_if_assigned_Thomson,flush=True)
 return result
if __name__=='__main__':run()
