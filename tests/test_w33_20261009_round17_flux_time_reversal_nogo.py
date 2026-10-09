"""Interacting W33 Levi-graph flux/time-reversal spectral negative control."""
import sys
from pathlib import Path
from itertools import combinations_with_replacement
import numpy as np
from scipy.sparse import diags
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_5state_ritz import geometry
from w33_20261009_round16_two_boson_hubbard_orbits import build
def maxabs(X):
 return float(np.max(np.abs(X.data))) if X.nnz else 0.0
def test_native_two_boson_flux_reversal_and_interaction_sign():
 edges,*_=geometry()
 reps=[[0,52,68],[0,52,70],[0,52,90]]
 phases=[0.49,-0.74,1.22]
 labels=np.array([(1 if i<40 else -1)*(1 if j<40 else -1)
                  for i,j in combinations_with_replacement(range(80),2)])
 J=diags(labels.astype(float),format="csr")
 for triple in reps:
  Hplus=build(edges,triple,phases,8.0)
  Hfluxrev=build(edges,triple,[-x for x in phases],8.0)
  HnegativeU=build(edges,triple,phases,-8.0)
  assert Hplus.shape==(3240,3240)
  assert maxabs(Hfluxrev-Hplus.conjugate())<1e-12
  assert maxabs(J@Hplus@J+HnegativeU)<1e-12
