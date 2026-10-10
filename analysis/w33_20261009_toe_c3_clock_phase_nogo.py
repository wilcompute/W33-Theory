"""Exact order-3 clock character and modular Jordan structure on the
81 integral Levi cycles: under unbroken PSp4(3), no Hermitian quadratic
mass splitting of this complex irreducible Steinberg. A chosen order-3
element allows a 27+27+27 phase *decomposition* but has no canonical choice.
"""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass1081_1086_core import build_w33,transvection_perm,line_perm,rank_mod
from w33_20261009_toe_integral_clique_levi_bridge import chain,integer_cycle_basis

def main():
 pts,ix,lines,li,edges,tris,flags,fi,E,T,DL,M,Lift=chain()
 Z,chords=integer_cycle_basis(flags)
 assert len(chords)==81
 id81=np.eye(81,dtype=np.int64)
 Gram=Z.T@Z
 res=[]
 for j in (0,1,4,5,13):
  g=transvection_perm(pts[j],pts,ix)
  lp=line_perm(g,lines,li)
  fmap=[fi[(g[p],lp[l])] for p,l in flags]
  acted=np.zeros_like(Z);acted[fmap,:]=Z
  X=acted[chords,:]
  assert np.array_equal(Z@X,acted)
  assert np.array_equal(X@X@X,id81)
  assert np.array_equal(X.T@Gram@X,Gram)
  A=X-id81
  ranks=[int(rank_mod(A%3,3)),int(rank_mod((A@A)%3,3))]
  assert ranks==[54,27] and not np.any((A@A@A)%3)
  assert np.trace(X)==np.trace(X@X)==0
  res.append(dict(seed_point=j,char_order3=[81,int(np.trace(X)),int(np.trace(X@X))],
       char3_nilpotent_ranks=ranks,mod3_jordan_three_blocks=27,
       integral_cycle_metric_preserved=True))
 print('CLOCK',res,flush=True)
 out=dict(status='PASS',order3_transvection_witnesses=res,
  irrep_prior='Complex irreducibility of the 81 Steinberg (Levi H1) is prior Pass20260901/BT1688, not new. On every PSp element its character is the same as the clique harmonic H1, prior Pass20260901.',
  theorem='Every sampled transvection has order 3 on H1, trace g=trace g²=0, so over C its eigenvalue multiplicities at (1,w,w²) are exactly (27,27,27). Mod3, g=I+N where N³=0, rank N=54,rank N²=27: the restricted 81 module consists of 27 Jordan blocks of size 3. This exact local regularity is not a selected physical generation clock.',
  quadratic_mass_obstruction='The 81-dimensional complex PSp irreducible Steinberg module has scalar commutant by Schur. Any Hermitian quadratic operator commuting with ALL PSp actions is m²I, and cannot split it into three masses. Choosing a transvection or star is symmetry breaking that requires a dynamical selection rule.',
  odd_dim_alternating_nogo='There is no nondegenerate alternating bilinear form on an 81D vector space, including over F3. A canonical symplectic Pauli phase space uses H1(F3) plus its dual, total dimension 162; standard finite Heisenberg group has order 3^163 and its irrep Hilbert dimension 3^81. The 81-dimensional coefficient module is not the 3^81-dimensional Hilbert space of 81 logical qutrits.',
  physical_boundary='No masses, clock rate, physical generations, Lorentz symmetry, scale or selection potential are derived from these finite representation statements.')
 (ROOT/'data/w33_20261009_toe_c3_clock_phase_nogo.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
