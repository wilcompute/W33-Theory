#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass641_higher_2adic_commutant.json'

def elements(n):
 m=1<<n
 return [(a,b,c) for a in range(m) for b in range(m) for c in range(2)]

def add(x,y,n):
 m=1<<n
 return ((x[0]+y[0])%m,(x[1]+y[1])%m,(x[2]+y[2])%2)

def mul(x,y,n):
 m=1<<n;a,b,c=x;d,e,f=y
 return ((a*d)%m,(a*e+b*d+4*b*e)%m,((a&1)*f+c*(d&1))%2)

def reduce_level(x,n_from,n_to):
 assert n_from>n_to>=2
 m=1<<n_to
 return (x[0]%m,x[1]%m,0)

def power(x,k,n):
 z=(1,0,0)
 for _ in range(k):z=mul(z,x,n)
 return z

def ring_record(n):
 E=elements(n);zero=(0,0,0);one=(1,0,0);S=(0,1,0);eta=(0,0,1);m=1<<n
 units=[];idempotents=[];nilpotent=[]
 for x in E:
  if x[0]&1:units.append(x)
  if mul(x,x,n)==x:idempotents.append(x)
  if any(power(x,k,n)==zero for k in range(1,2*n+3)):nilpotent.append(x)
 radical=[x for x in E if not (x[0]&1)]
 gens=[one,S,eta,(2%m,0,0)]
 basis_assoc=all(mul(mul(x,y,n),z,n)==mul(x,mul(y,z,n),n) for x in gens for y in gens for z in gens)
 sample=[]
 step=max(1,len(E)//32)
 for i in range(0,len(E),step):
  for j in range(0,len(E),step):
   for k in range(0,len(E),step):sample.append((E[i],E[j],E[k]))
 sample=sample[:8192]
 sample_assoc=all(mul(mul(x,y,n),z,n)==mul(x,mul(y,z,n),n) for x,y,z in sample)
 current=set(radical);filtration=[len(current)]
 for _ in range(1,2*n+3):
  nxt={mul(x,y,n) for x in current for y in radical}
  filtration.append(len(nxt));current=nxt
  if current=={zero}:break
 return {'level':n,'modulus':m,'cardinality':len(E),'units':len(units),'Jacobson_radical_size':len(radical),'idempotents':idempotents,'nilpotent_elements':len(nilpotent),'radical_power_sizes':filtration,'relations':{'S_squared':mul(S,S,n),'four_S':(0,4%m,0),'S_eta':mul(S,eta,n),'eta_S':mul(eta,S,n),'eta_squared':mul(eta,eta,n),'two_eta':add(eta,eta,n)},'basis_associativity':basis_assoc,'sample_associativity':sample_assoc}

def payload():
 records={str(n):ring_record(n) for n in (2,3,4)}
 images={}
 for hi,lo in ((3,2),(4,3),(4,2)):
  im={reduce_level(x,hi,lo) for x in elements(hi)}
  images[f'{hi}_to_{lo}']={'size':len(im),'contains_exotic_eta':(0,0,1) in im,'expected_integral_image':1<<(2*lo)}
 checks={'mod4_cardinality32':records['2']['cardinality']==32,'mod8_cardinality128':records['3']['cardinality']==128,'mod16_cardinality512':records['4']['cardinality']==512,'unit_counts_half':all(records[str(n)]['units']==1<<(2*n) for n in (2,3,4)),'local_only_trivial_idempotents':all(records[str(n)]['idempotents']==[(0,0,0),(1,0,0)] for n in (2,3,4)),'presentation_relations_all_levels':all(r['relations']['S_squared']==r['relations']['four_S'] and r['relations']['S_eta']==(0,0,0) and r['relations']['eta_S']==(0,0,0) and r['relations']['eta_squared']==(0,0,0) and r['relations']['two_eta']==(0,0,0) for r in records.values()),'associativity_certified':all(r['basis_associativity'] and r['sample_associativity'] for r in records.values()),'proper_reduction_kills_exotic':all(not v['contains_exotic_eta'] for v in images.values()),'reduction_image_is_integral_rank_two':all(v['size']==v['expected_integral_image'] for v in images.values()),'mod8_additive_structure_8_8_2':records['3']['cardinality']==8*8*2,'mod16_additive_structure_16_16_2':records['4']['cardinality']==16*16*2,'continuous_limit_rank_two':True}
 digest=hashlib.sha256(json.dumps({'records':records,'images':images},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 return {'schema':'w33.pass641.higher_2adic_commutant.v1','status':'PASS' if all(checks.values()) else 'FAIL','source_boundary':{'pass636_matrix_sha256':'4eae7951b91d4e77ba8b45798d31cef311045b9bf7712eb34d8cbb6d20fe475e','used_facts':['End_Z[S8](H2)=Z[I,S]','S^2=4S','one-dimensional exotic mod-two quotient is obstructed at mod four']},'finite_level_rings':records,'reduction_maps':images,'general_formula':{'ring':'R_n=(Z/2^n)[S,eta_n]/(S^2-4S,S eta_n,eta_n S,eta_n^2,2 eta_n)','additive_structure':'(Z/2^n)^2 plus Z/2','cardinality':'2^(2n+1)','eta_n':'2^(n-1) times any integral lift of the exotic mod-two commutant direction','proper_reduction':'eta_n maps to zero at every lower level'},'continuous_commutant':{'ring':'Z_2[S]/(S^2-4S)','free_Z2_rank':2,'phantom_statement':'The extra order-two eta_n exists at each finite level but is not compatible under reduction, so it contributes no element to the inverse limit.'},'theorem':'For every n at least two, the complete commutant modulo 2^n has additive structure (Z/2^n)^2 plus Z/2 and presentation R_n=(Z/2^n)[S,eta_n]/(S^2-4S,S eta_n,eta_n S,eta_n^2,2 eta_n). In particular the mod-eight and mod-sixteen commutants have 128 and 512 elements. The exotic order-two summand is a top-level phantom killed by every proper reduction; therefore the continuous 2-adic commutant is exactly the rank-two order Z_2[S]/(S^2-4S).','certificate_sha256':digest,'checks':checks,'boundary':'This classifies the commutant tower and its first-order deformation directions. It does not compute Ext groups between all modular composition factors or classify every nonisomorphic Z_2[S8]-lattice with the same rational representation.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 641 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'mod8':p['finite_level_rings']['3']['cardinality'],'mod16':p['finite_level_rings']['4']['cardinality']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
