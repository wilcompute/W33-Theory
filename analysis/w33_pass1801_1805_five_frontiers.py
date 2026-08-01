#!/usr/bin/env python3
"""Passes 1801--1805: exact Bockstein, XOR, orbit, decoder, and outer-extension packet."""
from __future__ import annotations
import argparse,collections,hashlib,itertools,json,math,random
from pathlib import Path
import numpy as np
import sympy as sp
from w33_pass1801_1805_common import (
 build_geometry,build_bockstein,rank_mod,rowspace_basis,nullspace,transform_module,
 basis_columns,inv_mod,
)
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1801_1805_five_frontiers.json'

def closure(v,gens):
 b=rowspace_basis([v],2)
 while True:
  c=rowspace_basis(np.vstack([b]+[(g@x)%2 for x in b for g in gens]),2)
  if len(c)==len(b):return c
  b=c
def matpoly(a,poly):
 n=len(a);r=np.zeros((n,n),dtype=np.uint8);p=np.eye(n,dtype=np.uint8)
 for i in range(poly.degree()+1):
  if int(poly.nth(i))%2:r^=p
  p=((p@a)%2).astype(np.uint8)
 return r
def find_subdims(gens,want):
 random.seed(1801);x=sp.symbols('x');found={}
 for trial in range(400):
  a=np.zeros_like(gens[0],dtype=np.uint8)
  for j in range(2+trial%4):
   w=np.eye(len(a),dtype=np.uint8)
   for z in range(1+(trial*7+j)%23):w=((gens[(trial+z+j)%len(gens)]@w)%2).astype(np.uint8)
   a^=w
  cp=sp.Poly(sp.Matrix(a.astype(int)).charpoly(x).as_expr(),x,modulus=2)
  for poly,_ in sp.factor_list(cp,modulus=2)[1]:
   for v in nullspace(matpoly(a,poly),2):
    c=closure(v,gens);found.setdefault(len(c),c)
  if all(d in found for d in want):break
 if not all(d in found for d in want):raise AssertionError((found.keys(),want))
 return found
def algebra_dimension(gens):
 n=len(gens[0]);piv={};queue=[]
 def enc(a):
  out=0
  for i,b in enumerate(a.reshape(-1)):
   if b:out|=1<<i
  return out
 def add(a):
  y=enc(a)
  while y:
   p=y.bit_length()-1
   if p in piv:y^=piv[p]
   else:piv[p]=y;queue.append(a.copy());return
 add(np.eye(n,dtype=np.uint8));q=0
 while q<len(queue):
  a=queue[q];q+=1
  for g in gens:add(((g@a)%2).astype(np.uint8))
 return len(piv)
def centralizer(gens):
 n=len(gens[0]);eq=[]
 for g in gens:
  for i in range(n):
   for j in range(n):
    row=np.zeros(n*n,dtype=np.uint8)
    for k in range(n):
     if g[k,j]:row[i*n+k]^=1
     if g[i,k]:row[k*n+j]^=1
    eq.append(row)
 return [x.reshape(n,n) for x in nullspace(np.array(eq,dtype=np.uint8),2)]
def pass1801(data,bock):
 k=data['K'];qgens=bock['Qgens'];qout=bock['Qout'];beta=bock['Beta']
 pmat=np.zeros((40,45),dtype=np.uint8)
 for j,(l,r) in enumerate(data['octets']):pmat[list(l)+list(r),j]=1
 u16=rowspace_basis((beta@nullspace(pmat,2).T).T,2)
 u1=nullspace(np.vstack([(g-np.eye(30,dtype=np.uint8))%2 for g in qgens]),2)
 assert (len(u1),len(u16))==(1,16)
 sub16,q14,b16,bi16,out16,_=transform_module(qgens,u16,2,qout)
 coords1=rowspace_basis((bi16@u1.T)[:16].T,2)
 _,q15,_,_,_,out15=transform_module(sub16,coords1,2,out16)
 found=find_subdims(q15,{8,9});s8=found[8];s9=found[9]
 assert len(rowspace_basis(np.vstack([s9,s8]),2))==9
 g8,_,_,_,out8,_=transform_module(q15,s8,2,out15)
 g9,q6,b9,bi9,out9,out6=transform_module(q15,s9,2,out15)
 coords8=rowspace_basis((bi9@s8.T)[:9].T,2)
 _,q1,_,_,_,out1=transform_module(g9,coords8,2,out9)
 assert all(int(g[0,0])==1 for g in q1) and int(out1[0,0])==1
 a8,a6,a14=algebra_dimension(g8),algebra_dimension(q6),algebra_dimension(q14)
 c8,c6,c14=centralizer(g8),centralizer(q6),centralizer(q14)
 assert (a8,len(c8),a6,len(c6),a14,len(c14))==(32,2,36,1,196,1)
 eye=np.eye(8,dtype=np.uint8);z=None
 for a in c8:
  if not np.array_equal(a,eye) and not np.any((a@a+a+eye)%2):z=a;break
 assert z is not None
 assert np.array_equal((out8@z@inv_mod(out8,2))%2,(z@z)%2)
 gram=(k@k.T)%2;ker=rowspace_basis(np.vstack([np.ones((1,45),dtype=np.uint8),gram]),2)
 assert len(ker)==15 and not np.any((beta@ker.T)%2)
 return {'beta_rank':rank_mod(beta,2),'beta_kernel_dimension':15,'beta_kernel':'<1_45> direct-sum im(KK^T mod2)','filtration_dimensions':[1,9,10,16,30],'successive_factors_over_F2':['1','8_F2','1','6','14'],'composition_factors_over_alg_closure':['1','4a','4b','1','6','14'],'factor_certificates':{'8_F2':{'algebra':a8,'centralizer':len(c8),'center':'F4 via z^2+z+1'},'6':{'algebra':a6,'centralizer':len(c6)},'14':{'algebra':a14,'centralizer':len(c14)}},'outer_on_8':'z -> z^2, hence the unordered pair {4a,4b} is exchanged','Q30_fixed_dimension':len(u1),'Q30_dual_fixed_dimension':len(nullspace(np.vstack([(g.T-np.eye(30,dtype=np.uint8))%2 for g in qgens]),2)),'prior_art_boundary':'Pass 1611 owns the unlabeled composition series 1,8,1,6,14. Pass 1801 adds the external Brauer-dimension identification and the exact outer-Frobenius action on the F4 endomorphism field.'}

def xor_rref(rows,n):
 piv={};mask=(1<<n)-1
 for x in rows:
  while True:
   v=x&mask
   if not v:
    if (x>>n)&1:raise AssertionError('inconsistent XOR system')
    break
   p=v.bit_length()-1
   if p in piv:x^=piv[p]
   else:
    for q in list(piv):
     if (piv[q]>>p)&1:piv[q]^=x
    piv[p]=x;break
 return sorted(piv.values())
def pass1802(data,bock):
 m=data['M'];j=bock['J'];n=4860;base=[]
 for f in range(540):base.append(sum(1<<(9*f+c) for c in range(9))|(1<<n))
 inc=[np.flatnonzero(m[:,e]) for e in range(240)]
 for e in range(240):
  for c in range(9):base.append(sum(1<<(9*int(f)+c) for f in inc[e])|(1<<n))
 sym=[(1<<(9*int(f)+c))|(1<<n) for c,f in enumerate(inc[0])]
 octets=[]
 for o in range(45):
  fs=np.flatnonzero(j[:,o]);assert len(fs)==72
  for c in range(9):octets.append(sum(1<<(9*int(f)+c) for f in fs))
 ranks={}
 for name,rows in [('base',base),('base_sym',base+sym),('aug',base+octets),('aug_sym',base+octets+sym)]:
  rr=xor_rref(rows,n);weights=collections.Counter((x&((1<<n)-1)).bit_count() for x in rr);ranks[name]={'rank':len(rr),'nullity':n-len(rr),'weight_histogram':dict(sorted(weights.items()))}
  if name=='aug_sym':raw='\n'.join(f'{x:x}' for x in rr).encode();basis_hash=hashlib.sha256(raw).hexdigest()
 assert [ranks[x]['rank'] for x in ranks]==[2100,2109,2340,2349]
 return {'equation_count':len(base)+len(octets)+len(sym),'rank_summary':{k:[v['rank'],v['nullity']] for k,v in ranks.items()},'new_global_XOR_directions':240,'augmented_symmetry_fixed_basis_sha256':basis_hash,'bounded_solver_falsifier':'HiGHS MILP with all 405 exact-8 cuts and standard 9-frame symmetry fixing reached a 20-second limit without an incumbent or SAT/UNSAT verdict; no conclusion is inferred.'}
def bit_tables(perms):
 out=[]
 for p in perms:
  chunks=[]
  for block in range(3):
   tab=[0]*32768;off=15*block
   for x in range(1,32768):
    lb=x&-x;i=lb.bit_length()-1;tab[x]=tab[x^lb]|(1<<p[off+i])
   chunks.append(tab)
  out.append(chunks)
 return out
def act_bits(x,t):return t[0][x&32767]|t[1][(x>>15)&32767]|t[2][(x>>30)&32767]
def pass1803(data):
 k=data['K'];perms=[a[4] for a in data['acts']];outer=data['outer'][4];tables=bit_tables(perms+[outer]);over=(k@k.T);adj=(over>0).astype(np.uint8);np.fill_diagonal(adj,0)
 triples={sum(1<<i for i in np.flatnonzero(k[:,e])) for e in range(240)}
 def invariant(mask):
  vs=[i for i in range(45) if mask>>i&1];e=sum(int(adj[a,b]) for a,b in itertools.combinations(vs,2));t=sum(1 for h in triples if h&mask==h);return (len(vs),e,t,16*len(vs)-2*e+4*t)
 def enumerate_orbits(size):
  unseen={sum(1<<i for i in c) for c in itertools.combinations(range(45),size)};out=[]
  while unseen:
   seed=min(unseen);unseen.remove(seed);orb={seed};queue=[seed]
   while queue:
    x=queue.pop()
    for tab in tables[:5]:
     y=act_bits(x,tab)
     if y not in orb:orb.add(y);unseen.discard(y);queue.append(y)
   out.append((seed,orb))
  return sorted(out,key=lambda z:(invariant(z[0]),len(z[1]),z[0]))
 o3,o4=enumerate_orbits(3),enumerate_orbits(4);i3={x:i for i,(_,o) in enumerate(o3) for x in o};i4={x:i for i,(_,o) in enumerate(o4) for x in o}
 up=np.zeros((len(o3),len(o4)),dtype=int);down=np.zeros((len(o4),len(o3)),dtype=int)
 for i,(s,_) in enumerate(o3):
  for v in range(45):
   if not s>>v&1:up[i,i4[s|1<<v]]+=1
 for i,(s,_) in enumerate(o4):
  for v in range(45):
   if s>>v&1:down[i,i3[s^(1<<v)]]+=1
 assert np.all(np.array([len(o) for _,o in o3])[:,None]*up==(np.array([len(o) for _,o in o4])[:,None]*down).T)
 payload={'triple_orbits':[{'size':len(o),'stabilizer':25920//len(o),'invariant':invariant(s),'outer_stable':act_bits(s,tables[5]) in o} for s,o in o3],'four_subset_orbits':[{'size':len(o),'stabilizer':25920//len(o),'invariant':invariant(s),'outer_stable':act_bits(s,tables[5]) in o} for s,o in o4],'up':up.tolist(),'down':down.tolist()}
 payload['transfer_sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 assert len(o3)==6 and len(o4)==20
 return payload
def pass1804(data):
 k=data['K'];sigs=np.array([sum(1<<i for i in np.flatnonzero(k[:,e])) for e in range(240)],dtype=np.uint64)
 pairs=np.empty(math.comb(240,2),dtype=np.uint64);q=0
 for i in range(239):a=sigs[i]^sigs[i+1:];pairs[q:q+len(a)]=a;q+=len(a)
 _,pc=np.unique(np.sort(pairs),return_counts=True);unique2=int(np.sum(pc[pc==1]))
 n=math.comb(240,3);arr=np.empty(n,dtype=np.uint64);q=0
 for i in range(238):
  for j in range(i+1,239):a=sigs[i]^sigs[j]^sigs[j+1:];arr[q:q+len(a)]=a;q+=len(a)
 arr.sort();u,c=np.unique(arr,return_counts=True);singles=set(map(int,sigs));shadow=np.array([int(x) in singles for x in u]);non=~shadow
 unique3=int(np.sum(c[(c==1)&non]));ambig3=int(np.sum(c[(c>1)&non]));shadow3=int(np.sum(c[shadow]))
 mult={int(x):int(y) for x,y in zip(u,c)};tables=bit_tables([a[4] for a in data['acts']]+[data['outer'][4]])
 unseen=set(mult);orbits=[]
 while unseen:
  seed=unseen.pop();orb={seed};queue=[seed]
  while queue:
   x=queue.pop()
   for tab in tables[:5]:
    y=act_bits(x,tab)
    if y not in orb:orb.add(y);unseen.discard(y);queue.append(y)
  vals={mult[x] for x in orb};sh={x in singles for x in orb};assert len(vals)==len(sh)==1
  orbits.append((len(orb),25920//len(orb),next(iter(vals)),next(iter(sh)),act_bits(seed,tables[5]) in orb))
 coarse=collections.Counter(orbits)
 assert (unique2,unique3,ambig3,shadow3,len(orbits))==(25440,1576000,697120,2160,110)
 return {'minimum_weight_decoder_coefficients':{'0':1,'1':240,'2':unique2,'3':unique3},'success_polynomial':'(1-p)^240 + 240 p(1-p)^239 + 25440 p^2(1-p)^238 + 1576000 p^3(1-p)^237','weight3_total':n,'weight3_ambiguous_minimum':ambig3,'weight3_shadowed_by_weight1':shadow3,'triple_bucket_profile':dict(sorted(collections.Counter(map(int,c)).items())),'syndrome_orbit_count_through_weight3':len(orbits),'orbit_coarse_profile':[{'orbit_size':a,'stabilizer':b,'minimum_bucket_multiplicity':d,'shadowed_by_weight1':e,'outer_stable':f,'count':count} for (a,b,d,e,f),count in sorted(coarse.items())]}
def pass1805(data):
 p=1000003;edges=data['edges'];octets=data['octets'];eidx=data['eidx'];d=np.zeros((40,240),dtype=np.int64)
 for j,(a,b) in enumerate(edges):d[a,j]=-1;d[b,j]=1
 s=np.zeros((45,40),dtype=np.int64);u=np.zeros((45,240),dtype=np.int64)
 for o,(left,right) in enumerate(octets):
  s[o,list(left)]=1;s[o,list(right)]=-1
  for a in left:
   for b in right:u[o,eidx[tuple(sorted((a,b)))]]=1 if a<b else -1
 v=4*u+s@d;assert not np.any(d@u.T+4*s.T) and not np.any(d@v.T) and rank_mod(v,p)==30
 rows=basis_columns(v.T,p);basis=v[rows,:]%p;cols=basis_columns(basis,p);cinv=inv_mod(basis[:,cols],p)
 def rep(act):
  pp,ep=act[0],act[1];sign=np.array([1 if pp[a]<pp[b] else -1 for a,b in edges],dtype=np.int64);y=np.zeros_like(basis);y[:,np.array(ep)]=(basis*sign)%p;r=(y[:,cols]@cinv)%p;assert np.array_equal((r@basis)%p,y%p);return r
 rout=rep(data['outer']);assert not np.any((rout@rout-np.eye(30,dtype=np.int64))%p)
 plus=30-rank_mod((rout-np.eye(30,dtype=np.int64))%p,p);minus=30-rank_mod((rout+np.eye(30,dtype=np.int64))%p,p);trace=int(np.trace(rout)%p);trace=trace if trace<p//2 else trace-p
 assert (plus,minus,trace)==(16,14,2)
 fixed=sum(i==data['outer'][4][i] for i in range(45));signed=sum(data['outer'][5][i] for i in range(45) if i==data['outer'][4][i])
 return {'oriented_lift_rank':30,'cycle_identity':'d V^T=0','coexact_identity':'L1 V^T=4 V^T','canonical_multiplier_minus_one_outer':{'trace':trace,'plus_eigenspace':plus,'minus_eigenspace':minus,'determinant':1},'signed_octet_outer_trace':signed,'fixed_octets':fixed,'extension_boundary':'This fixes the geometric extension by the canonical similitude; the sign-twisted extension has trace -2. No ATLAS class label is assigned without a standard-generator fusion certificate.'}
def certificate():
 data=build_geometry();bock=build_bockstein(data)
 checks={'geometry_counts':(len(data['points']),len(data['edges']),len(data['lines']),len(data['frames']),len(data['octets']))==(40,240,40,540,45),'frame_octet_hash_boundary':rank_mod(data['M'],2)==195 and rank_mod(data['K'],2)==45}
 payload={'schema':'w33.pass1801_1805.five_frontiers.v1','status':'PASS','pass1801_bockstein_brauer':pass1801(data,bock),'pass1802_xor_resolution':pass1802(data,bock),'pass1803_three_body_orbit_transfer':pass1803(data),'pass1804_optimal_low_weight_decoder':pass1804(data),'pass1805_full_weyl_coexact_extension':pass1805(data),'checks':checks,'evidence_boundary':'All promoted group, module, XOR-rank, orbit-transfer, low-weight decoder, and outer-extension statements are exact. The 20-second MILP run is a bounded falsifier only. The global Hoffman resolution and full weight enumerator remain open.','parallel_boundary':'Passes 1606-1616 and 1701-1705 were occupied by parallel continuation tracks while this packet was running. The release was collision-safely renumbered to 1801-1805. Pass 1805 records an independent canonical-similitude certificate and does not pre-empt any standard-generator/ATLAS class identification from those tracks.'}
 payload['status']='PASS' if all(checks.values()) else 'FAIL'
 raw=json.dumps(payload,sort_keys=True,separators=(',',':'));payload['certificate_sha256']=hashlib.sha256(raw.encode()).hexdigest();return payload
def main()->int:
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--check',action='store_true');args=ap.parse_args();payload=certificate();text=json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n'
 if args.check:
  if not args.output.exists() or args.output.read_text()!=text:raise SystemExit('Passes 1801-1805 certificate drift')
 else:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
 print(json.dumps({'status':payload['status'],'sha256':payload['certificate_sha256'],'checks':sum(payload['checks'].values()),'total':len(payload['checks'])}))
 return 0 if payload['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
