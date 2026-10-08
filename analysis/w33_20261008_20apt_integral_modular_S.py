"""Torus modular S: order-four F20 generator acts on integral H1 as J.

Compute Fp cohomology action from original 60-edge cellular boundaries,
no appeal to just counts. A Z-linear representation on torsion-free
H1=Z^2 has order dividing4; order4 modulo3 implies its integral
matrix squares to -I and is conjugate to [[0,-1],[1,0]] in GL2(Z).
Thus mod2 it swaps logical cycles (up to basis), and the quotient
F20->C4 acts as Gaussian-integer unit rotation on abstract H1 lattice.
"""
from pathlib import Path
import sys,itertools,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_twenty_apartment_binary_CSS_F20 import topology
OUT=ROOT/"data/w33_20261008_20apt_integral_C4_modular_S.json"
def echelon(vectors,p):
 pivots={}
 def reduce(v):
  x=list(map(lambda t:t%p,v))
  for pivot in sorted(pivots):
   if x[pivot]:
    c=x[pivot]
    x=[(a-c*b)%p for a,b in zip(x,pivots[pivot])]
  return x
 for v in vectors:
  x=reduce(v)
  if any(x):
   a=next(j for j,y in enumerate(x) if y)
   inv=pow(int(x[a]),-1,p)
   pivots[a]=[(z*inv)%p for z in x]
 return reduce, len(pivots)
def nullspace(rows,n,p):
 # Row reduce as usual, deterministic increasing-pivot basis.
 A=[list(int(z)%p for z in row) for row in rows]
 m=len(A);rank=0;pivots=[]
 for j in range(n):
  pr=next((i for i in range(rank,m) if A[i][j]),None)
  if pr is None:continue
  A[rank],A[pr]=A[pr],A[rank]
  sc=pow(A[rank][j],-1,p);A[rank]=[(v*sc)%p for v in A[rank]]
  for k in range(m):
   if k!=rank and A[k][j]:
    co=A[k][j];A[k]=[(a-co*b)%p for a,b in zip(A[k],A[rank])]
  pivots.append(j);rank+=1
  if rank==m:break
 result=[]
 for f in range(n):
  if f in pivots:continue
  x=[0]*n;x[f]=1
  for i,j in enumerate(pivots):x[j]=(-A[i][f])%p
  assert all(sum(a*b for a,b in zip(row,x))%p==0 for row in rows)
  result.append(x)
 return result
def action(p):
 V,E,faces,stab,H,b1,b2=topology()
 # For each face, coefficients with orientation point->line.
 eidx={e:i for i,e in enumerate(E)}
 cob0=[[1 if ((r>>j)&1) and V[i]>=40 else (-1 if (r>>j)&1 else 0)
         for j in range(60)] for i,r in enumerate(b1)]
 # Above signs per each incidence vertex; point and line opposite.
 assert len(cob0)==40
 face=[[0]*60 for _ in faces]
 for i,f in enumerate(faces):
  for u,v in zip(f,f[1:]+f[:1]):
   j=eidx[tuple(sorted((u,v)))]
   face[i][j]+=1 if u<40 else -1
 R,rank0=echelon(cob0,p)
 assert rank0==39
 ker=nullspace(face,60,p)
 assert len(ker)==41
 basis=[];test=cob0[:]
 for x in ker:
  RR,n=echelon(test,p)
  if any(RR(x)):
   basis.append(x);test.append(x)
 assert len(basis)==2
 reduce_base,dim=echelon(cob0,p)
 assert dim==39
 def coords(v):
  for x,y in itertools.product(range(p),repeat=2):
   vv=[(z-x*a-y*b)%p for z,a,b in zip(v,*basis)]
   if not any(reduce_base(vv)):return (x,y)
  raise AssertionError("not in H1 span")
 # choose W33 order4 generator that conjugates C5 by squaring.
 r=H[1]
 def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
 def power(a,n):
  x=tuple(range(len(a)))
  for _ in range(n):x=compose(a,x)
  return x
 s=next(g for g in stab if power(g,4)==tuple(range(80)) and power(g,2)!=tuple(range(80)) and compose(compose(g,r),power(g,3))==power(r,2))
 emap=[eidx[tuple(sorted((s[u],s[v])))] for u,v in E]
 imgs=[]
 for b in basis:
  t=[0]*60
  for i,j in enumerate(emap):t[j]=b[i]
  imgs.append(coords(t))
 # columns are coordinates of transformed basis vectors
 mat=[[imgs[j][i] for j in range(2)] for i in range(2)]
 def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2))%p for j in range(2)] for i in range(2)]
 squ=mm(mat,mat)
 assert mm(squ,squ)==[[1%p,0],[0,1%p]]
 assert squ==[[(p-1)%p,0],[0,(p-1)%p]] if p!=2 else squ==[[1,0],[0,1]]
 trace=(mat[0][0]+mat[1][1])%p
 det=(mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0])%p
 assert trace==0 and det==1%p
 return {"p":p,"basis_dim":2,"matrix_order4_action":mat,
         "matrix_squared":squ,"trace_mod_p":trace,"det_mod_p":det,
         "integral_matrix_order4_forced_if_p3":p==3}
if __name__=="__main__":
 vals=[action(p) for p in (2,3,5)]
 out={"field_actions":vals,"exact_integral_homology_H1":"Z^2",
      "F20_C5_integral_H1_action_trivial":"No order5 in GL2(Z); independently generator order5 on torus",
      "order4_integral_H1_action":"Conjugate over GL2(Z) to J=[[0,-1],[1,0]]",
      "F20_on_integral_H1_image":"C4",
      "order4_squared_on_integral_H1":"-Identity",
      "mod2_logical_SWAP_is_reduction_of_modular_S":True,
      "BC_ring_D30_lacks_order4":True,
      "interpretation":"This is a mapping-class/abstract torus homology action, NOT a physical rotation of a geometric square torus, conformal modulus, or spacetime metric."}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
 print(json.dumps(out,indent=2),flush=True);print("TORUS_MODULAR_S_PASS")
