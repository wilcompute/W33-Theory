from pathlib import Path
import importlib.util, numpy as np, os, os
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("dw",ROOT/"analysis/w33_diagonal_weld_e8_lie_generation.py");dw=importlib.util.module_from_spec(sp);sp.loader.exec_module(dw)
compiler,bridge,table=dw.load_inputs();amps=dw.backgrounds(bridge);vecs=dw.source_generators(compiler,amps)
P=int(os.environ.get("W33_SPLIT_PRIME", "107"))
print("prime",P)
L,_=dw.closure((vecs[(1,"center")],vecs[(2,"center")]),table,dw.ModularBasis(P),P); B=L.vectors
assert len(B)==24
class MB:
 def __init__(self,n):self.n=n;self.rows={};self.vecs=[]
 def add(self,v):
  v=[int(x)%P for x in v]
  for q in sorted(self.rows):
   if v[q]:
    f=v[q];r=self.rows[q];v=[(a-f*b)%P for a,b in zip(v,r)]
  q=next((i for i,x in enumerate(v) if x),None)
  if q is None:return False
  iv=pow(v[q],-1,P);v=[x*iv%P for x in v];self.rows[q]=v;self.vecs.append(v);return True
 def reduce(self,v):
  v=[int(x)%P for x in v]
  for q in sorted(self.rows):
   if v[q]:
    f=v[q];r=self.rows[q];v=[(a-f*b)%P for a,b in zip(v,r)]
  return v
 def dim(self):return len(self.rows)
def br(a,b):return [x%P for x in dw.bracket(a,b,table,P)]
def ideal(seed,ambient=B):
 M=MB(248);q=[]
 if M.add(seed):q=[M.vecs[-1]]
 while q:
  v=q.pop()
  for g in ambient:
   if M.add(br(g,v)):q.append(M.vecs[-1])
 return M
ideals={}
for i,v in enumerate(B):
 I=ideal(v);ideals.setdefault(tuple(sorted(I.rows)),(i,I))
print("ideal inventory",sorted((I.dim(),i) for i,I in ideals.values()))
# find 15 radical and 9 Heisenberg nested ideal by dimensions
I15=next(I for i,I in ideals.values() if I.dim()==15)
I9=next(I for i,I in ideals.values() if I.dim()==9 and all((lambda M: M.dim()==15)(M) for M in [])) if False else None
# choose 9D ideal contained in I15 if present
for i,I in ideals.values():
 if I.dim()==9:
  T=MB(248)
  for v in I15.vecs:T.add(v)
  old=T.dim()
  for v in I.vecs:T.add(v)
  if T.dim()==15:I9=I;break
print("I15",I15.dim(),"I9",I9.dim() if I9 else None)
assert I9 is not None
# quotient helpers
def quotient(Avals,Bvals):
 base=MB(248)
 for v in Bvals:base.add(v)
 Q=MB(248)
 for v in Avals:Q.add(base.reduce(v))
 piv=sorted(Q.rows);rows=[Q.rows[p] for p in piv]
 return base,rows,piv
baseI,qb,qp=quotient(B,I15.vecs);assert len(qb)==9
def coords(v,base,rows,pivs):
 r=base.reduce(v);co=[]
 for p,row in zip(pivs,rows):
  c=r[p]%P;co.append(c)
  if c:r=[(a-c*b)%P for a,b in zip(r,row)]
 assert not any(r);return co
def qcoords(v):return coords(v,baseI,qb,qp)
def qamb(x):
 v=[0]*248
 for c,b in zip(x,qb):
  if c:v=[(a+c*bb)%P for a,bb in zip(v,b)]
 return v
std=np.eye(9,dtype=int).tolist()
def qbr(x,y):return qcoords(br(qamb(x),qamb(y)))
ads=[np.array([qbr(e,f) for f in std],dtype=int).T%P for e in std]
def rank(A):
 if isinstance(A,np.ndarray):A=A.tolist()
 A=[list(map(lambda x:int(x)%P,r)) for r in A];rr=0
 if not A:return 0
 for c in range(len(A[0])):
  pi=next((i for i in range(rr,len(A)) if A[i][c]),None)
  if pi is None:continue
  A[rr],A[pi]=A[pi],A[rr];iv=pow(A[rr][c],-1,P);A[rr]=[x*iv%P for x in A[rr]]
  for i in range(len(A)):
   if i!=rr and A[i][c]:
    f=A[i][c];A[i]=[(x-f*y)%P for x,y in zip(A[i],A[rr])]
  rr+=1
 return rr
def nullbasis(A,nc):
 A=[r[:] for r in A];rr=0;piv=[]
 for c in range(nc):
  pi=next((i for i in range(rr,len(A)) if A[i][c]%P),None)
  if pi is None:continue
  A[rr],A[pi]=A[pi],A[rr];iv=pow(A[rr][c],-1,P);A[rr]=[x*iv%P for x in A[rr]]
  for i in range(len(A)):
   if i!=rr and A[i][c]:
    f=A[i][c];A[i]=[(x-f*y)%P for x,y in zip(A[i],A[rr])]
  piv.append(c);rr+=1
 free=[c for c in range(nc) if c not in piv];out=[]
 for f in free:
  v=[0]*nc;v[f]=1
  for ri,p in enumerate(piv):v[p]=(-A[ri][f])%P
  out.append(v)
 return out
# centroid
eq=[];n=9
for A in ads:
 for r in range(n):
  for c in range(n):
   row=[0]*(n*n)
   for k in range(n):row[r*n+k]=(row[r*n+k]+int(A[k,c]))%P
   for k in range(n):row[k*n+c]=(row[k*n+c]-int(A[r,k]))%P
   if any(row):eq.append(row)
cent=[np.array(v,dtype=int).reshape(n,n)%P for v in nullbasis(eq,n*n)]
print("centdim",len(cent));assert len(cent)==3
C=None;roots=None
for coeff in [(1,0,0),(0,1,0),(1,1,0),(1,2,3),(2,3,5),(1,5,17)]:
 T=sum((c*A for c,A in zip(coeff,cent)),np.zeros((n,n),dtype=int))%P
 rs=[]
 for r in range(P):
  nu=n-rank((T-r*np.eye(n,dtype=int))%P)
  if nu:rs.append((r,nu))
 if sorted(nu for _,nu in rs)==[3,3,3]:
  C=T;roots=[r for r,_ in rs];print("split",coeff,rs);break
assert C is not None
# projectors and factor coordinate bases
I=np.eye(n,dtype=int); factors=[]
for r in roots:
 Pr=I.copy();den=1
 for ss in roots:
  if ss==r:continue
  Pr=Pr@((C-ss*I)%P)%P;den=den*((r-ss)%P)%P
 Pr=Pr*pow(int(den),-1,P)%P
 M=MB(n)
 for j in range(n):M.add(Pr[:,j].tolist())
 V=[M.rows[p] for p in sorted(M.rows)];assert len(V)==3;factors.append(V)
print("factor_dims",[len(v) for v in factors])
# Z, W8, U6
Z=MB(248)
for a in I15.vecs:
 for b in I15.vecs:Z.add(br(a,b))
assert Z.dim()==1
baseZ,V14,p14=quotient(I15.vecs,Z.vecs)
baseZ8,V8,p8=quotient(I9.vecs,Z.vecs)
base9,U6,p6=quotient(I15.vecs,I9.vecs)
print("modules",len(V14),len(V8),len(U6));assert (len(V14),len(V8),len(U6))==(14,8,6)
def act(qx,base,mods,pivs):
 g=qamb(qx);A=np.zeros((len(mods),len(mods)),dtype=int)
 for j,v in enumerate(mods):A[:,j]=coords(br(g,v),base,mods,pivs)
 return A%P
def invdim(ms,nm):return nm-rank(np.vstack(ms)%P)
def movedbasis(ms,nm):
 M=MB(nm)
 for A in ms:
  for j in range(nm):M.add(A[:,j].tolist())
 return [M.rows[p] for p in sorted(M.rows)]
def commdim(ms,nm):
 eq=[]
 for A in ms:
  for r in range(nm):
   for c in range(nm):
    row=[0]*(nm*nm)
    for k in range(nm):row[r*nm+k]=(row[r*nm+k]+int(A[k,c]))%P
    for k in range(nm):row[k*nm+c]=(row[k*nm+c]-int(A[r,k]))%P
    if any(row):eq.append(row)
 return len(nullbasis(eq,nm*nm))
allW=[];allU=[];mU=[]
for i,F in enumerate(factors):
 Wm=[act(x,baseZ8,V8,p8) for x in F];Um=[act(x,base9,U6,p6) for x in F]
 allW+=Wm;allU+=Um;moved=movedbasis(Um,6);mU.append(moved)
 print("factor",i,"W_inv",invdim(Wm,8),"W_move",len(movedbasis(Wm,8)),"U_inv",invdim(Um,6),"U_move",len(moved))
print("commdims",commdim(allW,8),commdim(allU,6))
SUM=MB(6)
for M in mU:
 for v in M:SUM.add(v)
print("U_moved_direct_sum",SUM.dim(),[len(x) for x in mU])
for i,F in enumerate(factors):
 ms=[act(x,base9,U6,p6) for x in F]
 for j,M in enumerate(mU):
  nz=False
  for A in ms:
   for v in M:
    if any((A@np.array(v,dtype=int))%P):nz=True
  print("cross",i,j,"acts",nz)

# Strong module fingerprint: Burnside algebra dimensions and polynomial invariants.
def algdim(mats,nm):
 M=MB(nm*nm);eye=np.eye(nm,dtype=int);M.add(eye.reshape(-1).tolist());q=[eye]
 while q:
  X=q.pop()
  for G in mats:
   Y=X@G%P
   if M.add(Y.reshape(-1).tolist()):q.append(np.array(M.vecs[-1],dtype=int).reshape(nm,nm)%P)
 return M.dim()
for i,F in enumerate(factors):
 Wm=[act(x,baseZ8,V8,p8) for x in F];Um=[act(x,base9,U6,p6) for x in F]
 print("factor",i,"assoc W8/U6",algdim(Wm,8),algdim(Um,6))
print("full assoc W8/U6",algdim(allW,8),algdim(allU,6))

def monomials(n,d):
 out=[]
 def rec(i,left,cur):
  if i==n-1:out.append(tuple(cur+[left]));return
  for e in range(left+1):rec(i+1,left-e,cur+[e])
 rec(0,d,[]);return out
def invariant_poly_dim(mats,n,d):
 mons=monomials(n,d);idx={a:i for i,a in enumerate(mons)};eq=[]
 for A in mats:
  rows=[[0]*len(mons) for _ in mons]
  for col,a in enumerate(mons):
   for j,ej in enumerate(a):
    if not ej:continue
    for i in range(n):
     c=int(A[j,i])%P
     if not c:continue
     b=list(a);b[j]-=1;b[i]+=1
     rows[idx[tuple(b)]][col]=(rows[idx[tuple(b)]][col]+ej*c)%P
  eq.extend(r for r in rows if any(r))
 return len(mons)-rank(eq),len(mons)
for deg in (1,2,3,4):print("W8 invariant degree",deg,invariant_poly_dim(allW,8,deg))

# The centroid projectors are actual commuting simple A1 factors.
factor_perfect_dims=[]
for F in factors:
 D=MB(n)
 for a in F:
  for b in F:D.add(qbr(a,b))
 factor_perfect_dims.append(D.dim())
print("factor_perfect_dims",factor_perfect_dims)
assert factor_perfect_dims==[3,3,3]
factor_cross_zero=[]
for i in range(3):
 for j in range(i+1,3):
  z=all(not any(qbr(a,b)) for a in factors[i] for b in factors[j])
  factor_cross_zero.append(z)
print("factor_cross_zero",factor_cross_zero)
assert all(factor_cross_zero)
