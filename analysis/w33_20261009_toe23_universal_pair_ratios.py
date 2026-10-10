"""Round23 exact W33 Bose-Hubbard strong attraction universal band ratios.
The dimensionless ratios require U/t -> infinity but no fitted energy scale.
They are falsifiable predictions for a specified quantum-simulator model,
NOT Standard Model mass ratios or fundamental TOE predictions.
"""
from pathlib import Path
import json,sys,math
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe22_two_boson_quantum_selector import build
from w33_20261009_toe_integral_clique_levi_bridge import chain
OUT=ROOT/'data/w33_20261009_toe23_universal_pair_ratios.json'
def run():
 H,diag,basis=build()
 _,_,_,_,_,_,flags,_,_,_,_,_,_=chain()
 A=np.zeros((80,80),dtype=np.int64)
 for p,l in flags:A[p,40+l]=A[40+l,p]=1
 ix=[i for i,(a,b) in enumerate(basis) if a==b]
 assert len(ix)==80
 PH=H[ix,:]
 K=(PH@PH.T).toarray()
 target=8*np.eye(80,dtype=np.int64)+2*A
 assert np.allclose(K,target,atol=1e-13)
 adjacency_eig=np.linalg.eigvalsh(A)
 assert len(adjacency_eig)==80
 cuts=(-4.,-math.sqrt(6),0.,math.sqrt(6),4.)
 mults=[int(np.count_nonzero(abs(adjacency_eig-v)<1e-8)) for v in cuts]
 assert mults==[1,24,30,24,1]
 lowgaps={f'band_{v}':float((4-v)/(4-math.sqrt(6))) for v in (0,-math.sqrt(6),-4)}
 lowgaps['band_sqrt6']=1.
 rows={}
 for U in (16,32,64,128):
  val,_=eigsh(H-diags(U*diag),k=2,which='SA',tol=2e-9,maxiter=2500)
  val.sort()
  gap=float(val[1]-val[0])
  asym=2*(4-math.sqrt(6))/U
  rows[str(U)]=dict(exact_numerical_gap=gap,leading_pair_gap=asym,relative_error=(gap/asym)-1)
  print('PAIR',U,'gap',gap,'asym',asym,'relative',gap/asym-1,flush=True)
 assert abs(rows['128']['relative_error'])<abs(rows['16']['relative_error'])
 out=dict(status='PASS',Hilbert_dimension=3240,native_Levi_degree=4,
  exact_second_order_Schrieffer_Wolff_numerator='K=P H_hop (1-P) H_hop P = 8 I_80 + 2 A_Levi as an integer matrix',
  nonzero_adj_eigenvalue_multiplicities={'-4':1,'-sqrt6':24,'0':30,'sqrt6':24,'4':1},
  effective_low_energy_boson_pair_H='H_eff=-U I -(t^2/U)(8I+2A)+O(t^4/U^3) in N=2 doublon sector, U>>t.',
  universal_band_gap_ratio_from_ground=lowgaps,
  exact_gap_ratio_forms={'gap_to_zero_over_first':'4/(4-sqrt6)',
   'gap_to_minus_sqrt6_over_first':'(4+sqrt6)/(4-sqrt6)',
   'gap_to_minus4_over_first':'8/(4-sqrt6)'},
  rigorous_scope='Second-order degenerate perturbation theory fixes all leading splitting ratios, independently of t or U, once the attractive Bose-Hubbard model on this exact native graph is assumed. This is a parameter-independent quantum-simulator signature in the U/t->infinity limit, not a prediction of an observed particle mass/coupling. Finite U corrections persist.',
  finite_U_numeric=rows,
  missing_TOE_scale='Nothing in finite graph geometry chooses t, U, species, particle density or coupling to relativistic matter. A universal ratio measured in a device realizing a postulated Hamiltonian does not establish a fundamental Theory of Everything.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
