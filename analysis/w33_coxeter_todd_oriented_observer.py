"""K12 local cover -> oriented W33 triangle homology and observable dynamics.
Prior: Holotrade a0ed473 (K12 cover), BT862/866 (oriented H2), Pass4787
(alias4763: grid incidence). This supplies explicit intertwiners and observer
operators, not new lattice classification or a physical particle assignment.
"""
from itertools import product, combinations
from collections import deque
from pathlib import Path
import json
import numpy as np
import networkx as nx
from w33_pass4495_4502_distance_prism_reconstruction import geometry as canonical_geometry
from sympy.combinatorics import Permutation, PermutationGroup

UNITS=[(1,0),(0,1),(-1,-1),(-1,0),(0,-1),(1,1)]
FM=[[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]
HG=[[1,0,0,1,1,1],[0,1,0,1,2,3],[0,0,1,1,3,2]]
LIFT=[(0,0),(1,0),(0,1),(-1,-1)]
def mul(x,y):
 a,b=x;c,d=y;return (a*c-b*d,a*d+b*c-b*d)
def h(x,y):
 terms=[mul(a,(b[0]-b[1],-b[1])) for a,b in zip(x,y)]
 return tuple(sum(t[i] for t in terms) for i in range(2))
def refl(v,x):
 a,b=h(x,v);assert a%2==b%2==0
 return tuple(tuple(xi[j]-mul((a//2,b//2),vi)[j] for j in range(2)) for xi,vi in zip(x,v))
def canon(v):return min(tuple(mul(u,x) for x in v) for u in UNITS)
def parity(a):return (-1)**sum(a[i]>a[j] for i,j in combinations(range(len(a)),2))
def rank_mod(a,p=101):
 a=np.array(a,dtype=np.int64,copy=True)%p;r=0
 for j in range(a.shape[1]):
  piv=np.flatnonzero(a[r:,j])
  if not len(piv):continue
  k=r+int(piv[0]);a[[r,k]]=a[[k,r]];a[r]=a[r]*pow(int(a[r,j]),-1,p)%p
  for i in range(r+1,len(a)):
   if a[i,j]:a[i]=(a[i]-a[i,j]*a[r])%p
  r+=1
  if r==len(a):break
 return r

def geometry():
 code=set()
 for cf in product(range(4),repeat=3):
  code.add(tuple(FM[cf[0]][HG[0][j]]^FM[cf[1]][HG[1][j]]^FM[cf[2]][HG[2][j]] for j in range(6)))
 assert len(code)==64
 mins=[]
 for c in sorted(code):
  nz=[i for i,x in enumerate(c) if x]
  if len(nz)!=4:continue
  for signs in product((-1,1),repeat=4):
   v=[(0,0)]*6
   for i,sg in zip(nz,signs):v[i]=tuple(sg*t for t in LIFT[c[i]])
   mins.append(tuple(v))
 for i,u in product(range(6),UNITS):
  v=[(0,0)]*6;v[i]=tuple(2*x for x in u);mins.append(tuple(v))
 lines=sorted({canon(v) for v in mins});assert len(mins)==756 and len(lines)==126
 A=np.array([[i!=j and h(v,w)==(0,0) for j,w in enumerate(lines)] for i,v in enumerate(lines)],dtype=np.int64)
 I126=np.eye(126,dtype=np.int64);assert np.array_equal(A@A,27*I126-6*A+18*np.ones((126,126),int))
 N=np.flatnonzero(A[0]);M=np.array([i for i in range(1,126) if not A[0,i]])
 D=A[np.ix_(M,M)];zero=(D@D==0)&(D==0)&(~np.eye(80,dtype=bool));assert np.all(zero.sum(1)==1)
 fib=[(i,int(np.flatnonzero(zero[i])[0])) for i in range(80) if i<np.flatnonzero(zero[i])[0]]
 R=np.zeros((80,40),dtype=np.int64);F=R.copy()
 for a,(i,j) in enumerate(fib):R[i,a]=1;R[j,a]=-1;F[i,a]=F[j,a]=1
 S=R.T@D@R//2;Q=F.T@D@F//2;B=A[np.ix_(N,M)]@F//2;G=A[np.ix_(N,N)]
 return lines,A,N,M,D,fib,R,F,S,Q,B,G

def audit():
 lines,A,N,M,D,fib,R,F,S,Q,B,G=geometry();I=np.eye(40,dtype=int);J=np.ones((40,40),dtype=int)
 col=J-I-Q
 # Identify the actual canonical symplectic geometry, not just SRG parameters.
 canonical=canonical_geometry()[3]
 iso=next(nx.algorithms.isomorphism.GraphMatcher(nx.from_numpy_array(col),nx.from_numpy_array(canonical)).isomorphisms_iter())
 mapping=[iso[i] for i in range(40)]
 assert np.array_equal(col,canonical[np.ix_(mapping,mapping)])
 assert np.array_equal(D@R,R@S) and np.array_equal(D@F,F@Q)
 assert np.array_equal(S@S,27*I-6*S)
 P10=3*I-S;P30=9*I+S;P15=4*Q+12*I-3*J
 for P,den,tr in [(P10,12,10),(P30,12,30),(P15,24,15)]:
  assert np.array_equal(P@P,den*P) and np.trace(P)==den*tr
 assert not np.any(P10@P30) and not np.any(B@P15)
 assert np.array_equal(B@B.T,9*np.eye(45,dtype=int)-3*G+7*np.ones((45,45),int))
 assert np.array_equal(B.T@B,12*I+3*col+6*J)
 assert rank_mod(B)==25
 # Incidence duality: base vertices are W33 lines; base cliques are W33 points.
 cliques=sorted({tuple(sorted({i,j}|set(np.flatnonzero(col[i]&col[j])))) for i in range(40) for j in np.flatnonzero(col[i])})
 assert len(cliques)==40 and all(len(L)==4 for L in cliques)
 ci={L:i for i,L in enumerate(cliques)};stars=[sorted(i for i,L in enumerate(cliques) if v in L) for v in range(40)]
 lid={v:i for i,v in enumerate(lines)};mi={int(v):i for i,v in enumerate(M)}
 fi={x:(i,s) for i,(a,b) in enumerate(fib) for x,s in [(a,1),(b,-1)]}
 gens=[];gens80=[];signs=[];orient=[];constraints=[]
 for n in N:
  perm=[mi[lid[canon(refl(lines[0],refl(lines[n],lines[int(v)])))]] for v in M]
  pg=[fi[perm[a]][0] for a,b in fib];sg=[fi[perm[a]][1] for a,b in fib]
  cp=[ci[tuple(sorted(pg[i] for i in L))] for L in cliques]
  os=[parity([stars[pg[i]].index(cp[j]) for j in stars[i]]) for i in range(40)]
  gens.append(pg);gens80.append(perm);signs.append(sg);orient.append(os)
  constraints.append([a*b for a,b in zip(sg,os)])
 eps=[0]*40;eps[0]=1;queue=deque([0])
 while queue:
  i=queue.popleft()
  for pg,r in zip(gens,constraints):
   j=pg[i];e=eps[i]*r[i]
   if eps[j]:assert eps[j]==e
   else:eps[j]=e;queue.append(j)
 assert all(eps)
 assert PermutationGroup([Permutation(p) for p in gens]).order()==25920
 assert PermutationGroup([Permutation(p) for p in gens80]).order()==25920
 for p,s,o in zip(gens,signs,orient):
  U=np.zeros((40,40),dtype=int)
  for i in range(40):
   U[p[i],i]=s[i];assert s[i]*eps[p[i]]==eps[i]*o[i]
  assert np.array_equal(U@S,S@U)
 # Tetrahedron boundaries are a basis of H2 of the TRIANGLE (not full clique) complex.
 triangles=sorted({t for L in stars for t in combinations(L,3)});ti={t:i for i,t in enumerate(triangles)}
 edges=sorted({e for t in triangles for e in combinations(t,2)});ei={e:i for i,e in enumerate(edges)}
 boundary=np.zeros((240,160),dtype=int);cycles=np.zeros((160,40),dtype=int)
 for j,t in enumerate(triangles):
  for k in range(3):boundary[ei[t[:k]+t[k+1:]],j]=(-1)**k
 for j,L in enumerate(stars):
  for k in range(4):cycles[ti[tuple(L[:k]+L[k+1:])],j]=(-1)**k
 assert not np.any(boundary@cycles) and np.array_equal(cycles.T@cycles,4*I)
 assert rank_mod(boundary)==120 # matching blockwise rank upper bound 40*3
 # The unique signed collinearity orbital is an explicit Eisenstein operator.
 seed=(0,int(np.flatnonzero(col[0])[0]));values={seed:1};queue=deque([seed])
 while queue:
  i,j=queue.popleft()
  for p,s in zip(gens,signs):
   pair=(p[i],p[j]);v=values[(i,j)]*s[i]*s[j]
   if pair in values:assert values[pair]==v
   else:values[pair]=v;queue.append(pair)
 K=np.zeros((40,40),dtype=int)
 for ij,v in values.items():K[ij]=v
 assert len(values)==480 and np.array_equal(K,-K.T)
 assert np.array_equal(K@K,-4*P10) and np.array_equal(S@K,-9*K)
 for p,s in zip(gens,signs):
  U=np.zeros((40,40),int)
  for i in range(40):U[p[i],i]=s[i]
  assert np.array_equal(U@K,K@U)
 # Independent orientation/basis realization and Hermitian band regression.
 gauge=np.array([(-1)**(i%3) for i in range(40)])
 S2=gauge[:,None]*S*gauge[None,:];K2=gauge[:,None]*K*gauge[None,:]
 assert np.array_equal(K2@K2,-4*(3*I-S2))
 H=0.7*S+0.13j*K
 assert np.array_equal(H,H.conj().T)
 expected=sorted([2.1]*30+[-6.3+4*np.sqrt(3)*0.13]*5+[-6.3-4*np.sqrt(3)*0.13]*5)
 assert np.allclose(np.linalg.eigvalsh(H),expected,atol=1e-12,rtol=0)
 # Exact all-time dark sector, then an optimal coordinate-port completion.
 C=np.eye(126,dtype=int)[N];RR=np.zeros((126,40),int);FF=RR.copy();RR[M]=R;FF[M]=F
 assert np.array_equal(A@RR,RR@S) and not np.any(C@RR)
 assert np.array_equal(A@FF@P15,3*FF@P15) and not np.any(C@FF@P15)
 O=np.vstack([C,C@A,C@A@A]);assert rank_mod(O)==71
 extra=[3,4,6,7,8,10,12,13,14,16,18,20,22,23,25,26,28,30,33,35,36,37,41,42,43,46,47,49,50,52,53,54,55,56,57,62,64,66,68,71,72,73,76,77,79]
 ports=list(N)+extra;assert len(set(ports))==90 and set(extra)<=set(M)
 C2=np.eye(126,dtype=int)[ports];assert rank_mod(np.vstack([C2,C2@A,C2@A@A]))==126
 # E3 has 30 odd plus 15 even dark dimensions: each added scalar output
 # contributes at most one constraint there. Thus 45 additional ports is optimal.
 perturb=A.copy();perturb[0,M[0]]=perturb[M[0],0]=1
 assert np.any(C@perturb@perturb@RR) # breaking the deck symmetry removes darkness
 prior=json.loads((Path(__file__).resolve().parents[1]/'data/bt866_h2_oriented_irreducible_decomposition.json').read_text())
 assert prior['oriented_h2_module']['decomposition_degrees']==[5,5,30]
 return {'status':'PASS','schema':'w33.coxeter-todd-oriented-observer.v1',
  'reflection_lines_eisenstein':lines,'root_line':0,'orthogonal45':N.tolist(),'nonorthogonal80':M.tolist(),
  'fibres_local80':fib,'signed_adjacency':S.tolist(),'grid_incidence':B.tolist(),
  'signed_spectrum':{'3':30,'-9':10},'signed_identity':'S^2+6S=27I',
  'canonical_symplectic_line_bijection':mapping,'switched_basis_check':True,'hermitian_band_check':True,
  'group_order':25920,'generators40':gens,'generator_signs':signs,'orientation_gauge':eps,
  'w33_lines_as_reconstructed_point_sets':stars,'tetrahedron_boundary_map':cycles.tolist(),
  'intertwiner_checks':1800,'homology':'H2 of the W33 2-skeleton; adding tetrahedral 3-cells kills these 40 cycles',
  'eisenstein_operator':K.tolist(),'eisenstein_identities':['K^T=-K','K^2=-48P10','SK=-9K'],
  'complex_structure':'J=K/4, J^2=-3P10; sign of J is a conjugate orientation choice',
  'model_hamiltonian':'g*S + i*eta*K: energies 3g (30), -9g +/- 4sqrt(3)eta (5 each)',
  'tritangent_observer_rank':71,'dark_dimension':55,'dark_eigenvalue_multiplicities':{'3':45,'-9':10},
  'additional_coordinate_ports':extra,'additional_ports_minimum':45,'completed_observer_rank':126,
  'symmetry_breaking_negative_control':True,
  'boundary':'Exact finite maps and linear amplitude observability. K12, oriented H2 and grid incidence have prior owners. No physical masses, spacetime, selected absolute handedness, single-shot tomography, or built device is inferred.'}

if __name__=='__main__':
 import sys
 out=audit()
 if '--write' in sys.argv:Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ('reflection_lines_eisenstein','generators40','generator_signs','tetrahedron_boundary_map','eisenstein_operator','signed_adjacency','grid_incidence','w33_lines_as_reconstructed_point_sets')},indent=2))
