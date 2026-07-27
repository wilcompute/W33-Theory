from __future__ import annotations
import itertools,json,math,time
from collections import deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1104_e8_pair_carrier_census.json'
ATLAS=[('1A','(cdcdcddcdcdddcdd)^4',1,51840),('2A','(cdd)^4',2,1152),('2B','(cdcdcddcdcdddcdd)^2',2,192),('3A','(cdcdd)^4',3,648),('3C','(ccdcdddcddd)^2',3,216),('3D','(cddcdcdddcdd)^2',3,108),('4A','(cdd)^2',4,96),('4B','cdcdcddcdcdddcdd',4,16),('5A','(cd)^2',5,10),('6A','(cdcdd)^2',6,72),('6C','ccdcdddcddd',6,36),('6E','cddcdcdddcdd',6,36),('6F','(cdcdcdd)^2',6,24),('9A','d',9,9),('12A','cdcdd',12,12),('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),('2D','(cdcdddcdd)^3',2,96),('4C','(cdcdcdd)^3',4,96),('4D','dcdcdcdd',4,32),('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),('6H','dcdd',6,36),('6I','cdcdddcdd',6,12),('8A','cdd',8,8),('10A','cd',10,10),('12C','cdcdcdd',12,12)]
SIZES=[51840//x[3] for x in ATLAS]
CHI_PLUS=[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,-9,3,-3,1,0,0,0,-1,1,0]
CHI_MINUS=[81,9,-3,0,0,0,-3,-1,1,0,0,0,0,0,0,9,-3,3,-1,0,0,0,1,-1,0]
def roots_e8():
 r=[]
 for i in range(8):
  for j in range(i+1,8):
   for si in [1,-1]:
    for sj in [1,-1]:v=[0]*8;v[i]=2*si;v[j]=2*sj;r.append(tuple(v))
 for m in range(256):
  v=tuple(-1 if (m>>k)&1 else 1 for k in range(8))
  if sum(x==-1 for x in v)%2==0:r.append(v)
 return r
def compose(a,b):return a[b]
def invperm(p):q=np.empty_like(p);q[p]=np.arange(len(p),dtype=p.dtype);return q
def reflection_perm(r,roots,idx):
 out=[]
 for x in roots:q=sum(a*b for a,b in zip(x,r))//4;out.append(idx[tuple(a-q*b for a,b in zip(x,r))])
 return np.array(out,dtype=np.uint8)
def order(p):
 seen=np.zeros(len(p),bool);o=1
 for i in range(len(p)):
  if not seen[i]:
   j=i;l=0
   while not seen[j]:seen[j]=1;j=int(p[j]);l+=1
   o=math.lcm(o,l)
 return o
def enum_group(gens):
 I=np.arange(len(gens[0]),dtype=np.uint8);keys={I.tobytes():0};els=[I];par=[0];q=deque([0])
 while q:
  i=q.popleft();x=els[i]
  for g in gens:
   y=compose(g,x);k=y.tobytes()
   if k not in keys:keys[k]=len(els);els.append(y.copy());par.append(par[i]^1);q.append(len(els)-1)
 return np.stack(els),keys,np.array(par,dtype=np.uint8)
def classes(arr,index,gens):
 trs=[]
 for g in gens:gi=invperm(g);C=gi[arr[:,g]];trs.append(np.array([index[row.tobytes()] for row in C],dtype=np.int32))
 unseen=np.ones(len(arr),bool);out=[];co=np.empty(len(arr),dtype=np.int16)
 for seed in range(len(arr)):
  if not unseen[seed]:continue
  unseen[seed]=False;q=deque([seed]);orb=[]
  while q:
   x=q.popleft();orb.append(x)
   for tr in trs:
    y=int(tr[x])
    if unseen[y]:unseen[y]=False;q.append(y)
  co[orb]=len(out);out.append(orb)
 return out,co
def ppower(p,n):
 r=np.arange(len(p),dtype=p.dtype);b=p
 while n:
  if n&1:r=compose(r,b)
  b=compose(b,b);n//=2
 return r
def eval_word(expr,c,d):
 if expr.startswith('('):w,n=expr[1:].split(')^');n=int(n)
 else:w=expr;n=1
 r=np.arange(len(c),dtype=c.dtype)
 for ch in w:r=compose(r,c if ch=='c' else d)
 return ppower(r,n)
def gen_size(gens):
 I=np.arange(len(gens[0]),dtype=np.uint8);seen={I.tobytes()};q=deque([I])
 while q:
  x=q.popleft()
  for g in gens:
   y=compose(g,x);k=y.tobytes()
   if k not in seen:seen.add(k);q.append(y)
 return len(seen)
def inner_product(char,chi):return sum(s*a*b for s,a,b in zip(SIZES,char,chi))//51840
def fixed_unordered(p,pairs):im=np.sort(p[pairs],axis=1);return int(np.sum(np.all(im==pairs,axis=1)))
def main():
 t=time.time();roots=roots_e8();idx={r:i for i,r in enumerate(roots)};simples=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0)]
 gens=[reflection_perm(r,roots,idx) for r in simples];G,index,par=enum_group(gens);cls,co=classes(G,index,gens);rec=[]
 for ci,x in enumerate(cls):rep=G[x[0]];rec.append({'ci':ci,'size':len(x),'centralizer':51840//len(x),'order':order(rep),'inner':not bool(par[x[0]])})
 cci=next(r['ci'] for r in rec if not r['inner'] and r['order']==2 and r['centralizer']==1440);dci=next(r['ci'] for r in rec if r['inner'] and r['order']==9 and r['centralizer']==9);c=G[cls[cci][0]];d=None
 for ii in cls[dci]:
  z=G[ii]
  if order(compose(c,z))==10 and gen_size([c,z])==51840:d=z;break
 assert d is not None;reps=[]
 for name,w,o,cent in ATLAS:x=eval_word(w,c,d);rr=rec[int(co[index[x.tobytes()]])];assert rr['order']==o and rr['centralizer']==cent;reps.append(x)
 R=np.array(roots,dtype=np.int16);pairs=np.array(list(itertools.combinations(range(240),2)),dtype=np.int16);dots=np.einsum('ij,ij->i',R[pairs[:,0]],R[pairs[:,1]]);neg=np.array([idx[tuple(-a for a in r)] for r in roots],dtype=np.int16);line_roots=[i for i in range(240) if i<neg[i]];root_to_line=np.empty(240,dtype=np.int16)
 for li,i in enumerate(line_roots):root_to_line[i]=li;root_to_line[neg[i]]=li
 LP=np.array(list(itertools.combinations(range(120),2)),dtype=np.int16);LR=R[line_roots];ldots=np.abs(np.einsum('ij,ij->i',LR[LP[:,0]],LR[LP[:,1]]));carriers=[]
 for val in [-8,-4,0,4]:
  P=pairs[dots==val];char=[fixed_unordered(p,P) for p in reps];carriers.append({'family':'unordered_root_pairs','relation':f'dot={val}','degree':len(P),'character':char,'multiplicity_81_plus':inner_product(char,CHI_PLUS),'multiplicity_81_minus':inner_product(char,CHI_MINUS)})
 line_perms=[root_to_line[p[line_roots]] for p in reps]
 for val in [0,4]:
  P=LP[ldots==val];char=[fixed_unordered(p,P) for p in line_perms];carriers.append({'family':'unordered_antipodal_root_line_pairs','relation':f'absdot={val}','degree':len(P),'character':char,'multiplicity_81_plus':inner_product(char,CHI_PLUS),'multiplicity_81_minus':inner_product(char,CHI_MINUS)})
 positive=[x for x in carriers if x['multiplicity_81_plus'] or x['multiplicity_81_minus']];first_any=min(positive,key=lambda x:x['degree']);first_plus=min((x for x in positive if x['multiplicity_81_plus']),key=lambda x:x['degree']);expected={('unordered_root_pairs','dot=-8'):(120,0,0),('unordered_root_pairs','dot=-4'):(6720,0,10),('unordered_root_pairs','dot=0'):(15120,1,26),('unordered_root_pairs','dot=4'):(6720,0,7),('unordered_antipodal_root_line_pairs','absdot=0'):(3780,0,6),('unordered_antipodal_root_line_pairs','absdot=4'):(3360,0,4)}
 checks={'E8_roots240':len(roots)==240,'WE6_order51840':len(G)==51840,'ATLAS_classes25':len(cls)==25,'standard_pair_found':d is not None,'root_pair_partition28680':sum(x['degree'] for x in carriers if x['family']=='unordered_root_pairs')==28680,'root_line_pair_partition7140':sum(x['degree'] for x in carriers if x['family'].startswith('unordered_antipodal'))==7140,'all_expected_degrees_and_multiplicities':all((x['degree'],x['multiplicity_81_plus'],x['multiplicity_81_minus'])==expected[(x['family'],x['relation'])] for x in carriers),'antipodal_pairs_still_zero':next(x for x in carriers if x['relation']=='dot=-8')['multiplicity_81_minus']==0,'smallest_declared_carrier_degree3360':first_any['degree']==3360,'smallest_declared_carrier_is_root_line_absdot4':first_any['family']=='unordered_antipodal_root_line_pairs' and first_any['relation']=='absdot=4','smallest_declared_carrier_contains_four_81minus':first_any['multiplicity_81_minus']==4,'no_81plus_before_degree15120':all(x['multiplicity_81_plus']==0 for x in carriers if x['degree']<15120),'first_81plus_is_orthogonal_root_pairs':first_plus['family']=='unordered_root_pairs' and first_plus['relation']=='dot=0','first_81plus_multiplicity1':first_plus['multiplicity_81_plus']==1,'orthogonal_pairs_also_have_26_minus':first_plus['multiplicity_81_minus']==26,'all_multiplicities_nonnegative_integral':all(isinstance(x['multiplicity_81_plus'],int) and isinstance(x['multiplicity_81_minus'],int) and min(x['multiplicity_81_plus'],x['multiplicity_81_minus'])>=0 for x in carriers)};assert all(checks.values()),checks
 out={'schema':'w33.pass1104.e8_pair_carrier_census.v1','status':'PASS','headline':'Within the declared natural pair-carrier universe derived from E8 roots and antipodal root lines, the first carrier containing a frame Steinberg constituent is the 3360-element set of nonorthogonal antipodal root-line pairs; it contains 81_minus with multiplicity four and no 81_plus. The first 81_plus occurs in the 15120 orthogonal unordered-root-pair carrier with multiplicity one.','search_universe':['unordered E8 root pairs partitioned by root inner product','unordered antipodal E8 root-line pairs partitioned by absolute inner product'],'carriers':carriers,'first_any_steinberg':first_any,'first_81_plus':first_plus,'minimality_scope':'Minimal only inside the explicitly enumerated pair-carrier universe above; no claim is made over every subgroup coset action or every E8-derived combinatorial carrier.','check_count':len(checks),'checks':checks,'seconds':time.time()-t};OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'first_any':first_any,'first_plus':first_plus,'seconds':round(time.time()-t,3)},indent=2))
if __name__=='__main__':main()
