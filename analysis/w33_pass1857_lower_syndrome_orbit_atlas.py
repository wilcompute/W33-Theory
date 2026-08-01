#!/usr/bin/env python3
from __future__ import annotations
import collections,hashlib,importlib.util,itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COMMON=ROOT/'analysis'/'w33_pass1801_1805_common.py'

def load_common():
 s=importlib.util.spec_from_file_location('common',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m

def transform(x,p):
 y=0
 while x:
  b=(x&-x).bit_length()-1;y|=1<<p[b];x&=x-1
 return y

def main():
 c=load_common();g=c.build_geometry();cols=[]
 for e in range(240):
  x=0
  for i in range(45):
   if g['K'][i,e]:x|=1<<i
  cols.append(x)
 cnt1=collections.Counter(cols);cnt3=collections.Counter()
 for a in range(238):
  xa=cols[a]
  for b in range(a+1,239):
   xab=xa^cols[b]
   for cc in range(b+1,240):cnt3[xab^cols[cc]]+=1
 lower=set(cnt1)|set(cnt3);gens=[x[4] for x in g['acts']]
 unseen=set(lower);orbits=[]
 while unseen:
  seed=min(unseen);orb={seed};q=[seed]
  while q:
   x=q.pop()
   for p in gens:
    y=transform(x,p)
    assert y in lower
    if y not in orb:orb.add(y);q.append(y)
  unseen.difference_update(orb)
  vals={(cnt1[x],cnt3[x],x.bit_count()) for x in orb};assert len(vals)==1
  n1,n3,sw=vals.pop();orbits.append({'representative':seed,'orbit_size':len(orb),'syndrome_weight':sw,'weight1_multiplicity':n1,'weight3_multiplicity':n3,'minimum_weight':1 if n1 else 3})
 orbits.sort(key=lambda z:(z['minimum_weight'],z['weight1_multiplicity'],z['weight3_multiplicity'],z['syndrome_weight'],z['representative']))
 hist=collections.Counter((z['minimum_weight'],z['weight1_multiplicity'],z['weight3_multiplicity'],z['syndrome_weight'],z['orbit_size']) for z in orbits)
 checks={
  'weight1_errors':sum(cnt1.values())==240,
  'weight3_errors':sum(cnt3.values())==2275280,
  'orbit_partition':sum(z['orbit_size'] for z in orbits)==len(lower),
  'orbit_sizes_divide_group':all(25920%z['orbit_size']==0 for z in orbits),
  'weight1_shadow_syndromes':sum(1 for x in lower if cnt1[x])==len(cnt1),
 }
 out={'schema':'w33.pass1857.lower_syndrome_orbit_atlas.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
 'lower_syndrome_count':len(lower),'weight1_distinct_syndromes':len(cnt1),'weight3_distinct_syndromes':len(cnt3),'orbit_count':len(orbits),
 'minimum_weight_orbit_count':dict(collections.Counter(str(z['minimum_weight']) for z in orbits)),
 'minimum_weight_syndrome_count':dict(collections.Counter(str(1 if cnt1[x] else 3) for x in lower)),
 'orbit_type_histogram':{'|'.join(map(str,k)):v for k,v in sorted(hist.items())},'orbits':orbits,
 'decoder':'Store one representative, minimum weight, and lower-error multiplicities per orbit; recover any lower odd syndrome by the five certified octet permutations. Weight-five syndromes outside this atlas have no weight-one or weight-three shadow.',
 'boundary':'This is the complete inner-group orbit atlas of every syndrome reachable at odd weight below five. It certifies the symmetry-compressed lower-shadow decoder, but does not enumerate all minimum-weight-five syndrome orbits.'}
 raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['sha256']=hashlib.sha256(raw).hexdigest();print(json.dumps(out,sort_keys=True,separators=(',',':')));raise SystemExit(out['status']!='PASS')
if __name__=='__main__':main()
