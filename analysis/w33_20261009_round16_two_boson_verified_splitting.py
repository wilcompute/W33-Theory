"""Round16 high-precision interaction audit after full-band one-particle
isospectrality: five PSp orbits in 2-boson onsite Hubbard sector.

Calculate eigenpair residuals, then assert between-orbit differences
exceed numerical residual envelope at U=8 and flux (0.49,-.74,1.22).
All five states have identical U=0 spectra by previous exact theorem.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_round16_two_boson_hubbard_orbits import build
from w33_20261008_5state_ritz import geometry
def certificate():
 edges,*_=geometry(); reps=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 r=[]
 for U in (2.,8.,20.):
  vals=[];err=[]
  for rep in reps:
   h=build(edges,rep['representative'],[.49,-.74,1.22],U)
   eigen,vec=eigsh(h,k=2,which='SA',tol=2e-12,maxiter=12000)
   ordering=np.argsort(eigen);eigen=eigen[ordering];vec=vec[:,ordering]
   residual=np.linalg.norm(h@vec-vec*eigen[None,:],axis=0)
   vals.append([float(z) for z in eigen])
   err.append([float(z) for z in residual])
  groundspread=max(x[0] for x in vals)-min(x[0] for x in vals)
  excitedspread=max(x[1] for x in vals)-min(x[1] for x in vals)
  residual_bound=max(max(x) for x in err)
  r.append(dict(U=U,ground_spread=groundspread,excited_spread=excitedspread,
    maximum_eigenpair_residual=residual_bound,
    orbit_two_lowest_eigenvalues=vals,orbit_residuals=err))
  print('HUBBARD_PREC',U,groundspread,excitedspread,'err',residual_bound,flush=True)
 assert all(x['excited_spread']>100*x['maximum_eigenpair_residual'] for x in r)
 return dict(status='PASS',sector_dimension=3240,interaction='uniform onsite U/2 sum_i n_i(n_i-1)',phase_vector=[.49,-.74,1.22],
   exact_one_particle_isospectral_all_orbits=True,results=r,
   physical_interpretation='A UNIFORM genuine two-photon on-site interaction resolves distinctions invisible to one-photon full-band energy measurements in a finite Peierls-flux W33 graph. Numerical eigenvalue differences exceed displayed Ritz residuals; not an exact characteristic-polynomial theorem.',
   limitations='No optical nonlinearity or two-photon Bose-Hubbard Hamiltonian implemented physically; no gravity or non-imposed spatial continuum.')
if __name__=='__main__':
 z=certificate();(ROOT/'data/w33_20261009_round16_two_boson_verified_splitting.json').write_text(json.dumps(z,indent=2)+'\n')
 print('VERIFIED TWO-BOSON',[(x['U'],x['excited_spread']) for x in z['results']])
