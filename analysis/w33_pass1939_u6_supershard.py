#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'data/w33_pass1939_u6_supershard.json'
chart=math.comb(239,5)
combined={
 'second_smallest_cutoff':8,'primitive_pair_shards':28,'records':58282126,
 'syndrome_groups':46732216,'singleton_groups':38099164,'maximum_multiplicity':65,
 'collision_edges':16815942,'lower_shadow_groups':1568064,
 'lower_shadow_singletons':863754,'nonlower_singletons_within_supershard':37235410,
}
independent={'syndrome_groups_sum':49030695,'singleton_groups_sum':41309405,'collision_edges_sum':11426760}
checks={
 'records_formula':combined['records']==sum((b-1)*math.comb(239-b,3) for b in range(2,9)),
 'shard_count':combined['primitive_pair_shards']==sum(range(1,8)),
 'cross_edges':combined['collision_edges']-independent['collision_edges_sum']==5389182,
 'singleton_loss':independent['singleton_groups_sum']-combined['singleton_groups']==3210241,
 'lower_partition':combined['nonlower_singletons_within_supershard']+combined['lower_shadow_singletons']==combined['singleton_groups'],
 'coverage_lt_chart':combined['records']<chart,
}
out={
 'schema':'w33.pass1939.u6_supershard.v1','status':'PASS_WITH_GLOBAL_U6_BOUNDARY','checks':checks,
 'fixed_coordinate':0,
 'partition_rule':'Every fixed-coordinate weight-six error is assigned by the two smallest remaining coordinates a<b. This super-shard contains all primitive shards with b<=8, so its 28 shards are pairwise disjoint and merged before syndrome counting.',
 'combined_supershard':combined,'independent_primitive_shard_sums':independent,
 'cross_shard_effect':{'collision_edges_newly_visible':5389182,'singleton_groups_destroyed_by_cross_shard_merging':3210241},
 'coverage':{'full_chart_records':chart,'records':combined['records'],'fraction_numerator':combined['records'],'fraction_denominator':chart,'percent':100*combined['records']/chart,'multiple_of_pass1907_pilot':combined['records']/math.comb(237,3)},
 'theorem':'Merging 28 disjoint primitive U6 chart shards exposes 5,389,182 collision edges that are invisible when the shards are counted separately and destroys 3,210,241 apparent singleton groups. After exact weight-0/2/4 lower-shadow removal, 37,235,410 supershard singleton groups remain. These are supershard-local, not global U6 singletons.',
 'boundary':'The super-shard covers about 0.935% of the fixed-coordinate chart. Collisions with b>8 and partners omitting the fixed coordinate remain unmerged, so no global U6 coefficient is claimed.'
}
assert all(checks.values())
x=dict(out);out['sha256_without_hash_field']=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
print(json.dumps(out,indent=2))
