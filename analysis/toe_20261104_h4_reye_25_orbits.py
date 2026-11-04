#!/usr/bin/env python3
"""H4 on all 25 inscribed 24-cells and overlap-geometry orbit decomposition.

Compute from 120 exact icosians, not abstractly assume wreath/A5xA5.
Prior art: 25 24-cells and W(H4) classical, Denney et al 2020; earlier
repo H4 and 576/288 Reye. Added this pass: exact action on all 25
Reye packets and pair/triple orbit/no-single-packet selector check.
"""
from __future__ import annotations
import collections,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261104_icosian_24cell_tomotope_obstruction as ico
OUT=ROOT/"data"/"toe_20261104_h4_reye_25_orbits.json"
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def order(p):
    x=tuple(range(len(p)))
    for k in range(1,61):
        x=compose(p,x)
        if x==tuple(range(len(p))):return k
    raise ValueError
def main():
    G,H=ico.build()
    cells,_=ico.twentyfive(G,H)
    lookup={c:i for i,c in enumerate(cells)}
    def left(a):
        return tuple(lookup[frozenset(ico.qmul(a,x) for x in cell)] for cell in cells)
    def right(b):
        return tuple(lookup[frozenset(ico.qmul(x,b) for x in cell)] for cell in cells)
    lset=set(map(left,G));rset=set(map(right,G))
    assert len(lset)==len(rset)==60
    C=tuple(lookup[frozenset(ico.conjugate(x) for x in cell)] for cell in cells)
    I=tuple(range(25))
    assert order(C)==2
    g0={compose(l,r) for l in lset for r in rset}
    assert len(g0)==3600
    group=g0|{compose(C,p) for p in g0}
    assert len(group)==7200
    assert all(len(set(p))==25 for p in group)
    assert {p[i] for p in group for i in (0,)}==set(range(25))
    assert collections.Counter(order(p) for p in group)[1]==1
    # 25 packets as permutations on rows/columns of the exact 5x5 grid.
    packet_stab=sum(p[0]==0 for p in group)
    assert packet_stab==288
    def orbit(vals):
        return {tuple(sorted(p[i] for i in vals)) for p in group}
    pair_map=collections.Counter()
    pair_records=[]
    pair_orbits=[]
    remaining=set(itertools.combinations(range(25),2))
    while remaining:
        seed=min(remaining)
        o=orbit(seed)
        assert o<=remaining
        remaining-=o
        pair_orbits.append(dict(seed=list(seed),orbit_size=len(o),
             shared_vertices=len(cells[seed[0]]&cells[seed[1]]),
             stabilizer_order=7200//len(o)))
    assert len(pair_orbits)==2
    assert sorted(x["orbit_size"] for x in pair_orbits)==[100,200]
    # Triple-orbit data are an independent candidate for three-frame
    # selection. Full H4 cannot select one triple when orbit sizes>1.
    triple_orbits=[]
    triples=set(itertools.combinations(range(25),3))
    def triple_signature(t):
        a,b,c=t
        paircommon=sorted(len(cells[i]&cells[j]) for i,j in itertools.combinations(t,2))
        common=len(cells[a]&cells[b]&cells[c])
        return paircommon,common
    while triples:
        seed=min(triples)
        o=orbit(seed)
        assert o<=triples
        triples-=o
        assert all(triple_signature(x)==triple_signature(seed) for x in o)
        sig,ncommon=triple_signature(seed)
        triple_orbits.append(dict(seed=list(seed),orbit_size=len(o),
             pairwise_shared_vertices=sig,three_way_shared_vertices=ncommon,
             stabilizer_order=7200//len(o)))
    assert sum(x["orbit_size"] for x in triple_orbits)==2300
    assert all(x["orbit_size"]>1 for x in triple_orbits)
    assert set(len(cells[i]&cells[j]) for i,j in itertools.combinations(range(25),2))=={0,6}
    result=dict(status="PASS_EXPLICIT_H4_25_REYE_PACKET_AND_TRIPLE_ORBITS",
        H4_full_order=14400,central_antipode_kernel_on_25_packets=2,
        induced_H4_permutation_group_order=7200,
        row_icosian_left_image_order=60,
        column_icosian_right_image_order=60,
        index_two_extension_by_quaternion_conjugation=True,
        point_orbit_size=25,one_packet_stabilizer_effective=packet_stab,
        all_H4_invariant_single_packet_selectors_constant=True,
        pair_orbits=pair_orbits,
        triple_orbit_count=len(triple_orbits),
        triple_orbits=sorted(triple_orbits,key=lambda x:x["orbit_size"]),
        H4_invariant_three_packet_choice_exists=False,
        scope="Exact 25-subset action of binary icosian left/right/conjugation; H4 14400 acts via 7200 projective quotient. Invariants on pairs/triples do not uniquely identify a selected physical cell or a full tomotope cover.",
        prior_art="25 24-cells and H4 action Denney et al 2020; earlier repository Schur-Reye288 and H4-Reye bridge. New local certificate is full 25-cell group and triple orbit census in icosian coordinates.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"triple orbit count",len(triple_orbits),[(x["orbit_size"],x["three_way_shared_vertices"]) for x in triple_orbits],flush=True)
    return result
if __name__=="__main__":main()
