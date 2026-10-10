"""W33 1620-apartment frame dynamics: exact overlap-three components,
plus overlap-two connected tunneling. Existing Pass4474 already identified
1620 apartment symplectic frames; this tests a NEW quantum graph dynamics.
"""
import itertools,json
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.sparse import coo_matrix,csgraph,diags
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
import sys;sys.path.insert(0,str(ROOT/'analysis'))
from w33_h1_det_apartment_phase_bridge import POINTS,om
OUT=ROOT/'data/w33_20261009_toe23_dynamic_apartment_frame.json'
def build():
 A=np.zeros((40,40),dtype=np.int8)
 for i in range(40):
  for j in range(i+1,40):
   if om(POINTS[i],POINTS[j])==0:A[i,j]=A[j,i]=1
 apt=[]
 for Q in itertools.combinations(range(40),4):
  B=A[np.ix_(Q,Q)]
  if B.sum()==8 and np.all(B.sum(axis=1)==2):apt.append(Q)
 assert len(apt)==1620
 groups=[defaultdict(list),defaultdict(list)]
 for i,Q in enumerate(apt):
  for k,rec in ((3,groups[0]),(2,groups[1])):
   for T in itertools.combinations(Q,k):rec[T].append(i)
 neighbors3=set()
 for ids in groups[0].values():
  for x,y in itertools.combinations(ids,2):neighbors3.add((x,y))
 neighbors2=set()
 for ids in groups[1].values():
  for x,y in itertools.combinations(ids,2):
   if (x,y) not in neighbors3:neighbors2.add((x,y))
 def matrix(pairs):
  ii=[];jj=[]
  for a,b in pairs:ii.extend((a,b));jj.extend((b,a))
  return coo_matrix((np.ones(len(ii)),(ii,jj)),shape=(1620,1620)).tocsr()
 return apt,matrix(neighbors3),matrix(neighbors2)
def heat(m,t):
 e=1-np.cos(2*np.pi*np.arange(m)/m);w=np.exp(-t*e)
 return float((w.mean())**4),float(8*t*np.dot(e,w)/w.sum())
def run():
 apt,A3,A2=build()
 n3,lab=csgraph.connected_components(A3,directed=False)
 n2,_=csgraph.connected_components(A2,directed=False)
 nfull,_=csgraph.connected_components(A3+A2,directed=False)
 size=np.bincount(lab)
 d3=np.asarray(A3.sum(axis=1)).ravel();d2=np.asarray(A2.sum(axis=1)).ravel()
 print('FRAME degree overlap3',np.unique(d3),'overlap2',np.unique(d2),
       'components',n3,'sizes',np.unique(size,return_counts=True),
       'overlap2_components',n2,flush=True)
 assert len(set(d3))==1 and len(set(d2))==1
 assert n3==45 and set(size)=={36}
 assert nfull==1
 rep=np.flatnonzero(lab==lab[0])
 eig=np.linalg.eigvalsh(A3[rep][:,rep].toarray())
 assert abs(eig[-1]-8)<1e-9 and eig[-1]-eig[-2]>1e-6
 local_gap=float(eig[-1]-eig[-2])
 unique,multiplicity=np.unique(np.round(eig,8),return_counts=True)
 component_spectrum={str(float(lam)):int(n) for lam,n in zip(unique,multiplicity)}
 compmat=A3[rep][:,rep].toarray()
 component_triangles=int(np.trace(compmat@compmat@compmat)//6)
 print('LOCAL FRAME 36 eigen',component_spectrum,'triangles',component_triangles,flush=True)
 # At epsilon=0 there are 45 EXACT ground vectors, one uniform on
 # each connected component; at epsilon>0 global graph connected and
 # Perron Frobenius restores unique G-invariant uniform ground.
 mixed={}
 for eps in (.01,.1,1):
  H=A3+eps*A2
  ev=np.sort(eigsh(H,k=3,which='LA',return_eigenvectors=False,tol=1e-8))
  mixed[str(eps)]=dict(gap=float(ev[-1]-ev[-2]),
    max_eigenvalue=float(ev[-1]),exact_row_sum=float(8+eps*d2[0]))
  print('FRAME TUNNEL',eps,mixed[str(eps)]['gap'],flush=True)
  assert mixed[str(eps)]['gap']>0
 assert abs(mixed['1']['max_eigenvalue']-(8+d2[0]))<1e-7
 pin={}
 for h in (.5,2,8):
  potential=np.zeros(1620);potential[0]=-h
  ev,V=eigsh(-A3+diags(potential),k=1,which='SA',tol=1e-8)
  pin[str(h)]=dict(E0=float(ev[0]),selected_frame_probability=float(V[0,0]**2))
 family={str(m):[dict(t=t,return_probability=heat(m,t)[0],running_spectral_dimension=heat(m,t)[1]) for t in (1,4,16,64,256)] for m in (3,9,27,81)}
 print('TORUS',[(m,heat(m,16)[1]) for m in (3,9,27,81)],flush=True)
 assert abs(heat(81,16)[1]-4)<.3 and heat(3,16)[1]<.01
 out=dict(status='PASS',prior='Pass4474 and other prior apartment works already establish 1620 apartment W33 C4 symplectic frames. Current work studies an explicitly chosen Hamiltonian on their OVERLAP RELATIONS.',
   frame_count=1620,overlap_3_degree=int(d3[0]),overlap_2_degree=int(d2[0]),component_spectrum=component_spectrum,component_triangles=component_triangles,
   overlap_3_connected_components=n3,component_size=36,component_36_spectral_gap=local_gap,
   overlap_2_connected_components=n2,combined_graph_connected=True,
   conditional_H0='H=-t A_3 on 1620 apartment basis, where A3 connects apartment ray sets sharing exactly three of four rays. Exactly 45 disconnected equal 36-state components; hence for t>0 exactly 45 degenerate lowest-energy states (uniform on each component). The frame vacuum is not uniquely selected by symmetry.',
   conditional_tunnel='Add -epsilon A_2, where A2 connects apartments sharing exactly two rays. This remains PGSp-invariant and makes the graph connected, so any epsilon>0 yields unique positive fully symmetry-invariant ground state. The 45-fold frame degeneracy is therefore not symmetry protected against all invariant couplings.',
   tunneling_gaps=mixed,pinned_component_response=pin,
   conditional_spacetime='Selecting one of 1620 apartment symplectic frames provides 4 affine coordinate axes on F3^4 but that 81-site four-torus does not have a broad 4-dimensional heat-kernel scaling plateau. Externally postulated C_m^4 coordinate refinements, with m=9,27,81, acquire running spectral dimension near4 for 1<<t<<m²; no W33 law fixes m or Lorentzian dynamics.',
   torus_heat=family,
   physical_boundary='Geometric frame dynamics and chosen-geometry local lattice are toy Hamiltonians; no frame-to-vierbein field theory, Lorentzian light cone, Einstein equations, or matter coupling is derived.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
