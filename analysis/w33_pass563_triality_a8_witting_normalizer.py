#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass563_triality_a8_witting_normalizer.json'
BLOCKS=(
 frozenset((0b0001,0b0010,0b0100,0b1000,0b1111)),
 frozenset((0b0101,0b1001,0b1010,0b1011,0b1101)),
 frozenset((0b0011,0b0110,0b0111,0b1100,0b1110)),
)
ID4=(1,2,4,8)

def f2rank(rows):
 b=[]
 for x in rows:
  y=x
  for p in b:y=min(y,y^p)
  if y:
   q=1<<(y.bit_length()-1);b=[z^y if z&q else z for z in b];b.append(y);b.sort(reverse=True)
 return len(b)
def mv(g,x):
 y=0
 for i,c in enumerate(g):
  if (x>>i)&1:y^=c
 return y
def comp(f,g):return tuple(mv(f,c) for c in g)
def gl4():return tuple(g for g in itertools.permutations(range(1,16),4) if f2rank(g)==4)
def inv_fast(g):
 p=[mv(g,x) for x in range(16)];q=[0]*16
 for i,x in enumerate(p):q[x]=i
 return tuple(q[1<<i] for i in range(4))
def closure(gens):
 H={ID4};front=[ID4]
 while front:
  a=front.pop()
  for b in gens:
   for c in (comp(a,b),comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)
def order(g):
 x=ID4
 for n in range(1,121):
  x=comp(g,x)
  if x==ID4:return n
 raise AssertionError
def conjugate_set(h,H,hinv):return frozenset(comp(comp(h,g),hinv) for g in H)

def permutation_comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def permutation_inv(p):
 q=[0]*len(p)
 for i,x in enumerate(p):q[x]=i
 return tuple(q)
def permutation_order(p):
 q=tuple(range(len(p)))
 for n in range(1,121):
  q=permutation_comp(p,q)
  if q==tuple(range(len(p))):return n
 raise AssertionError
def permutation_parity(p):
 return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
def perm_from_cycles(n,cycles):
 p=list(range(n))
 for cyc in cycles:
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):p[a]=b
 return tuple(p)
def perm_closure(gens,n):
 I=tuple(range(n));H={I};front=[I]
 while front:
  a=front.pop()
  for b in gens:
   for c in (permutation_comp(a,b),permutation_comp(b,a)):
    if c not in H:H.add(c);front.append(c)
 return frozenset(H)

def a8_model():
 r=perm_from_cycles(8,[(0,1,2),(3,4,5,6,7)])
 s=perm_from_cycles(8,[(1,2),(4,5,7,6)])
 G=perm_closure((r,s),8)
 A8=tuple(p for p in itertools.permutations(range(8)) if permutation_parity(p)==0)
 C=perm_closure((r,),8)
 N=[]
 for h in A8:
  hi=permutation_inv(h)
  if frozenset(permutation_comp(permutation_comp(h,g),hi) for g in C)==C:N.append(h)
 return r,s,G,A8,frozenset(N)

def gf4_mul(a,b):
 if a==0 or b==0:return 0
 a0,a1=a&1,(a>>1)&1;b0,b1=b&1,(b>>1)&1
 c0=a0*b0+a1*b1;c1=a0*b1+a1*b0+a1*b1
 return ((c1%2)<<1)|(c0%2)
def gf4_square(a):return gf4_mul(a,a)
def gf4_trace(a):return (a^gf4_square(a))&1
def gf4_inv(a):return next(b for b in (1,2,3) if gf4_mul(a,b)==1)
def normalize(v):
 for x in v:
  if x:return tuple(gf4_mul(gf4_inv(x),y) for y in v)
def witting_hit_lines():
 omega=(1,2,3);states=[]
 for i in range(4):
  v=[0]*4;v[i]=1;states.append(tuple(v))
 for mu,nu in itertools.product(range(3),repeat=2):
  a,b=omega[mu],omega[nu]
  states.extend(((0,1,a,b),(1,0,a,b),(1,a,0,b),(1,a,b,0)))
 states=list(dict.fromkeys(normalize(v) for v in states))
 lines=set()
 for v in states:
  imgs=set()
  for c in omega:
   t=tuple(gf4_trace(gf4_mul(c,x)) for x in v)
   n=(t[0]<<3)|(t[1]<<2)|(t[2]<<1)|t[3]
   if n:imgs.add(n)
  if len(imgs)==3:
   a,b,c=sorted(imgs)
   if a^b==c:lines.add((a,b,c))
 return frozenset(lines)
def image_line(g,L):return tuple(sorted(mv(g,x) for x in L))

def payload():
 GL=gl4();part=frozenset(BLOCKS)
 G=frozenset(g for g in GL if frozenset(frozenset(mv(g,x) for x in b) for b in BLOCKS)==part)
 inverses={g:inv_fast(g) for g in GL}
 N=frozenset(h for h in GL if conjugate_set(h,G,inverses[h])==G)
 central=frozenset(h for h in GL if all(comp(h,g)==comp(g,h) for g in G))
 singer=next(g for g in G if order(g)==15)
 singerC=closure((singer,))
 singercentral=frozenset(h for h in GL if all(comp(h,g)==comp(g,h) for g in singerC))
 singerN=frozenset(h for h in GL if conjugate_set(h,singerC,inverses[h])==singerC)
 r,s,GA,A8,NA=a8_model()
 hit=witting_hit_lines();W=frozenset(g for g in GL if all(image_line(g,L) in hit for L in hit))
 inter=G&W
 conj={frozenset(comp(comp(h,g),inverses[h]) for g in G) for h in GL}
 checks={
  'gl42_order20160':len(GL)==20160,
  'triality_group_order60':len(G)==60,
  'triality_is_singer_normalizer':G==singerN and len(singerC)==15,
  'triality_self_normalizing':N==G,
  'group_centralizer_trivial':len(central)==1,
  'singer_centralizer_is_c15':singercentral==singerC,
  'conjugacy_class_size336':len(conj)==336 and len(GL)//len(N)==336,
  'a8_model_even_generators':permutation_parity(r)==permutation_parity(s)==0,
  'a8_model_order60':len(GA)==60,
  'a8_normalizer_of_3x5_cycle':GA==NA,
  'a8_element_order_census_matches':Counter(order(g) for g in G)==Counter(permutation_order(p) for p in GA),
  'witting_hit_lines16':len(hit)==16,
  'witting_stabilizer_computed':len(W)>0,
  'not_witting_line_stabilizer':G!=W,
  'not_icosahedral_A5':Counter(order(g) for g in G).get(15,0)==8 and Counter(order(g) for g in G).get(4,0)==30,
 }
 return {
  'schema':'w33.pass563.triality_a8_witting_normalizer.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'gl42_a8':{
   'ambient_order':len(GL),'triality_order':len(G),'normalizer_order':len(N),'group_centralizer_order':len(central),'singer_centralizer_order':len(singercentral),
   'conjugacy_class_size':len(conj),'index':len(GL)//len(G),
   'identification':'The triality group is the self-normalizing Singer-cycle normalizer N_GL(4,2)(C15) = C15 semidirect C4.',
   'a8_permutation_model':{'r_cycle_type':'(3)(5)','s_description':'simultaneous inversion on C3 and exponent-doubling on C5','normalizer_order':len(NA)},
   'element_order_histogram':dict(sorted(Counter(order(g) for g in G).items())),
  },
  'witting_alignment':{
   'hit_line_count':len(hit),'line_stabilizer_order':len(W),'intersection_order':len(inter),
   'relation':'The Singer normalizer is transitive on the 15 PG(3,2) points, whereas the Witting 16-line stabilizer fixes its missing point. They are distinct subgroups; the exact intersection is recorded.',
  },
  'tower_boundary':{
   'positive':'The subgroup is canonically located at the repository GL(4,2) ~= A8 symmetry horizon as the normalizer of an A8 element of cycle type (3)(5).',
   'negative_600_cell':'It is not the icosahedral rotation group A5: it is solvable, contains elements of orders 4 and 15, and has normal C15.',
   'e6_witting':'No objectwise embedding into the E6/Witting action is asserted beyond the exact GL(4,2) horizon and the computed Witting-line-stabilizer intersection.',
  },
  'checks':checks,
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 563 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'normalizer':p['gl42_a8']['normalizer_order']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
