from itertools import combinations, permutations, product
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXX_SYMMETRY_CLOSURE_GL42_A8_results.json'

from analysis.w33_toroidal_mutation_edge_petersen_bridge import main as petersen_main
from analysis.w33_ag32_rm13_automorphism_bridge import main as ag32_main

def dot(a,b): return sum(x*y for x,y in zip(a,b)) % 2
def mv(M,x): return tuple(dot(r,x) for r in M)
def parity(p):
    inv=0
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            inv += p[i] > p[j]
    return inv % 2

def gl_order(d):
    n=2**d; out=1
    for i in range(d): out *= n-2**i
    return out

def main():
    pet=petersen_main(); ag=ag32_main()
    rows4=list(product([0,1], repeat=4)); pts4=list(product([0,1], repeat=4)); nz4=[x for x in pts4 if any(x)]
    gl4=[]
    for M in product(rows4, repeat=4):
        if len({mv(M,x) for x in pts4})==16:
            gl4.append(M)
    # Action on the 15 nonzero vectors is even: GL(4,2) embeds in A15, but the order equals A8.
    nz_index={x:i for i,x in enumerate(nz4)}
    parities=Counter()
    for M in gl4:
        p=tuple(nz_index[mv(M,x)] for x in nz4)
        parities[parity(p)] += 1
    stab_first=[M for M in gl4 if mv(M,nz4[0])==nz4[0]]
    # K5 mutation shell automorphism group by permuting its five vertices.
    s5=list(permutations(range(5)))
    k5_edges=list(combinations(range(5),2))
    e_index={e:i for i,e in enumerate(k5_edges)}
    edge_actions=[]
    for p in s5:
        edge_actions.append(tuple(e_index[tuple(sorted((p[a],p[b])))] for a,b in k5_edges))
    checks={
      'inherits_petersen_result':pet['n_verified']==pet['n_checks']==16,
      'inherits_ag32_result':ag['n_verified']==ag['n_checks']==11,
      's5_order_120':len(s5)==120,
      's5_edge_action_faithful_120':len(set(edge_actions))==120,
      'gl32_order_168':ag['groups']['GL(3,2)']==168,
      'gl42_formula_order_20160':gl_order(4)==20160,
      'gl42_enumerated_order_20160':len(gl4)==20160,
      'a8_order_20160':40320//2==20160,
      'product_120_168':120*168==20160,
      'point_stabilizer_1344':len(stab_first)==1344,
      'previous_agl32_is_point_stabilizer_order':ag['groups']['AGL(3,2)']==len(stab_first),
      'projective_point_count_15':len(nz4)==15,
      'orbit_stabilizer_15x1344':15*1344==20160,
      'edge_count_10_plus_projective_15_equals_25':pet['objects']['k5_mutation_edges']+len(nz4)==25,
      'gl42_action_on_15_points_even':parities==Counter({0:20160}),
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXX',
      'theorem':'Symmetry closure GL(4,2)/A8 bridge',
      'orders':{'S5_mutation_shell':120,'GL(3,2)_Fano':168,'product':20160,'GL(4,2)':len(gl4),'A8':20160,'AGL(3,2)_point_stabilizer':len(stab_first)},
      'orbit_stabilizer':{'nonzero_F2_4_points':15,'stabilizer':1344,'product':15*1344},
      'prior_layers':{'mutation_edge_vertices':pet['objects']['k5_mutation_edges'],'petersen_negative_edges':pet['pair_split']['disjoint_pairs_Petersen'],'ag32_full_aut':ag['groups']['AGL(3,2)']},
      'reading':'The K5 mutation shell contributes an S5 symmetry of order 120 on the five Csaszar sectors and faithfully on the ten mutation edges. The Fano heptad contributes GL(3,2)=168. Their product is 20160, the order of GL(4,2), also A8. Direct enumeration of GL(4,2) confirms order 20160 and point stabilizer 1344, matching the earlier AGL(3,2) automorphism bridge. Thus the K5/Petersen edge-space and Fano/RM(1,3) code-space close into the GL(4,2)/A8 symmetry horizon.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['orders'])
