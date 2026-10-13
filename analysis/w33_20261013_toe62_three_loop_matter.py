"""TOE62 front4: interacting THREE overlapping W33 octagons with true fermion hops.

Gauss-constrained connected native 14-site/16-link patch, three integer
cycle coordinates. Fock hop-depth + integer-flux Galerkin cutoffs are
explicitly limited, with Fock/flux boundary probabilities reported.
"""
from pathlib import Path
from collections import deque
from itertools import product
import json,sys,numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'analysis'))
from w33_pass11969_full_native_gauss_compiler import NativeGaussCompiler
native=NativeGaussCompiler()
row_ids=[0,186,164]
support=np.flatnonzero(np.any(native.P[row_ids],axis=0))
nodes=sorted(set(native.edges[e][j] for e in support for j in (0,1)))
reindex={x:i for i,x in enumerate(nodes)}
edges=[(reindex[native.edges[e][0]],reindex[native.edges[e][1]]) for e in support]
Nv=len(nodes);Ne=len(edges)
assert (Nv,Ne)==(14,16)
background=np.asarray([native.color[v] for v in nodes],int)
B=np.zeros((Ne,Nv),int);adj=[[] for _ in range(Nv)]
for k,(a,b) in enumerate(edges):
 B[k,a]=-1;B[k,b]=1
 adj[a].append((b,k,1));adj[b].append((a,k,-1))
order=[0];parent={0:None};parentedge={}
for a in order:
 for b,e,sg in adj[a]:
  if b not in parent:parent[b]=a;parentedge[b]=(a,e,sg);order.append(b)
tree={v[1] for v in parentedge.values()}
chords=[e for e in range(Ne) if e not in tree]
assert len(chords)==3 and len(order)==Nv
# Check ALL native magnetic octagons fully inside the patch, not just seed 3.
outside=np.setdiff1d(np.arange(160),support)
contained=np.flatnonzero(np.any(native.P,axis=1)&~np.any(native.P[:,outside],axis=1))
P=native.P[contained][:,support]
assert np.count_nonzero(P@B)==0
selected_chords=P[:,chords]
assert np.linalg.matrix_rank(selected_chords)==3
fermions=int(sum(background))
init=sum(int(x)<<i for i,x in enumerate(background))
def levels(max_depth):
 level={init:0}; queue=deque([init])
 while queue:
  bits=queue.popleft();dep=level[bits]
  if dep>=max_depth:continue
  for a,b in edges:
   if ((bits>>a)&1)==((bits>>b)&1):continue
   t=bits^(1<<a)^(1<<b)
   if t not in level:level[t]=dep+1;queue.append(t)
 return level
def flux(bits,l,external):
 occ=np.array([(bits>>i)&1 for i in range(Nv)],int)
 n=np.zeros(Ne,int);n[chords]=l
 accum=occ-background+external+B.T@n
 for b in reversed(order[1:]):
  a,e,sg=parentedge[b];n[e]=-sg*accum[b];accum[a]+=accum[b]
 assert accum[0]==0
 assert np.count_nonzero(B.T@n+occ-background+external)==0
 return n
def sector(depth,L,charged,g=.8,kappa=.7,beta=.4,mass=.3):
 ff=levels(depth);occur=list(sorted(ff))
 nocc=len(occur)
 ls=list(product(range(-L,L+1),repeat=3));nl=len(ls)
 lindex={m:i for i,m in enumerate(ls)};oindex={o:i for i,o in enumerate(occur)}
 ext=np.zeros(Nv,int)
 if charged:
  a,b=edges[0];ext[a]=1;ext[b]=-1
 dim=nocc*nl
 rr=[];cc=[];vv=[];diag=np.zeros(dim)
 for oi,bits in enumerate(occur):
  occ=np.array([(bits>>j)&1 for j in range(Nv)],int)
  assert sum(occ)==fermions
  stagger=mass*float((1-2*background)@occ)
  fhops=[]
  for e,(a,b) in enumerate(edges):
   oa=(bits>>a)&1;ob=(bits>>b)&1
   if oa==ob:continue
   target=bits^(1<<a)^(1<<b)
   if target not in oindex:continue
   direction=1 if oa else -1
   fermsign=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
   fhops.append((oindex[target],e,direction,fermsign))
  for mi,m in enumerate(ls):
   idx=oi*nl+mi
   n=flux(bits,m,ext)
   diag[idx]=g*g*(n@n)/2+stagger+len(P)*beta/(g*g)
   rr.append(idx);cc.append(idx);vv.append(diag[idx])
   for dest,e,direction,sign in fhops:
    new=list(m)
    if e in chords:new[chords.index(e)]-=direction
    lm=lindex.get(tuple(new))
    if lm is not None:
     rr.append(idx);cc.append(dest*nl+lm);vv.append(-kappa*sign)
   for delta in selected_chords:
    for sgn in (-1,1):
     lm=lindex.get(tuple(np.asarray(m)+sgn*delta))
     if lm is not None:
      rr.append(idx);cc.append(oi*nl+lm);vv.append(-beta/(2*g*g))
 H=coo_matrix((vv,(rr,cc)),shape=(dim,dim)).tocsr()
 asym=H-H.T; assert asym.nnz==0 or max(abs(asym.data))<1e-11
 vals,vecs=eigsh(H,k=2,which='SA',tol=2e-9,maxiter=4000)
 order_ev=np.argsort(vals);val=vals[order_ev[0]];u=vecs[:,order_ev[0]]
 weights=(abs(u.reshape(nocc,nl))**2)
 fbound=float(sum(weights[i].sum() for i,bits in enumerate(occur) if ff[bits]==depth))
 lbound=float(sum(weights[:,j].sum() for j,m in enumerate(ls) if max(abs(x) for x in m)==L))
 residual=float(np.linalg.norm(H@u-val*u))
 return {'depth':depth,'L':L,'Fock_configs':nocc,'dimension':dim,'ground':float(val),
         'gap':float(vals[order_ev[1]]-val),'Fock_boundary_weight':fbound,
         'electric_flux_boundary_weight':lbound,'eigensolver_residual':residual}
runs=[]
for depth,L in ((1,1),(2,1),(2,2),(3,1)):
 sectors={}
 for charged in (False,True):
  s=sector(depth,L,charged)
  sectors['charged' if charged else 'neutral']=s
  print('TOE62 coupled',depth,L,charged,s['dimension'],s['ground'],flush=True)
 runs.append({'depth':depth,'L':L,'charge_cost':sectors['charged']['ground']-sectors['neutral']['ground'],'sectors':sectors})
assert all(x['sectors']['neutral']['eigensolver_residual']<1e-5 for x in runs)
out={'status':'PASS_TOE62_NATIVE_INTERACTING_THREE_LOOP_MATTER_PATCH',
'native_nodes':nodes,'native_edge_ids':list(map(int,support)),'selected_seed_rows':row_ids,
'contained_native_wilson_rows':list(map(int,contained)),'contained_count':len(P),
'patch_sites':Nv,'patch_links':Ne,'independent_fluxes':len(chords),
'fermion_count':fermions,'initial_background_bitstring':init,
'parameters':{'g':.8,'kappa':.7,'magnetic_beta':.4,'mass':.3},'runs':runs,
'method':"Use all fermion configurations reachable within depth d link hops from the native alternating fermion background, plus all 3 integer chord flux modes in [-L,L]^3. Reconstruct all 16 link electric fluxes through exact spanning-tree Gauss solution for each occupancy. Include all native plaquette Wilson shifts fully supported in this patch, native signed link fermion hops, electric energy, and staggered mass. Diagonalize the explicit Hermitian Galerkin Hamiltonian in neutral and external endpoint-charge sectors.",
'limitation':"Interacting selected three-loop finite patch and restricted Fock hop-depth, not full 80-site or all 1382 active plaquette W33 Hamiltonian; simultaneous variational exhaustion of Fock and flux Hilbert is not proved. Boundary weights, residuals, static-charge differences are not physical confinement or a machine-certified spectral interval."}
(R/'data/w33_20261013_toe62_three_loop_matter.json').write_text(json.dumps(out,indent=2)+'\n')
