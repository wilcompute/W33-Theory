"""Exact all-eighty high-dimensional flat classical zero planes of W33 current symbols.

For point-star q_e=a*(39 at point e,-1 at other points,0 line coords),
and line-star q_e=-a*(39 at line e,-1 at other lines,0 points),
exactly four of 160 affine z-factors survive; their U directions have
integer Gram diag3120, offdiag1520. Their common p-nullspace in the
78D physical augmentation has dimension 74. Explicit reference
p_e/a=-(sum_{four} 40U_e)/192 annihilates all four active current
factors, and ANY p=p_e+delta with U_active delta=0 is an exact
classical zero, not merely a Hessian-flat infinitesimal perturbation.

The quantum operator may still have compact resolvent/gap due to
uncertainty and Hörmander commutators. No global gap follows.
"""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11769_quantized_current_vacuum as H
def certificate():
 geo=H.geometry()
 U=np.rint(40*geo['u']).astype(np.int64);V=np.rint(40*geo['v']).astype(np.int64)
 assert U.shape==V.shape==(160,80)
 modes=[]
 grams=np.full((4,4),1520,dtype=np.int64);np.fill_diagonal(grams,3120)
 for anchor in range(80):
  sgn=1 if anchor<40 else -1
  qi=np.zeros(80,dtype=np.int64);b=0 if anchor<40 else 40
  qi[b:b+40]=-sgn;qi[anchor]=39*sgn
  X=V@qi+40
  active=np.flatnonzero(X)
  assert len(active)==4 and all(X[active]==1600)
  assert np.count_nonzero(X)==4
  ua=U[active]
  assert np.array_equal(ua@ua.T,grams)
  pnum=-np.sum(ua,axis=0)
  # Momentum is p/a=pnum/192; verify U0 p/a+40 annihilates active four
  assert np.array_equal(ua@pnum,np.full(4,-7680,dtype=np.int64))
  Y=U@pnum+40*192
  assert np.array_equal(X*Y,np.zeros(160,dtype=np.int64))
  assert np.sum(qi[:40])==np.sum(qi[40:])==0
  assert np.sum(pnum[:40])==np.sum(pnum[40:])==0
  modes.append(dict(anchor=anchor,type='point' if anchor<40 else 'line',active_flags=active.tolist(),
                    sample_momentum_numerator=pnum.tolist() if anchor in (0,40) else None))
 assert len({tuple(m['active_flags']) for m in modes})==80
 return dict(status='PASS',exact_classical_zero_planes=80,
    point_orbit_planes=40,line_orbit_planes=40,
    affine_momentum_plane_dimension=74,normal_gram_eigenvalues=[1600,1600,1600,7680],
    exact_active_flag_gram=grams.tolist(),
    reference_modes=[m for m in modes if m['anchor'] in (0,40)],
    all_80_active_flag_sets=[m['active_flags'] for m in modes],
    theorem='Every one of 80 distinct star q vectors has exactly 4 surviving z; their 40U rows have rank4. The explicit p_e/a=-(sum four integer Urows)/192 solves all four active symbols. Hence for every delta in the 78D physical subspace annihilated by these four U rows, a 74D affine momentum plane consists entirely of EXACT zeros of all 160 classical currents.',
    not_solved='This forbids proving a global quantum mass gap via a strictly confining classical symbol alone. The quantized model can nevertheless have positive spectral gap from commutators and uncertainty; no global E0 lower enclosure is established.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round15_eighty_classical_zero_planes.json').write_text(json.dumps(d,indent=2)+'\n')
 print('ZERO PLANES',d['exact_classical_zero_planes'],d['affine_momentum_plane_dimension'])
