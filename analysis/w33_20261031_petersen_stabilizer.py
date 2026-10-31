"""Exhaustive PSp(4,5) stabilizer and its actual ten-pair action.

Uses the Pass 12484 frozen optimum; no numerical group identification by order.
The cut-module semidirect product here is NOT the affine Mathieu group M20.
"""
import sys,pathlib,json,itertools,time,collections
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
R=ROOT
sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
from even_line_sets_gf import build

def enumerate_stabilizer():
 q=5;t0=time.time();pts,lines,N=build(q)
 pts=np.array(pts,dtype=np.int64);pid={tuple(p):i for i,p in enumerate(pts)}
 def norm(v):
  return tuple(int(x)*pow(next(int(a) for a in v if a%q),-1,q)%q for x in v)
 def inverse(a):
  a=np.concatenate([np.array(a,dtype=np.int64)%q,np.eye(len(a),dtype=np.int64)],axis=1);n=len(a)
  for i in range(n):
   k=next(k for k in range(i,n) if a[k,i]);a[[i,k]]=a[[k,i]];a[i]=a[i]*pow(int(a[i,i]),-1,q)%q
   for j in range(n):
    if j!=i:a[j]=(a[j]-a[j,i]*a[i])%q
  return a[:,n:]
 lid={frozenset(L):i for i,L in enumerate(lines)}
 src=json.loads((R/'analysis/search_drivers_12466/even_line_sets_gf_q5.json').read_text())
 S=sorted(lid[frozenset(pid[tuple(p)] for p in L)] for L in src['chosen_lines']);local={j:i for i,j in enumerate(S)}
 adj=[frozenset(j for j in range(20) if i!=j and set(lines[S[i]])&set(lines[S[j]])) for i in range(20)]
 cl=collections.defaultdict(list)
 for i in range(20):cl[adj[i]].append(i)
 pairs=sorted(tuple(c) for c in cl.values());pair_of={i:j for j,p in enumerate(pairs) for i in p}
 assert len(pairs)==10 and all(len(c)==2 for c in pairs)
 J=np.block([[np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],[-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)]])
 def frame(i,j):
  U=pts[list(lines[S[i]][:2])].T;V=pts[list(lines[S[j]][:2])].T
  return np.column_stack([U,V@inverse(U.T@J@V)%q])
 F0i=inverse(frame(*pairs[0]))
 gl=[]
 for a,b,c,d in itertools.product(range(q),repeat=4):
  if (a*d-b*c)%q:
   M=np.array([[a,b],[c,d]],dtype=np.int64);gl.append(np.block([[M,np.zeros((2,2),dtype=int)],[np.zeros((2,2),dtype=int),inverse(M).T]]))
 gl=np.array(gl)
 pointpair={tuple(sorted((a,b))):i for i,L in enumerate(lines) for a,b in itertools.combinations(L,2)}
 base=pts[np.array([lines[j][:2] for j in S])]
 matrices={};perms={}
 for u,v in pairs:
  for i,j in [(u,v),(v,u)]:
   mats=(frame(i,j)@gl@F0i)%q
   for g in mats:
    raw=(base@g.T)%q
    target=[pointpair[tuple(sorted((pid[norm(a)],pid[norm(b)])))] for a,b in raw]
    if set(target)!=set(S):continue
    key=norm(g.ravel());p=tuple(local[x] for x in target);matrices[key]=g;perms[p]=key
 print('group',len(perms),'seconds',time.time()-t0,flush=True)
 def pairperm(p):return tuple(pair_of[p[a]] for a,b in pairs)
 quot={pairperm(p) for p in perms};ker=[p for p in perms if pairperm(p)==tuple(range(10))]
 def compose(p,r):return tuple(p[r[i]] for i in range(len(p)))
 def order(p):
  cur=tuple(range(len(p)))
  for n in range(1,100):
   cur=compose(p,cur)
   if cur==tuple(range(len(p))):return n
  return None
 def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
 print('quotient',len(quot),'orders',collections.Counter(map(order,quot)),'kernel',len(ker),'orders',collections.Counter(map(order,ker)),flush=True)
 bits=[tuple(int(p[a]==b) for a,b in pairs) for p in ker]
 print('kernelweights',collections.Counter(map(sum,bits)),flush=True)
 out={'projective_stabilizer_order':len(perms),'pair_image_order':len(quot),'pair_image_element_orders':dict(collections.Counter(map(order,quot))),
      'kernel_order':len(ker),'kernel_element_orders':dict(collections.Counter(map(order,ker))),'kernel_flip_weights':dict(collections.Counter(map(sum,bits))),
      'pairs':pairs,'selected_line_indices':S,'kernel_flip_vectors':bits,'permutations':[list(p) for p in perms],
      'matrix_representatives':[matrices[key].tolist() for key in perms.values()]}
 return out

def analyze(d):
 G=[tuple(p) for p in d['permutations']];identity=tuple(range(20));pairs=d['pairs'];pair_of={a:j for j,p in enumerate(pairs) for a in p}
 def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
 def inv(p):return tuple(p.index(i) for i in range(len(p)))
 def order(p):
  z=identity
  for n in range(1,121):
   z=mul(p,z)
   if z==identity:return n
 def close(gens):
  out={identity};queue=[identity]
  for p in queue:
   for g in gens:
    z=mul(g,p)
    if z not in out:out.add(z);queue.append(z)
  return out
 def qp(p):return tuple(pair_of[p[a]] for a,b in pairs)
 def orbits(H):
  left=set(range(20));out=[]
  while left:
   a=min(left);O=sorted({p[a] for p in H});out.append(O);left.difference_update(O)
  return out
 K={p for p in G if qp(p)==tuple(range(10))};complements=[]
 r=next(p for p in G if order(p)==3)
 for s in G:
  if order(s)==5 and order(mul(r,s))==2:
   H=close([r,s]);assert len(H)==60 and len(H&K)==1
   sig=sorted(map(len,orbits(H)))
   if not any(a['orbit_lengths']==sig for a in complements):
    complements.append(dict(orbit_lengths=sig,generators=[r,s],elements=list(H)));print('complement',sig,flush=True)
   if sig==[10,10]:break
 print('all group orders',dict(collections.Counter(map(order,G))),flush=True)
 bits=[tuple(x) for x in d['kernel_flip_vectors']];stars=[x for x in bits if sum(x)==4]
 edge_labels=[tuple(i for i,s in enumerate(stars) if s[j]) for j in range(10)]
 assert sorted(edge_labels)==list(itertools.combinations(range(5),2))
 adj=lambda a,b: len(set(edge_labels[a])&set(edge_labels[b]))==0
 # Recover line adjacency from saved geometry, not from the abstract code alone.
 R=ROOT;sys.path.insert(0,str(R/'analysis/search_drivers_12466'))
 from even_line_sets_gf import build
 pts,lines,N=build(5);S=d['selected_line_indices']
 assert all(bool(set(lines[S[pairs[i][0]]])&set(lines[S[pairs[j][0]]]))==adj(i,j) for i,j in itertools.combinations(range(10),2))
 print('kernel is exactly K5 cut code, pair graph exactly Kneser(5,2)',flush=True)
 simple=next((a for a in complements if a['orbit_lengths']==[10,10]),None)
 if simple:
  O=set(orbits(simple['elements'])[0]);sign={a:int(a not in O) for a in range(20)}
  def action_data(g):
   # g conjugates the five weight-four kernel elements, equivalently pushes their supports.
   qq=qp(g);sigma=[]
   for st in stars:
    image=tuple(st[qq.index(j)] for j in range(10));sigma.append(stars.index(image))
   flips=[sign[g[a]]^sign[a] for a,b in pairs]
   choices=[v for v in itertools.product(range(2),repeat=5) if sum(v)%2==0 and all(v[i]^v[j]==flips[k] for k,(i,j) in enumerate(edge_labels))]
   assert len(choices)==1
   eps=choices[0]
   # eps is indexed by input axes. Image of ray e_i+(-1)^s e_j is
   # (-1)^eps_i e_sigma_i +(-1)^(s+eps_j)e_sigma_j.
   for a in range(20):
    i,j=edge_labels[pair_of[a]]
    assert set(edge_labels[pair_of[g[a]]])=={sigma[i],sigma[j]}
    assert sign[g[a]]==(sign[a]^eps[i]^eps[j])
   return dict(sigma=sigma,input_axis_signs=eps)
  actions=[action_data(g) for g in G]
  print('exact equivariant D5 root-ray action verified for all',len(G),'elements',flush=True)
 else:actions=None;print('No 10+10 complement found')
 out={k:v for k,v in d.items() if k not in ['permutations','matrix_representatives']}
 out.update(group_element_order_counts=dict(collections.Counter(map(order,G))),split_extension=True,
            complement_types=[{k:v for k,v in a.items() if k!='elements'} for a in complements],kernel_stars=stars,K5_edge_labels=edge_labels,
            equivariant_D5_root_rays=bool(actions),signed_axis_actions=actions,ray_signs=sign if actions else None)
 return out

def representation(d, result):
 G=[tuple(p) for p in d['permutations']];ident=tuple(range(20));pairs=d['pairs']
 pair_of={a:j for j,p in enumerate(pairs) for a in p}
 mul=lambda a,b:tuple(a[b[i]] for i in range(20))
 inv=lambda a:tuple(a.index(i) for i in range(20))
 qp=lambda a:tuple(pair_of[a[x]] for x,y in pairs)
 stars=[tuple(s) for s in result['kernel_stars']]
 edge=[tuple(e) for e in result['K5_edge_labels']]
 def group_closure(gens):
  out={ident};todo=[ident]
  for a in todo:
   for g in gens:
    b=mul(g,a)
    if b not in out:out.add(b);todo.append(b)
  return out
 Hgens=[tuple(g) for g in result['complement_types'][0]['generators']]
 H=group_closure(Hgens);byq={qp(h):h for h in H};assert len(byq)==60
 K=[g for g in G if qp(g)==tuple(range(10))]
 bits=lambda g:tuple(int(g[a]==b) for a,b in pairs)
 vertexbits={tuple(v[i]^v[j] for i,j in edge):tuple(v) for v in itertools.product(range(2),repeat=5) if sum(v)%2==0}
 assert len(vertexbits)==16
 def rep(g):
  qq=qp(g);h=byq[qq];k=mul(g,inv(h));eps=vertexbits[bits(k)]
  sigma=[stars.index(tuple(st[qq.index(j)] for j in range(10))) for st in stars]
  M=np.zeros((5,5),dtype=int)
  for i,j in enumerate(sigma):M[j,i]=(-1)**eps[j]
  return M
 reps={g:rep(g) for g in G}
 Kgens=[];span={ident}
 for k in K:
  if k not in span:Kgens.append(k);span=group_closure(Kgens)
 gens=Kgens+Hgens;assert len(group_closure(gens))==960
 commutators=[mul(mul(mul(a,b),inv(a)),inv(b)) for a in gens for b in gens]
 normal_commutators={mul(mul(h,c),inv(h)) for h in H for c in commutators}
 assert len(group_closure(normal_commutators))==960
 assert all(np.array_equal(reps[mul(g,h)],reps[g]@reps[h]) for g in G for h in gens)
 assert len({tuple(M.ravel()) for M in reps.values()})==960
 assert all(np.array_equal(M.T@M,np.eye(5,dtype=int)) and round(np.linalg.det(M))==1 for M in reps.values())
 # Every order-3 element is conjugate to the chosen one. Thus every A5
 # complement is conjugate to one enumerated in analyze(), which fixes it.
 r=Hgens[0];conjugates={mul(mul(g,r),inv(g)) for g in G};assert len(conjugates)==80
 assert result['complement_types']==[result['complement_types'][0]] and result['complement_types'][0]['orbit_lengths']==[20]
 mats=d['matrix_representatives'];mat_for={g:np.array(M,dtype=int) for g,M in zip(G,mats)}
 lifted=[sg*mat_for[k]%5 for k in K for sg in (1,-1)]
 I=np.eye(4,dtype=int);minus=-I%5
 sqtypes=collections.Counter()
 for A in lifted:
  A_squared=A@A%5
  if np.array_equal(A,I):sqtypes[1]+=1
  elif np.array_equal(A_squared,I):sqtypes[2]+=1
  else:assert np.array_equal(A_squared,minus);sqtypes[4]+=1
 assert sqtypes=={1:1,2:11,4:20}
 assert all(np.array_equal((A@B)%5,(B@A)%5) or np.array_equal((A@B)%5,(-B@A)%5) for A in lifted for B in lifted)
 matrix_gens=[mat_for[g].tolist() for g in gens]
 result.update(group_name='cut(F2,K5) semidirect A5 = derived subgroup of W(D5)',
   not_M20='This module has nonzero orbits 5+10 and 240 order-six elements; affine M20=ASL(2,4) has the other 4-dimensional F2 A5 module.',
   signed_five_dimensional_generators=[reps[g].tolist() for g in gens],
   projective_permutation_generators=[list(g) for g in gens],symplectic_matrix_generators=matrix_gens,
   homomorphism_products_checked=960*len(gens),faithful_signed_SO5_representation=True,
   perfect_group=True,minimum_faithful_real_dimension=5,
   representation_dimension_proof='The normal even-sign group has 15 nontrivial characters in A5 orbits of lengths 5 and 10 (self-dual deleted permutation module). A representation nontrivial on this kernel contains a whole such character orbit, hence dimension >=5. The signed SO5 witness attains 5.',
   order_three_conjugacy_size=80,
   no_equivariant_D5_root_ray_action='Every A5 complement is transitive on these 20 lines; in the signed-coordinate D5 root-ray action the unsigned A5 complement has two orbits of 10. The equal counts do not give an equivariant identification.',
   lifted_kernel_order=32,lifted_kernel_order_counts=dict(sqtypes),lifted_kernel_type='extraspecial minus type 2_-^(1+4)',
   invariant_metric='In the signed 5D representation the even sign subgroup forces a symmetric invariant form to be diagonal and A5 forces all five diagonal entries equal. Nondegenerate invariant forms are definite, not Lorentzian.')
 return result

def qubit_intertwiner(result):
 """Explicitly reduce Q8 central-product D8 Pauli matrices via i -> 2 mod5.

 This identifies the actual lifted kernel, not the full stabilizer, with a
 two-qubit operator presentation. It is distinct from the repo's qutrit H27.
 """
 I=np.eye(4,dtype=int);minus=-I%5
 gens=[np.array(g,dtype=int) for g in result['symplectic_matrix_generators'][:4]]
 key=lambda M:tuple(int(x) for x in M.ravel())
 seen={key(I):I};queue=[I]
 for M in queue:
  for g in gens:
   V=g@M%5
   if key(V) not in seen:seen[key(V)]=V;queue.append(V)
 assert len(queue)==32
 noncentral=[M for M in queue if not np.array_equal(M,I) and not np.array_equal(M,minus)]
 minus_square=[M for M in noncentral if np.array_equal(M@M%5,minus)]
 A,B=next((A,B) for A in minus_square for B in minus_square if np.array_equal(A@B%5,-B@A%5))
 complement=[M for M in noncentral if np.array_equal(M@M%5,I) and np.array_equal(M@A%5,A@M%5) and np.array_equal(M@B%5,B@M%5)]
 C,D=next((C,D) for C in complement for D in complement if np.array_equal(C@D%5,-D@C%5))
 X=np.array([[0,1],[1,0]],dtype=int);Z=np.diag([1,-1]);I2=np.eye(2,dtype=int)
 canonical=[2*np.kron(X,I2)%5,2*np.kron(Z,I2)%5,np.kron(I2,X)%5,np.kron(I2,Z)%5]
 actual=[A,B,C,D];rows=[]
 for G,T in zip(actual,canonical):
  for r in range(4):
   for c in range(4):
    row=np.zeros(16,dtype=int)
    for k in range(4):row[k*4+c]+=G[r,k];row[r*4+k]-=T[k,c]
    rows.append(row%5)
 E=np.array(rows);pivots=[];row=0
 for c in range(16):
  candidates=[k for k in range(row,len(E)) if E[k,c]]
  if not candidates:continue
  k=candidates[0];E[[row,k]]=E[[k,row]];E[row]=E[row]*pow(int(E[row,c]),-1,5)%5
  for j in range(len(E)):
   if j!=row:E[j]=(E[j]-E[j,c]*E[row])%5
  pivots.append(c);row+=1
 free=[j for j in range(16) if j not in pivots];assert len(free)==1
 v=np.zeros(16,dtype=int);v[free[0]]=1
 for r,c in enumerate(pivots):v[c]=-E[r,free[0]]%5
 S=v.reshape(4,4);assert round(np.linalg.det(S))%5!=0
 assert all(np.array_equal(G@S%5,S@T%5) for G,T in zip(actual,canonical))
 return dict(kernel_order=32,actual_symplectic_generators=[M.tolist() for M in actual],
   reduced_Pauli_generators=[M.tolist() for M in canonical],intertwiner_mod5=S.tolist(),
   complex_Pauli_presentation=['i X tensor I','i Z tensor I','I tensor X','I tensor Z'],
   reduction='Gaussian integer reduction i -> 2 in F5; S T_i = actual_i S',
   boundary='Exact kernel dictionary only. The full complex unitary stabilizer lift and a physical qubit/qutrit coupling are not constructed.')

def main():
 d=enumerate_stabilizer();result=representation(d,analyze(d))
 result['two_qubit_kernel_intertwiner']=qubit_intertwiner(result)
 (ROOT/'data/w33_20261031_petersen_stabilizer.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print('PASS: full stabilizer, cut code, split extension, faithful SO5 representation, and extraspecial lift')
if __name__=='__main__':main()
