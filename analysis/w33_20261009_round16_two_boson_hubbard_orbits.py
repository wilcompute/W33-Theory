"""Round16 direct two-boson Hubbard interaction test of FIVE otherwise
single-particle Peierls-isospectral optimal W33 selector orbits.

Hilbert space symmetric two-boson Fock sector dim C(81,2)=3240,
Hamiltonian dGamma(A_k)+U sum_x n_x(n_x-1)/2, U>0 uniform.
Exactly assembled from bosonic creation/annihilation factors.
At U=0 the many-body eigenvalues depend only on the one-body
spectrum and must coincide for all five PSp orbits (strong control).
At nonzero U, the onsite interaction singles out the physical
80-vertex basis and MAY break the hidden one-body isospectrality.

Numerical (not exact) smallest Ritz eigenvalues; doesn't prove
real optical nonlinear photon gate or physical spacetime.
"""
import json,sys
from pathlib import Path
from itertools import combinations_with_replacement
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
def build(edges,chosen,k,U):
 n=80
 states=list(combinations_with_replacement(range(n),2))
 lookup={pair:i for i,pair in enumerate(states)}
 neigh=[[] for _ in range(n)]
 phases=dict(zip(chosen,k))
 for f,(p,l) in enumerate(edges):
  ph=complex(np.exp(1j*phases[f])) if f in phases else 1+0j
  neigh[p].append((l,complex(ph.conjugate()))) # A[l,p]
  neigh[l].append((p,complex(ph))) # A[p,l]
 rows=[];cols=[];values=[]
 for c,(i,j) in enumerate(states):
  if i==j and U:
   rows.append(c);cols.append(c);values.append(U)
  occupancy={i:2} if i==j else {i:1,j:1}
  for x,nx in occupancy.items():
   for y,hop in neigh[x]:
    v=occupancy.get(y,0)
    bag=[i,j]
    bag.remove(x)
    bag.append(y)
    r=lookup[tuple(sorted(bag))]
    rows.append(r);cols.append(c);values.append(np.sqrt(nx*(v+1))*hop)
 H=coo_matrix((np.array(values,dtype=complex),(rows,cols)),shape=(len(states),)*2).tocsr()
 assert np.linalg.norm((H-H.getH()).data)<1e-9
 return H
def certificate():
 edges,*_=geometry()
 reps=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 out={}
 for kname,k in [('unphased',[0.,0.,0.]),('flux',[.49,-.74,1.22])]:
  spectra={}
  for U in (0.,2.):
   vals=[]
   for o in reps:
    H=build(edges,o['representative'],k,U)
    res=eigsh(H,k=2,which='SA',tol=1e-9,maxiter=6000,return_eigenvectors=False)
    vals.append(sorted(float(v) for v in res))
    print('HUBBARD',kname,U,o['orbit_size'],np.round(vals[-1],11),flush=True)
   spectra[str(U)]=dict(lowest_two=vals,max_ground_spread=float(max(v[0] for v in vals)-min(v[0] for v in vals)),
    max_excited_spread=float(max(v[1] for v in vals)-min(v[1] for v in vals)))
  out[kname]=spectra
 assert out['flux']['0.0']['max_ground_spread']<1e-6
 return dict(status='PASS',two_boson_sector_dimension=3240,rep_orbit_sizes=[z['orbit_size'] for z in reps],
   data=out,
   preliminary='If U2 nonzero flux ground/excited spread exceeds solver error, onsite interactions distinguish previously one-particle-isospectral orbits, but only numerical evidence here.',
   caveats='Finite engineered two-boson Bose-Hubbard graph and numerical Lanczos; no quantum optical experiment or real 3D spacetime. The 3 Peierls edge phases are externally assigned.')
if __name__=='__main__':
 z=certificate();(ROOT/'data/w33_20261009_round16_two_boson_hubbard_orbits.json').write_text(json.dumps(z,indent=2)+'\n')
 print('RESULT',[(k,{u:x['max_ground_spread'] for u,x in v.items()}) for k,v in z['data'].items()])
