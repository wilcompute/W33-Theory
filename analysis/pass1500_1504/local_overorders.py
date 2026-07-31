from __future__ import annotations
import collections,math
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form
from pass1370_1374 import core
from .common import capture,denominator_lcm,matrix_stats,sha

def rational_factor(n):
 n=abs(int(n));out={};p=2
 while p*p<=n:
  while n%p==0:out[p]=out.get(p,0)+1;n//=p
  p+=1
 if n>1:out[n]=out.get(n,0)+1
 return {str(k):v for k,v in sorted(out.items())}
def flatten_units(blocks):
 cols=[];slices=[];start=0
 for block in blocks:
  E=block['E'];n=len(E);local=[E[i][j] for i in range(n) for j in range(n)];cols.extend(local);slices.append((start,start+n*n,n));start+=n*n
 assert start==83;return sp.Matrix.hstack(*cols),slices
def matrix_from_coeff(coeff,start,n):return sp.Matrix(n,n,lambda i,j:sp.cancel(coeff[start+i*n+j]))
def analyze():
 _public,cap=capture();g=cap['g'];blocks=core.matrix_units_full(g,cap['full_records']);C,slices=flatten_units(blocks);assert C.det()!=0;B=C.inv()
 reps=[]
 for start,stop,n in slices:
  reps.append([matrix_from_coeff(B[:,k],start,n) for k in range(83)])
 block_data=[];T=sp.zeros(83);cursor=0
 for bi,((start,stop,n),mats) in enumerate(zip(slices,reps)):
  generators=sp.Matrix.hstack(*[M[:,0] for M in mats]);d=denominator_lcm(generators);V=(d*generators).applyfunc(lambda x:int(x));H=hermite_normal_form(V);assert H.shape==(n,n) and H.det()!=0;P=(sp.Rational(1,d)*H).applyfunc(sp.cancel);Pinv=P.inv()
  integral=[]
  for M in mats:
   Z=(Pinv*M*P).applyfunc(sp.cancel);assert all(sp.Rational(x).q==1 for x in Z);integral.append(Z)
  local_cols=[]
  for a in range(n):
   for b in range(n):
    Eab=sp.zeros(n);Eab[a,b]=1;F=(P*Eab*Pinv).applyfunc(sp.cancel);local_cols.append(sp.Matrix([F[i,j] for i in range(n) for j in range(n)]))
  Tb=sp.Matrix.hstack(*local_cols);T[start:stop,start:stop]=Tb
  block_data.append({'block_index':bi,'matrix_size':n,'minimal_left_lattice_basis':matrix_stats(P),'standard_to_stable_lattice_determinant':[int(sp.Rational(P.det()).p),int(sp.Rational(P.det()).q)],'maximal_order_basis_transform':matrix_stats(Tb),'all_83_orbital_actions_integral_on_lattice':True,'orbital_action_hashes':[matrix_stats(Z)['sha256'] for Z in integral]})
 assert T.det()!=0
 D=(C*T).applyfunc(sp.cancel)
 Dinv=D.inv().applyfunc(sp.cancel)
 assert all(sp.Rational(x).q==1 for x in Dinv)
 index=abs(int(Dinv.det()));index_factors=rational_factor(index)
 assert index_factors=={'2':36,'3':113}
 Gm=sp.zeros(83);cur=0
 for _start,_stop,n in slices:
  for i in range(n):
   for j in range(n):Gm[cur+i*n+j,cur+j*n+i]=1
  cur+=n*n
 Gmax=(T.T*Gm*T).applyfunc(sp.cancel);assert all(sp.Rational(x).q==1 for x in Gmax);disc_max=abs(int(Gmax.det(method='domain-ge')));assert disc_max==1
 GramO=(B.T*Gm*B).applyfunc(sp.cancel);disc_O=abs(int(GramO.det(method='domain-ge')));assert disc_O==index*index
 local_indices={p:str(p**index_factors[str(p)]) for p in (2,3)}
 result={'theorem':'Pass 1503 Explicit Global Maximal Overorder Containing the Orbital Order','orbital_order':'O = Z-span of the 83 stabilizer orbitals','maximal_overorder':'M_O = direct sum over rational blocks of End_Z(O e_b), using one primitive matrix-unit idempotent e_b per block','block_count':len(block_data),'blocks':block_data,'orbital_order_contained_in_maximal_overorder':True,'transition_maximal_basis_in_orbital_coordinates':matrix_stats(D),'orbital_in_maximal_coordinates':matrix_stats(Dinv),'global_index_maximal_over_orbital':str(index),'global_index_factorization':index_factors,'local_indices':local_indices,'maximal_order_reduced_trace_discriminant':str(disc_max),'orbital_reduced_trace_discriminant':str(disc_O),'discriminant_index_identity_verified':True,'p_maximal_at_2_and_3':True,'conclusion':'The minimal-left-ideal lattices Oe_b produce an explicit conjugate split maximal order containing O. Its global index is 2^36 3^113 and its reduced-trace discriminant is one, so the localizations at 2 and 3 are maximal overorders with indices 2^36 and 3^113.','boundary':'The previously selected frozen matrix-unit order is commensurable with O but need not contain it. The present order is a different conjugate maximal order constructed from O-stable lattices, so containment is objectwise verified rather than inferred from discriminants.'};result['sha256']=sha(result);return result
