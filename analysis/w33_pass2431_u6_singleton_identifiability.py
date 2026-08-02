#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass2411_global_u6_collision_ledger.json'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build(shards=4096):
 s=json.loads(SRC.read_text());N=int(s['weight6_errors']);E=int(s['global_equal_syndrome_collision_edges']);S2=N+2*E
 ranges=[]
 for i in range(shards):
  a=(N*i)//shards;b=(N*(i+1))//shards;ranges.append([a,b])
 manifest_hash=hashlib.sha256(json.dumps(ranges,separators=(',',':')).encode()).hexdigest()
 # Same total representatives and pair collisions, different singleton counts.
 A={'n1':0,'n2':3,'n3':0,'representatives':6,'pair_collisions':3}
 B={'n1':3,'n2':0,'n3':1,'representatives':6,'pair_collisions':3}
 out={
  'schema':'w33.pass2431.u6_singleton_identifiability.v1',
  'status':'PASS_EXACT_SECOND_MOMENT_WITH_SINGLETON_NONIDENTIFIABILITY_AND_DISTRIBUTED_UNION_CONTRACT',
  'global_weight6_representatives':N,
  'global_pair_collisions':E,
  'exact_second_moment_sum_m2_n_m':S2,
  'size_biased_mean_multiplicity':{'numerator':S2,'denominator':N},
  'cauchy_lower_bound_on_occupied_weight6_syndromes':(N*N+S2-1)//S2,
  'nonidentifiability_witness':{'distribution_A':A,'distribution_B':B,'conclusion':'N and E, equivalently the first and second factorial moments, do not determine n1.'},
  'factorial_moment_requirement':{'F1':'sum m n_m = N','F2':'sum m(m-1)n_m = 2E','next_missing':'F3=sum m(m-1)(m-2)n_m','full_recovery':'If maximum multiplicity is M, F0 through FM determine the finite histogram by triangular inversion.'},
  'lower_shadow_union_boundary':'The existing lower-shadow incidence counts do not give the intersection between lower-shadow-marked errors and collision-marked errors, so the bitmap union cannot be inferred from separate totals.',
  'distributed_union_contract':{
    'chart_bitmap_bits':int(s['fixed_coordinate_chart_records']),
    'chart_bitmap_bytes':int(s['map_reduce_contract']['external_partner_bitmap_bytes']),
    'rank_shards':shards,
    'minimum_bits_per_shard':min(b-a for a,b in ranges),
    'maximum_bits_per_shard':max(b-a for a,b in ranges),
    'rank_ranges_sha256':manifest_hash,
    'map_output':'idempotent bitset of chart combinadic ranks marked by any collision partner or lower-shadow syndrome',
    'reduce':'bitwise OR followed by exact popcount',
    'globalization':'After fixed-chart union and cross-chart consistency, multiply only orbitwise-deduplicated singleton counts; never multiply pair incidences.'
  },
  'boundary':'No global U6 singleton coefficient is claimed. The packet proves exactly which statistic is missing and freezes a disjoint deterministic reduction of that statistic.',
  'checks':{
    'source_pair_total':E==1724138884380,
    'second_moment_identity':S2==3697497150640,
    'witness_same_N':A['representatives']==B['representatives'],
    'witness_same_E':A['pair_collisions']==B['pair_collisions'],
    'witness_different_singletons':A['n1']!=B['n1'],
    'ranges_partition_all_representatives':ranges[0][0]==0 and ranges[-1][1]==N and all(ranges[i][1]==ranges[i+1][0] for i in range(shards-1))
  }
 }
 assert all(out['checks'].values());out['sha256_without_hash_field']=digest(out);return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--shards',type=int,default=4096);ap.add_argument('--write-json',type=Path);a=ap.parse_args();o=build(a.shards)
 if a.write_json:a.write_json.write_text(json.dumps(o,indent=2,sort_keys=True))
 print(json.dumps(o,sort_keys=True))
if __name__=='__main__':main()
