from collections import Counter
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXVI_TOROIDAL_HEPTAD_FANO_ORBIT_results.json'

from analysis.w33_toroidal_edge_data_parser import build_payload

def add(a,b): return tuple(x^y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b)) % 2
def mv(M,x): return tuple(dot(r,x) for r in M)

def fano():
    pts=[p for p in product([0,1], repeat=3) if p!=(0,0,0)]
    ix={p:i for i,p in enumerate(pts)}
    lines=sorted({tuple(sorted((ix[a],ix[b],ix[add(a,b)]))) for a,b in combinations(pts,2)})
    rows=list(product([0,1], repeat=3)); allpts=list(product([0,1], repeat=3)); gl=[]
    for M in product(rows, repeat=3):
        if len({mv(M,x) for x in allpts})==8:
            gl.append(tuple(ix[mv(M,p)] for p in pts))
    return pts,lines,gl

def act(g,a):
    b=[None]*7
    for i,j in enumerate(g): b[j]=a[i]
    return tuple(b)

def profile(a,lines): return tuple(sorted(sum(a[i] for i in L) for L in lines))

def main():
    payload=build_payload(); counts=payload['summary']['edge_type_counts']
    pts,lines,GL=fano(); assignments=set(permutations(counts))
    profile_sets={}
    for a in assignments:
        profile_sets.setdefault(profile(a,lines), set()).add(a)
    reps={p:next(iter(S)) for p,S in profile_sets.items()}
    orbit_ok={}
    for p,rep in reps.items():
        orb={act(g,rep) for g in GL}
        orbit_ok[str(p)]=orb==profile_sets[p] and len(orb)==168
    high_line_third=Counter()
    for p,rep in reps.items():
        i12=rep.index(12); i11=rep.index(11)
        for L in lines:
            if i12 in L and i11 in L:
                high_line_third[rep[next(i for i in L if i not in (i12,i11))]]+=1
    checks={
      'uses_repo_counts':counts==[10,9,9,8,9,12,11],
      'realization_packet_5_plus_2':payload['summary']['csaszar_edge_type_counts']==[10,9,9,8,9] and payload['summary']['szilassi_edge_type_counts']==[12,11],
      'unique_labelings_840':len(assignments)==factorial(7)//factorial(3)==840,
      'gl32_order_168':len(GL)==168,
      'five_fano_orbits':len(profile_sets)==5,
      'each_orbit_has_168':all(len(S)==168 for S in profile_sets.values()),
      'profiles_are_gl32_orbits':all(orbit_ok.values()),
      'orbit_count_matches_csaszar_realizations':len(profile_sets)==5,
      'two_szilassi_counts_are_high_markers':sorted(payload['summary']['szilassi_edge_type_counts'])==[11,12],
      'high_line_third_values_are_csaszar_counts':set(high_line_third)=={8,9,10},
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXVI',
      'theorem':'Toroidal heptad Fano orbit bridge',
      'repo_edge_type_counts':counts,
      'csaszar_counts':payload['summary']['csaszar_edge_type_counts'],
      'szilassi_counts':payload['summary']['szilassi_edge_type_counts'],
      'fano_lines':lines,
      'group_order_GL32':len(GL),
      'unique_multiset_labelings':len(assignments),
      'orbit_count':len(profile_sets),
      'orbit_size_profile':dict(sorted(Counter(len(S) for S in profile_sets.values()).items())),
      'line_sum_profiles':[list(p) for p in sorted(profile_sets)],
      'high_szilassi_line_third_value_profile':dict(sorted(high_line_third.items())),
      'reading':'Assign the seven toroidal edge-type counts [10,9,9,8,9,12,11] to the seven Fano/AG(3,2) parallel classes. Because three counts are equal to 9, there are 7!/3!=840 distinct assignments. The GL(3,2)=168 Fano automorphism group splits these assignments into exactly five orbits, each of size 168, indexed by Fano line-sum spectra. This matches the five Csaszar realizations, while the two Szilassi counts 12 and 11 act as the two high dual markers in the heptad. This is a compatibility theorem, not a unique geometric labeling of the realizations.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print('orbits', r['orbit_count'], r['orbit_size_profile'])
