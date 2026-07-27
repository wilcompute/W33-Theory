from __future__ import annotations

import json, math
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1120_we6_class_algebra_decomposition.json'
ATLAS=[('1A','(cdcdcddcdcdddcdd)^4',1,51840),('2A','(cdd)^4',2,1152),('2B','(cdcdcddcdcdddcdd)^2',2,192),('3A','(cdcdd)^4',3,648),('3C','(ccdcdddcddd)^2',3,216),('3D','(cddcdcdddcdd)^2',3,108),('4A','(cdd)^2',4,96),('4B','cdcdcddcdcdddcdd',4,16),('5A','(cd)^2',5,10),('6A','(cdcdd)^2',6,72),('6C','ccdcdddcddd',6,36),('6E','cddcdcdddcdd',6,36),('6F','(cdcdcdd)^2',6,24),('9A','d',9,9),('12A','cdcdd',12,12),('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),('2D','(cdcdddcdd)^3',2,96),('4C','(cdcdcdd)^3',4,96),('4D','dcdcdcdd',4,32),('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),('6H','dcdd',6,36),('6I','cdcdddcdd',6,12),('8A','cdd',8,8),('10A','cd',10,10),('12C','cdcdcdd',12,12)]
SIZES=np.array([51840//x[3] for x in ATLAS],dtype=np.int64)
PERM=np.array([2240,32,160,26,242,8,32,12,20,2,32,2,10,2,2,672,40,8,80,42,6,4,8,2,8],dtype=np.int64)

def roots_e8():
 r=[]
 for i in range(8):
  for j in range(i+1,8):
   for si in (1,-1):
    for sj in (1,-1):
     v=[0]*8;v[i]=2*si;v[j]=2*sj;r.append(tuple(v))
 for m in range(256):
  v=tuple(-1 if (m>>k)&1 else 1 for k in range(8))
  if sum(x==-1 for x in v)%2==0:r.append(v)
 return r
def compose(a,b):return a[b]
def invperm(p):q=np.empty_like(p);q[p]=np.arange(len(p),dtype=p.dtype);return q
def reflection_perm(r,roots,idx):
 out=[]
 for x in roots:
  q=sum(a*b for a,b in zip(x,r))//4;out.append(idx[tuple(a-q*b for a,b in zip(x,r))])
 return np.array(out,dtype=np.uint8)
def order(p):
 seen=np.zeros(len(p),bool);o=1
 for i in range(len(p)):
  if not seen[i]:
   j=i;l=0
   while not seen[j]:seen[j]=True;j=int(p[j]);l+=1
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
 for g in gens:
  gi=invperm(g);C=gi[arr[:,g]];trs.append(np.array([index[row.tobytes()] for row in C],dtype=np.int32))
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

def main():
 roots=roots_e8();idx={r:i for i,r in enumerate(roots)};simples=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0)]
 gens=[reflection_perm(r,roots,idx) for r in simples];G,index,par=enum_group(gens);cls,co=classes(G,index,gens);rec=[]
 for ci,x in enumerate(cls):
  rep=G[x[0]];rec.append({'ci':ci,'size':len(x),'centralizer':51840//len(x),'order':order(rep),'inner':not bool(par[x[0]])})
 cci=next(r['ci'] for r in rec if not r['inner'] and r['order']==2 and r['centralizer']==1440);dci=next(r['ci'] for r in rec if r['inner'] and r['order']==9 and r['centralizer']==9);c=G[cls[cci][0]];d=None
 for ii in cls[dci]:
  z=G[ii]
  if order(compose(c,z))==10 and gen_size([c,z])==51840:d=z;break
 assert d is not None;reps=[];mapping=[]
 for _,w,o,cent in ATLAS:
  x=eval_word(w,c,d);ci=int(co[index[x.tobytes()]]);rr=rec[ci];assert rr['order']==o and rr['centralizer']==cent;reps.append(x);mapping.append(ci)
 invG=np.empty_like(G);ar=np.arange(240,dtype=np.uint8)
 for i,p in enumerate(G):invG[i,p]=ar
 internal_to_atlas={ci:i for i,ci in enumerate(mapping)};co_atlas=np.array([internal_to_atlas[int(x)] for x in co],dtype=np.int16);cls_atlas=[np.array(cls[ci],dtype=np.int32) for ci in mapping]
 L=[]
 for elems in cls_atlas:
  M=np.zeros((25,25),dtype=np.int64);invblock=invG[elems]
  for k,z in enumerate(reps):
   prod=invblock[:,z];inds=np.fromiter((index[row.tobytes()] for row in prod),dtype=np.int32,count=len(prod));M[k,:]=np.bincount(co_atlas[inds],minlength=25)
  L.append(M)
 assert np.array_equal(L[0],np.eye(25,dtype=np.int64))
 coeff=np.array([1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89],float);A=sum(coeff[i]*L[i] for i in range(25));vals,vecs=np.linalg.eig(A.astype(float));assert len({round(float(x.real),7) for x in vals})==25 and np.max(np.abs(vals.imag))<1e-8
 rows=[]
 for col in range(25):
  v=vecs[:,col].real;den=float(v@v);lam=np.rint([float(v@(M@v)/den) for M in L]).astype(np.int64);s=sum((int(lam[i])**2)/int(SIZES[i]) for i in range(25));deg=int(round(math.sqrt(51840/s)));chi=[deg*int(lam[i])//int(SIZES[i]) for i in range(25)];mult=deg*sum(int(PERM[i])*int(lam[i]) for i in range(25))//51840;rows.append({'degree':deg,'character':chi,'multiplicity':mult})
 rows.sort(key=lambda x:(x['degree'],x['character']));X=np.array([x['character'] for x in rows],dtype=np.int64);gram=X@np.diag(SIZES)@X.T
 checks={'we6_order_51840':len(G)==51840,'classes_25':len(cls)==25,'class_sizes_match':all(len(cls[mapping[i]])==SIZES[i] for i in range(25)),'class_algebra_identity':np.array_equal(L[0],np.eye(25,dtype=np.int64)),'generic_spectrum_simple':len({round(float(x.real),7) for x in vals})==25,'characters_integral':all(all(isinstance(y,int) for y in x['character']) for x in rows),'row_orthogonality':np.array_equal(gram,51840*np.eye(25,dtype=np.int64)),'degree_square_sum':sum(x['degree']**2 for x in rows)==51840,'multiplicities_nonnegative':all(x['multiplicity']>=0 for x in rows),'degree_reconstruction':sum(x['degree']*x['multiplicity'] for x in rows)==2240,'steinberg_minus_three':any(x['degree']==81 and x['character'][15]==9 and x['multiplicity']==3 for x in rows),'steinberg_plus_zero':any(x['degree']==81 and x['character'][15]==-9 and x['multiplicity']==0 for x in rows)};assert all(checks.values()),checks
 out={'schema':'w33.pass1120.we6_class_algebra_decomposition.v1','status':'PASS','headline':'The complete 25-row irreducible character table of W(E6)=U4(2):2 is reconstructed directly from its exact conjugacy-class algebra. The 2240-point A2-root-triple permutation character has eleven nonzero constituents and contains three copies of 81_minus and no 81_plus.','atlas_class_order':[x[0] for x in ATLAS],'class_sizes':SIZES.tolist(),'permutation_character':PERM.tolist(),'irreducible_rows':rows,'nonzero_decomposition':[{'degree':x['degree'],'multiplicity':x['multiplicity'],'character':x['character']} for x in rows if x['multiplicity']],'decomposition_by_degree':{str(d):sum(x['multiplicity'] for x in rows if x['degree']==d) for d in sorted({x['degree'] for x in rows})},'check_count':len(checks),'checks':checks,'scope':'Exact finite-group class-algebra reconstruction. CTblLib remains the independent canonical row-order and alias witness.'};OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'nonzero':[(x['degree'],x['multiplicity']) for x in rows if x['multiplicity']]},indent=2))
if __name__=='__main__':main()
