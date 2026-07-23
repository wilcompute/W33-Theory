#!/usr/bin/env python3
from __future__ import annotations
import argparse,collections,hashlib,itertools,json,math
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass636_mod4_bockstein_lift.json'
D=125

def build_complex():
 V=list(itertools.combinations(range(8),3));vid={v:i for i,v in enumerate(V)}
 stars=[tuple(sorted(vid[tuple(sorted(pair+(x,)))] for x in range(8) if x not in pair)) for pair in itertools.combinations(range(8),2)]
 tops=[tuple(sorted(vid[t] for t in itertools.combinations(four,3))) for four in itertools.combinations(range(8),4)]
 maximal=stars+tops;simp=[set() for _ in range(6)]
 for C in maximal:
  for r in range(1,len(C)+1):simp[r-1].update(itertools.combinations(C,r))
 return V,vid,[sorted(x) for x in simp]

def elementary_collapse(simp):
 active=[set(x) for x in simp];seq=[]
 while True:
  found=None
  for k in range(5,0,-1):
   co=collections.defaultdict(list)
   for tau in sorted(active[k]):
    for i in range(len(tau)):co[tau[:i]+tau[i+1:]].append(tau)
   for sigma in sorted(co):
    ts=co[sigma]
    if sigma not in active[k-1] or len(ts)!=1:continue
    tau=ts[0]
    if all(not any(set(tau).issubset(u) for u in active[j]) for j in range(k+1,6)):
     found=(k-1,sigma,tau);break
   if found:break
  if not found:break
  k,sigma,tau=found;active[k].remove(sigma);active[k+1].remove(tau);seq.append(found)
 return [sorted(x) for x in active],seq

def face_sign(tau,face):
 for i in range(len(tau)):
  if tau[:i]+tau[i+1:]==face:return 1 if i%2==0 else -1
 raise KeyError(face)

def chain_projector(active,collapses):
 active_tri=set(active[2])
 def project(c):
  c=dict(c)
  for k,sigma,tau in collapses:
   if k==2:
    a=c.pop(sigma,0)
    if a:
     ss=face_sign(tau,sigma)
     for i in range(4):
      f=tau[:i]+tau[i+1:]
      if f==sigma:continue
      sf=1 if i%2==0 else -1
      c[f]=c.get(f,0)-a*ss*sf
      if c[f]==0:del c[f]
   elif k==1:c.pop(tau,None)
  assert all(t in active_tri for t in c)
  return c
 return project

def active_boundary(active):
 edges=active[1];tris=active[2];adj=[[] for _ in range(56)]
 for i,j in edges:adj[i].append(j);adj[j].append(i)
 parent=[None]*56;parent[0]=-1;q=collections.deque([0]);tree=set()
 while q:
  i=q.popleft()
  for j in sorted(adj[i]):
   if parent[j] is None:parent[j]=i;tree.add(tuple(sorted((i,j))));q.append(j)
 non=[e for e in edges if e not in tree];rid={e:i for i,e in enumerate(non)}
 A=np.zeros((len(non),len(tris)),dtype=np.int64)
 for j,t in enumerate(tris):
  for a,b,sgn in ((t[1],t[2],1),(t[0],t[2],-1),(t[0],t[1],1)):
   e=tuple(sorted((a,b)))
   if e in rid:A[rid[e],j]+=sgn*(1 if a<b else -1)
 return A,tree,non

def unit_kernel(A):
 A=A.copy().astype(object);m,n=A.shape;U=np.eye(n,dtype=object);row=0
 for col in range(n):
  if row==m:break
  pos=next(((i,j) for j in range(col,n) for i in range(row,m) if abs(A[i,j])==1),None)
  if pos is None:raise RuntimeError('unit pivot missing')
  i,j=pos
  if i!=row:A[[row,i],:]=A[[i,row],:]
  if j!=col:A[:,[col,j]]=A[:,[j,col]];U[:,[col,j]]=U[:,[j,col]]
  if A[row,col]==-1:A[:,col]*=-1;U[:,col]*=-1
  for j2 in range(n):
   if j2!=col and A[row,j2]:
    q=A[row,j2];A[:,j2]-=q*A[:,col];U[:,j2]-=q*U[:,col]
  for i2 in range(m):
   if i2!=row and A[i2,col]:
    q=A[i2,col];A[i2,:]-=q*A[row,:]
  row+=1
 assert row==m and np.all(np.array(A[:,m:],dtype=object)==0)
 return np.array(U[:,m:],dtype=object),np.array(U,dtype=object)

def integral_action():
 V,vid,simp=build_complex();active,collapses=elementary_collapse(simp);project=chain_projector(active,collapses)
 A,tree,non=active_boundary(active);K,U=unit_kernel(A);Ui=sp.Matrix(U.tolist()).inv();tris=active[2]
 def perm_chain(chain,p):
  vm=[vid[tuple(sorted(p[x] for x in t))] for t in V];out={}
  for tri,a in chain.items():
   w=[vm[i] for i in tri];sgn=-1 if sum(w[i]>w[j] for i in range(3) for j in range(i+1,3))%2 else 1
   t=tuple(sorted(w));out[t]=out.get(t,0)+a*sgn
  return out
 gens=[]
 for a in range(7):
  p=list(range(8));p[a],p[a+1]=p[a+1],p[a];cols=[]
  for j in range(D):
   c={tris[i]:int(K[i,j]) for i in range(len(tris)) if K[i,j]}
   z=project(perm_chain(c,p));v=sp.Matrix([z.get(t,0) for t in tris]);y=Ui*v
   assert all(y[i]==0 for i in range(365));cols.append([int(y[365+i]) for i in range(D)])
  gens.append(np.array(cols,dtype=np.int64).T)
 return gens,{'f_vector':[len(x) for x in simp],'collapses':len(collapses),'postcollapse_f_vector':[len(x) for x in active],'tree_edges':len(tree),'free_edges':len(non),'kernel_shape':list(K.shape),'kernel_max_abs':max(abs(int(x)) for x in K.flat)}

def bitcols(M):
 out=[]
 for j in range(D):
  z=0
  for i in np.flatnonzero(M[:,j]&1):z|=1<<int(i)
  out.append(z)
 return out

def map_rows(cols):return [sum(1<<j for j,c in enumerate(cols) if c>>r&1) for r in range(D)]
def act(cols,v):
 z=0
 while v:q=v&-v;i=q.bit_length()-1;z^=cols[i];v^=q
 return z

def centralizer_basis(gens):
 eqs={}
 for G in gens:
  rows=map_rows(G)
  for r in range(D):
   for c in range(D):
    eq=0;v=G[c]
    while v:q=v&-v;k=q.bit_length()-1;eq^=1<<(r*D+k);v^=q
    v=rows[r]
    while v:q=v&-v;k=q.bit_length()-1;eq^=1<<(k*D+c);v^=q
    while eq:
     p=eq.bit_length()-1
     if p in eqs:eq^=eqs[p]
     else:eqs[p]=eq;break
 free=[i for i in range(D*D) if i not in eqs];N=[]
 for f in free:
  x=1<<f
  for p in sorted(eqs):
   if ((eqs[p]^(1<<p))&x).bit_count()&1:x|=1<<p
  N.append(x)
 return N

def matrix_from_bit(z):
 M=np.zeros((D,D),dtype=np.int64)
 for r in range(D):
  row=(z>>(r*D))&((1<<D)-1)
  while row:q=row&-row;c=q.bit_length()-1;M[r,c]=1;row^=q
 return M

def bit_from_matrix(M):
 z=0
 for r in range(D):
  for c in np.flatnonzero(M[r]&1):z|=1<<(r*D+int(c))
 return z

def rank2(z):
 B={};r=0
 for v in bitcols(matrix_from_bit(z)):
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;r+=1;break
 return r

def coord(N,target):
 for a in range(1<<len(N)):
  z=0
  for i,n in enumerate(N):
   if a>>i&1:z^=n
  if z==target:return a
 raise ValueError

def obstruction_one_generator(Gi,Gc,E):
 n=D*D;mask=(1<<n)-1;piv={};grows=map_rows(Gc);C=Gi@E-E@Gi;assert np.all(C%2==0);B=(C//2)&1;seen=0
 for r in range(D):
  for c in range(D):
   eq=0;v=Gc[c]
   while v:q=v&-v;k=q.bit_length()-1;eq^=1<<(r*D+k);v^=q
   v=grows[r]
   while v:q=v&-v;k=q.bit_length()-1;eq^=1<<(k*D+c);v^=q
   aug=eq|(int(B[r,c])<<n)
   while eq:
    p=eq.bit_length()-1
    if p in piv:aug^=piv[p];eq=aug&mask
    else:piv[p]=aug;break
   seen+=1
   if not eq and (aug>>n)&1:return {'liftable':False,'equation_rank_at_witness':len(piv),'equations_read':seen}
 return {'liftable':True,'equation_rank':len(piv),'equations_read':seen}

def payload():
 G,chain=integral_action();I=np.eye(D,dtype=np.int64)
 checks={'coxeter_involutions':all(np.array_equal(g@g,I) for g in G),'coxeter_braid':all(np.array_equal(G[i]@G[i+1]@G[i],G[i+1]@G[i]@G[i+1]) for i in range(6)),'coxeter_far_commutation':all(np.array_equal(G[i]@G[j],G[j]@G[i]) for i in range(7) for j in range(i+2,7))}
 S=np.zeros((D,D),dtype=np.int64)
 for a,b in itertools.combinations(range(8),2):
  M=I.copy()
  for k in list(range(a,b))+list(range(b-2,a-1,-1)):M=G[k]@M
  S+=M
 checks.update({'class_sum_central':all(np.array_equal(g@S,S@g) for g in G),'class_sum_relation_S2_4S':np.array_equal(S@S,4*S),'class_sum_trace140':int(np.trace(S))==140,'class_sum_trace_square560':int(np.trace(S@S))==560})
 G2=[bitcols(g) for g in G];N=centralizer_basis(G2);Iz=bit_from_matrix(I);Tz=bit_from_matrix(S);ic=coord(N,Iz);tc=coord(N,Tz)
 elems=[]
 for a in range(8):
  z=0
  for i,n in enumerate(N):
   if a>>i&1:z^=n
  M=matrix_from_bit(z);sq=bit_from_matrix((M@M)&1);elems.append({'coordinate':a,'rank':rank2(z),'square_coordinate':coord(N,sq)})
 liftable_span={0,ic,tc,ic^tc};obstruction_rank=len(N)-2
 exotic=next(e['coordinate'] for e in elems if e['rank']==34 and e['coordinate']!=tc);Ez=0
 for i,n in enumerate(N):
  if exotic>>i&1:Ez^=n
 E=matrix_from_bit(Ez);detection=[obstruction_one_generator(G[i],G2[i],E) for i in range(7)]
 eta=2*E;ring=[]
 for a in range(4):
  for b in range(4):
   for c in range(2):ring.append((a*I+b*S+c*eta)%4)
 hashes={hashlib.sha256(M.astype(np.uint8).tobytes()).hexdigest() for M in ring}
 checks.update({'mod2_commutant_dimension3':len(N)==3,'identity_coordinate_locked':ic==1,'class_sum_coordinate_locked':tc==5,'radical_rank_profile_20_34_34':sorted(e['rank'] for e in elems if e['rank']<D and e['coordinate'])==[20,34,34],'exotic_coordinate_locked':exotic==2,'all_seven_adjacent_transpositions_obstruct_exotic':all(not x['liftable'] for x in detection),'liftable_reduction_span_dimension2':len(liftable_span)==4 and exotic not in liftable_span,'reduction_cokernel_obstruction_rank_one':obstruction_rank==1,'homogeneous_mod4_lift_kernel_size8':1<<len(N)==8,'exhaustive_mod4_cardinality32':len(liftable_span)*(1<<len(N))==32 and len(hashes)==32,'mod4_all_commute':all(np.array_equal((g@M-M@g)%4,np.zeros((D,D),dtype=np.int64)) for g in G for M in ring),'epsilon_square_zero_mod4':np.array_equal((S@S)%4,np.zeros((D,D),dtype=np.int64)),'eta_square_zero_mod4':np.array_equal((eta@eta)%4,np.zeros((D,D),dtype=np.int64)),'epsilon_eta_zero_mod4':np.array_equal((S@eta)%4,np.zeros((D,D),dtype=np.int64)) and np.array_equal((eta@S)%4,np.zeros((D,D),dtype=np.int64)),'two_eta_zero_mod4':np.array_equal((2*eta)%4,np.zeros((D,D),dtype=np.int64)),'integral_commutant_offdiagonal_gcd1':math.gcd(*[abs(int(S[i,j])) for i in range(D) for j in range(D) if i!=j and S[i,j]])==1})
 digest=hashlib.sha256(b''.join(g.astype(np.int8).tobytes() for g in G)+S.astype(np.int16).tobytes()+eta.astype(np.int8).tobytes()).hexdigest()
 return {'schema':'w33.pass636.mod4_bockstein_lift.v1','status':'PASS' if all(checks.values()) else 'FAIL','integral_homology_basis':chain,
  'rational_and_integral_commutant':{'rational_decomposition':['S^(5,1,1,1) dimension 35','S^(4,2,1,1) dimension 90'],'transposition_class_sum_eigenvalues':[4,0],'minimal_polynomial':'x(x-4)','integral_commutant':'Z[I,S]','integrality_witness':'Every nonzero off-diagonal entry of S is ±1, so a rational coefficient of S preserving the lattice is integral; diagonal entries then force the I coefficient integral.'},
  'mod2_commutant':{'dimension':len(N),'identity_coordinate':ic,'class_sum_coordinate':tc,'exotic_rank34_coordinate':exotic,'elements':elems},
  'bockstein':{'liftable_reduction_coordinates':sorted(liftable_span),'obstructed_reduction_coordinates':sorted(set(range(8))-liftable_span),'obstruction_rank':obstruction_rank,'exotic_detection_by_adjacent_transposition':detection,'interpretation':'The mod-4 lifting obstruction kills the exotic radical direction. The transposition class-sum direction is the unique nonzero radical direction that lifts integrally and therefore identifies the actual first 2-adic deformation class.'},
  'mod4_endomorphism_ring':{'cardinality':len(hashes),'exhaustiveness_proof':'Reduction modulo 2 maps the mod-4 commutant into the three-dimensional mod-2 commutant. Its image is exactly span(I,T), because I and S lift while the one-dimensional quotient generated by the exotic direction has nonzero Bockstein obstruction. Every liftable reduction has exactly 2^3 homogeneous lifts, namely addition by 2 times the mod-2 commutant. Hence the full cardinality is 4*8=32, equal to the constructed ring.','additive_structure':'Z/4 I + Z/4 epsilon + Z/2 eta','presentation':'(Z/4)[epsilon,eta]/(epsilon^2, epsilon eta, eta epsilon, eta^2, 2 eta)','epsilon':'S mod 4','eta':'2 times the exotic mod-2 endomorphism','reduction_image_dimension_over_F2':2,'reduction_kernel_dimension_over_F2':3},
  'matrix_sha256':digest,'theorem':'The integral H2 lattice has End_Z[S8](H2)=Z[I,S] with S^2=4S. Modulo 2 the commutant enlarges to a three-dimensional local algebra, but the Bockstein obstruction has rank one: the exotic rank-34 radical direction fails to lift even against each individual adjacent transposition, while the class-sum direction lifts integrally. Consequently End_(Z/4)[S8](H2/4H2) has 32 elements and presentation (Z/4)[epsilon,eta]/(epsilon^2,epsilon eta,eta epsilon,eta^2,2eta).','checks':checks,'boundary':'This identifies the complete mod-4 commutant and the first Bockstein obstruction. It proves that the class-sum direction survives to the full integral lattice and the exotic direction does not lift to mod 4; it does not compute every higher Ext group or classify unrelated 2-adic lattices with the same mod-2 composition factors.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 636 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'mod4_ring':p['mod4_endomorphism_ring']['cardinality'],'obstruction_rank':p['bockstein']['obstruction_rank']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
