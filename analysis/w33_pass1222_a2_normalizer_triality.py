import sys,json,hashlib
from pathlib import Path
import numpy as np
from collections import Counter
import w33_pass1218_1222_exact_core as c
triples=c.a2_triples();orbits=c.a2_orbits();orbit_of={x:i for i,o in enumerate(orbits) for x in o}
a,b,_=c.base_data()['a2_triple'];sa=c.reflection_permutation(a);sb=c.reflection_permutation(b)

def orbit_perm(root_perm):
 act=c.induced_triple_action(root_perm);p=[]
 for o in orbits:
  im={orbit_of[int(act[x])] for x in o};assert len(im)==1;p.append(next(iter(im)))
 return tuple(p)
pa,pb=orbit_perm(sa),orbit_perm(sb)
G=c.generated_subgroup([np.array(pa,dtype=np.uint8),np.array(pb,dtype=np.uint8)])
assert len(G)==6
color_actions=sorted({tuple([11,12,13].index(int(g[i])) for i in (11,12,13)) for g in G})
six27_actions=sorted({tuple([2,3,4,5,6,7].index(int(g[i])) for i in range(2,8)) for g in G})
# Every point in six-set has trivial stabilizer -> regular S3 torsor.
assert len(six27_actions)==6
for j in range(6):assert sum(p[j]==j for p in six27_actions)==1
# color action transitive with point stabilizer order2; C3 subgroup regular.
orders=[c.permutation_order(np.array(p,dtype=np.uint8)) for p in color_actions]
c3=[p for p,o in zip(color_actions,orders) if o in (1,3)]
assert len(c3)==3 and all(len({p[j] for p in c3})==3 for j in range(3))
out={'schema':'w33.pass1222.a2_normalizer_triality.v1','status':'PASS','base_a2_triple':list(c.base_data()['a2_triple']),
 'commutes_with_WE6':all(np.array_equal(c.compose(sa,g),c.compose(g,sa)) and np.array_equal(c.compose(sb,g),c.compose(g,sb)) for g in c.e6_generators()),
 'centralizer_product_subgroup':{'structure':'W(E6) x W(A2)','order':51840*6},
 'full_A2_subsystem_normalizer':{'order':51840*12,'index_in_W(E8)':696729600//(51840*12),'A2_subsystems':1120},
 'S3_generators':{'reflection_a_orbit_permutation':list(pa),'reflection_b_orbit_permutation':list(pb)},
 'three_432_carriers':{'orbit_indices':[11,12,13],'S3_image_order':6,'action_permutations':color_actions,'point_stabilizer_order':2,
   'verdict':'transitive S3 triality action, not a free S3 torsor','orientation_preserving_C3_is_free_transitive':True},
 'six_27_carriers':{'orbit_indices':[2,3,4,5,6,7],'action_permutations':six27_actions,'verdict':'regular S3 torsor','stabilizer_order':1},
 'two_singletons':{'orbit_indices':[0,1],'reflection_a':list(pa[:2]),'reflection_b':list(pb[:2]),'interpretation':'opposite A2 orientations'},
 'correction':'The three 432 colors cannot be an S3 torsor because |S3|=6. They are S3/S2; their C3 rotation subgroup is the torsor. The signed sixfold 27-shell refinement is the genuine S3 torsor.'}
out['sha256']=hashlib.sha256(json.dumps(out,separators=(',',':'),sort_keys=True).encode()).hexdigest()
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'w33_pass1222_a2_normalizer_triality.json'
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
print('PASS 1222 S3 triality / C3 torsor / six-shell S3 torsor')
