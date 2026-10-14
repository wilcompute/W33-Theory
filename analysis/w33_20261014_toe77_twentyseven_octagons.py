"""TOE77 exact test of apparent 27=H27/E6 numerical correspondence.

Two native theta chord edges occur together in 27 of W33's 1620
primitive girth-eight octagons. Is this a canonical H27 27-state
orbit, or only a 27-element incidence count? Compute actual
PGSp(4,3) orbit of the unordered flag-edge pair, its stabilizer
order, and actual stabilizer orbit decomposition on the 27
common octagons, using Schreier generators induced by the native
symplectic transvections. Never infer H27 from the number 27 alone.
"""
from __future__ import annotations
from collections import deque
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_embedded_theta_exterior_flux import build
from w33_pass1081_1086_core import (
 build_w33,transvection_perm,outer_similitude_perm,line_perm)
def compose(a,b):return tuple(a[i] for i in b)
def inverse(a):
    z=[0]*len(a)
    for i,j in enumerate(a):z[j]=i
    return tuple(z)
def certificate():
    ed,cycles,p,chords=build()
    assert len(cycles)==1620
    a,b=sorted(chords)
    contain=[set(i for i,c in enumerate(cycles) if e in c) for e in chords]
    assert list(map(len,contain))==[81,81]
    common=sorted(contain[0]&contain[1])
    assert len(common)==27
    P,pi,lines,li,_,_,_,flags,flagidx=build_w33()
    assert len(flags)==160
    def action(perm):
        ll=line_perm(perm,lines,li)
        return tuple(flagidx[(perm[pp],ll[k])] for pp,k in flags)
    gens=[action(transvection_perm(P[i],P,pi)) for i in (0,1,2,4,8,15)]
    gens.append(action(outer_similitude_perm(P,pi)))
    N=160
    identity=tuple(range(N))
    seed=(a,b)
    representatives={seed:identity}
    fifo=deque([seed])
    schreier={}
    while fifo:
        pair=fifo.popleft()
        rx=representatives[pair]
        for s in gens:
            nxt=tuple(sorted((s[pair[0]],s[pair[1]])))
            r_y=representatives.get(nxt)
            if r_y is None:
                representatives[nxt]=compose(s,rx)
                fifo.append(nxt)
            else:
                h=compose(inverse(r_y),compose(s,rx))
                if h!=identity:schreier[h]=True
    orbit_size=len(representatives)
    assert 51840%orbit_size==0,(orbit_size,51840)
    stab_order=51840//orbit_size
    assert stab_order>=1
    index={frozenset(c):i for i,c in enumerate(cycles)}
    common_set=set(common)
    induced=[]
    for gen in schreier:
        perm=[]
        for i in common:
            transformed=frozenset(gen[e] for e in cycles[i])
            j=index[transformed]
            assert j in common_set
            perm.append(common.index(j))
        induced.append(tuple(perm))
    remaining=set(range(len(common)))
    orbits=[]
    while remaining:
        s=min(remaining)
        visited={s};q=deque([s])
        while q:
            v=q.popleft()
            for gg in induced:
                w=gg[v]
                if w not in visited:
                    visited.add(w);q.append(w)
        assert visited<=remaining
        remaining-=visited
        orbits.append(sorted(visited))
    assert sum(len(x) for x in orbits)==27
    # no canonical H27 conclusion without verifying transitivity,
    # group structure, and compatibility with the regular/projective
    # H27 address/operator action already in the repository.
    return {
      "status":"PASS_TOE77_TWO_CHORD_27_OCTAGON_STABILIZER_AUDIT",
      "native_W33_octagons":1620,
      "theta_chord_global_edges":[a,b],
      "octagons_per_native_flag_edge":[len(x) for x in contain],
      "octagons_containing_both_edges":27,
      "octagons_containing_at_least_one":135,
      "exact_integer_incidence_inclusion_exclusion":"81+81-27=135",
      "PGSp_group_order":51840,
      "unordered_two_flag_pair_orbit_size":orbit_size,
      "unordered_pair_stabilizer_order":stab_order,
      "schreier_generators_count":len(schreier),
      "stabilizer_orbit_sizes_on_27_common_octagons":sorted(len(x) for x in orbits),
      "stabilizer_action_transitive_on_27":len(orbits)==1,
      "first_shared_octagon_edge_lists":[list(cycles[i]) for i in common[:4]],
      "classification_guard":"The numerical value 27 alone cannot identify the extra-special H27 address group, the E6 27-dimensional representation, or the 27 PGSp orbits of 20-loop covers. Group actions must be exhibited, and H27 is not inferred from a numerical coincidence. A regular transitive 27-state action would be necessary but not sufficient.",
      "scope":"Exact subgroup/orbit census on native W33 two-chord flags and 27 shared octagons, not a gravitational/particle-spectrum derivation."
    }
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe77_twentyseven_octagon_orbits.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],"orbit",c["unordered_two_flag_pair_orbit_size"],
          "stabilizer",c["unordered_pair_stabilizer_order"],
          "orbits_on_27",c["stabilizer_orbit_sizes_on_27_common_octagons"])
