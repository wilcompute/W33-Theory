#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json
from collections import Counter,defaultdict,deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass568_singer_intersection_design.json'
BLOCKS=(
 frozenset((0b0001,0b0010,0b0100,0b1000,0b1111)),
 frozenset((0b0101,0b1001,0b1010,0b1011,0b1101)),
 frozenset((0b0011,0b0110,0b0111,0b1100,0b1110)),
)
ID=(1,2,4,8)

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
def inv(g):
 p=[mv(g,x) for x in range(16)];q=[0]*16
 for i,x in enumerate(p):q[x]=i
 return tuple(q[1<<i] for i in range(4))
def order(g):
 x=ID
 for n in range(1,121):
  x=comp(g,x)
  if x==ID:return n
 raise AssertionError
def conj(h,g,hi):return comp(comp(h,g),hi)
def conj_group(h,H,hi):return frozenset(conj(h,g,hi) for g in H)

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
def dot(a,b):return (a&b).bit_count()%2

def subgroup_signature(H):
 return (len(H),tuple(sorted(Counter(order(g) for g in H).items())))
def sigstr(sig):return f"{sig[0]}|"+','.join(f'{a}^{b}' for a,b in sig[1])

def payload():
 GL=gl4();invs={g:inv(g) for g in GL};part=frozenset(BLOCKS)
 G=frozenset(g for g in GL if frozenset(frozenset(mv(g,x) for x in b) for b in BLOCKS)==part)
 conjugates={conj_group(h,G,invs[h]) for h in GL};conjugates=tuple(sorted(conjugates,key=lambda H:tuple(sorted(H))))
 idx={H:i for i,H in enumerate(conjugates)}
 hit=witting_hit_lines();W=frozenset(g for g in GL if all(image_line(g,L) in hit for L in hit))
 points=tuple(range(1,16))
 lines=tuple(sorted({tuple(sorted((a,b,a^b))) for a in points for b in points if a<b and a^b not in (0,a,b)}))
 planes=tuple(frozenset(x for x in points if dot(h,x)==0) for h in points)
 point_stabs={p:frozenset(g for g in GL if mv(g,p)==p) for p in points}
 line_stabs={L:frozenset(g for g in GL if frozenset(mv(g,x) for x in L)==frozenset(L)) for L in lines}
 plane_stabs={i:frozenset(g for g in GL if frozenset(mv(g,x) for x in P)==P) for i,P in enumerate(planes)}
 
 winter=[];point_all=[];line_all=[];plane_all=[]
 per_conj=[]
 for H in conjugates:
  IW=H&W;winter.append(subgroup_signature(IW))
  ps=[subgroup_signature(H&S) for S in point_stabs.values()]
  ls=[subgroup_signature(H&S) for S in line_stabs.values()]
  hs=[subgroup_signature(H&S) for S in plane_stabs.values()]
  point_all.extend(ps);line_all.extend(ls);plane_all.extend(hs)
  per_conj.append({'witting':sigstr(subgroup_signature(IW)),'point_size_hist':dict(sorted(Counter(s[0] for s in ps).items())),'line_size_hist':dict(sorted(Counter(s[0] for s in ls).items())),'plane_size_hist':dict(sorted(Counter(s[0] for s in hs).items()))})
 
 # W acts on the 336 conjugates; classify the incidence orbits.
 unseen=set(range(len(conjugates)));worbits=[]
 while unseen:
  seed=min(unseen);orb={idx[conj_group(w,conjugates[seed],invs[w])] for w in W}
  # close in case W generators not all represented due direct image duplicates (normally already closed)
  frontier=list(orb)
  while frontier:
   j=frontier.pop()
   for w in W:
    k=idx[conj_group(w,conjugates[j],invs[w])]
    if k not in orb:orb.add(k);frontier.append(k)
  unseen-=orb;worbits.append(tuple(sorted(orb)))
 worbit_rows=[]
 for O in sorted(worbits,key=lambda x:(len(x),x)):
  sigs=Counter(winter[i] for i in O)
  worbit_rows.append({'size':len(O),'witting_intersection_signatures':{sigstr(k):v for k,v in sorted(sigs.items(),key=lambda z:sigstr(z[0]))}})
 
 def census(arr):
  c=Counter(arr)
  return {sigstr(k):v for k,v in sorted(c.items(),key=lambda z:(z[0][0],z[0][1]))}
 checks={
  'gl42_order20160':len(GL)==20160,
  'singer_normalizer_order60':len(G)==60,
  'exact_336_conjugates':len(conjugates)==336,
  'witting_stabilizer_order48':len(W)==48,
  'projective_points15':len(points)==15,
  'projective_lines35':len(lines)==35,
  'projective_planes15':len(set(planes))==15,
  'point_stabilizers_order1344':set(map(len,point_stabs.values()))=={1344},
  'line_stabilizers_order576':set(map(len,line_stabs.values()))=={576},
  'plane_stabilizers_order1344':set(map(len,plane_stabs.values()))=={1344},
  'witting_orbits_partition336':sum(map(len,worbits))==336 and len(set().union(*map(set,worbits)))==336,
  'all_intersections_are_subgroups':all(ID in (H&W) for H in conjugates),
 }
 return {
  'schema':'w33.pass568.singer_intersection_design.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'ambient':{'GL42_order':len(GL),'Singer_normalizer_order':len(G),'Singer_normalizer_conjugates':len(conjugates),'Witting_line_stabilizer_order':len(W)},
  'families':{
   'Witting_fixed_16_line_stabilizer':{'intersection_signature_census':census(winter),'W_orbits_on_336':worbit_rows},
   'PG32_point_stabilizers':{'family_size':15,'member_order':1344,'intersection_signature_census':census(point_all)},
   'PG32_line_stabilizers':{'family_size':35,'member_order':576,'intersection_signature_census':census(line_all)},
   'PG32_plane_stabilizers':{'family_size':15,'member_order':1344,'intersection_signature_census':census(plane_all)},
  },
  'incidence_summary':{
   'witting_nontrivial_conjugates':sum(s[0]>1 for s in winter),
   'witting_max_intersection_order':max(s[0] for s in winter),
   'witting_orbit_count':len(worbits),
   'point_incidence_pairs':len(point_all),'line_incidence_pairs':len(line_all),'plane_incidence_pairs':len(plane_all),
   'duality_point_plane_census_equal':Counter(point_all)==Counter(plane_all),
  },
  'checks':checks,
  'boundary':'The W33-side families here are the canonical point, line, and plane stabilizer families at the repository PG(3,2)/GL(4,2) symmetry horizon. This is not a claim that every full W(3,3) stabilizer embeds into GL(4,2).'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 568 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'witting_orbits':p['incidence_summary']['witting_orbit_count']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
