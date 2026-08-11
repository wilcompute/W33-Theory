#!/usr/bin/env python3
"""Passes 4849/4852/4854/4855/4856 — E6 root signing closes the 36-bit incidence kernel.

Rebuild the GQ(4,2) 27-line graph, 1080 four-cycles, and 360 induced K3,3s.
The binary cycle/K3,3 incidence kernel is [360,36,20]. Its 36 minimum words
are the 36 twelve-line K6,6-minus-matching carriers. Their carrier-vs-K3,3
incidence is the vertex-edge incidence matrix of SRG(36,20,10,12), hence the
minimum shell spans the 35-dimensional cut code.

Construct E6 from its Cartan matrix. The 36 projective root pairs with
nonorthogonality adjacency are explicitly isomorphic to the 36-carrier graph,
and the full 51840 permutation action agrees with W(E6). Choosing a positive
root from every pair signs each edge by the inner product. The negative-edge
set is a weight-120 vector in the 36-dimensional incidence kernel and extends
the cut space by one dimension. Switching the root signs is exactly addition of
a graph cut. An exact 36-vertex MILP independently certifies switching minimum
120. Weyl chambers give the complete 25920 minimum switching representatives.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy import sparse
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4849_4852_4854_4855_4856_E6_KERNEL_CODE.json'

def Q(x):
 b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b
 return (a*c+d*e+f+f*g+g)&1

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def comm(a,b):return comp(comp(comp(a,b),inv(a)),inv(b))
def closure(gens,n):
 I=tuple(range(n));S={I};D=deque([I])
 while D:
  a=D.popleft()
  for g in gens:
   c=comp(g,a)
   if c not in S:S.add(c);D.append(c)
 return S

def rankbits(V):
 P={}
 for x in V:
  y=int(x)
  while y:
   k=y.bit_length()-1
   if k in P:y^=P[k]
   else:P[k]=y;break
 return len(P)

def rankmod(A,p):
 A=np.array(A,dtype=np.int64)%p;r=0
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
  if r==A.shape[0]:break
 return r

def main()->int:
 # Bare GQ(4,2) line graph.
 qp=[x for x in range(1,64) if Q(x)==0]
 pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
 lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 assert G.number_of_edges()==135 and set(dict(G.degree()).values())=={10}
 q4=[]
 for S in itertools.combinations(range(27),4):
  H=G.subgraph(S)
  if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):q4.append(frozenset(S))
 K=[]
 for S in itertools.combinations(range(27),6):
  H=G.subgraph(S)
  if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
   A,B=nx.algorithms.bipartite.sets(H)
   if len(A)==len(B)==3:K.append(frozenset(S))
 assert len(q4)==1080 and len(K)==360;Kidx={S:i for i,S in enumerate(K)}
 M=np.zeros((1080,360),dtype=np.uint8)
 for j,S in enumerate(K):
  I=[i for i,C in enumerate(q4) if C<=S];assert len(I)==9;M[I,j]=1
 assert rankmod(M,2)==324

 # Find one binary minimum word exactly, then take its full 51840 orbit.
 rr=[];cc=[];dd=[]
 for i in range(1080):
  for j in np.flatnonzero(M[i]):rr.append(i);cc.append(int(j));dd.append(1.)
  rr.append(i);cc.append(360+i);dd.append(-2.)
 Aeq=sparse.coo_matrix((dd,(rr,cc)),shape=(1080,1440)).tocsr()
 row=sparse.csr_matrix(([1.]*360,([0]*360,list(range(360)))),shape=(1,1440))
 AA=sparse.vstack([Aeq,row]);lb=np.r_[np.zeros(1080),1.];ub=np.r_[np.zeros(1080),np.inf]
 R=milp(np.r_[np.ones(360),np.zeros(1080)],integrality=np.ones(1440),bounds=Bounds(np.zeros(1440),np.r_[np.ones(360),np.full(1080,2.)]),constraints=LinearConstraint(AA,lb,ub),options={'presolve':True})
 assert R.status==0 and round(R.fun)==20
 x0=frozenset(j for j,z in enumerate(R.x[:360]) if z>.5);carrier=frozenset().union(*(K[j] for j in x0));assert len(carrier)==12
 Hc=G.subgraph(carrier);assert Hc.number_of_edges()==30 and set(dict(Hc.degree()).values())=={5} and nx.is_bipartite(Hc)

 autos=[tuple(m[i] for i in range(27)) for m in nx.algorithms.isomorphism.GraphMatcher(G,G).isomorphisms_iter()];assert len(autos)==51840
 carriers=sorted({frozenset(p[x] for x in carrier) for p in autos},key=lambda S:tuple(sorted(S)));assert len(carriers)==36
 Cidx={S:i for i,S in enumerate(carriers)}
 mins=[]
 for C in carriers:
  x=0
  for j,S in enumerate(K):
   if S<=C:x|=1<<j
  assert x.bit_count()==20;mins.append(x)
 assert rankbits(mins)==35 and Counter(sum((x>>j)&1 for x in mins) for j in range(360))==Counter({2:360})

 # Each K3,3 is an edge joining its two minimum carriers.
 edgepairs=[]
 for j in range(360):
  V=tuple(i for i,x in enumerate(mins) if (x>>j)&1);assert len(V)==2;edgepairs.append(V)
 assert len(set(edgepairs))==360
 H36=nx.Graph();H36.add_nodes_from(range(36));H36.add_edges_from(edgepairs)
 assert nx.is_connected(H36) and H36.number_of_edges()==360 and set(dict(H36.degree()).values())=={20}
 lam=set();mu=set()
 for a,b in itertools.combinations(range(36),2):
  z=len(set(H36[a])&set(H36[b]));(lam if H36.has_edge(a,b) else mu).add(z)
 assert lam=={10} and mu=={12}
 ev=np.linalg.eigvalsh(nx.to_numpy_array(H36));assert Counter(np.rint(ev).astype(int))==Counter({2:20,-4:15,20:1})
 N=np.zeros((36,360),dtype=np.uint8)
 for j,(a,b) in enumerate(edgepairs):N[a,j]=N[b,j]=1
 nranks={p:rankmod(N,p) for p in (2,3,5,7)};assert nranks=={2:35,3:36,5:36,7:36}
 NN=N.astype(int)@N.T.astype(int);assert np.array_equal(NN,20*np.eye(36,dtype=int)+nx.to_numpy_array(H36,dtype=int))

 # Recover full PSp as derived/square subgroup of the 51840 group.
 gens=[];cur={tuple(range(27))}
 for p in autos:
  T=closure(gens+[p],27)
  if len(T)>len(cur):gens.append(p);cur=T
  if len(cur)==51840:break
 soc=closure([comp(g,g) for g in gens]+[comm(a,b) for a,b in itertools.combinations(gens,2)],27);assert len(soc)==25920
 carperms=[]
 for p in autos:carperms.append(tuple(Cidx[frozenset(p[x] for x in C)] for C in carriers))
 assert len(set(carperms))==51840

 # E6 root system in simple-root coordinates (arms 2,2,1).
 Cart=np.eye(6,dtype=int)*2
 for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):Cart[a,b]=Cart[b,a]=-1
 assert round(np.linalg.det(Cart))==3
 def refl(v,i):
  v=np.array(v,dtype=int);m=int(v@Cart[:,i]);w=v.copy();w[i]-=m;return tuple(map(int,w))
 roots={tuple((1,0,0,0,0,0))};D=deque(roots)
 while D:
  v=D.popleft()
  for i in range(6):
   w=refl(v,i)
   if w not in roots:roots.add(w);D.append(w)
 assert len(roots)==72 and {int(np.array(v)@Cart@np.array(v)) for v in roots}=={2}
 pos=sorted(v for v in roots if all(a>=0 for a in v));assert len(pos)==36
 ER=nx.Graph();ER.add_nodes_from(range(36));inner={}
 for i,j in itertools.combinations(range(36),2):
  z=int(np.array(pos[i])@Cart@np.array(pos[j]));inner[(i,j)]=z
  if abs(z)==1:ER.add_edge(i,j)
 assert ER.number_of_edges()==360 and nx.is_isomorphic(H36,ER)
 iso=next(nx.algorithms.isomorphism.GraphMatcher(H36,ER).isomorphisms_iter())

 # Weyl action on projective root pairs equals transported carrier action.
 def pkey(v):
  v=tuple(v);nv=tuple(-x for x in v);return min(v,nv)
 pairkey={pkey(v):i for i,v in enumerate(pos)}
 wgens=[]
 for s in range(6):wgens.append(tuple(pairkey[pkey(refl(v,s))] for v in pos))
 Weyl=closure(wgens,36);assert len(Weyl)==51840
 conj=set()
 for pc in set(carperms):
  q=[0]*36
  for i in range(36):q[iso[i]]=iso[pc[i]]
  conj.add(tuple(q))
 assert conj==Weyl

 # E6 positive-root signing on carrier edges = missing binary kernel coset.
 sigma=0
 for e,(a,b) in enumerate(edgepairs):
  ia,ib=iso[a],iso[b];z=inner[tuple(sorted((ia,ib)))]
  if z<0:sigma|=1<<e
 assert sigma.bit_count()==120 and rankbits(mins+[sigma])==36
 rowm=[]
 for row in M:
  x=0
  for j in np.flatnonzero(row):x|=1<<int(j)
  rowm.append(x)
 assert all(not ((r&sigma).bit_count()&1) for r in rowm)
 Bsg=np.zeros((36,36),dtype=int)
 for e,(a,b) in enumerate(edgepairs):Bsg[a,b]=Bsg[b,a]=(-1 if (sigma>>e)&1 else 1)
 assert Counter(np.rint(np.linalg.eigvalsh(Bsg)).astype(int))==Counter({-2:30,10:6})
 Gram=2*np.eye(36,dtype=int)+Bsg;assert np.linalg.matrix_rank(Gram)==6

 # Independent exact switching-minimum certificate on the 36-vertex signed graph.
 # z_e = sigma_e xor u_a xor u_b.
 nv=36;ne=360;NNV=ne+nv+ne;rr=[];cc=[];dd=[];rhs=[]
 for e,(a,b) in enumerate(edgepairs):
  rr += [e,e,e,e];cc += [e,ne+a,ne+b,ne+nv+e];dd += [1.,-1.,-1.,2.];rhs.append(float((sigma>>e)&1))
 A=sparse.coo_matrix((dd,(rr,cc)),shape=(ne,NNV)).tocsr();lo=np.zeros(NNV);hi=np.ones(NNV);lo[ne]=hi[ne]=0
 RS=milp(np.r_[np.ones(ne),np.zeros(nv+ne)],integrality=np.ones(NNV),bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(rhs),np.array(rhs)),options={'presolve':True})
 assert RS.status==0 and round(RS.fun)==120

 # Weyl-chamber shell: full group orbit 25920; PSp splits it in two 12960 orbits.
 supp=[j for j in range(360) if (sigma>>j)&1]
 def actword(xsupp,p):
  z=0
  for j in xsupp:z|=1<<Kidx[frozenset(p[x] for x in K[j])]
  return z
 orbF={actword(supp,p) for p in autos};orbP={actword(supp,p) for p in soc}
 assert len(orbF)==25920 and len(orbP)==12960
 # Both groups are transitive on coordinates. Therefore K has no fixed vector:
 # ambient fixed space is <1>, while M*1=1 because every row has weight 3.
 assert len({Kidx[frozenset(p[x] for x in K[0])] for p in soc})==360
 assert len({Kidx[frozenset(p[x] for x in K[0])] for p in autos})==360
 assert all(r.bit_count()==3 for r in rowm)

 # Low shell of K. The coset starts at 120, so all weights <64 are cuts.
 # Laplacian lambda_2=18 gives |delta U| >= |U|(36-|U|)/2, hence |U|>=4 gives >=64.
 tri=Counter(H36.subgraph(S).number_of_edges() for S in itertools.combinations(range(36),3))
 low={20:36,38:H36.number_of_edges(),40:630-H36.number_of_edges(),54:tri[3],56:tri[2],58:tri[1],60:tri[0]}
 assert low=={20:36,38:360,40:270,54:1200,56:3240,58:2160,60:540}
 # Dual = even-sigma cycle space; 1200 graph triangles split 1080 even / 120 odd.
 eindex={tuple(sorted(e)):j for j,e in enumerate(edgepairs)};even=odd=0
 for T in itertools.combinations(range(36),3):
  if H36.subgraph(T).number_of_edges()!=3:continue
  t=sum(1<<eindex[tuple(sorted(e))] for e in itertools.combinations(T,2))
  if (t&sigma).bit_count()&1:odd+=1
  else:even+=1
 assert (even,odd)==(1080,120)

 old=json.loads((ROOT/'manuscripts/parts/PART_MCCCXCV_SPREAD_DOUBLE_SIX_AUTOMORPHISM_ORDER_results.json').read_text())
 assert old['orbit_stabilizer']['automorphism_order']==51840
 out={
  'passes':[4849,4852,4854,4855,4856],
  'kernel_code':{'parameters':'[360,36,20]_2','minimum_shell_size':36,'minimum_shell_span_dimension':35,
    'structure':'Cut(SRG(36,20,10,12)) + <E6 root-inner-product signing>',
    'low_weight_shell_below_64':{str(k):v for k,v in sorted(low.items())},
    'dual':{'parameters':'[360,324,3]_2','weight3_words':1080,'interpretation':'even-E6-sign triangles / binary Levi cycles'},
    'bounded_distance_radius':9,'ML_decoder':'two exact signed-MaxCut/switching instances on the 36-vertex E6 root graph, one for each coset of the cut code',
    'automorphism_group_order':51840,'automorphism_group':'W(E6) = PGSp(4,3) on projective E6 roots/double-sixes'},
  'minimum_carriers':{'count':36,'line_support_size':12,'induced_graph':'K6,6 minus perfect matching','classical_identity':'the 36 cubic-surface double-sixes of Pass4659','carrier_graph':'SRG(36,20,10,12)','carrier_graph_complement':'SRG(36,15,6,6) double-six overlap scheme','spectrum':{'20':1,'2':20,'-4':15}},
  'E6_identification':{'roots':72,'projective_root_pairs':36,'explicit_graph_isomorphism':True,'full_action_conjugacy_to_Weyl_group':True,'Weyl_order':51840,'signed_adjacency_spectrum':{'10':6,'-2':30},'root_Gram':'2I+B, rank 6, nonzero eigenvalue 12^6'},
  'extra_kernel_coset':{'canonical_generator':'negative-inner-product edges after choosing an E6 positive system','representative_weight':120,'minimum_coset_weight':120,'complete_minimum_shell_size':25920,'PGSp_orbit_size':25920,'PGSp_stabilizer_order':2,'PSp_orbits':2,'PSp_orbit_size_each':12960,'PSp_stabilizer_order':2,
    'Weyl_chamber_proof':'For one representative from each root pair, ||sum r||^2 = 792-4 N_minus. A positive system has sum=2 rho and ||2 rho||^2=312, so N_minus=120. Equality orientations are Weyl chambers; opposite chambers give the same edge signing, hence 51840/2=25920 minimum signings.'},
  'characteristic_two_extension':{'exact_sequence':'0 -> Cut(H36) [360,35,20] -> K [360,36,20] -> F2 -> 0','quotient_is_trivial_module':True,'splits_over_PSp':False,'splits_over_PGSp':False,'proof':'Both groups are transitive on 360 coordinates, so the ambient fixed subspace is <1>; the all-one vector is not in K because each of the 1080 defining rows has odd weight 3. A split trivial quotient would require a fixed lift.'},
  'carrier_incidence_36x360':{'row_degree':20,'column_degree':2,'ranks':{str(p):r for p,r in nranks.items()},'binary_row_span':'35-dimensional cut code','real_singular_square_spectrum':{'40':1,'22':20,'16':15},'right_Gram':'2I + adjacency(line graph of SRG(36,20,10,12)); zero multiplicity 324'},
  'theorem':'The unresolved one-bit quotient of the [360,36,20]_2 incidence kernel is the E6 root-signing switching class. The 36 minimum words are exactly the cubic-surface double-sixes/projective E6 roots, their K3,3 incidence is the edge incidence of SRG(36,20,10,12), and the kernel is its cut code plus the nonsplit E6 signing. The nontrivial coset has exact minimum 120 and 25920 Weyl-chamber minima.',
  'boundary':'The E6 statement is an exact finite root/double-six/code identification. No physical E6 field or particle interpretation is inferred.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
