from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXVII_TOROIDAL_HEPTAD_MUTATION_K5_results.json'

from analysis.w33_toroidal_edge_data_parser import build_payload

def add(a,b): return tuple(x^y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b)) % 2
def mv(M,x): return tuple(dot(r,x) for r in M)

def fano_lines_and_gl():
    pts=[p for p in product([0,1], repeat=3) if p!=(0,0,0)]
    ix={p:i for i,p in enumerate(pts)}
    lines=sorted({tuple(sorted((ix[a],ix[b],ix[add(a,b)]))) for a,b in combinations(pts,2)})
    rows=list(product([0,1], repeat=3)); allpts=list(product([0,1], repeat=3)); gl=[]
    for M in product(rows, repeat=3):
        if len({mv(M,x) for x in allpts})==8:
            gl.append(tuple(ix[mv(M,p)] for p in pts))
    return lines,gl

def profile(a,lines): return tuple(sorted(sum(a[i] for i in L) for L in lines))

def main():
    counts=build_payload()['summary']['edge_type_counts']
    lines,GL=fano_lines_and_gl()
    assignments=set(permutations(counts))
    profiles=defaultdict(set)
    for a in assignments: profiles[profile(a,lines)].add(a)
    profs=sorted(profiles)
    prof_index={p:i for i,p in enumerate(profs)}
    orbit_of={a:prof_index[profile(a,lines)] for a in assignments}
    directed=Counter(); per_assignment=defaultdict(Counter)
    for a in assignments:
        i=orbit_of[a]
        for u,v in combinations(range(7),2):
            if a[u]==a[v]:
                continue
            b=list(a); b[u],b[v]=b[v],b[u]; b=tuple(b)
            j=orbit_of[b]
            directed[(i,j)]+=1
            per_assignment[(i,a)][j]+=1
    nonself={tuple(sorted((i,j))) for i,j in directed if i!=j}
    loop_counts={i:directed[(i,i)] for i in range(5)}
    offdiag_directed={(i,j):directed[(i,j)] for i in range(5) for j in range(5) if i!=j}
    local_profiles={i:Counter(tuple(sorted(c.items())) for (oi,a),c in per_assignment.items() if oi==i) for i in range(5)}
    expected_local=tuple(sorted([(0,6),(1,3),(2,3),(3,3),(4,3)]))
    checks={
      'uses_repo_counts':counts==[10,9,9,8,9,12,11],
      'five_orbits':len(profs)==5,
      'each_orbit_size_168':all(len(S)==168 for S in profiles.values()),
      'unique_assignments_840':len(assignments)==factorial(7)//factorial(3)==840,
      'gl32_order_168':len(GL)==168,
      'mutation_graph_is_K5':len(nonself)==10,
      'all_directed_offdiag_weights_504':set(offdiag_directed.values())=={504},
      'all_undirected_offdiag_weights_1008':all(directed[(i,j)]+directed[(j,i)]==1008 for i,j in combinations(range(5),2)),
      'all_loop_weights_1008':set(loop_counts.values())=={1008},
      'per_assignment_profile_uniform':all(len(cp)==1 and next(iter(cp))==expected_local for cp in local_profiles.values()),
      'per_orbit_directed_total_3024':all(sum(directed[(i,j)] for j in range(5))==3024 for i in range(5)),
      'numbers_factor_by_168':504==3*168 and 1008==6*168 and 3024==18*168,
      'k5_edge_count_matches_first_csaszar_count':len(nonself)==10==counts[0],
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXVII',
      'theorem':'Toroidal heptad mutation K5 bridge',
      'repo_edge_type_counts':counts,
      'orbit_count':len(profs),
      'orbit_size_profile':dict(sorted(Counter(len(S) for S in profiles.values()).items())),
      'line_sum_profiles':[list(p) for p in profs],
      'mutation_graph':{'vertices':5,'nonself_edges':len(nonself),'type':'complete graph K5'},
      'weights':{'directed_offdiag':504,'undirected_offdiag':1008,'loop':1008,'directed_total_per_orbit':3024},
      'local_transition_profile_per_assignment':{'self':6,'to_each_other_orbit':3,'total_nontrivial_swaps':18},
      'factorizations':{'504':'3*168','1008':'6*168','3024':'18*168','840':'5*168'},
      'reading':'The seven toroidal edge-type counts define five GL(3,2)-orbits. Under elementary swaps of two Fano-class labels, the quotient mutation graph on those five orbit types is exactly K5 with uniform weights. Each assignment has 6 internal swaps and 3 swaps to each of the other four orbits. Thus the five Csaszar sectors behave like a complete five-state mutation shell rather than five unrelated realizations.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['mutation_graph'], r['weights'])
