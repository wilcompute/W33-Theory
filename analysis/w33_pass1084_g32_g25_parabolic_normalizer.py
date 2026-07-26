from __future__ import annotations
from fractions import Fraction
from collections import deque,Counter
import json,time
from pathlib import Path
import numpy as np
P=43;OMEGA_MOD=6
DIRS=[(0,0,-1,0),(1,1,1,0),(0,1,0,0),(1,-1,0,-1)]
class E:
 __slots__=('a','b')
 def __init__(self,a=0,b=0):self.a=Fraction(a);self.b=Fraction(b)
 def __add__(self,o):o=C(o);return E(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return E(-self.a,-self.b)
 def __sub__(self,o):return self+(-C(o))
 def __rsub__(self,o):return C(o)-self
 def __mul__(self,o):o=C(o);return E(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a-self.b*o.b)
 __rmul__=__mul__
 def __truediv__(self,o):o=C(o);n=o.a*o.a-o.a*o.b+o.b*o.b;return self*E((o.a-o.b)/n,-o.b/n)
 def __eq__(self,o):o=C(o);return self.a==o.a and self.b==o.b
 def __hash__(self):return hash((self.a,self.b))
 def z(self):return self.a==0 and self.b==0
 def txt(self):
  if self.b==0:return str(self.a)
  if self.a==0:return 'w' if self.b==1 else ('-w' if self.b==-1 else f'{self.b}w')
  return f'{self.a}{"+" if self.b>0 else ""}{self.b}w'
def C(x):return x if isinstance(x,E) else E(x)
W=E(0,1);Z=E();ONE=E(1)
def I(n):return [[ONE if i==j else Z for j in range(n)] for i in range(n)]
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Z) for j in range(len(B[0]))] for i in range(len(A))]
def mpow(A,n):
 o=I(len(A));b=A
 while n:
  if n&1:o=mm(o,b)
  b=mm(b,b);n//=2
 return o
def refl_exact(v):
 n=len(v);R=I(n);den=sum(x*x for x in v)
 for i in range(n):
  for j in range(n):R[i][j]=R[i][j]+(W-ONE)*E(v[i]*v[j])/den
 return R
def refl_mod(v):
 n=len(v);den=sum(x*x for x in v)%P;c=(OMEGA_MOD-1)*pow(den,-1,P)%P
 return tuple(((1 if i==j else 0)+c*v[i]*v[j])%P for i in range(n) for j in range(n))
def mmod(A,B,n):return tuple(sum(A[n*i+k]*B[n*k+j] for k in range(n))%P for i in range(n) for j in range(n))
def ident(n):return tuple(1 if i==j else 0 for i in range(n) for j in range(n))
def group_words(gens,n):
 id=ident(n);seen={id:0};elems=[id];par=[None];q=deque([id])
 while q:
  x=q.popleft();xi=seen[x]
  for j,g in enumerate(gens):
   y=mmod(g,x,n)
   if y not in seen:seen[y]=len(elems);elems.append(y);par.append((xi,j));q.append(y)
 return elems,seen,par
def word_for(i,par):
 w=[]
 while par[i] is not None:i,j=par[i];w.append(j)
 return list(reversed(w))
def normE(v):
 for x in v:
  if not x.z():return tuple(y/x for y in v)
 raise ValueError
def cov_orbit(seed,gens):
 invTs=[]
 for g in gens:
  gi=mpow(g,2);invTs.append([[gi[j][i] for j in range(len(g))] for i in range(len(g))])
 s=normE(tuple(E(x) for x in seed));seen={s};q=deque([s])
 while q:
  v=q.popleft()
  for T in invTs:
   y=normE(tuple(sum((T[i][j]*v[j] for j in range(len(v))),Z) for i in range(len(v))))
   if y not in seen:seen.add(y);q.append(y)
 return sorted(seen,key=lambda v:tuple(x.txt() for x in v))
def eval_orbit_sum(arr,a,X,d):
 rows=np.einsum('i,nij->nj',np.array(a,dtype=np.int64),arr,optimize=True)%P;vals=rows@X.T%P
 return np.array([sum(pow(int(z),d,P) for z in vals[:,j])%P for j in range(vals.shape[1])],dtype=np.int64)
def main():
 t=time.time();R4m=[refl_mod(v) for v in DIRS];R3m=[tuple(R4m[k][4*i+j] for i in range(3) for j in range(3)) for k in range(3)];G32,idx,par=group_words(R4m,4);G25,_,_=group_words(R3m,3);assert len(G32)==155520 and len(G25)==648
 setwise=[i for i,A in enumerate(G32) if A[12]==A[13]==A[14]==0 and A[15]!=0];pointwise=[i for i in setwise if tuple(G32[i][4*r+3] for r in range(4))==(0,0,0,1)];assert len(setwise)==3888 and len(pointwise)==648
 ti=next(i for i in setwise if i not in pointwise);word=word_for(ti,par);Tm=G32[ti];T3=np.array(Tm,dtype=np.int64).reshape(4,4)[:3,:3]%P
 R4e=[refl_exact(v) for v in DIRS];Te=I(4)
 for j in word:Te=mm(R4e[j],Te)
 assert all(Te[3][j].z() for j in range(3)) and not Te[3][3].z()
 H32=cov_orbit((0,0,0,1),R4e);H25=cov_orbit((0,0,1),[[row[:3] for row in R4e[k][:3]] for k in range(3)]);restricted=[];slice_count=0
 for h in H32:
  r=h[:3]
  if all(x.z() for x in r):slice_count+=1
  else:restricted.append(normE(r))
 mult=Counter(restricted);h25=set(H25);profile=Counter(mult.values());assert len(H32)==40 and len(H25)==12 and slice_count==1 and profile==Counter({1:12,3:9}) and h25.issubset(mult)
 A25=np.array(G25,dtype=np.int16).reshape(-1,3,3);rng=np.random.default_rng(1084);X=rng.integers(0,P,size=(24,3),dtype=np.int64);cands=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1),(1,2,3),(2,3,5),(1,4,7)];invs={}
 for d,name in [(6,'u6'),(9,'v9'),(12,'w12')]:
  vals=[eval_orbit_sum(A25,a,X,d) for a in cands]
  if d==12:
   u=invs['u6'];base=(u*u)%P;k=next(i for i,v in enumerate(vals) if np.linalg.matrix_rank(np.stack([base,v],axis=1).astype(float))==2)
  else:k=next(i for i,v in enumerate(vals) if np.any(v))
  invs[name]=vals[k];invs[name+'_candidate']=k
 TX=X@T3.T%P;action={}
 for d,name in [(6,'u6'),(9,'v9'),(12,'w12')]:
  a=cands[invs[name+'_candidate']];tv=eval_orbit_sum(A25,a,TX,d);v=invs[name];nz=next(i for i,z in enumerate(v) if z);scalar=int(tv[nz])*pow(int(v[nz]),-1,P)%P;assert np.array_equal(tv,scalar*v%P);action[name]=scalar
 assert action=={'u6':1,'v9':42,'w12':1}
 out={'status':'PASS','normalizer':{'setwise_slice_stabilizer_order':3888,'pointwise_G25_order':648,'quotient':'C6; its action on the basic invariant ring factors through C2','outer_word_zero_based':word,'outer_word_one_based':[i+1 for i in word],'exact_matrix':[[x.txt() for x in row] for row in Te],'mod43_slice_matrix':T3.tolist(),'invariant_action_mod43':action},'exact_arrangement':{'G32_hyperplanes':40,'slice_factor':1,'G25_hyperplanes':12,'restricted_distinct':21,'multiplicity_profile':dict(profile),'extra_triple_hyperplanes':9},'theorem':'The setwise stabilizer of the parabolic slice has order 3888 = 648*6; modulo the pointwise G25 it is C6, and its action on the basic invariant ring factors through parity C2. Its nontrivial quotient fixes u6 and w12 and negates v9, explaining structurally why every G32 invariant restriction lies in the v9-even subring. The characteristic-zero reflecting arrangement restricts exactly as one slice factor, twelve parabolic factors once, and nine extra factors cubed.','seconds':time.time()-t}
 out['check_count']=12;out['checks']={'G25_order648':len(G25)==648,'G32_order155520':len(G32)==155520,'slice_stabilizer3888':len(setwise)==3888,'pointwise_G25_648':len(pointwise)==648,'quotient_order6':len(setwise)//len(pointwise)==6,'exact_word_lifts':len(word)>0,'exact_matrix_preserves_slice':all(Te[3][j].z() for j in range(3)),'u6_fixed':action['u6']==1,'v9_negated':action['v9']==42,'w12_fixed':action['w12']==1,'exact_arrangement_profile_12_once_9_triple':profile==Counter({1:12,3:9}),'slice_factor_unique':slice_count==1};(Path(__file__).resolve().parents[1]/'data'/'w33_pass1084_g32_g25_parabolic_normalizer.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
