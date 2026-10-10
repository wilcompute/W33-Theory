"""Full 3240-state two-boson attractive Bose-Hubbard W33 Levi Hamiltonian:
finite-system Perron-Frobenius test of the previous focusing selector idea.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,diags
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe_integral_clique_levi_bridge import chain
OUT=ROOT/'data/w33_20261009_toe22_two_boson_quantum_selector.json'
def build():
 _,_,_,_,_,_,flags,_,_,_,_,_,_=chain()
 adj=[set() for i in range(80)]
 for p,l in flags:
  adj[p].add(40+l);adj[40+l].add(p)
 basis=[(i,j) for i in range(80) for j in range(i,80)]
 idx={v:k for k,v in enumerate(basis)}
 assert len(basis)==3240
 ii=[];jj=[];vv=[]
 for k,(a,b) in enumerate(basis):
  occ={a:2} if a==b else {a:1,b:1}
  for x,n in occ.items():
   for y in adj[x]:
    m=occ.get(y,0)
    nxt=dict(occ);nxt[x]-=1
    if not nxt[x]:nxt.pop(x)
    nxt[y]=m+1
    tup=tuple(sorted([z for z,count in nxt.items() for _ in range(count)]))
    dest=idx[tup]
    ii.append(dest);jj.append(k);vv.append(-math.sqrt(n*(m+1)))
 hop=coo_matrix((vv,(ii,jj)),shape=(3240,3240)).tocsr()
 assert (hop-hop.T).nnz==0
 dbl=np.array([a==b for a,b in basis],dtype=np.float64)
 return hop,dbl,basis
def run():
 hop,dbl,basis=build()
 observations={}
 for U in (0,3,8,16,32):
  H=hop-diags(U*dbl)
  evals,vecs=eigsh(H,k=2,which='SA',tol=2e-9,maxiter=2500)
  gap=float(evals[1]-evals[0])
  psi=vecs[:,0];dens=np.zeros(80)
  for (a,b),prob in zip(basis,abs(psi)**2):
   dens[a]+=prob;dens[b]+=prob
  maxdev=float(np.max(np.abs(dens-2/80)))
  p2=float(np.dot(dbl,abs(psi)**2))
  assert gap>0 and maxdev<2e-6
  observations[str(U)]={'energy0':float(evals[0]),'gap':gap,
   'doublon_probability':p2,'max_site_density_error_from_2_over_80':maxdev}
  print('BOSON',U,'E',round(evals[0],6),'gap',round(gap,6),
      'doublon',round(p2,6),'maxsymbreak',maxdev,flush=True)
 assert abs(observations['0']['energy0']+8)<1e-7
 assert observations['32']['doublon_probability']>0.98
 assert observations['32']['gap']<observations['0']['gap']
 out={'status':'PASS','Hilbert_dimension':3240,'graph_sites':80,'boson_number':2,
  'model':'H=-sum_undirected_edges(b†_i b_j+h.c.)-U/2 sum_i n_i(n_i-1), t=1, U>=0',
  'calculations':observations,
  'exact_theorem':'For every finite U and positive hopping t, the 3240-configuration graph is connected and the Hamiltonian is real symmetric, with negative off-diagonals. The Perron-Frobenius theorem gives a strictly positive UNIQUE ground state. Because the Hamiltonian commutes with all native W33 graph automorphisms, the ground state is symmetry invariant. Hence expected site occupation is exactly 2/80 at each site even when doublon pairing becomes strong. Finite two-boson symmetry does not spontaneously select a site.',
  'strong_attraction_effective_hopping':'For U>>t, pair states virtually hop between adjacent nodes with effective pair hopping magnitude 2 t²/U and diagonal shift -8t²/U (degree4), predicting leading low-band gap 2t²(4-sqrt6)/U. The exactly diagonalized 3240D spectrum can test this approximation.',
  'limit_scope':'Finite-two-boson ground-state uniqueness is exact; extrapolating to finite density N~80 or thermodynamic SSB is not justified. The quartic mean-field functional from Round21 is an added semiclassical assumption and cannot override this finite quantum result.'}
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
