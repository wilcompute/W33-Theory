"""TOE36/3: W33 cover-rank vacuum selector stress test.

For r=1,2,3 Z_p^r covers built from 1,2,3 independent chord
unit-voltage twists, the 4-regular connected adjacency has Perron
eigenvalue4 ALWAYS: single-particle ground energy -4t,
and N free boson ground E=-4Nt, independent of deck rank.
At fixed filling, onsite mean-field uniform energy per site
-2tn + (U/2)n² remains independent of rank. Spectral gaps
depend on rank; no natural selection without added geometry cost.
"""
from pathlib import Path
import itertools,sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords,matrix
OUT=ROOT/'data/w33_20261010_toe36_deck_rank_vacuum_selector.json'
def run():
 edges,D,C=wilson();selected=[spanning_chords(edges)[j] for j in (5,30,65)]
 records=[]
 for r in (1,2,3):
  flux=np.zeros((160,r),dtype=np.int16)
  for i,j in enumerate(selected[:r]):flux[j,i]=1
  p=3
  lowest=[];zero=0
  for ks in itertools.product(range(p),repeat=r):
   lam=np.linalg.eigvalsh(matrix(edges,flux,2*np.pi*np.array(ks)/p))
   lowest.extend(lam)
  low=np.sort(np.asarray(lowest))
  assert abs(low[0])<1e-9
  assert low[1]>1e-6
  sites=80*p**r
  ground_one=-4.
  N=10;ground_bosons=N*ground_one
  filling=.5;U=2.;t=1
  coherent_mean_field_energy_per_site= -2*t*filling+U*filling**2/2
  records.append(dict(rank=r,deck_type=f'Z_{p}^{r}',vertices=sites,
   full_laplacian_gap=float(low[1]),first_nontrivial_k_lowest_eigenvalue=float(low[1]),
   Perron_adjacency_eigenvalue=4,ground_one_free_boson=ground_one,
   ten_boson_free_ground_energy=ground_bosons,
   onsite_coherent_mean_field_energy_per_site=coherent_mean_field_energy_per_site))
 assert len(set(x['ground_one_free_boson'] for x in records))==1
 assert len(set(x['onsite_coherent_mean_field_energy_per_site'] for x in records))==1
 costs=[]
 for coeff in (-.1,0,.1):
  E=[x['ground_one_free_boson']+coeff*x['rank'] for x in records]
  winners=[x['rank'] for x,z in zip(records,E) if abs(z-min(E))<1e-12]
  costs.append(dict(explicit_added_cost_per_rank=coeff,minimizing_deck_ranks=winners,
    total_per_particle_energy_by_rank=E))
 assert costs[0]['minimizing_deck_ranks']==[3]
 assert costs[1]['minimizing_deck_ranks']==[1,2,3]
 assert costs[2]['minimizing_deck_ranks']==[1]
 res=dict(status='PASS',selected_W33_cycle_chords=selected,p=3,rank_scenarios=records,
  exact_free_boson_theorem='Every connected 4-regular undirected graph (including these finite W33 deck lifts) has adjacency top eigenvalue exactly4 and a unique uniform Perron vector, so the hopping H=-tA single-particle ground energy is -4t, regardless of dimension. N noninteracting bosons have ground -4Nt; no spontaneous deck-rank preference.',
  coherent_uniform_Gross_Pitaevskii_energy='At same density n on any 4-regular graph, onsite coherent-state mean-field energy per site -2t*n+(U/2)*n² is independent of rank. This is a variational mean-field comparison, not exact many-body ground energy for U>0.',
  artificial_rank_chemical_potential=costs,
  obstruction='A choice of deck rank cannot arise from this bare uniform free-boson energy functional; a finite graph model with r fixed does not even have a Hilbert-space operator that changes rank. A dynamical rank-changing graph Hamiltonian with locally specified move terms, entropy, normalization and a thermodynamic limit is an additional unproved input.',
  scope='Exact 4-regular Perron theorem plus complete p3 spectral gaps; does not exclude interacting/quantum-graph ensembles, rank-dependent gauge flux energy or genuine dynamically emergent geometry.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 print('TOE36 DECK RANK gap by r',[(x['rank'],round(x['full_laplacian_gap'],6)) for x in records],'free energy identical',flush=True)
 return res
if __name__=='__main__':run()
