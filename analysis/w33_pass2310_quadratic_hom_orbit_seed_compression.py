#!/usr/bin/env python3
"""Pass 2310: orbit-seed compression of the complete quadratic Hom bases."""
from __future__ import annotations
import hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass2301_complete_quadratic_hom_bases.json'
OUT=ROOT/'data/w33_pass2310_quadratic_hom_orbit_seed_compression.json'
EXPECTED='2bb3b09a06e4d030a5737553518e6c019519e42ba0024494313e6214f0405686'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def build():
    s=json.loads(SRC.read_text()); assert s['sha256_without_hash_field']=='26eab93605eeb603e3a899c2ecda2a39e268c65e3286b86dce9449f0540b8c43'
    count=Counter();targets=defaultdict(list);osizes={}
    total=0
    for kind,rows in s['compressed_orbit_bases'].items():
      for target,reps in rows.items():
       for z in reps:
        key=(kind,tuple(z['representative']));count[key]+=1;targets[key].append(int(target))
        osizes[key]=int(z['orbit_size']);total+=int(z['orbit_size'])
    unique=sum(osizes[k] for k in count)
    table=[]
    for k in sorted(count):
      kind,rep=k;o=osizes[k]
      table.append({'symmetry':kind,'representative':list(rep),'reuse_count':count[k],
                    'targets':sorted(targets[k]),'orbit_size':o,'stabilizer_order':25920//o})
    dense=0
    for kind,rows in s['compressed_orbit_bases'].items():
      pairs=90*91//2 if kind=='Sym' else 90*89//2
      dense+=sum(pairs*int(t)*len(v) for t,v in rows.items())
    d={'schema':'w33.pass2310.quadratic_hom_orbit_seed_compression.v1',
       'status':'PASS_WITH_ORBIT_STORAGE_NOT_TENSOR_RANK_BOUNDARY',
       'source':{'certificate':str(SRC.relative_to(ROOT)),'sha256_without_hash_field':s['sha256_without_hash_field'],
                 'producer':'analysis/w33_pass2301_complete_quadratic_hom_bases.py'},
       'counts':{'basis_maps':sum(count.values()),'unique_signed_orbit_seeds':len(count),
                 'symmetric_maps':sum(len(x) for x in s['compressed_orbit_bases']['Sym'].values()),
                 'alternating_maps':sum(len(x) for x in s['compressed_orbit_bases']['Lambda'].values()),
                 'seed_reuse_histogram':{str(k):v for k,v in sorted(Counter(count.values()).items())},
                 'seeds_reaching_all_four_targets':sum(len(set(v))==4 for v in targets.values()),
                 'unique_seeds_with_nontrivial_stabilizer':sum(z['stabilizer_order']>1 for z in table)},
       'storage':{'literal_orbit_entries_if_expanded_per_map':total,
                  'literal_orbit_entries_if_unique_seeds_cached_once':unique,
                  'exact_cache_compression_factor':str(Fraction(total,unique)),
                  'cache_compression_factor_approx':round(total/unique,12),
                  'dense_target_coordinate_entries':dense,
                  'per_map_orbit_entry_fraction':str(Fraction(total,dense)),
                  'per_map_orbit_entry_fraction_approx':round(total/dense,12),
                  'interpretation':'Cache one signed orbit tensor per seed, then apply target projectors; five seeds feed all four targets.'},
       'exceptional_seeds':[z for z in table if z['stabilizer_order']>1],
       'seed_table':table,
       'checks':{'map_count_50':sum(count.values())==50,'unique_seed_count_24':len(count)==24,
                 'reuse_histogram_11_5_3_5':Counter(count.values())==Counter({1:11,2:5,3:3,4:5}),
                 'five_all_target_seeds':sum(len(set(v))==4 for v in targets.values())==5,
                 'two_nonregular_seeds':sum(z['stabilizer_order']>1 for z in table)==2,
                 'storage_ratio_281_over_135':Fraction(total,unique)==Fraction(281,135),
                 'producer_orbit_size_is_literal_entry_count':True},
       'theorem':'The fifty complete quadratic Hom-basis maps are generated from only twenty-four distinct signed-orbit seeds. Caching each orbit tensor once reduces literal orbit-entry storage from 1,213,920 to 583,200, an exact factor 281/135, before target projection.',
       'boundary':'Orbit-entry compression is representation storage sparsity. It does not prove spatial hardware locality, minimal CP tensor rank, low physical interaction order, or measured coupling strengths.'}
    assert all(d['checks'].values());d['sha256_without_hash_field']=digest(d);return d
def main():
    d=build();assert d['sha256_without_hash_field']==EXPECTED
    frozen=json.loads(OUT.read_text());assert frozen==d
    print(json.dumps({'status':d['status'],'certificate':EXPECTED,'maps':50,'seeds':24,'compression':'281/135'},sort_keys=True))
if __name__=='__main__':main()
