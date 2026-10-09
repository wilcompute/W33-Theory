"""CANONICAL flat-band/cycle-space theorem for 160 W33 collinear triples.

160 triples are canonically the Levi flags (L,p_missing): complement of
one point of a 4-point line. Let D[L,trip]=1 for parent line,
M[p,trip]=1 for the missing point, P[p,trip]=1 for the 3 included
points, and R[p,L]=1 if p on L. Then P=R D-M and
   A_trip + 2I = P^T P - D^T D.
Thus Levi cycle vectors ker[M;D] lie in eigenspace A_trip=-2.
The two kernels both have dimension 81 by exact prime-rank witnesses,
so are equal; equivalently L_trip=32 on H1.
No physical mass/eigenvalue identification is claimed.
"""
from itertools import combinations
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import bt1688_exact_h1_character_irreducibility as B
from w33_20261009_local_hormander_depth import rank_mod
def certificate():
  lines=B.w33_lines(B.make_points())
  T=[];parents=[];missing=[]
  R=np.zeros((40,40),dtype=np.int64)
  for li,L in enumerate(lines):
    for p in L:R[p,li]=1
    for triple in combinations(L,3):
      T.append(tuple(triple));parents.append(li)
      miss=tuple(set(L)-set(triple))
      assert len(miss)==1
      missing.append(miss[0])
  assert len(T)==160
  D=np.zeros((40,160),dtype=np.int64);D[parents,np.arange(160)]=1
  M=np.zeros((40,160),dtype=np.int64);M[missing,np.arange(160)]=1
  P=np.zeros((40,160),dtype=np.int64)
  for j,tri in enumerate(T):
    P[list(tri),j]=1
  assert np.array_equal(P,R@D-M)
  intersection=P.T@P
  A=(intersection==1).astype(np.int64)
  # Same-line offdiagonal intersection=2; also all such triangles
  # have two shared points.  Different lines intersect at <=1.
  A|=((intersection==2)&(D.T@D==1)).astype(np.int64)
  np.fill_diagonal(A,0)
  A=A.astype(np.int64)
  # Confirm A is the "share at least one point" adjacency.
  assert np.all(A.sum(axis=1)==30)
  assert np.array_equal(A+2*np.eye(160,dtype=np.int64),P.T@P-D.T@D)
  Blevi=np.vstack([M,D]) # signless Levi incidence
  I=np.eye(160,dtype=np.int64)
  Aflag=Blevi.T@Blevi-2*I # BT548/Pass4019 preexisting Levi line graph
  assert np.all(Blevi.sum(axis=0)==2)
  assert np.all(Aflag.sum(axis=1)==6)
  assert np.all(A.sum(axis=1)==30)
  common_edges=int(np.triu((A!=0)&(Aflag!=0),1).sum())
  assert common_edges==240 and int(A.sum()/2)==2400 and int(Aflag.sum()/2)==480
  assert rank_mod(Aflag+2*I)==79
  # This is a SECOND coupler with the SAME H1 flat band; not a first
  # discovery of the H1 flat band, which BT548/Pass4019 established.
  rkB=rank_mod(Blevi)
  rkA=rank_mod(A+2*np.eye(160,dtype=np.int64))
  assert rkB==rkA==79
  # Both matrices have rational rank at most79: B by connected
  # bipartite Levi relation, A+2I via the P,D factorization and P=RD-M.
  # Therefore modular rank >=79 establishes exact rational rank79.
  graphL=30*np.eye(160,dtype=np.int64)-A
  # Strict exact integer minimal polynomial; expected
  # spec(L)={0,26+-sqrt46,28,32,36}.
  H=graphL@((graphL-28*I)@(graphL-32*I)@(graphL-36*I))
  H=H@(((graphL-26*I)@(graphL-26*I))-46*I)
  assert not np.any(H)
  # Trace(M) and ranks force multiplicities; use projective ranks to
  # certify the 32 eigenspace EXACTLY.
  ev=np.linalg.eigvalsh(graphL.astype(float))
  counts={}
  for key,val in [('0',0),('26-sqrt46',26-np.sqrt(46)),('28',28),
                  ('32',32),('26+sqrt46',26+np.sqrt(46)),('36',36)]:
    counts[key]=int(sum(abs(ev-val)<1e-7))
  assert counts=={'0':1,'26-sqrt46':24,'28':15,'32':81,'26+sqrt46':24,'36':15}
  # Obtain all multiplicities exactly from the integer annihilating
  # polynomial, exact rank0=1, rank32=81, rational conjugacy, and
  # first/second matrix traces, without trusting floating eigenvalues.
  import sympy as S
  assert rank_mod(graphL)==159
  n28,n36,conj=S.symbols('n28 n36 conjugate',integer=True)
  equations=[n28+n36+2*conj-78,
             28*n28+36*n36+52*conj-(int(np.trace(graphL))-81*32),
             784*n28+1296*n36+1444*conj-(int(np.trace(graphL@graphL))-81*32**2)]
  solved=S.solve(equations,(n28,n36,conj),dict=True)
  assert solved==[{n28:15,n36:15,conj:24}]
  # For EVERY rational or real mixing t of the two couplers,
  # ((1-t)Aflag+t*A+2I) c=0 for all Levi cycles c.
  assert rank_mod((Aflag+2*I)+(A+2*I))<=79
  return dict(status='PASS',
    canonical_map='Each 3-subset T of a W33 line L ↔ Levi incidence flag (L,p=L\\T), i.e. the excluded point.',
    flags=160,Levi_vertices=80,Levi_edges=160,Levi_cycle_rank=81,
    integer_identity='A_triples+2I=P^T P-D^T D, P=R D - M',
    modular_exact_rank_witness={'prime':32003,'rank_signless_Levi_incidence':rkB,
      'rank_A_plus_2I':rkA},
    flat_band_adjacency_eigenvalue=-2,flat_band_laplacian_eigenvalue=32,
    flat_band_exact_multiplicity=81,
    full_laplacian_spectrum=counts,
    exact_trace_multiplicity_proof={'laplacian_rank':159,'multiplicity_32':81,
      'multiplicity_28':15,'multiplicity_36':15,'multiplicity_each_Galois_conjugate':24},
    prior_BT548_Pass4019='BT548 and Pass4019-4024 already proved the Levi LINE GRAPH degree6 shared H1 flat band and 1620 apartment tight-frame states. This result is the independent degree30 collinear triple-overlap graph with the same exact H1 eigenspace.',
    different_couplers={'existing_Levi_line_graph_degree':6,'existing_edges':480,
      'new_triple_overlap_graph_degree':30,'new_edges':2400,'shared_edges':common_edges,
      'common_exact_minus_two_band_rank':81,
      'all_1620_prior_apartment_eigenstates_remain_eigenstates':True,
      'affine_interpolation_law':'A(t)=(1-t)A_line+t*A_triples acts as -2I on H1 for every real t; additional eigenvectors at -2 may occur at special t.'},
    spectral_minimal_polynomial='L*(L-28I)*(L-32I)*(L-36I)*((L-26I)^2-46I)=0, integer matrix identity',
    theorem='Exact canonical equality ker(A_triples+2I)=ker([M;D])=H1(Levi,R) after orientation sign convention: both dimension81; inclusion from factor identity; equality from exact rank79. Thus the W33 Levi cycle space is exactly the -2 adjacency flat band (32 Laplacian eigenspace) of the native 160-triple hopping graph.',
    physics_boundary='This is a finite exact graph/representation theorem, not a 78D quantum Hamiltonian spectral gap, a 3D spacetime, massless gauge boson, particle multiplicity, or propagating physical band; dynamics needed to couple this flat band to a spatial continuum.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_triple_flatband_cycle_space.json').write_text(json.dumps(d,indent=2)+'\n')
 print('EXACT FLATBAND=H1',d['flat_band_exact_multiplicity'],d['full_laplacian_spectrum'])
