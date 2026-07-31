from __future__ import annotations
import numpy as np
import sympy as sp
import _selector_five_frontiers_impl as ff
from pass1370_1374 import core
from .common import capture,matrix_stats,sha

def multiplicity_coordinates(Cinv,vector,slices):
 out=[];coeff=Cinv*sp.Matrix(vector)
 for start,stop,n,degree in slices:
  M=sp.Matrix(n,n,lambda i,j:sp.cancel(coeff[start+i*n+j]))
  out.append({'matrix_size':n,'irreducible_degree':degree,'matrix':[[[int(sp.Rational(x).p),int(sp.Rational(x).q)] for x in M.row(i)] for i in range(n)],'sha256':matrix_stats(M)['sha256']})
 return out

def selector(rows,n=120):
 S=sp.zeros(len(rows),n)
 for i,r in enumerate(rows):S[i,r]=1
 return S

def analyze():
 _public,cap=capture();g=cap['g'];blocks=core.matrix_units_full(g,cap['full_records'])
 tensor_columns=[];inverse_rows=[];block_records=[];matrix_unit_columns=[];slices=[];cursor=0
 for bi,block in enumerate(blocks):
  n=int(block['n']);degree=int(block['m']);E=block['E'];e00=ff.orbital_matrix(g,E[0][0]);pivots=list(e00.rref()[1]);assert len(pivots)==degree;W=e00[:,pivots];local=[]
  for a in range(n):
   translated=ff.orbital_matrix(g,E[a][0])*W;assert translated.rank()==degree;local.append(translated)
  Ublock=sp.Matrix.hstack(*local);dim=n*degree;assert Ublock.rank()==dim;tensor_columns.append(Ublock)
  row_pivots=list(Ublock.T.rref()[1]);assert len(row_pivots)==dim;V=Ublock[row_pivots,:];Z=ff.orbital_matrix(g,cap['full_records'][bi]['z']);Q=(V.inv()*selector(row_pivots)*Z).applyfunc(sp.cancel);assert Q*Ublock==sp.eye(dim);inverse_rows.append(Q)
  flat=[E[i][j] for i in range(n) for j in range(n)];matrix_unit_columns.extend(flat);slices.append((cursor,cursor+n*n,n,degree));cursor+=n*n
  block_records.append({'block_index':bi,'multiplicity_space_dimension':n,'irreducible_degree':degree,'isotypic_dimension':dim,'primitive_copy_pivots':pivots,'inverse_pivot_rows':row_pivots,'tensor_basis_sha256':matrix_stats(Ublock)['sha256'],'tensor_inverse_block_sha256':matrix_stats(Q)['sha256'],'matrix_unit_action':'E_ab acts as e_ab tensor I_degree in multiplicity-major ordering'})
 assert cursor==83
 U=sp.Matrix.hstack(*tensor_columns);Uinv=sp.Matrix.vstack(*inverse_rows);assert U.shape==(120,120) and Uinv.shape==(120,120) and Uinv*U==sp.eye(120)
 C=sp.Matrix.hstack(*matrix_unit_columns);assert C.shape==(83,83) and C.det()!=0;Cinv=C.inv();orbital_actions=[]
 for k in range(83):
  unit=sp.zeros(83,1);unit[k]=1;orbital_actions.append({'orbital_index':k,'blocks':multiplicity_coordinates(Cinv,unit,slices)})
 Acoord=sp.Matrix([g['A'][i,j] for i,j in g['reps']]);Dcoord=sp.Matrix([g['D'][i,j] for i,j in g['reps']]);s2,s4=core.splitters(g);named={'A':multiplicity_coordinates(Cinv,Acoord,slices),'D':multiplicity_coordinates(Cinv,Dcoord,slices),'S':multiplicity_coordinates(Cinv,s2+s4,slices)}
 for name,vector in (('A',Acoord),('D',Dcoord),('S',s2+s4)):
  O=ff.orbital_matrix(g,vector)
  for bi,(rec,Ublock) in enumerate(zip(block_records,tensor_columns)):
   n=rec['multiplicity_space_dimension'];degree=rec['irreducible_degree'];Mdata=named[name][bi]['matrix'];M=sp.Matrix([[sp.Rational(*Mdata[i][j]) for j in range(n)] for i in range(n)]);assert O*Ublock==Ublock*sp.kronecker_product(M,sp.eye(degree))
 action_payload=[{'orbital_index':x['orbital_index'],'block_hashes':[b['sha256'] for b in x['blocks']]} for x in orbital_actions]
 result={'theorem':'Pass 1501 Deterministic Tensor-Factor Selector Fourier Transform','ordering':'Mackey blocks in frozen matrix-unit order; multiplicity index first, deterministic primitive-copy column pivots and blockwise inverse row pivots','blocks':block_records,'block_dimensions':[r['isotypic_dimension'] for r in block_records],'tensor_basis_U':matrix_stats(U),'tensor_inverse_Uinv':matrix_stats(Uinv),'exact_inverse_verified':True,'inverse_constructed_blockwise_from_central_projectors':True,'all_83_orbital_multiplicity_actions_sha256':sha(action_payload),'all_83_orbital_multiplicity_actions':orbital_actions,'named_multiplicity_actions':named,'conclusion':'Every orbital operator acts as a multiplicity-space matrix tensored with the identity on the irreducible factor; the remaining repeated-copy gauge is fixed by deterministic pivots.','boundary':'The pivot rule is canonical relative to frozen matrix units and selector coordinate order.'};result['sha256']=sha(result);return result
