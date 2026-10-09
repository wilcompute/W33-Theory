"""PSp-invariant, parameter-free-local-motif energy landscapes on the exact
86,400 intrinsic near-isotropic 3-flag selectors.

Define for optimal triple T=(p_i,L_i), point-center count C_p
= number of W33 points collinear with all three p_i, line-center
count C_l=number W33 lines meeting all three L_i.
Both exact intrinsic group invariants.

The two Hamiltonians H_-(T)=-C_p-C_l, H_+(T)=-C_p+C_l
have DIFFERENT 4320-fold C6 orbit ground manifolds (prior PSp orbit
decomposition), with explicit integer spectral gaps to next orbit.
Under any bounded additional diagonal perturbation ||V||infty <
gap/2, minimizing orbit remains globally selected as a set.
No finite PSp-invariant energy can select a UNIQUE state inside its
orbit; a transverse-hopping finite quantum model may have unique
PF ground and cannot be claimed as spontaneous infinite-volume SSB.

Novel geometric idea: extra C6 order parameter with residual
C3 action on three directions while 2-element kernel fixes all.
"""
import sys,json
from pathlib import Path
from collections import defaultdict
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261008_5state_ritz import geometry
def certificate():
 edges,N,*_=geometry()
 base=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())
 PP=(N@N.T)==1;LL=(N.T@N)==1
 L=np.zeros((80,160),dtype=np.int64)
 for j,(p,l) in enumerate(edges):L[p,j]=1;L[l,j]=-1
 V=L@L.T;V2=V@V;V3=V2@V;V4=V3@V
 pi=(12800*np.eye(160,dtype=np.int64)-L.T@(-47*V4+900*V3-5686*V2+12152*V)@L)//80
 A=pi==1
 np.fill_diagonal(A,False)
 rows=[]
 for o in base['orbits']:
  tri=o['representative']
  p=[edges[i][0] for i in tri]
  l=[edges[i][1]-40 for i in tri]
  cp=int(np.sum(np.all(PP[p,:],axis=0)))
  cl=int(np.sum(np.all(LL[l,:],axis=0)))
  assert N[np.ix_(p,l)].tolist()==np.eye(3,dtype=int).tolist()
  degree=0
  for ii in range(3):
   for jj in range(ii+1,3):
    degree+=int(np.sum(A[tri[ii]]&A[tri[jj]]))-1
  rows.append(dict(representative=tri,orbit_size=o['orbit_size'],
      stabilizer=o['stabilizer_order'],point_center_count=cp,
      line_transversal_count=cl,selector_one_flag_swap_degree=degree))
 assert sorted((r['point_center_count'],r['line_transversal_count']) for r in rows)==[(1,0),(1,2),(1,2),(4,0),(4,2)]
 for row in rows:
  row['E_plus']=-row['point_center_count']+row['line_transversal_count']
  row['E_minus']=-row['point_center_count']-row['line_transversal_count']
 energies={}
 for k in ('E_plus','E_minus'):
  dist=defaultdict(int)
  for row in rows:dist[row[k]]+=row['orbit_size']
  lev=sorted(dist)
  emin=lev[0];minima=[r for r in rows if r[k]==emin]
  assert len(minima)==1 and minima[0]['orbit_size']==4320
  energies[k]=dict(classical_ground_energy=emin,ground_degeneracy=4320,
    first_excitation_gap=lev[1]-lev[0],histogram={str(v):dist[v] for v in lev},
    selected_orbit_representative=minima[0]['representative'],
    residual_stabilizer_order=6)
 assert energies['E_plus']['selected_orbit_representative']!=energies['E_minus']['selected_orbit_representative']
 return dict(status='PASS',total_intrinsic_isotropic_selectors=sum(x['orbit_size'] for x in rows),
    exact_PSp_orbits=rows,integer_local_motif_energies=energies,
    deterministic_classical_orbit_selection='Two explicit local incidence-motif PSp-invariant energy functions select the two DIFFERENT 4320-state C6 orbits with positive integer gap. They do not pick one state without SSB or external field.',
    robustness='For diagonal additive perturbation bounded by eta at every selector, the same selected orbit set remains the unique lowest orbit (no crossing between orbit types) whenever 2eta<gap; within-orbit splitting allowed if perturbation breaks PSp.',
    physical_boundary='Finite discrete selector Hamiltonians explicitly engineered from common-neighbor motifs, NOT derived from quantum-current Hamiltonian nor any underlying physical microscopic interaction. No thermodynamic/continuum dynamics or Einstein gravity.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round14_intrinsic_selector_energies.json').write_text(json.dumps(d,indent=2)+'\n')
 print('SELECTOR MOTIF',[(v['representative'],v['point_center_count'],v['line_transversal_count'],v['selector_one_flag_swap_degree']) for v in d['exact_PSp_orbits']],'H',d['integer_local_motif_energies'])
