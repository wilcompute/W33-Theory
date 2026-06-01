from collections import Counter, defaultdict
from itertools import combinations, permutations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXIII_S6_DUAD_SYNTHEME_PENTAD_results.json'

from analysis.w33_petersen_k6_pg32_operation_weld import main as operation_weld_main, perfect_matchings


def act_edge(p,e): return tuple(sorted((p[e[0]], p[e[1]])))
def act_syntheme(p,S): return tuple(sorted(act_edge(p,e) for e in S))

def main():
    prev=operation_weld_main()
    V=tuple(range(6))
    duads=list(combinations(V,2)); duad_index={e:i for i,e in enumerate(duads)}
    synthemes=perfect_matchings(V); syntheme_index={S:i for i,S in enumerate(synthemes)}

    pentads=[]
    all_duads=set(duads)
    for subset in combinations(range(len(synthemes)),5):
        edges=[]
        for si in subset: edges.extend(synthemes[si])
        if len(edges)==15 and set(edges)==all_duads and len(set(edges))==15:
            pentads.append(tuple(sorted(subset)))
    pentad_index={P:i for i,P in enumerate(pentads)}

    duad_to_synthemes=defaultdict(list)
    for si,S in enumerate(synthemes):
        for e in S: duad_to_synthemes[e].append(si)
    syntheme_to_pentads=defaultdict(list)
    for pi,P in enumerate(pentads):
        for si in P: syntheme_to_pentads[si].append(pi)

    pentad_pair_to_syntheme={}
    for a,b in combinations(range(len(pentads)),2):
        inter=set(pentads[a]) & set(pentads[b])
        if len(inter)==1:
            pentad_pair_to_syntheme[(a,b)]=next(iter(inter))

    # S6 actions on duads, synthemes, and pentads.
    s6=list(permutations(V))
    duad_actions=set(); syntheme_actions=set(); pentad_actions=set()
    duad_stab=syntheme_stab=pentad_stab=0
    for p in s6:
        da=tuple(duad_index[act_edge(p,e)] for e in duads)
        sa=tuple(syntheme_index[act_syntheme(p,S)] for S in synthemes)
        pa=[]
        for P in pentads:
            image=tuple(sorted(syntheme_index[act_syntheme(p, synthemes[si])] for si in P))
            pa.append(pentad_index[image])
        pa=tuple(pa)
        duad_actions.add(da); syntheme_actions.add(sa); pentad_actions.add(pa)
        if da[0]==0: duad_stab+=1
        if sa[0]==0: syntheme_stab+=1
        if pa[0]==0: pentad_stab+=1

    checks={
      'inherits_operation_weld':prev['n_verified']==prev['n_checks']==15,
      'duads_15':len(duads)==15,
      'synthemes_15':len(synthemes)==15,
      'pentads_6':len(pentads)==6,
      'each_syntheme_three_duads':set(len(S) for S in synthemes)=={3},
      'each_pentad_five_synthemes':set(len(P) for P in pentads)=={5},
      'each_duad_in_three_synthemes':Counter(len(v) for v in duad_to_synthemes.values())==Counter({3:15}),
      'each_syntheme_in_two_pentads':Counter(len(v) for v in syntheme_to_pentads.values())==Counter({2:15}),
      'pentad_pairs_label_all_synthemes':len(pentad_pair_to_syntheme)==15 and set(pentad_pair_to_syntheme.values())==set(range(15)),
      'duad_syntheme_incidence_45':sum(len(v) for v in duad_to_synthemes.values())==45,
      'syntheme_pentad_incidence_30':sum(len(v) for v in syntheme_to_pentads.values())==30,
      's6_order_720':len(s6)==720,
      's6_duad_action_faithful':len(duad_actions)==720,
      's6_syntheme_action_faithful':len(syntheme_actions)==720,
      's6_pentad_action_faithful':len(pentad_actions)==720,
      'duad_stabilizer_48':duad_stab==48,
      'syntheme_stabilizer_48':syntheme_stab==48,
      'pentad_stabilizer_120':pentad_stab==120,
      'orbit_stabilizer_identities':15*48==720 and 6*120==720,
      'outer_shadow_pair_of_pentads_to_syntheme':len(set(pentad_pair_to_syntheme.values()))==15,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXIII',
      'theorem':'S6 duad-syntheme-pentad bridge',
      'counts':{'duads':15,'synthemes':15,'pentads':6,'duad_syntheme_incidences':45,'syntheme_pentad_incidences':30},
      'groups':{'S6':720,'duad_stabilizer':48,'syntheme_stabilizer':48,'pentad_stabilizer':120,'faithful_actions':['duads','synthemes','pentads']},
      'outer_automorphism_shadow':'The six pentads form a second six-set. Pairs of pentads label the 15 synthemes, while pairs of original letters label the 15 duads. This exchanges the two 15-state carriers in the classical S6 outer-automorphism construction.',
      'connection_to_previous':'The operation weld gave Petersen edge -> K6 duad -> PG(3,2) point and PG(3,2) line = K6 triangle or one-factor. This pass adds the six synthematic totals/pentads and proves the S6 incidence layer that explains why the K6 model is exceptional.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['counts'], r['groups'])
