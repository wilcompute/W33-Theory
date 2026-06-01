from collections import Counter
from itertools import permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXIV_S6_OUTER_AUTOMORPHISM_CLASS_SWAP_results.json'

from analysis.w33_s6_duad_syntheme_pentad_bridge import main as dsp_main, act_syntheme
from analysis.w33_petersen_k6_pg32_operation_weld import perfect_matchings


def compose(p,q): return tuple(p[i] for i in q)
def inv(p):
    r=[0]*len(p)
    for i,j in enumerate(p): r[j]=i
    return tuple(r)
def cycle_type(p):
    seen=[False]*len(p); lens=[]
    for i in range(len(p)):
        if not seen[i]:
            j=i; c=0
            while not seen[j]:
                seen[j]=True; c+=1; j=p[j]
            if c>1: lens.append(c)
    return tuple(sorted(lens, reverse=True)) or (1,)

def main():
    prev=dsp_main()
    V=tuple(range(6)); S6=list(permutations(V)); synthemes=perfect_matchings(V)
    # Rebuild pentads: five synthemes whose 15 duads partition K6.
    all_duads=set(tuple(sorted(e)) for e in __import__('itertools').combinations(V,2))
    pentads=[]
    for subset in __import__('itertools').combinations(range(len(synthemes)),5):
        edges=[]
        for si in subset: edges.extend(synthemes[si])
        if set(edges)==all_duads and len(set(edges))==15:
            pentads.append(tuple(sorted(subset)))
    pentads=sorted(pentads); pindex={P:i for i,P in enumerate(pentads)}
    sindex={S:i for i,S in enumerate(synthemes)}

    phi={}
    for g in S6:
        image=[]
        for P in pentads:
            im=tuple(sorted(sindex[act_syntheme(g, synthemes[si])] for si in P))
            image.append(pindex[im])
        phi[g]=tuple(image)

    image_set=set(phi.values())
    homo_ok=all(phi[compose(g,h)]==compose(phi[g],phi[h]) for g in S6 for h in S6)
    inverse_ok=all(phi[inv(g)]==inv(phi[g]) for g in S6)
    class_pairs=Counter((cycle_type(g), cycle_type(phi[g])) for g in S6)
    domain_class=Counter(cycle_type(g) for g in S6)
    image_class=Counter(cycle_type(phi[g]) for g in S6)
    transpositions=[g for g in S6 if cycle_type(g)==(2,)]
    triple_transpositions=[g for g in S6 if cycle_type(g)==(2,2,2)]
    class_swap_trans=Counter(cycle_type(phi[g]) for g in transpositions)
    class_swap_triple=Counter(cycle_type(phi[g]) for g in triple_transpositions)

    # Not inner: inner automorphisms preserve cycle type in Sn; phi swaps two different classes.
    checks={
      'inherits_duad_syntheme_pentad':prev['n_verified']==prev['n_checks']==20,
      'six_pentads':len(pentads)==6,
      'phi_image_size_720':len(image_set)==720,
      'homomorphism':homo_ok,
      'inverse_respected':inverse_ok,
      'automorphism_bijective':len(phi)==720 and len(image_set)==720,
      'transpositions_15':domain_class[(2,)]==15,
      'triple_transpositions_15':domain_class[(2,2,2)]==15,
      'transpositions_map_to_triple_transpositions':class_swap_trans==Counter({(2,2,2):15}),
      'triple_transpositions_map_to_transpositions':class_swap_triple==Counter({(2,):15}),
      'not_inner_cycle_type_not_preserved':any(cycle_type(g)!=cycle_type(phi[g]) for g in S6),
      'class_table_preserved_as_counts':domain_class==image_class,
      'class_pair_transposition_certificate':class_pairs[((2,),(2,2,2))]==15 and class_pairs[((2,2,2),(2,))]==15,
      'pentad_stabilizer_120':sum(1 for g in S6 if phi[g][0]==0)==120,
      'orbit_stabilizer_6x120':6*120==720,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXIV',
      'theorem':'S6 outer automorphism class-swap certificate',
      'class_counts':{str(k):v for k,v in sorted(domain_class.items(), key=lambda kv:(sum(kv[0]),kv[0]))},
      'key_class_swaps':{'transpositions_to_triple_transpositions':15,'triple_transpositions_to_transpositions':15},
      'groups':{'domain_S6':720,'image_on_pentads':len(image_set),'pentad_stabilizer':120},
      'interpretation':'The six pentads form a second six-set. The induced action phi:S6->S6 is a bijective homomorphism. It maps the 15 original transpositions to the 15 triple-transpositions on the pentad six-set and maps triple-transpositions back to transpositions. Since inner automorphisms of S6 preserve cycle type, this is an explicit outer automorphism certificate for the duad-syntheme-pentad bridge.',
      'w33_reading':'The previous 15 duad/15 syntheme carriers are now connected by an actual S6 outer class-swap. This gives a group-theoretic mechanism for exchanging the Petersen/K6 duad carrier with the syntheme carrier while preserving the 15-state PG(3,2)/E15 packet layer.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['key_class_swaps'])
