#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
from w33_pass543_547_common import *
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass546_z9_kernel_fourier_image.json'
def det(g,m):a,b,c,d=g;return (a*d-b*c)%m
def mats(m):return [g for g in itertools.product(range(m),repeat=4) if det(g,m)==1]
def act(g,v,m):a,b,c,d=g;return ((a*v[0]+b*v[1])%m,(c*v[0]+d*v[1])%m)
def red9(v):
 if v[0]%3 or v[1]%3:return cp((v[0]%3,v[1]%3),3),'primitive'
 return cp((v[0]//3%3,v[1]//3%3),3),'deep'
def kcoord(g):a,b,c,d=g;return (((a-1)//3)%3,(b//3)%3,(c//3)%3)
def signed_actions3():
 C=classes(3);I={v:i for i,v in enumerate(C)};A=[]
 for a,b,c,d in mats(3):
  gi=(d%3,(-b)%3,(-c)%3,a%3);P=[];E=[]
  for r in C:
   w=act(gi,r,3);q=cp(w,3);P.append(I[q]);E.append(1 if w==q else -1)
  A.append((P,E))
 return A
def orb(s,A):return {tuple(E[i]*s[P[i]]%3 for i in range(4)) for P,E in A}
def payload():
 A9,A3=classes(9),classes(3);S9=mats(9);K=[g for g in S9 if tuple(x%3 for x in g)==(1,0,0,1)];fib={b:{'primitive':[],'deep':[]} for b in A3}
 for v in A9:b,s=red9(v);fib[b][s].append(v)
 H=[]
 for b in A3:
  v=fib[b]['primitive'][0];H.append([kcoord(g) for g in K if cp(act(g,v,9),9)==v])
 mult={u:sum(all(sum(x*y for x,y in zip(u,h))%3==0 for h in hsub) for hsub in H) for u in itertools.product(range(3),repeat=3)}
 module_mult={u:(m+4 if u==(0,0,0) else m) for u,m in mult.items()};dist=Counter(module_mult.values())
 C9=Cyc9();L=tangent_z9();gram=[[trace(matmul(L[i],L[j],C9),C9) for j in range(40)] for i in range(40)]
 idx={b:i for i,b in enumerate(A3)};rows={}
 for vals3 in itertools.product(range(3),repeat=4):
  offs=[]
  for v in A9:
   b,s=red9(v);offs.append(3*vals3[idx[b]] if s=='primitive' else 0)
  rows[vals3]=tuple(charpoly_z9(offs)[0])
 cpcounts=Counter(rows.values());A=signed_actions3();unseen=set(rows);splits=[]
 while unseen:
  s=next(iter(unseen));O=orb(s,A);splits.append({'orbit_size':len(O),'support':sum(x!=0 for x in s),'charpoly_count':len({rows[x] for x in O}),'fibre_sizes':sorted(Counter(rows[x] for x in O).values())});unseen-=O
 checks={
  'kernel_order27':len(K)==27 and len(set(map(kcoord,K)))==27,
  'four_primitive_stabilizer_lines':len(H)==4 and all(len(x)==3 for x in H),
  'fourier_multiplicity_dimension40':sum(module_mult.values())==40,
  'fourier_distribution_exact':dist==Counter({2:12,1:8,0:6,8:1}),
  'six_characters_absent':sum(1 for x in module_mult.values() if x==0)==6,
  'z9_tangent_gram_minus18_identity':all(gram[i][j]==((-18,0,0,0,0,0) if i==j else C9.zero()) for i in range(40) for j in range(40)),
  'linearized_image_injective40':all(gram[i][i]!=C9.zero() for i in range(40)),
  'base_slice_81_sections':sum(cpcounts.values())==81,
  'base_slice_13_exact_charpolys':len(cpcounts)==13,
  'q3_orbits_split_pattern':sorted(x['charpoly_count'] for x in splits)==[1,2,2,2,2,3,3],
 }
 return {'schema':'w33.pass546.z9_kernel_fourier_image.v1','status':'PASS' if all(checks.values()) else 'FAIL','kernel_fourier':{'kernel':'C3^3','coordinate_module_character_multiplicities':{'trivial':8,'nontrivial_multiplicity_2':12,'nontrivial_multiplicity_1':8,'absent':6},'dimension_check':sum(module_mult.values()),'stabilizer_lines':H},'linearized_characteristic_map':{'gram':'-18 I_40','conclusion':'All 40 coordinate modes, including every Fourier character that occurs, survive in the first-order Heisenberg block image.'},'nonlinear_base_slice':{'definition':'primitive offsets constant on each of four tetrahedral fibres, values 0,3,6; deep anchors zero','sections':81,'distinct_exact_charpolys':len(cpcounts),'charpoly_multiplicities':sorted(cpcounts.values()),'q3_signed_orbit_splitting':sorted(splits,key=lambda x:(x['orbit_size'],x['support'])),'conclusion':'The naive q=3 orbit table does not lift equivariantly: its seven signed orbits split into thirteen Z/9 characteristic polynomials.'},'checks':checks,'boundary':'Exact Fourier decomposition and an exact 81-section nonlinear slice; not the full 9^40 characteristic image.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 546 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
