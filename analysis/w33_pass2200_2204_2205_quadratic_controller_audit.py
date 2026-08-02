#!/usr/bin/env python3
"""Corrected quadratic-target table and actual single-J controller image."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CERT=ROOT/'data/w33_pass2200_2204_2205_quadratic_controller_audit.json'
G=[(a,b,e) for a in range(4) for b in range(6) for e in range(2)];ID=(0,0,0)
def mul(x,y):
 a,b,e=x;c,d,f=y;s=-1 if e else 1;return ((a+s*c)%4,(b+s*d)%6,(e+f)%2)
def inv(x):return next(y for y in G if mul(x,y)==ID and mul(y,x)==ID)
def dmul(x,y):
 k,e=x;l,f=y;return ((k+(-1 if e else 1)*l)%12,(e+f)%2)
def image(x):a,b,e=x;return ((3*a+2*b)%12,e)
def subgroup(gs):
 S={ID};changed=True
 while changed:
  changed=False
  for x in list(S):
   for g in gs:
    for y in (mul(x,g),mul(g,x)):
     if y not in S:S.add(y);changed=True
 return S
def comm(x,y):return mul(mul(mul(inv(x),inv(y)),x),y)
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build():
 assert len(set(mul(x,y) for x in G for y in G))==48
 assert all(mul(mul(x,y),z)==mul(x,mul(y,z)) for x in G for y in G for z in G)
 center=[x for x in G if all(mul(x,y)==mul(y,x) for y in G)]
 derived=subgroup([comm(x,y) for x in G for y in G])
 assert all(image(mul(x,y))==dmul(image(x),image(y)) for x in G for y in G)
 D=[(k,e) for k in range(12) for e in range(2)];im=set(map(image,G));ker=[x for x in G if image(x)==(0,0)]
 assert im==set(D) and ker==[(0,0,0),(2,3,0)]
 r4,r6,s=(1,0,0),(0,1,0),(0,0,1);D8=subgroup([r4,s]);D12=subgroup([r6,s])
 assert (len(D8),len(D12),len(D8&D12))==(8,12,2)
 assert (len(set(map(image,D8))),len(set(map(image,D12))),len(set(map(image,D8))&set(map(image,D12))))==(8,12,4)
 historical={'Sym2_90':{'15':3,'24':1,'30':3,'81':5},'Lambda2_90':{'15':0,'24':4,'30':2,'81':7}}
 corrected={'Sym2_90':{'15':3,'24':5,'30':3,'81':7},'Lambda2_90':{'15':0,'24':0,'30':2,'81':5}}
 changed={s0:{d:{'historical':historical[s0][d],'corrected':v} for d,v in corrected[s0].items() if historical[s0][d]!=v} for s0 in corrected}
 qrows=[]
 for q in (7,11):
  ns=pow(q-1,(q-1)//2,q)==q-1
  qrows.append({'q':q,'q_mod_4':q%4,'minus_one_nonsquare':ns,'geometric_i_exists':ns,
   'representation_phase_evidence':'18 non-real irreducibles observed in the existing CTblLib q=7 audit' if q==7 else 'not recomputed in this packet',
   'D4_two_i_incompatibility':'open in this packet'})
 checks={'abstract_controller_order_48':len(G)==48,'abstract_controller_center_order_4':len(center)==4,
  'abstract_controller_derived_order_6':len(derived)==6,'single_J_image_order_24':len(im)==24,'single_J_kernel_order_2':len(ker)==2,
  'image_is_D24':im==set(D),'abstract_D8_D12_intersection_order_2':len(D8&D12)==2,
  'represented_D8_D12_intersection_order_4':len(set(map(image,D8))&set(map(image,D12)))==4,
  'corrected_gauge_antisymmetric_channels_zero':corrected['Lambda2_90']['15']==corrected['Lambda2_90']['24']==0,
  'q7_q11_geometric_i_exists':all(r['geometric_i_exists'] for r in qrows)};assert all(checks.values())
 out={'schema':'w33.pass2200_2204_2205.quadratic_controller_audit.v1','status':'PASS_WITH_Q11_REPRESENTATION_BOUNDARY',
  'quadratic_Hom_correction':{'historical_target_ambiguous_table':historical,'corrected_actual_signed_edge_targets':corrected,'changed_entries':changed,
   'selection_rule':'Both gauge blocks 15 and 24 are absent from Lambda^2(90), while Sym^2(90) reaches both.',
   'canonical_map_boundary':'The seven Pass-2051 tensors are explicit surjective generators, not complete Hom-space bases.'},
  'controller':{'abstract_group':'(C4 x C6):C2, inversion action, order 48','abstract_center':center,'abstract_derived_subgroup':sorted(derived),
   'single_J_representation':'(a,b,e) maps to (3a+2b mod 12,e) in C12:C2','image':'D24=C12:C2 of order 24','kernel':ker,
   'interpretation':'the canonical 90-sector supplies one complex phase circle; faithful order 48 needs two independent complex phase registers',
   'abstract_phase_subgroup_intersection_order':2,'represented_phase_subgroup_intersection_order':4},
  'q7_q11_two_i_audit':qrows,'checks':checks,
  'boundaries':['The historical Pass-2015 JSON is preserved for provenance but its 24/81 multiplicities are superseded by the corrected target-identified table.','The order-48 controller remains a valid abstract independent-clock model; it is not faithful on the canonical single-J 90-sector.','At q=7 and q=11 the geometric i exists because -1 is nonsquare; this packet does not claim the representation-theoretic inversion theorem at q=11.','No controller group is identified with a measured coupling, particle label, or fabricated circuit.']}
 out['sha256_without_hash_field']=digest(out);return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true');a=ap.parse_args();out=build()
 if a.verify_frozen:assert json.loads(CERT.read_text())==out
 if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
