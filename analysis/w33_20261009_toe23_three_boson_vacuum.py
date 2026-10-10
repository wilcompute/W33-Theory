"""Round23 finite-density extension of W33 attractive Bose-Hubbard model.
Exactly N=3 on 80 native Levi sites, with 88,560 Fock states.
PF theorem proves finite N quantum vacuum unique for any finite U,t>0.
"""
from pathlib import Path
import sys,json,math,itertools
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain
OUT=ROOT/'data/w33_20261009_toe23_three_boson_vacuum.json'
def build():
 _,_,_,_,_,_,flags,_,_,_,_,_,_=chain()
 adj=[set() for i in range(80)]
 for p,l in flags:adj[p].add(40+l);adj[40+l].add(p)
 basis=list(itertools.combinations_with_replacement(range(80),3))
 idx={v:i for i,v in enumerate(basis)}
 assert len(basis)==math.comb(82,3)==88560
 row=[];col=[];val=[];pairs=np.zeros(len(basis))
 for i,state in enumerate(basis):
  occ={x:state.count(x) for x in set(state)}
  pairs[i]=sum(n*(n-1)//2 for n in occ.values())
  for a,n in occ.items():
   for b in adj[a]:
    m=occ.get(b,0)
    dst=list(state);dst.remove(a);dst.append(b);dst.sort()
    j=idx[tuple(dst)]
    row.append(j);col.append(i);val.append(-math.sqrt(n*(m+1)))
 H=coo_matrix((val,(row,col)),shape=(len(basis),)*2).tocsr()
 assert (H-H.T).nnz==0
 return H,pairs,basis
def run():
 H,pairs,basis=build()
 print('N3 MATRIX',len(basis),H.nnz,'finite hermitian',flush=True)
 out={}
 from scipy.sparse import diags
 for U in (0,4,8):
  vals,vecs=eigsh(H-diags(U*pairs),k=2,which='SA',tol=2e-8,maxiter=900)
  o=np.argsort(vals);vals=vals[o];u=vecs[:,o[0]]
  density=np.zeros(80)
  for i,(a,b,c) in enumerate(basis):
   p=u[i]*u[i];density[a]+=p;density[b]+=p;density[c]+=p
  pfull=float(sum(u[i]*u[i] for i,state in enumerate(basis) if state[0]==state[2]))
  row=dict(E0=float(vals[0]),gap=float(vals[1]-vals[0]),triple_onsite_probability=pfull,
   max_density_deviation=float(np.max(np.abs(density-3/80))))
  print('N3',U,row,flush=True)
  assert row['gap']>0 and row['max_density_deviation']<3e-5
  out[str(U)]=row
 assert abs(out['0']['E0']+12)<1e-6
 record=dict(status='PASS',graph_sites=80,particle_number=3,Fock_dimension=len(basis),
   hopping_sparse_nnz=H.nnz,model='H=-t sum_Levi_edges(b†_i b_j+h.c.)-U/2 sum_i n_i(n_i-1), fixed N=3, t=1',
   computed=out,PF_theorem='For any finite boson number N and t>0, the configuration hopping graph is connected and all nonzero off-diagonals are negative. Perron-Frobenius implies a strictly positive unique finite ground state. Graph symmetry therefore forces occupation <n_i>=N/80 for all sites, irrespective of attractive pair/trimer clustering. Exact finite-N spontaneous symmetry breaking is impossible in this model; symmetry-breaking may be probed via an external pinning field or a controlled large-system limit.',
   boundary='N=3 is a full interacting 88560-dimensional native-graph quantum calculation, not finite density in the thermodynamic sense. No universal phase transition or symmetry-selected absolute site demonstrated.')
 OUT.write_text(json.dumps(record,indent=2)+'\n')
 return record
if __name__=='__main__':run()
