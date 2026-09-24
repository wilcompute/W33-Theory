from pathlib import Path
import importlib.util
from fractions import Fraction
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("dw",ROOT/"analysis/w33_diagonal_weld_e8_lie_generation.py");dw=importlib.util.module_from_spec(s);s.loader.exec_module(dw)
compiler,bridge,table=dw.load_inputs();amps=dw.backgrounds(bridge);vecs=dw.source_generators(compiler,amps)
L,_=dw.closure((vecs[(1,"center")],vecs[(2,"center")]),table,dw.RationalBasis());B=L.vectors
def br(a,b):return dw.bracket(a,b,table,None)
def ideal(seed):
 M=dw.RationalBasis();q=[]
 if M.add(seed,0):q=[M.vectors[-1]]
 while q:
  v=q.pop()
  for g in B:
   if M.add(br(g,v),0):q.append(M.vectors[-1])
 return M
I15=ideal(B[6]);I9=ideal(B[10]);assert(len(I15.rows),len(I9.rows))==(15,9)
# derived center Z
Z=dw.RationalBasis()
for a in I15.vectors:
 for b in I15.vectors:Z.add(br(a,b),0)
assert len(Z.rows)==1
def quotient(Avals,Bvals):
 base=dw.RationalBasis()
 for v in Bvals:base.add(v,0)
 Q=dw.RationalBasis()
 for v in Avals:
  r=list(map(Fraction,v))
  for p in sorted(base.rows):
   if r[p]:
    f=r[p];row=base.rows[p];r=[a-f*b for a,b in zip(r,row)]
  Q.add(r,0)
 ps=sorted(Q.rows);rows=[Q.rows[p] for p in ps];return base,rows,ps
baseI,Q9,p9=quotient(B,I15.vectors);baseZ,W14,p14=quotient(I15.vectors,Z.vectors);baseZ8,W8,p8=quotient(I9.vectors,Z.vectors);base9,U6,p6=quotient(I15.vectors,I9.vectors)
assert(len(Q9),len(W14),len(W8),len(U6))==(9,14,8,6)
def coords(v,base,rows,pivs):
 r=list(map(Fraction,v))
 for p in sorted(base.rows):
  if r[p]:
   f=r[p];row=base.rows[p];r=[a-f*b for a,b in zip(r,row)]
 co=[]
 for p,row in zip(pivs,rows):
  c=r[p];co.append(c)
  if c:r=[a-c*b for a,b in zip(r,row)]
 assert all(x==0 for x in r);return co
def action(q,base,mods,pivs):
 A=sp.zeros(len(mods),len(mods))
 for j,v in enumerate(mods):
  co=coords(br(q,v),base,mods,pivs)
  for i,x in enumerate(co):A[i,j]=sp.Rational(x.numerator,x.denominator)
 return A
acts8=[action(q,baseZ8,W8,p8) for q in Q9]
acts6=[action(q,base9,U6,p6) for q in Q9]
def commdim(mats,n):
 vars=sp.symbols('x0:'+str(n*n));X=sp.Matrix(n,n,vars);eq=[]
 for A in mats:eq.extend(list(X*A-A*X))
 M,_=sp.linear_eq_to_matrix(eq,vars);return len(M.nullspace())
print("char0_commutants W8 U6",commdim(acts8,8),commdim(acts6,6))
# invariant alternating forms dimensions (symplectic structure should be one-dimensional on W8 and U6?)
def altform_dim(mats,n):
 pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
 vars=sp.symbols('a0:'+str(len(pairs)));J=sp.zeros(n)
 for z,(i,j) in zip(vars,pairs):J[i,j]=z;J[j,i]=-z
 eq=[]
 for A in mats:eq.extend(list(A.T*J+J*A))
 M,_=sp.linear_eq_to_matrix(eq,vars);return len(M.nullspace())
print("char0_altforms W8 U6",altform_dim(acts8,8),altform_dim(acts6,6))
