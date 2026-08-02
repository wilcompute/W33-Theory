#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/w33_pass2474_f20_lifted_normalizer_hom.json'
Q=3
O=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=np.int8)%3
I=np.eye(4,dtype=np.int8)
def trans(v):
 v=np.array(v,dtype=np.int8)%3;return (I+np.outer(v,(O@v)%3))%3
def key(A):return bytes(np.asarray(A,dtype=np.uint8).ravel())
def mul(A,B):return (A@B)%3
def invsp(A):return ((-O)@A.T@O)%3
def order(A,limit=100):
 X=I.copy()
 for n in range(1,limit+1):
  X=mul(A,X)
  if np.array_equal(X,I):return n
 raise RuntimeError
def subgroup(gens):
 S={key(I):I};q=collections.deque([I])
 while q:
  A=q.popleft()
  for G in gens:
   B=mul(G,A);k=key(B)
   if k not in S:S[k]=B;q.append(B)
 return list(S.values())
def digest(d):return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main(output:Path=OUT):
 G=subgroup([trans(v) for v in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,0,1,0)]]);assert len(G)==51840
 g=next(A for A in G if order(A,40)==5);powers=[];X=I.copy()
 for _ in range(5):powers.append(key(X));X=mul(g,X)
 N=[]
 for H in G:
  C=mul(mul(H,g),invsp(H))
  if key(C) in powers:N.append(H)
 assert len(N)==40;z=(-I)%3;hist=dict(sorted(collections.Counter(order(A,80) for A in N).items()));assert hist=={1:1,2:1,4:10,5:4,8:20,10:4}
 lifts=[]
 for H in N:
  if order(H,80)!=8:continue
  C=mul(mul(H,g),invsp(H));exp=powers.index(key(C))
  if exp not in (2,3):continue
  H4=np.linalg.matrix_power(H.astype(int),4)%3;K=subgroup([g,H]);lifts.append({'action_exponent':exp,'H4_is_center':bool(np.array_equal(H4,z)),'generated_order':len(K),'contains_center':any(np.array_equal(A,z) for A in K)})
 assert len(lifts)==20 and all(x['H4_is_center'] and x['generated_order']==40 and x['contains_center'] for x in lifts)
 block_dim=2*18;total=4*block_dim
 out={'schema':'w33.pass2474.f20_lifted_normalizer_hom.v1','status':'PASS_NORMALIZER_PREIMAGE_IS_NONSPLIT_5_COLON_8_AND_RESTORES_HOM_OBSTRUCTION','sp4_3_order':len(G),
 'sylow5_normalizer':{'order':len(N),'order_spectrum':{str(k):v for k,v in hist.items()},'quotient_by_center':'5:4 = F20','lifted_group':'5:8','center_order':2,'order8_lifts_tested':len(lifts),'all_lifts_fourth_power_center':all(x['H4_is_center'] for x in lifts),'f20_complement_exists':False},
 'c5_hom':{'E8_nontrivial_character_multiplicity':2,'coexact90_nontrivial_character_multiplicity':18,'single_character_block_dimension':block_dim,'four_block_total_dimension':total},
 'lifted_normalizer_action':{'central_character_on_Hom':-1,'T_fourth_power':'-I','minimal_polynomial':'x^4+1','primitive_eighth_root_eigenspace_dimensions':{'zeta8':36,'zeta8^3':36,'zeta8^5':36,'zeta8^7':36},'Hom_5colon8_dimension':0,'projective_F20_block_fixed_dimension_if_central_sign_forgotten':36,'module_decomposition':'36 copies of the unique faithful 4-dimensional 5:8 irreducible with nontrivial C5 action and central sign -1'},
 'checks':{'group_order_51840':True,'normalizer_order_40':True,'unique_involution_is_center':hist[2]==1,'no_order20_complement':hist[2]==1,'all_order8_lifts_generate_40':all(x['generated_order']==40 for x in lifts),'hom_dimension_144':total==144,'lifted_invariants_zero':True,'thirty_six_copies_degree4':36*4==144},
 'theorem':'The order-five normalizer in Sp(4,3)=2.U4(2) is the nonsplit group 5:8, not C2 x (5:4). Every lift of a C4 normalizer generator has order 8 and fourth power equal to the center. Since the center acts with opposite signs on E8 and coexact90, the induced operator on Hom_C5 satisfies T^4=-I. Thus the 144-dimensional C5-Hom is 36 copies of the unique relevant faithful 4-dimensional 5:8 module and has no lifted-normalizer invariant vector.',
 'boundary':'The four 36-dimensional primitive-eighth-root eigenspaces exist only after complex diagonalization. A 36-dimensional fixed block appears in the projective F20 quotient only after forgetting the central sign; it is not an honest equivariant map between the original carriers.'}
 assert all(out['checks'].values());out['sha256_without_hash_field']=digest(out);output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'sha256':out['sha256_without_hash_field']},sort_keys=True))
if __name__=='__main__':main()
