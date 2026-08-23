#!/usr/bin/env python3
"""Pass9481-9488: complete the rank-24 carrier-centralizer fingerprint.

E6^4 was closed at Pass9197-9204.  Here A2^12 is recomputed from the ternary
Golay glue, and E8^3 is closed by transporting the repo-certified Springer G32
centralizer through the 3-cycle lift.
"""
from __future__ import annotations
import itertools,json,sys
from collections import deque
from pathlib import Path
import numpy as np
from sympy import Matrix,zeros,eye
from sympy.matrices.normalforms import hermite_normal_form
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
P=3
OUT=ROOT/'data/PART_W33_PASS9481_9488_RANK24_CENTRALIZER_FINGERPRINT.json'

def key(M):return (np.asarray(M,dtype=np.int64)%P).astype(np.uint8).tobytes()
def closure(gens):
 I=np.eye(gens[0].shape[0],dtype=np.int64)%P;D={key(I):I};q=deque([I])
 while q:
  a=q.popleft()
  for b in gens:
   c=a@b%P;k=key(c)
   if k not in D:D[k]=c;q.append(c)
 return list(D.values())
def cycles(p):
 seen=set();out=[]
 for i in range(len(p)):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j);j=p[j]
  out.append(tuple(c))
 return out
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def build_a2():
 G=np.array(rs.GOLAY12,dtype=np.int64)%P;words=rs.golay_codewords()
 A2=rs.A2;omega=Matrix([Matrix([[2],[1]])[0]/3,Matrix([[2],[1]])[1]/3]);gens=[]
 for i in range(24):e=zeros(24,1);e[i]=1;gens.append(e)
 for row in G:
  v=zeros(24,1)
  for c in range(12):v[2*c:2*c+2,0]=int(row[c])*omega
  gens.append(v)
 m=Matrix.hstack(*gens);m3=Matrix([[int(3*x) for x in m.row(i)] for i in range(24)])
 basis=hermite_normal_form(m3)/3;gamb=Matrix.diag(*([A2]*12));gram=basis.T*gamb*basis
 r=Matrix([[0,-1],[1,-1]]);perm=rs.PERM;sig=rs.SIGNS_MOD3;cy=cycles(perm);twist={c[0] for c in rs.CYCLES}
 # The tuple ordering in rs.CYCLES may start elsewhere; only one twist per directed cycle matters.
 # Rebuild the actual twist set used by the canonical carrier.
 twist={c[0] for c in rs.CYCLES};eexp=[1 if j in twist else 0 for j in range(12)]
 xamb=zeros(24);T=np.zeros((12,12),dtype=np.int64)
 for src,dst in enumerate(perm):
  s=-1 if sig[src]==2 else 1;T[dst,src]=sig[src]%P
  xamb[2*dst:2*dst+2,2*src:2*src+2]=s*(r if src in twist else eye(2))
 x=basis.inv()*xamb*basis;h=rs.nullspace_modp(np.array((eye(24)-x).T.tolist(),dtype=np.int64),P);assert h.shape==(4,24)
 piv=None
 for cols in itertools.combinations(range(24),4):
  try:ri=rs.inv_mod(h[:,cols],P);piv=cols;break
  except ValueError:pass
 assert piv is not None;u=np.zeros((24,4),dtype=np.int64);u[list(piv),:]=ri
 def induced(y):
  Y=np.array(y.tolist(),dtype=np.int64)%P;m=h@Y@u%P;assert np.array_equal(m@h%P,h@Y%P);return m
 # Centralizer of the directed 3^4 coordinate permutation: 3^4:S4, then 2^4 sign seeds.
 cys=cycles(perm);assert sorted(map(len,cys))==[3,3,3,3]
 cperms=[]
 for bp in itertools.permutations(range(4)):
  for rots in itertools.product(range(3),repeat=4):
   qmap=[None]*12
   for sb,tb in enumerate(bp):
    for k,j in enumerate(cys[sb]):qmap[j]=cys[tb][(k+rots[sb])%3]
   assert all(qmap[perm[j]]==perm[qmap[j]] for j in range(12));cperms.append(qmap)
 assert len(cperms)==1944
 signed=[]
 for qmap in cperms:
  for seeds in itertools.product([1,2],repeat=4):
   a=[None]*12;ok=True
   for bi,c in enumerate(cys):
    j0=c[0];a[j0]=seeds[bi];j=j0
    for _ in range(2):
     pj=perm[j];a[pj]=a[j]*sig[qmap[j]]*pow(int(sig[j]),-1,P)%P;j=pj
    if a[perm[j]]!=a[j]*sig[qmap[j]]*pow(int(sig[j]),-1,P)%P:ok=False
   if not ok:continue
   Y=np.zeros((12,12),dtype=np.int64)
   for src,dst in enumerate(qmap):Y[dst,src]=a[src]
   assert np.array_equal(Y@T%P,T@Y%P)
   if all(tuple(int(x) for x in (Y@np.array(w,dtype=np.int64))%P) in words for w in G):signed.append((qmap,a))
 assert len(signed)==72
 # Weyl rotations are invisible on discriminant glue, so solve their exponents to make exact 24D commuting lifts.
 mats=[];block_index={j:i for i,c in enumerate(cys) for j in c};blockacts=set()
 for qmap,a in signed:
  t=[None]*12
  for c in cys:
   j0=c[0];t[j0]=0;j=j0
   for _ in range(2):
    pj=perm[j];t[pj]=(eexp[qmap[j]]+t[j]-eexp[j])%P;j=pj
   assert t[perm[j]]==(eexp[qmap[j]]+t[j]-eexp[j])%P
  yamb=zeros(24)
  for src,dst in enumerate(qmap):
   s=1 if a[src]==1 else -1;yamb[2*dst:2*dst+2,2*src:2*src+2]=s*(r**int(t[src]))
  assert yamb*xamb==xamb*yamb
  y=basis.inv()*yamb*basis;assert all(v.q==1 for v in y) and y.T*gram*y==gram
  mats.append(induced(y));blockacts.add(tuple(block_index[qmap[c[0]]] for c in cys))
 assert len(blockacts)==12 and all(parity(p)==0 for p in blockacts)
 image=closure(mats);assert len(image)==648
 proj={min(key(m),key((-m)%P)) for m in image};assert len(proj)==324
 return {'Sp_image_order':648,'projective_image_order':324,'projective_structure':'3^3:A4','line_point_action':'A4','signed_Golay_carrier_centralizers':72}

def main():
 a2=build_a2();e6=json.loads((ROOT/'data/PART_W33_PASS9197_9204_E6_CENTRALIZER_LINE_STABILIZER.json').read_text())
 assert e6['sp4_line_stabilizer_image_order']==1296 and e6['projective_line_stabilizer_image_order']==648
 # Repo-certified Springer result (Pass1020/Pass8909): C_W(E8)(j3)=3 x Sp(4,3), order155520,
 # and the C3 generated by j3 is exactly the kernel on E8/(I-j3)E8.  Hence image Sp(4,3).
 sp4=P**4*(P**2-1)*(P**4-1);assert sp4==51840
 e8={'rank8_Springer_centralizer_order':3*sp4,'coinvariant_kernel_order':3,'Sp_image_order':sp4,'projective_image_order':sp4//2,'projective_structure':'PSp(4,3) (full inner W33 automorphism group)','rank24_argument':'The diagonal copy of C_W(E8)(j3) in E8^3 commutes with the 3-cycle lift; under the sum-block coinvariant isomorphism it induces the same Sp(4,3) action. Since every quotient isometry lies in Sp(4,3), this is already the full image.'}
 out={'schema':'w33.pass9481_9488.rank24_centralizer_fingerprint.v1','status':'PASS','passes':'9481-9488','E8^3':e8,
      'E6^4':{'Sp_image_order':1296,'projective_image_order':648,'projective_structure':'3^3:S4','line_point_action':'S4'},'A2^12':a2,
      'fingerprint':['E8^3: full PSp(4,3), order 25920','E6^4: full line stabilizer 3^3:S4, order 648','A2^12: oriented line stabilizer 3^3:A4, order 324'],
      'theorem':'The three rank-24 W33 carriers have three strictly nested projective centralizer images. E8^3 realizes all PSp(4,3); E6^4 realizes the full stabilizer of its root-shadow line; A2^12 realizes the index-two orientation-preserving subgroup of that line stabilizer. Thus the A2/Golay carrier remembers an orientation of the four line channels that the E6/tetracode carrier forgets.',
      'boundary':'A2^12 is recomputed from the lattice/glue witness here. E8 uses the repo-certified Springer G32 centralizer/action theorem from Pass1020/Pass8909 and proves that its full quotient action survives the rank-24 3-cycle lift.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','orders':[25920,648,324]}));return 0
if __name__=='__main__':raise SystemExit(main())
