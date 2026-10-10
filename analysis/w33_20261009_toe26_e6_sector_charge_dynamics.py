"""Round26: dynamical stability/selection test for the 45 E6 tritangent
components. Full PSp permits tunneling A2, so sector charge needs an
extra conservation law. First-order degenerate splitting calculated exactly.
"""
import json,sys,numpy as np
from pathlib import Path
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe23_dynamic_apartment_frame import build
OUT=ROOT/'data/w33_20261009_toe26_e6_sector_charge_dynamics.json'
def run():
 apt,A3,A2=build()
 n,lab=connected_components(A3,directed=False)
 assert n==45 and all(np.bincount(lab)==36)
 P=np.eye(45,dtype=np.int64)[lab]
 Q=(P.T@A2@P)/36
 B=np.rint((Q-18*np.eye(45))*4/9).astype(np.int64)
 assert np.allclose(Q,18*np.eye(45)+(9/4)*B)
 assert np.all(B.sum(axis=1)==32)
 assert np.array_equal(B@B,32*np.eye(45,dtype=int)+22*B+24*(np.ones((45,45),dtype=int)-np.eye(45,dtype=int)-B))
 ev=np.linalg.eigvalsh(Q);rounded=np.round(ev,8)
 spec={str(float(x)):int(np.count_nonzero(rounded==x)) for x in sorted(set(rounded))}
 assert spec=={'9.0':20,'22.5':24,'90.0':1}
 # Sector projectors commute with all A3 internal hops.
 P0=np.zeros(1620,dtype=np.int8);P0[lab==0]=1
 assert not np.any(A3[P0.astype(bool),:][:,~P0.astype(bool)].data)
 assert A2[P0.astype(bool),:][:,~P0.astype(bool)].nnz>0
 # 45D degenerate perturbation: E0=-8, perturbation -eps Q.
 # Ground eigenvalue lambda_max Q=90, next 22.5 -> first-order
 # gap 67.5 eps. Actual full 1620D spectrum deviates at O(eps²).
 actual=[]
 for eps in (.001,.003,.01):
  H=A3.astype(float)+eps*A2
  vals=np.sort(eigsh(H,k=3,which='LA',return_eigenvectors=False,tol=2e-9))
  gap=float(vals[-1]-vals[-2])
  predicted=67.5*eps
  actual.append(dict(epsilon=eps,full_gap=gap,projected_first_order_gap=predicted,
   relative_correction=gap/predicted-1))
  print('E6 CHARGE',eps,gap,predicted,flush=True)
 assert abs(actual[0]['relative_correction'])<.01
 rec=dict(status='PASS',
  prior='Round23 45x36 components, Round24 exact E6-tritangent identification, Round25 SRG45 compression Q=18I+(9/4)B already established.',
  sector_count=45,states_per_sector=36,
  exact_projected_tunneling_eigenspectrum=spec,
  first_order_vacuum_gap_per_epsilon='67.5',
  finite_tunneling_gap=actual,
  sector_projectors_commute_with_A3=True,
  sector_projectors_commute_with_A2=False,
  no_go='A3 sector projectors define a complete commuting set of 45-sector superselection charges only IF all added terms preserve that block partition. A2 is simultaneously PSp-invariant, geometrically local in the chosen frame-overlap metric, and violates each sector projector. It lifts the 45-fold degeneracy already at first order. Invariant diagonal potentials on the transitive 45 E6 tritangent carrier are necessarily constant, so full PSp symmetry alone cannot energetically select one preferred sector.',
  physical_condition='To prohibit A2 one must specify an additional conserved non-scalar operator, selection rule, emergent gauge charge, or engineered superselection restriction. None follows from W33 geometry by itself.',
  caution='Q is only the degenerate first-order compression; A2 does not preserve sector-uniform vectors. Exact finite-epsilon splittings were computed on the full 1620D matrix. Not a fundamental vacuum law.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
