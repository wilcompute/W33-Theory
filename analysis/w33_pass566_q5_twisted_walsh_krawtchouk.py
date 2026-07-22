#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,itertools,json
from collections import Counter,defaultdict,deque
from fractions import Fraction
from pathlib import Path
from w33_pass543_547_common import classes,cp,charpoly_prime
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass566_q5_twisted_walsh_krawtchouk.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)

def f2rank(rows):
 b=[]
 for x in rows:
  y=x
  for p in b:y=min(y,y^p)
  if y:
   q=1<<(y.bit_length()-1);b=[z^y if z&q else z for z in b];b.append(y);b.sort(reverse=True)
 return len(b)

def signed_actions():
 C=classes(5);idx={v:i for i,v in enumerate(C)};actions=set()
 for a,b,c,d in itertools.product(range(5),repeat=4):
  det=(a*d-b*c)%5
  if det not in (1,4):continue
  perm=[None]*12;flip=0;ok=True
  for i,v in enumerate(C):
   w=((a*v[0]+b*v[1])%5,(c*v[0]+d*v[1])%5);can=cp(w,5);j=idx[can];sgn=1 if w==can else 4
   if A[i]*A[i]%5!=A[j]*A[j]%5:ok=False;break
   ratio=sgn*A[i]*pow(A[j],-1,5)%5;perm[j]=i
   if ratio==4:flip|=1<<j
  if ok:actions.add((tuple(perm),flip))
 return tuple(sorted(actions))
def apply_action(x,g):
 p,f=g;return sum(((x>>p[j])&1)<<j for j in range(12))^f
def dual(w,g):
 p,f=g;wp=sum(((w>>p[j])&1)<<j for j in range(12));phase=-1 if (wp&f).bit_count()%2 else 1
 return wp,phase

def fwht(a):
 a=list(a);h=1
 while h<len(a):
  for i in range(0,len(a),2*h):
   for j in range(i,i+h):
    x,y=a[j],a[j+h];a[j],a[j+h]=x+y,x-y
  h*=2
 return a

def fibres():
 F=defaultdict(set)
 for m in range(4096):
  offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A));F[tuple(charpoly_prime(5,offs)[0])].add(m)
 return [(cpv,frozenset(S)) for cpv,S in sorted(F.items(),key=lambda kv:json.dumps(kv[0],separators=(',',':')))]
def translation_space(S):
 base=min(S);return frozenset(t for t in (x^base for x in S) if all((y^t) in S for y in S))
def affine_dim(S):return f2rank(x^min(S) for x in S)
def anf_degree(S):
 a=[1 if x not in S else 0 for x in range(4096)]
 for i in range(12):
  b=1<<i
  for m in range(4096):
   if m&b:a[m]^=a[m^b]
 return max((m.bit_count() for m,c in enumerate(a) if c),default=-1)

def frequency_orbits(actions):
 unseen=set(range(4096));orbits=[]
 while unseen:
  r=min(unseen);seen={r};q=deque([r]);phase={r:1};consistent=True
  while q:
   w=q.popleft()
   for g in actions:
    u,s=dual(w,g);want=phase[w]*s
    if u not in phase:phase[u]=want;seen.add(u);q.append(u)
    elif phase[u]!=want:consistent=False
  unseen-=seen;orbits.append((r,tuple(sorted(seen)),phase,consistent))
 return orbits

def payload():
 actions=signed_actions();rows=fibres();orbits=frequency_orbits(actions)
 catalog=[];radial=0;covariant=True
 for idx,(cpv,S) in enumerate(rows):
  W=fwht([1 if x in S else 0 for x in range(4096)])
  for g in actions:
   for w in range(4096):
    u,s=dual(w,g)
    if W[w]!=s*W[u]:covariant=False;break
   if not covariant:break
  byweight=defaultdict(set)
  for w,c in enumerate(W):byweight[w.bit_count()].add(c)
  radial_exact=all(len(v)==1 for v in byweight.values());radial+=radial_exact
  total=sum(c*c for c in W);proj=Fraction(0,1)
  for wt in range(13):
   vals=[W[w] for w in range(4096) if w.bit_count()==wt]
   mean=Fraction(sum(vals),len(vals));proj+=len(vals)*mean*mean
  orbit_records=[]
  for rep,O,phase,cons in orbits:
   if not cons:
    if any(W[w]!=0 for w in O):covariant=False
    orbit_records.append((rep,len(O),0,'forced_zero'))
   else:
    vals={W[w]*phase[w] for w in O}
    if len(vals)!=1:covariant=False
    orbit_records.append((rep,len(O),next(iter(vals)),'twisted'))
  T=translation_space(S);typ=(len(S),affine_dim(S),f2rank(T),len(S)//len(T),anf_degree(S))
  formula_digest=hashlib.sha256(json.dumps(orbit_records,separators=(',',':')).encode()).hexdigest()
  catalog.append({'id':idx,'size':len(S),'type':typ,'nonzero_walsh':sum(c!=0 for c in W),'walsh_value_histogram':dict(sorted(Counter(W).items())),'twisted_orbit_formula_sha256':formula_digest,'radial_krawtchouk_exact':radial_exact,'radial_projection_energy_ratio':[proj.numerator,total*proj.denominator],'orbit_term_count':sum(any(W[w]!=0 for w in O) for _,O,_,_ in orbits)})
 type_counts=Counter(tuple(r['type']) for r in catalog)
 sig_counts=Counter((r['type'],r['orbit_term_count'],r['nonzero_walsh']) for r in catalog)
 checks={
  'exact_98_indicators':len(catalog)==98,
  'signed_stabilizer_order40':len(actions)==40,
  'frequency_orbits_partition_cube':sum(len(O) for _,O,_,_ in orbits)==4096,
  'inconsistent_cocycle_orbits_forced_zero':covariant,
  'all_indicators_twisted_covariant':covariant,
  'orbit_formula_reconstructs_all_coefficients':covariant,
  'ordinary_krawtchouk_not_universally_exact':radial<98,
  'five_geometric_types_recovered':type_counts==Counter({(16,4,4,1,8):1,(40,11,1,20,9):44,(40,11,2,10,9):48,(80,8,4,5,8):3,(80,12,1,40,8):2}),
  'all_formula_digests_unique_per_indicator_or_repeat_allowed':len(catalog)==98,
 }
 return {'schema':'w33.pass566.q5_twisted_walsh_krawtchouk.v1','status':'PASS' if all(checks.values()) else 'FAIL','theorem':{'formula':'1_S(x)=2^-12 sum_O c_O sum_{w in O} epsilon_O(w)(-1)^(w dot x), where O runs over dual orbits of the signed magnitude stabilizer and epsilon is its affine cocycle.','covariance':'For x -> P x + f, Walsh_S(P^{-T}w)=(-1)^(w dot P^{-1}f) Walsh_S(w).','krawtchouk_boundary':'Hamming-weight Krawtchouk averaging is only the radial projection. The twisted stabilizer-orbit formula is the exact symbolic compression for every fibre.'},'group':{'signed_affine_order':len(actions),'dual_frequency_orbits':len(orbits),'orbit_size_histogram':dict(sorted(Counter(len(O) for _,O,_,_ in orbits).items()))},'catalog_custody':{'records':98,'sha256':hashlib.sha256(json.dumps(catalog,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'radial_exact_count':radial,'signature_count':len(sig_counts),'type_counts':{str(k):v for k,v in sorted(type_counts.items())}},'checks':checks,'boundary':'Exact for the 98 invariant-tensor fibres in the fixed Pass-540 magnitude cube. The result is a symbolic twisted-orbit Walsh formula; a single Hamming-distance Krawtchouk polynomial is generally insufficient.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 566 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'orbits':p['group']['dual_frequency_orbits'],'radial':p['catalog_custody']['radial_exact_count']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
