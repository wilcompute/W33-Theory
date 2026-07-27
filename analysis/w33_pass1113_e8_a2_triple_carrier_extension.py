from __future__ import annotations
import json, math, time
from collections import deque, Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1113_e8_a2_triple_carrier_extension.json'
ATLAS=[('1A','(cdcdcddcdcdddcdd)^4',1,51840),('2A','(cdd)^4',2,1152),('2B','(cdcdcddcdcdddcdd)^2',2,192),('3A','(cdcdd)^4',3,648),('3C','(ccdcdddcddd)^2',3,216),('3D','(cddcdcdddcdd)^2',3,108),('4A','(cdd)^2',4,96),('4B','cdcdcddcdcdddcdd',4,16),('5A','(cd)^2',5,10),('6A','(cdcdd)^2',6,72),('6C','ccdcdddcddd',6,36),('6E','cddcdcdddcdd',6,36),('6F','(cdcdcdd)^2',6,24),('9A','d',9,9),('12A','cdcdd',12,12),('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),('2D','(cdcdddcdd)^3',2,96),('4C','(cdcdcdd)^3',4,96),('4D','dcdcdcdd',4,32),('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),('6H','dcdd',6,36),('6I','cdcdddcdd',6,12),('8A','cdd',8,8),('10A','cd',10,10),('12C','cdcdcdd',12,12)]
def roots_e8():
 r=[]
 for i in range(8):
  for j in range(i+1,8):
   for a in (1,-1):
    for b in (1,-1):
     v=[0]*8;v[i]=2*a;v[j]=2*b;r.append(tuple(v))
 for m in range(256):
  v=tuple(-1 if (m>>k)&1 else 1 for k in range(8))
  if sum(x==-1 for x in v)%2==0:r.append(v)
 return r
def refl(r,roots,idx):
 out=[]
 for x in roots:
  q=sum(a*b for a,b in zip(x,r))//4
  out.append(idx[tuple(a-q*b for a,b in zip(x,r))])
 return np.array(out,dtype=np.uint8)
def comp(a,b):return a[b]
def inv(p):q=np.empty_like(p);q[p]=np.arange(len(p),dtype=p.dtype);return q
def order(p):
 seen=np.zeros(len(p),bool);o=1
 for i in range(len(p)):
  if not seen[i]:
   j=i;l=0
   while not seen[j]:seen[j]=1;j=int(p[j]);l+=1
   o=math.lcm(o,l)
 return o
def enum(gens):
 I=np.arange(len(gens[0]),dtype=np.uint8);D={I.tobytes():0};E=[I];par=[0];q=deque([0])
 while q:
  i=q.popleft();x=E[i]
  for g in gens:
   y=comp(g,x);k=y.tobytes()
   if k not in D:D[k]=len(E);E.append(y.copy());par.append(par[i]^1);q.append(len(E)-1)
 return np.stack(E),D,np.array(par,dtype=np.uint8)
def classes(G,idx,gens):
 trans=[]
 for g in gens:
  gi=inv(g);C=gi[G[:,g]];trans.append(np.array([idx[x.tobytes()] for x in C],dtype=np.int32))
 unseen=np.ones(len(G),bool);cs=[];co=np.empty(len(G),dtype=np.int16)
 for s in range(len(G)):
  if not unseen[s]:continue
  unseen[s]=0;q=deque([s]);orb=[]
  while q:
   x=q.popleft();orb.append(x)
   for t in trans:
    y=int(t[x])
    if unseen[y]:unseen[y]=0;q.append(y)
  ci=len(cs);co[orb]=ci;cs.append(orb)
 return cs,co
def ppow(p,n):
 r=np.arange(len(p),dtype=np.uint8);b=p
 while n:
  if n&1:r=comp(r,b)
  b=comp(b,b);n//=2
 return r
def word(e,c,d):
 if e.startswith('('):w,n=e[1:].split(')^');n=int(n)
 else:w=e;n=1
 r=np.arange(len(c),dtype=np.uint8)
 for ch in w:r=comp(r,c if ch=='c' else d)
 return ppow(r,n)
def generated(gens):
 I=np.arange(len(gens[0]),dtype=np.uint8);S={I.tobytes()};q=deque([I])
 while q:
  x=q.popleft()
  for g in gens:
   y=comp(g,x);k=y.tobytes()
   if k not in S:S.add(k);q.append(y)
 return len(S)
def fixed_subsets(p, objects):return sum(1 for o in objects if tuple(sorted(int(p[i]) for i in o))==o)
def ip(vals,chi,sizes):return sum(s*a*b for s,a,b in zip(sizes,vals,chi))//51840
def main():
 t=time.time();roots=roots_e8();idx={r:i for i,r in enumerate(roots)}
 simples=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0)]
 gens=[refl(r,roots,idx) for r in simples];G,gidx,par=enum(gens);assert len(G)==51840
 cls,co=classes(G,gidx,gens);assert len(cls)==25
 rec=[]
 for ci,C in enumerate(cls):p=G[C[0]];rec.append((ci,order(p),51840//len(C),not bool(par[C[0]])))
 cci=next(ci for ci,o,z,inn in rec if not inn and o==2 and z==1440);dci=next(ci for ci,o,z,inn in rec if inn and o==9 and z==9)
 c=G[cls[cci][0]];d=None
 for j in cls[dci]:
  z=G[j]
  if order(comp(c,z))==10 and generated([c,z])==51840:d=z;break
 assert d is not None
 reps=[];sizes=[]
 for name,w,o,cent in ATLAS:
  p=word(w,c,d);ci=int(co[gidx[p.tobytes()]]);rr=rec[ci];assert rr[1]==o and rr[2]==cent
  reps.append(p);sizes.append(51840//cent)
 dots=np.array([[sum(a*b for a,b in zip(x,y)) for y in roots] for x in roots],dtype=np.int16)
 pair_carriers={}
 for val in (-8,-4,0,4):pair_carriers[f'root_pairs_dot_{val}']=[(i,j) for i in range(240) for j in range(i+1,240) if int(dots[i,j])==val]
 tri=set()
 for i in range(240):
  for j in range(i+1,240):
   if dots[i,j]!=-4:continue
   z=tuple(-(roots[i][k]+roots[j][k]) for k in range(8))
   if z in idx:
    k=idx[z]
    if j<k:tri.add((i,j,k))
 pair_carriers['A2_root_triples_sum_zero']=sorted(tri)
 neg=[idx[tuple(-a for a in r)] for r in roots];lines=[];line_of={}
 for i in range(240):
  if i<neg[i]:li=len(lines);lines.append((i,neg[i]));line_of[i]=li;line_of[neg[i]]=li
 line_perms=[np.array([line_of[int(p[a])] for a,b in lines],dtype=np.uint8) for p in reps]
 line_pair={}
 for av in (0,4):
  objs=[]
  for i,(a,_) in enumerate(lines):
   for j in range(i+1,120):
    if abs(int(dots[a,lines[j][0]]))==av:objs.append((i,j))
  line_pair[f'root_line_pairs_absdot_{av}']=objs
 chars=json.loads((ROOT/'data'/'w33_pass1092_u42dot2_character_identification.json').read_text())['characters'];outcar={}
 for label,objs in pair_carriers.items():
  vals=[fixed_subsets(p,objs) for p in reps];ips={k:ip(vals,v,sizes) for k,v in chars.items()};outcar[label]={'degree':len(objs),'fixed_character':vals,'frame_visible_inner_products':ips,'contains_81_plus':ips['81_plus']>0,'contains_81_minus':ips['81_minus']>0}
 for label,objs in line_pair.items():
  vals=[fixed_subsets(p,objs) for p in line_perms];ips={k:ip(vals,v,sizes) for k,v in chars.items()};outcar[label]={'degree':len(objs),'fixed_character':vals,'frame_visible_inner_products':ips,'contains_81_plus':ips['81_plus']>0,'contains_81_minus':ips['81_minus']>0}
 positives=[(v['degree'],k,v['frame_visible_inner_products']['81_plus'],v['frame_visible_inner_products']['81_minus']) for k,v in outcar.items() if v['contains_81_plus'] or v['contains_81_minus']];positives.sort();first=positives[0]
 upstream=json.loads((ROOT/'data'/'w33_pass1104_e8_pair_carrier_census.json').read_text());a2=outcar['A2_root_triples_sum_zero']
 checks={'roots240':len(roots)==240,'group51840':len(G)==51840,'classes25':len(cls)==25,'A2_triples2240':len(tri)==2240,'root_lines120':len(lines)==120,'carrier_characters_integral':all(isinstance(x,int) for v in outcar.values() for x in v['frame_visible_inner_products'].values()),'positive_81_carrier_found':first is not None,'A2_character_exact':a2['fixed_character']==[2240,32,160,26,242,8,32,12,20,2,32,2,10,2,2,672,40,8,80,42,6,4,8,2,8],'A2_has_no_81plus':a2['frame_visible_inner_products']['81_plus']==0,'A2_has_three_81minus':a2['frame_visible_inner_products']['81_minus']==3,'upstream_pair_census_passed':upstream['status']=='PASS','upstream_pair_minimum3360':upstream['first_any_steinberg']['degree']==3360,'A2_strictly_smaller_than_pair_minimum':len(tri)<upstream['first_any_steinberg']['degree'],'first_plus_still_orthogonal_pairs15120':upstream['first_81_plus']['degree']==15120 and upstream['first_81_plus']['multiplicity_81_plus']==1}
 assert all(checks.values()),(checks,positives)
 out={'schema':'w33.pass1113.e8_a2_triple_carrier_extension.v1','status':'PASS','headline':'Extending the Pass-1104 pair-carrier census by the canonical A2 root triples reveals a smaller E8-derived Steinberg carrier: the 2240 unordered triples of roots summing to zero contain exactly three copies of 81_minus and no 81_plus. This strictly improves the 3360 pair-carrier minimum while leaving the first tested 81_plus occurrence at the 15120 orthogonal-root-pair carrier.','upstream_pass1104':{'path':'data/w33_pass1104_e8_pair_carrier_census.json','pair_universe_minimum':upstream['first_any_steinberg'],'first_81_plus':upstream['first_81_plus']},'a2_triple_carrier':a2,'tested_carriers_for_independent_crosscheck':outcar,'positive_carriers_sorted':positives,'first_positive_after_extension':{'degree':first[0],'carrier':first[1],'multiplicity_81_plus':first[2],'multiplicity_81_minus':first[3]},'checks':checks,'check_count':len(checks),'seconds':time.time()-t,'scope':'Exact W(E6) permutations on doubled-coordinate E8 roots. Minimality is only over the union of the explicit Pass-1104 pair universe and the A2 triple carrier added here; no claim is made over every E8-derived G-set.'}
 OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','first':out['first_positive_after_extension'],'positive':positives,'degrees':{k:v['degree'] for k,v in outcar.items()},'seconds':round(time.time()-t,2)},indent=2))
if __name__=='__main__':main()
