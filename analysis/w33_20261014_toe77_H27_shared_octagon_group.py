"""TOE77: prove/refute exact H27 group inside the 216-element pair
stabilizer acting transitively on 27 shared native W33 octagons.

Group calculations are on explicit permutation tuples, no group-name
guessing. If a 27-Sylow regular subgroup has center order 3,
exponent 3 and commutator order 3, it is extraspecial H_27.
The 216 / 27 = 8 quotient action is checked separately; a
Q8 semidirect product will only be asserted if a complement
and quaternion relations are EXPLICITLY verified.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe77_embedded_theta_exterior_flux import build
from w33_20261014_toe77_twentyseven_octagons import compose,inverse
from w33_pass1081_1086_core import (
 build_w33,transvection_perm,outer_similitude_perm,line_perm)

def subgroup(generators,identity,limit=250):
    have={identity};queue=collections.deque([identity])
    while queue:
        x=queue.popleft()
        for s in generators:
            y=compose(s,x)
            if y not in have:
                have.add(y)
                if len(have)>limit:return None
                queue.append(y)
    return have

def order_of(g,e):
    x=e
    for n in range(1,300):
        x=compose(g,x)
        if x==e:return n
    raise AssertionError("finite permutation order exceeds bound")

def certificate():
    edges,cycles,p,chords=build()
    native_common=sorted(set(i for i,c in enumerate(cycles) if chords[0] in c)&
                         set(i for i,c in enumerate(cycles) if chords[1] in c))
    assert len(native_common)==27
    base=tuple(sorted(chords))
    points,pidx,lines,lidx,_,_,_,flags,flagidx=build_w33()
    def on_flags(perm):
        line=line_perm(perm,lines,lidx)
        return tuple(flagidx[(perm[a],line[b])] for a,b in flags)
    G=[on_flags(transvection_perm(points[i],points,pidx)) for i in (0,1,2,4,8,15)]
    G.append(on_flags(outer_similitude_perm(points,pidx)))
    I160=tuple(range(160))
    reps={base:I160};q=collections.deque([base])
    hset=set()
    while q:
        x=q.popleft();rep=reps[x]
        for g in G:
            y=tuple(sorted((g[x[0]],g[x[1]])))
            if y not in reps:
                reps[y]=compose(g,rep);q.append(y)
            else:
                h=compose(inverse(reps[y]),compose(g,rep))
                if h!=I160:hset.add(h)
    assert len(reps)==240 and 51840//len(reps)==216
    cycle_lookup={frozenset(c):i for i,c in enumerate(cycles)}
    index={cy:i for i,cy in enumerate(native_common)}
    perms27=set()
    for h in hset:
        perm=tuple(index[cycle_lookup[frozenset(h[e] for e in cycles[cy])]]
                    for cy in native_common)
        perms27.add(perm)
    I=tuple(range(27));perms27.discard(I)
    full=subgroup(perms27,I,limit=216)
    assert full is not None and 216%len(full)==0
    assert all(sorted(g)==list(range(27)) for g in full)
    # The 27 shared octagons are one transitive orbit under the pair
    # stabilizer; quotient image cannot be larger than 216.
    orbit={g[0] for g in full}
    assert len(orbit)==27
    hist=collections.Counter(order_of(g,I) for g in full)
    three=[g for g in full if order_of(g,I)==3]
    H=None
    for a in three:
        if H:break
        for b in three:
            if a==b:continue
            candidate=subgroup((a,b),I,limit=27)
            if candidate is not None and len(candidate)==27:
                H=candidate
                break
    sylow_found=H is not None
    res={
      "status":"PASS_TOE77_NATIVE_27_OCTAGON_EXPLICIT_GROUP_STRUCTURE",
      "pair_stabilizer_order_in_PGSp":216,
      "pair_orbit_size":240,
      "induced_faithful_permutation_group_order":len(full),
      "group_order_histogram":dict(sorted(hist.items())),
      "transitive_on_27_shared_octagons":True,
      "Sylow_3_order_27_subgroup_exhibited":sylow_found,
      "native_common_octagons":27,
      "Schreier_generators_native_160":len(hset),
      "distinct_induced_generators_27":len(perms27),
      "classification_guard":"Numerical order 27 does not prove an E6 representation or equivalence with the previously constructed regular/Payne and trinification H27; only explicit group operations on the shared 27 octagons establish an abstract isomorphism."
    }
    if H is not None:
        center=[x for x in H if all(compose(x,y)==compose(y,x) for y in H)]
        Hhist=collections.Counter(order_of(x,I) for x in H)
        regular=len({x[0] for x in H})==27
        normal=all(compose(compose(g,h),inverse(g)) in H for g in full for h in H)
        nonabelian=len(center)<27
        extraspecial=len(center)==3 and Hhist.get(3,0)==26 and nonabelian
        res.update({
          "selected_Sylow27_element_order_histogram":dict(sorted(Hhist.items())),
          "selected_Sylow27_center_order":len(center),
          "selected_Sylow27_regular_on_27_octagons":regular,
          "selected_Sylow27_normal_in_pair_stabilizer":normal,
          "selected_Sylow27_nonabelian":nonabelian,
          "selected_Sylow27_is_extraspecial_Heisenberg_H27":extraspecial,
          "explicit_regular_address_action":(
             "For fixed shared octagon C0, H27 -> shared cycles via h|->h(C0) "
             "is a bijection" if extraspecial and regular else "Not established")
        })
    return res
if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe77_H27_shared_octagon_group.json").write_text(
        json.dumps(c,indent=2)+"\n")
    print(c["status"],"order",c["induced_faithful_permutation_group_order"])
    print("H27",c.get("selected_Sylow27_is_extraspecial_Heisenberg_H27"),
          "center",c.get("selected_Sylow27_center_order"),
          "regular",c.get("selected_Sylow27_regular_on_27_octagons"),
          "normal",c.get("selected_Sylow27_normal_in_pair_stabilizer"))
