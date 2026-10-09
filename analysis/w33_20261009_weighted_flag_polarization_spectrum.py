"""New exact W33 160-port polarization interpolation.
B(t)^T B(t)=t M^T M+(1-t)D^T D where M,D
are 40x160 missing-point and parent-line flag indicators.
At 0<t<1 its spectrum (positive) is that of
[4t I, sqrt(t(1-t)) R; sqrt(t(1-t))R.T,4(1-t) I]
with R=point-line W33 incidence, singular values 4^1,
sqrt(6)^24,0^15. The 160x160 spectrum is:
0^81, 4^1,
(2+-sqrt(4(2t-1)^2+6t(1-t)))^24,
(4t)^15, (4(1-t))^15.
At t=0 or1 rank40, kernel120. At t=1/2 both 15s
are exactly degenerate at 2, but NO threshold crossing:
all nonzero branches stay >0 in interior.
This is a duality preserving quantum photonic graph.
"""
import json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_correlated_disorder_dual_couplers import construct
def certificate():
 B,A6,A30,M,D,P=construct()
 assert M.shape==D.shape==(40,160)
 RR=M@D.T
 assert np.max(abs(M@M.T-4*np.eye(40)))<1e-10
 assert np.max(abs(D@D.T-4*np.eye(40)))<1e-10
 eig=np.linalg.eigvalsh(RR@RR.T)
 assert np.max(abs(eig[:15]))<1e-9 and np.max(abs(eig[15:39]-6))<1e-9 and abs(eig[-1]-16)<1e-9
 rows=[]
 for t in (0,.001,.01,.1,.25,.5,.75,.9,.99,.999,1):
  K=t*M.T@M+(1-t)*D.T@D
  actual=np.linalg.eigvalsh(K)
  delta=math.sqrt(4*(2*t-1)**2+6*t*(1-t))
  spec=[0.]*81+[4.]+[2-delta]*24+[2+delta]*24+[4*t]*15+[4*(1-t)]*15
  assert max(abs(actual-np.sort(spec)))<5e-9
  nzeros=int(sum(abs(actual)<1e-8))
  assert nzeros==(120 if t in (0,1) else 81)
  rows.append(dict(t=t,zero_dimension=nzeros,min_positive=float(min(x for x in actual if x>1e-8)),
    numerical_vs_formula_maxerror=float(max(abs(actual-np.sort(spec))))))
 return dict(status='PASS',flag_dimension=160,universal_flatband_dimension=81,
    endpoint_flatband_dimensions=[120,120],midpoint_dual_15_plus_15_degeneracy_at_positive_eigenvalue=2,
    exact_formula='spec K_t = 0^81 +4^1 +(2+-sqrt(4(2t-1)^2+6t(1-t)))^24+(4t)^15+(4(1-t))^15 for 0<t<1. At t=0,1 additional 39 zeros from endpoint rank loss.',
    fixed_symmetry='PSp acts on incidence columns. Exchanging point and line sends t to 1-t and swaps two inequivalent 15-dimensional point/line sectors, leaving eigenvalues invariant.',
    critical_observation='The entire 81D topological incidence cycle kernel persists for t interior. The endpoint 120D zero sector is NOT protected by generic mixing. Unlike earlier A6/A30, this strictly positive weighted incidence model has no 96/105 internal zero crossing.',
    finite_hardware='A squared-incidence positive-semidefinite single-photon hopping kernel; no actual optical device, TOE or emergent spacetime.',
    samples=rows)
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_weighted_flag_polarization_spectrum.json').write_text(json.dumps(d,indent=2)+'\n')
 print('POLARIZATION',[(x['t'],x['zero_dimension'],round(x['min_positive'],7)) for x in d['samples']])
