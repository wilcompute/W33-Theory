"""TOE Round38: construct genuinely LOCAL contractible plaquette curl
on a three-deck W33 Levi lift. The 80 edge-flat bands are
divergence-free (physical transverse candidate), not gauge pure modes.
Use native zero-deck-winding octagons and three commutators of
fundamental deck loops to make a 2-complex. Tests d1*d2=0,
rank of zero-winding cycles, transverse two light modes.
"""
import sys,json,itertools,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261009_round18_chirality_plaquette_audit import cycles_touching
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords
from w33_20261010_toe36_incidence_relativistic_walk import gradient
OUT=ROOT/'data/w33_20261010_toe38_local_maxwell_2complex.json'
def prep():
 ed,D,C=wilson();ch=spanning_chords(ed);picked=[ch[i] for i in (5,30,65)]
 volts=np.zeros((len(ed),3),dtype=np.int32)
 for i,e in enumerate(picked):volts[e,i]=1
 lookup={tuple(sorted(e)):i for i,e in enumerate(ed)}
 rings=set()
 for j in range(160):rings.update(cycles_touching(ed,j))
 rings=sorted(rings)
 assert len(rings)==1620
 zero=[];flux_counts=collections.Counter()
 for ring in rings:
  v=np.zeros(3,dtype=int)
  for a,b in zip(ring,ring[1:]+ring[:1]):
   e=lookup[tuple(sorted((a,b)))]
   v+=volts[e] if a==ed[e][0] else -volts[e]
  flux_counts[tuple(v)]+=1
  if not np.any(v):zero.append(ring+(ring[0],))
 # Build tree paths for 3 chord generators starting at zero.
 tree_edges=set(range(len(ed)))-set(ch)
 G=[[] for _ in range(80)]
 for j in tree_edges:
  a,b=ed[j];G[a].append(b);G[b].append(a)
 def route(a,b):
  seen={a:None};q=collections.deque([a])
  while q:
   u=q.popleft()
   if u==b:break
   for v in G[u]:
    if v not in seen:seen[v]=u;q.append(v)
  assert b in seen
  path=[b]
  while path[-1]!=a:path.append(seen[path[-1]])
  return path[::-1]
 loops=[]
 for j in picked:
  a,b=ed[j]
  walk=route(0,a)+[b]+route(b,0)[1:]
  assert walk[0]==walk[-1]==0
  loops.append(walk)
 def invert(w):return w[::-1]
 def concatenate(*ws):
  path=[ws[0][0]]
  for w in ws:
   assert path[-1]==w[0]
   path.extend(w[1:])
  assert path[-1]==path[0]
  return path
 comm=[concatenate(loops[i],loops[j],invert(loops[i]),invert(loops[j])) for i,j in ((0,1),(0,2),(1,2))]
 return ed,volts,lookup,zero,comm,picked,flux_counts
def cycle_row(walk,ed,volts,lookup,k):
 acc=np.zeros(3,dtype=int);row=np.zeros(160,dtype=complex)
 for u,v in zip(walk,walk[1:]):
  j=lookup[tuple(sorted((u,v)))]
  a,b=ed[j];f=volts[j]
  if u==a:
   row[j]+=np.exp(+1j*np.dot(k,acc));acc+=f
  else:
   row[j]-=np.exp(+1j*np.dot(k,acc-f));acc-=f
 assert np.array_equal(acc,np.zeros(3,dtype=int)),('nonclosed',acc)
 return row
def run():
 ed,volts,look,zero,comm,picked,fc=prep()
 # Fourier plaquette rows are localized (8 edges or finite length commutators).
 cases=[];Cv0=np.array([cycle_row(w,ed,volts,look,np.zeros(3)) for w in zero])
 rank0=np.linalg.matrix_rank(Cv0,tol=1e-8)
 from w33_20261010_toe37_finite_translation_form_obstruction import rank3
 exact_GF3_rank=rank3(np.rint(Cv0.real).astype(np.int64))
 assert exact_GF3_rank==rank0==78
 B0=gradient(ed,volts,np.zeros(3))
 assert np.max(np.abs(Cv0@B0))<1e-12
 assert rank0<=78,(rank0,len(zero))
 # Commutator boundaries vanish identically at 0 in abelian chain group.
 for w in comm: assert np.linalg.norm(cycle_row(w,ed,volts,look,np.zeros(3)))<1e-12
 for k in (np.zeros(3),np.array([.02,0,0]),np.array([.01,0,0]),np.array([0,.02,0]),np.array([0,0,.02]),np.array([.02,.017,-.012])):
  B=gradient(ed,volts,k)
  P=np.array([cycle_row(w,ed,volts,look,k) for w in zero+comm])
  closure=float(np.max(np.abs(P@B)))
  assert closure<1e-10,closure
  # row-cycle P acts on edge, B† maps edge to vertex.
  effective_rank=np.linalg.matrix_rank(P,tol=1e-7)
  b_rank=np.linalg.matrix_rank(B,tol=1e-7)
  # No dense projection used: 8-cycle rows each have 8 nonzero
  if np.linalg.norm(k):
   # SVD of B yields transverse edge subspace.
   U,s,Vh=np.linalg.svd(B,full_matrices=True)
   transverse=U[:,80:]
   K=(P@transverse).conj().T@(P@transverse)
   eig=np.linalg.eigvalsh(K)
   num_small=int(np.count_nonzero(eig<1e-8))
   lowest=[float(x) for x in eig[:5]]
  else:
   # At k0 B rank79: exact transverse dimension81.
   num_small=160-b_rank-effective_rank
   lowest=[]
  rec=dict(k=k.tolist(),base_gradient_rank=int(b_rank),
   plaquette_boundary_rank=int(effective_rank),transverse_harmonic_dim=int(num_small),
   max_d1_d2_violation=closure,lowest_transverse_curl_eigenvalues=lowest)
  cases.append(rec)
  print('TOE38 MAXWELL',rec,flush=True)
 out=dict(status='PASS',selected_chords=picked,n_zero_winding_native_octagons=len(zero),
  zero_winding_8cycle_rank_at_zero=int(rank0),exact_F3_rank_zero_winding_8cycles=int(exact_GF3_rank),
  nonzero_winding_octagons=1620-len(zero),
  full_octagon_deck_winding_histogram={str(k):v for k,v in fc.items()},
  commutator_plaquette_lengths=[len(w)-1 for w in comm],
  cases=cases,
  theoretical='Genuinely closed plaquette boundaries are local zero-deck-winding octagons and three finite commutator loops. Their twisted Bloch chain maps obey B(k)†∂2(k)=0 (the discrete Bianchi law), without any all-to-all edge-cycle projector. Transverse modes correspond to divergence-free edge cochains and must not be discarded as gauge.',
  photons_claim='A gauge-invariant local curl sector may allow two low-energy transverse polarizations if the plaquette rank rises from78 at zero to80 generic k, with curl eigenvalues proportional to k². This is NOT itself quantum electrodynamics, a derived universal c, a free Maxwell physical Hamiltonian, or an observed photon.',
  new_vs_prior='Round37 tested edge onsite mI (destroys z1) and dense projector (preserves z1 but nonlocal); these explicit W33 degree-8 plus commutator plaquettes offer a third, finite-range derivative/gauge completion subject to rank tests.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
